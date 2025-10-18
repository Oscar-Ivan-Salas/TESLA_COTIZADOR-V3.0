-- Script de inicialización de la base de datos PostgreSQL
-- Tesla Cotizador V3

-- Crear base de datos
CREATE DATABASE tesla_cotizador
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_PE.UTF-8'
    LC_CTYPE = 'es_PE.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

\c tesla_cotizador;

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Para búsquedas de texto

-- Tipo ENUM para estados de proyecto
CREATE TYPE estado_proyecto AS ENUM (
    'planificacion',
    'en_progreso',
    'completado',
    'cancelado'
);

-- Tabla: proyectos
CREATE TABLE IF NOT EXISTS proyectos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    cliente VARCHAR(200) NOT NULL,
    estado estado_proyecto DEFAULT 'planificacion',
    metadata_adicional JSONB,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_inicio TIMESTAMP,
    fecha_fin TIMESTAMP,
    
    -- Índices
    CONSTRAINT proyectos_nombre_check CHECK (char_length(nombre) >= 3)
);

CREATE INDEX idx_proyectos_cliente ON proyectos(cliente);
CREATE INDEX idx_proyectos_estado ON proyectos(estado);
CREATE INDEX idx_proyectos_fecha_creacion ON proyectos(fecha_creacion DESC);

-- Tabla: cotizaciones
CREATE TABLE IF NOT EXISTS cotizaciones (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(50) UNIQUE NOT NULL,
    cliente VARCHAR(200) NOT NULL,
    proyecto VARCHAR(200) NOT NULL,
    descripcion TEXT,
    
    -- Totales
    subtotal NUMERIC(10, 2) DEFAULT 0.00,
    igv NUMERIC(10, 2) DEFAULT 0.00,
    total NUMERIC(10, 2) DEFAULT 0.00,
    
    -- Estado
    estado VARCHAR(50) DEFAULT 'borrador',
    
    -- Datos estructurados
    items JSONB,
    metadata_adicional JSONB,
    
    -- Timestamps
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Relación con proyecto
    proyecto_id INTEGER REFERENCES proyectos(id) ON DELETE SET NULL,
    
    -- Constraints
    CONSTRAINT cotizaciones_total_check CHECK (total >= 0),
    CONSTRAINT cotizaciones_estado_check CHECK (estado IN ('borrador', 'enviada', 'aprobada', 'rechazada'))
);

CREATE INDEX idx_cotizaciones_numero ON cotizaciones(numero);
CREATE INDEX idx_cotizaciones_cliente ON cotizaciones(cliente);
CREATE INDEX idx_cotizaciones_estado ON cotizaciones(estado);
CREATE INDEX idx_cotizaciones_proyecto_id ON cotizaciones(proyecto_id);
CREATE INDEX idx_cotizaciones_fecha_creacion ON cotizaciones(fecha_creacion DESC);

-- Tabla: documentos
CREATE TABLE IF NOT EXISTS documentos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    nombre_original VARCHAR(200) NOT NULL,
    ruta_archivo VARCHAR(500) NOT NULL,
    tipo_mime VARCHAR(100) NOT NULL,
    tamano INTEGER NOT NULL,
    
    -- Contenido extraído
    contenido_texto TEXT,
    metadata_extraida JSONB,
    
    -- Estado de procesamiento
    procesado SMALLINT DEFAULT 0,  -- 0: pendiente, 1: procesado, 2: error
    
    -- Timestamps
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_procesamiento TIMESTAMP,
    
    -- Relación con proyecto
    proyecto_id INTEGER REFERENCES proyectos(id) ON DELETE CASCADE,
    
    -- Constraints
    CONSTRAINT documentos_tamano_check CHECK (tamano > 0),
    CONSTRAINT documentos_procesado_check CHECK (procesado IN (0, 1, 2))
);

CREATE INDEX idx_documentos_proyecto_id ON documentos(proyecto_id);
CREATE INDEX idx_documentos_procesado ON documentos(procesado);
CREATE INDEX idx_documentos_fecha_subida ON documentos(fecha_subida DESC);

-- Índice de búsqueda full-text en contenido de documentos
CREATE INDEX idx_documentos_contenido_texto ON documentos USING gin(to_tsvector('spanish', contenido_texto));

-- Tabla: items (opcional, si quieres normalizar)
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    descripcion TEXT NOT NULL,
    cantidad NUMERIC(10, 2) NOT NULL DEFAULT 1.0,
    precio_unitario NUMERIC(10, 2) NOT NULL,
    total NUMERIC(10, 2) NOT NULL,
    
    cotizacion_id INTEGER NOT NULL REFERENCES cotizaciones(id) ON DELETE CASCADE,
    
    CONSTRAINT items_cantidad_check CHECK (cantidad > 0),
    CONSTRAINT items_precio_check CHECK (precio_unitario >= 0),
    CONSTRAINT items_total_check CHECK (total >= 0)
);

CREATE INDEX idx_items_cotizacion_id ON items(cotizacion_id);

-- Función para actualizar fecha_modificacion automáticamente
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_modificacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers para actualizar fecha_modificacion
CREATE TRIGGER trigger_proyectos_fecha_modificacion
    BEFORE UPDATE ON proyectos
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trigger_cotizaciones_fecha_modificacion
    BEFORE UPDATE ON cotizaciones
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

-- Función para generar número de cotización automático
CREATE OR REPLACE FUNCTION generar_numero_cotizacion()
RETURNS TRIGGER AS $$
DECLARE
    ultimo_numero INTEGER;
    nuevo_numero VARCHAR(50);
BEGIN
    IF NEW.numero IS NULL OR NEW.numero = '' THEN
        SELECT COALESCE(MAX(CAST(SUBSTRING(numero FROM 10) AS INTEGER)), 0)
        INTO ultimo_numero
        FROM cotizaciones
        WHERE numero LIKE 'COT-' || EXTRACT(YEAR FROM CURRENT_DATE) || '-%';
        
        nuevo_numero := 'COT-' || EXTRACT(YEAR FROM CURRENT_DATE) || '-' || LPAD((ultimo_numero + 1)::TEXT, 4, '0');
        NEW.numero := nuevo_numero;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para generar número de cotización
CREATE TRIGGER trigger_generar_numero_cotizacion
    BEFORE INSERT ON cotizaciones
    FOR EACH ROW
    EXECUTE FUNCTION generar_numero_cotizacion();

-- Vista: resumen de proyectos
CREATE OR REPLACE VIEW vista_resumen_proyectos AS
SELECT 
    p.id,
    p.nombre,
    p.cliente,
    p.estado,
    COUNT(DISTINCT c.id) as total_cotizaciones,
    COUNT(DISTINCT d.id) as total_documentos,
    COALESCE(SUM(CASE WHEN c.estado = 'aprobada' THEN c.total ELSE 0 END), 0) as valor_total_aprobado,
    p.fecha_creacion,
    p.fecha_modificacion
FROM proyectos p
LEFT JOIN cotizaciones c ON p.id = c.proyecto_id
LEFT JOIN documentos d ON p.id = d.proyecto_id
GROUP BY p.id;

-- Vista: estadísticas de cotizaciones
CREATE OR REPLACE VIEW vista_estadisticas_cotizaciones AS
SELECT 
    estado,
    COUNT(*) as total,
    SUM(total) as valor_total,
    AVG(total) as valor_promedio,
    MIN(total) as valor_minimo,
    MAX(total) as valor_maximo
FROM cotizaciones
GROUP BY estado;

-- Datos de ejemplo (opcional)
-- INSERT INTO proyectos (nombre, descripcion, cliente, estado) VALUES
-- ('Proyecto Demo', 'Proyecto de demostración', 'Cliente Demo S.A.C.', 'planificacion');

-- Comentarios en tablas
COMMENT ON TABLE proyectos IS 'Tabla principal de proyectos';
COMMENT ON TABLE cotizaciones IS 'Cotizaciones generadas para proyectos';
COMMENT ON TABLE documentos IS 'Documentos subidos y procesados';
COMMENT ON TABLE items IS 'Items individuales de las cotizaciones';

-- Permisos (ajustar según necesidad)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tu_usuario;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tu_usuario;

-- Información de la base de datos
SELECT 
    'Base de datos inicializada correctamente' as mensaje,
    version() as version_postgresql,
    current_database() as base_datos,
    current_timestamp as fecha_inicializacion;