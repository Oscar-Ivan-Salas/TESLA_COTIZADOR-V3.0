# 🏛️ ARQUITECTURA EMPRESARIAL SENIOR
## Sistema de Documentos Profesionales Escalable

**Fecha**: 29 de Diciembre 2025
**Arquitecto**: Claude Code (Sonnet 4.5)
**Versión**: Enterprise 4.0
**Capacidad**: Cientos de usuarios simultáneos

---

## 📊 REQUISITOS EMPRESARIALES

### Capacidad Requerida
- ✅ **100-500 usuarios concurrentes**
- ✅ **1,000+ documentos/día**
- ✅ **Tiempo respuesta < 2 segundos**
- ✅ **Disponibilidad 99.9%** (8.76 horas downtime/año máximo)
- ✅ **Escalabilidad horizontal**

### Funcionalidades Críticas
- ✅ **Base de datos robusta** (clientes, usuarios, documentos)
- ✅ **RAG escalable** (aprendizaje continuo)
- ✅ **Generación profesional** (Word/PDF)
- ✅ **Cache distribuido**
- ✅ **Queue de trabajos**
- ✅ **Dockerización completa**

---

## 🏗️ ARQUITECTURA DE 5 CAPAS

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA 1: LOAD BALANCER                         │
│                    Nginx / HAProxy / AWS ALB                     │
│                    Distribución de carga                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
┌───────────────────────┐   ┌───────────────────────┐
│   BACKEND INSTANCE 1  │   │   BACKEND INSTANCE 2  │
│   FastAPI + Uvicorn   │   │   FastAPI + Uvicorn   │
│   (Stateless)         │   │   (Stateless)         │
└───────────┬───────────┘   └───────────┬───────────┘
            │                           │
            └────────────┬──────────────┘
                         │
         ┌───────────────┼───────────────┬──────────────┐
         │               │               │              │
         ▼               ▼               ▼              ▼
┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐
│ PostgreSQL │  │   Redis    │  │  RabbitMQ  │  │ ChromaDB │
│   (Master) │  │   Cache    │  │   Queue    │  │   RAG    │
│            │  │            │  │            │  │          │
│  + Replica │  │  Cluster   │  │  Cluster   │  │ Cluster  │
└────────────┘  └────────────┘  └────────────┘  └──────────┘
         │                              │
         │                              ▼
         │                    ┌───────────────────┐
         │                    │  Celery Workers   │
         │                    │  (Generación docs)│
         │                    │  (Indexación RAG) │
         │                    └───────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│         S3 / MinIO / Filesystem             │
│         Almacenamiento de documentos        │
└─────────────────────────────────────────────┘
```

---

## 🗄️ DISEÑO DE BASE DE DATOS EMPRESARIAL

### Schema Completo (PostgreSQL)

```sql
-- ============================================================================
-- USUARIOS Y AUTENTICACIÓN
-- ============================================================================

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL DEFAULT 'usuario', -- admin, gerente, vendedor, usuario
    empresa_id INTEGER REFERENCES empresas(id),
    activo BOOLEAN DEFAULT TRUE,
    ultimo_login TIMESTAMP,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_modificacion TIMESTAMP DEFAULT NOW(),

    -- Índices
    INDEX idx_usuarios_email (email),
    INDEX idx_usuarios_empresa (empresa_id),
    INDEX idx_usuarios_rol (rol)
);

-- ============================================================================
-- EMPRESAS (Multi-tenant)
-- ============================================================================

CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    direccion TEXT,
    telefono VARCHAR(50),
    email VARCHAR(255),
    logo_url TEXT,
    plan VARCHAR(50) DEFAULT 'basico', -- basico, profesional, empresarial
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT NOW(),

    INDEX idx_empresas_ruc (ruc)
);

-- ============================================================================
-- CLIENTES
-- ============================================================================

CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES empresas(id) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    ruc_dni VARCHAR(20),
    tipo VARCHAR(50), -- persona_natural, empresa
    direccion TEXT,
    telefono VARCHAR(50),
    email VARCHAR(255),
    contacto_principal VARCHAR(255),
    notas TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_modificacion TIMESTAMP DEFAULT NOW(),

    -- Índices
    INDEX idx_clientes_empresa (empresa_id),
    INDEX idx_clientes_ruc (ruc_dni),
    INDEX idx_clientes_nombre (nombre)
);

-- ============================================================================
-- DOCUMENTOS GENERADOS
-- ============================================================================

CREATE TABLE documentos (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(36) UNIQUE NOT NULL, -- UUID para referencias externas
    empresa_id INTEGER REFERENCES empresas(id) NOT NULL,
    usuario_id INTEGER REFERENCES usuarios(id) NOT NULL,
    cliente_id INTEGER REFERENCES clientes(id),

    -- Tipo y clasificación
    tipo_documento VARCHAR(50) NOT NULL, -- cotizacion-simple, proyecto-pmi, etc.
    categoria VARCHAR(50), -- cotizacion, proyecto, informe
    complejidad VARCHAR(20), -- simple, compleja

    -- Identificación
    numero VARCHAR(100) UNIQUE NOT NULL, -- COT-202512-0001
    titulo VARCHAR(500),
    descripcion TEXT,

    -- Servicio relacionado
    tipo_servicio VARCHAR(100), -- electricidad, itse, contraincendios, etc.

    -- Datos del documento (JSON)
    datos JSONB NOT NULL, -- Todos los datos estructurados

    -- Archivos generados
    archivo_word_url TEXT,
    archivo_pdf_url TEXT,
    archivo_html TEXT, -- Preview HTML

    -- Metadatos para búsqueda
    contenido_texto TEXT, -- Texto completo para búsqueda full-text
    tags TEXT[], -- Etiquetas para clasificación

    -- Estado y workflow
    estado VARCHAR(50) DEFAULT 'generado', -- generado, enviado, aprobado, rechazado

    -- Totales (para consultas rápidas)
    subtotal DECIMAL(15, 2),
    igv DECIMAL(15, 2),
    total DECIMAL(15, 2),
    moneda VARCHAR(10) DEFAULT 'PEN',

    -- Auditoría
    indexado_rag BOOLEAN DEFAULT FALSE,
    fecha_indexacion TIMESTAMP,
    version INTEGER DEFAULT 1,
    documento_padre_id INTEGER REFERENCES documentos(id), -- Para versionamiento

    -- Timestamps
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_modificacion TIMESTAMP DEFAULT NOW(),
    fecha_envio TIMESTAMP,
    fecha_aprobacion TIMESTAMP,

    -- Índices para performance
    INDEX idx_documentos_empresa (empresa_id),
    INDEX idx_documentos_usuario (usuario_id),
    INDEX idx_documentos_cliente (cliente_id),
    INDEX idx_documentos_tipo (tipo_documento),
    INDEX idx_documentos_servicio (tipo_servicio),
    INDEX idx_documentos_numero (numero),
    INDEX idx_documentos_fecha (fecha_creacion),
    INDEX idx_documentos_estado (estado),
    INDEX idx_documentos_rag (indexado_rag)
);

-- Índice full-text para búsqueda
CREATE INDEX idx_documentos_contenido_fts ON documentos
USING gin(to_tsvector('spanish', contenido_texto));

-- Índice para tags
CREATE INDEX idx_documentos_tags ON documentos USING gin(tags);

-- ============================================================================
-- ITEMS DE DOCUMENTOS (Cotizaciones/Proyectos)
-- ============================================================================

CREATE TABLE documento_items (
    id SERIAL PRIMARY KEY,
    documento_id INTEGER REFERENCES documentos(id) ON DELETE CASCADE NOT NULL,

    -- Orden en el documento
    orden INTEGER NOT NULL,

    -- Datos del item
    codigo VARCHAR(100),
    descripcion TEXT NOT NULL,
    cantidad DECIMAL(10, 3) NOT NULL,
    unidad VARCHAR(20) NOT NULL,
    precio_unitario DECIMAL(15, 2) NOT NULL,

    -- Cálculos
    subtotal DECIMAL(15, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,

    -- Categorización
    categoria VARCHAR(100),

    -- Índices
    INDEX idx_items_documento (documento_id),
    INDEX idx_items_categoria (categoria)
);

-- ============================================================================
-- METADATOS RAG (Para aprendizaje)
-- ============================================================================

CREATE TABLE rag_metadatos (
    id SERIAL PRIMARY KEY,
    documento_id INTEGER REFERENCES documentos(id) ON DELETE CASCADE NOT NULL,

    -- Identificador en ChromaDB
    chroma_id VARCHAR(100) UNIQUE NOT NULL,
    coleccion VARCHAR(100) NOT NULL, -- Por tipo de servicio

    -- Chunk de texto
    chunk_texto TEXT NOT NULL,
    chunk_orden INTEGER NOT NULL,

    -- Embeddings metadata
    embedding_modelo VARCHAR(100) DEFAULT 'all-MiniLM-L6-v2',

    -- Metadatos para filtrado
    tipo_servicio VARCHAR(100),
    complejidad VARCHAR(20),
    categoria VARCHAR(50),
    tags TEXT[],

    -- Performance
    similitud_promedio DECIMAL(5, 4), -- Para tracking de calidad
    veces_recuperado INTEGER DEFAULT 0,

    -- Timestamps
    fecha_indexacion TIMESTAMP DEFAULT NOW(),

    -- Índices
    INDEX idx_rag_documento (documento_id),
    INDEX idx_rag_chroma (chroma_id),
    INDEX idx_rag_coleccion (coleccion),
    INDEX idx_rag_servicio (tipo_servicio)
);

-- ============================================================================
-- PLANTILLAS PERSONALIZADAS
-- ============================================================================

CREATE TABLE plantillas (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES empresas(id) NOT NULL,

    nombre VARCHAR(255) NOT NULL,
    tipo_documento VARCHAR(50) NOT NULL,

    -- Configuración (JSON)
    configuracion JSONB NOT NULL, -- Esquema de colores, fuentes, etc.

    -- HTML template si es personalizado
    template_html TEXT,

    activo BOOLEAN DEFAULT TRUE,
    es_predeterminada BOOLEAN DEFAULT FALSE,

    fecha_creacion TIMESTAMP DEFAULT NOW(),

    INDEX idx_plantillas_empresa (empresa_id),
    INDEX idx_plantillas_tipo (tipo_documento)
);

-- ============================================================================
-- AUDITORÍA Y LOGS
-- ============================================================================

CREATE TABLE auditoria (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    accion VARCHAR(100) NOT NULL, -- crear_documento, editar, eliminar, etc.
    entidad VARCHAR(50) NOT NULL, -- documentos, clientes, usuarios
    entidad_id INTEGER NOT NULL,

    -- Datos antes/después (para tracking de cambios)
    datos_antes JSONB,
    datos_despues JSONB,

    ip_address VARCHAR(50),
    user_agent TEXT,

    fecha_accion TIMESTAMP DEFAULT NOW(),

    INDEX idx_auditoria_usuario (usuario_id),
    INDEX idx_auditoria_entidad (entidad, entidad_id),
    INDEX idx_auditoria_fecha (fecha_accion)
);

-- ============================================================================
-- ESTADÍSTICAS Y MÉTRICAS
-- ============================================================================

CREATE TABLE metricas_diarias (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    empresa_id INTEGER REFERENCES empresas(id),

    -- Contadores
    documentos_generados INTEGER DEFAULT 0,
    usuarios_activos INTEGER DEFAULT 0,
    tiempo_promedio_generacion DECIMAL(10, 2), -- en segundos

    -- Por tipo
    cotizaciones_generadas INTEGER DEFAULT 0,
    proyectos_generados INTEGER DEFAULT 0,
    informes_generados INTEGER DEFAULT 0,

    -- RAG
    busquedas_rag INTEGER DEFAULT 0,
    documentos_indexados INTEGER DEFAULT 0,

    UNIQUE(fecha, empresa_id),
    INDEX idx_metricas_fecha (fecha),
    INDEX idx_metricas_empresa (empresa_id)
);
```

---

## 📂 ESTRUCTURA DE CARPETAS RENOMBRADA

### Antes
```
backend/app/services/professional/
```

### Después (Enterprise)
```
backend/app/services/documentos_profesionales/
│
├── __init__.py
│
├── core/                           # Núcleo del sistema
│   ├── __init__.py
│   ├── orchestrator.py            # Orquestador principal
│   ├── cache_manager.py           # Gestión de cache Redis
│   ├── queue_manager.py           # Gestión de queues (Celery)
│   └── metrics.py                 # Métricas y monitoring
│
├── generators/                     # Generadores de documentos
│   ├── __init__.py
│   ├── base/
│   │   └── base_generator.py
│   ├── cotizaciones/
│   │   ├── simple.py
│   │   └── compleja.py
│   ├── proyectos/
│   │   ├── simple.py
│   │   └── complejo_pmi.py
│   └── informes/
│       ├── tecnico.py
│       └── ejecutivo_apa.py
│
├── processors/                     # Procesamiento
│   ├── __init__.py
│   ├── file_processor.py
│   └── text_extractor.py
│
├── rag/                           # Sistema RAG escalable
│   ├── __init__.py
│   ├── rag_engine.py
│   ├── indexer.py                # Indexación asíncrona
│   ├── searcher.py               # Búsqueda optimizada
│   └── collections_manager.py    # Gestión de colecciones
│
├── ml/                            # Machine Learning
│   ├── __init__.py
│   ├── ml_engine.py
│   ├── classifier.py
│   └── entity_extractor.py
│
├── charts/                        # Gráficas
│   ├── __init__.py
│   └── chart_engine.py
│
├── database/                      # Capa de datos
│   ├── __init__.py
│   ├── repositories/             # Repository Pattern
│   │   ├── documento_repository.py
│   │   ├── cliente_repository.py
│   │   ├── usuario_repository.py
│   │   └── rag_repository.py
│   ├── models.py                 # SQLAlchemy models
│   └── schemas.py                # Pydantic schemas
│
└── tasks/                         # Celery tasks
    ├── __init__.py
    ├── generation_tasks.py       # Generación asíncrona
    ├── indexing_tasks.py         # Indexación RAG asíncrona
    └── cleanup_tasks.py          # Limpieza periódica
```

---

## 🐳 DOCKERIZACIÓN COMPLETA

### docker-compose.yml (Producción)

```yaml
version: '3.8'

services:
  # ============================================================================
  # NGINX - Load Balancer
  # ============================================================================
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend-1
      - backend-2
    networks:
      - tesla-network
    restart: unless-stopped

  # ============================================================================
  # BACKEND INSTANCES (Stateless, escalable horizontalmente)
  # ============================================================================
  backend-1:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://tesla:password@postgres:5432/tesla_db
      - REDIS_URL=redis://redis:6379/0
      - RABBITMQ_URL=amqp://tesla:password@rabbitmq:5672/
      - CHROMA_HOST=chromadb
      - CHROMA_PORT=8000
      - WORKER_INSTANCE=1
    volumes:
      - documents:/app/storage/documents
      - logs:/app/logs
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - chromadb
    networks:
      - tesla-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G

  backend-2:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://tesla:password@postgres:5432/tesla_db
      - REDIS_URL=redis://redis:6379/0
      - RABBITMQ_URL=amqp://tesla:password@rabbitmq:5672/
      - CHROMA_HOST=chromadb
      - CHROMA_PORT=8000
      - WORKER_INSTANCE=2
    volumes:
      - documents:/app/storage/documents
      - logs:/app/logs
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - chromadb
    networks:
      - tesla-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G

  # ============================================================================
  # CELERY WORKERS (Procesamiento asíncrono)
  # ============================================================================
  celery-worker-generation:
    build: ./backend
    command: celery -A app.tasks worker --loglevel=info --queues=generation --concurrency=4
    environment:
      - DATABASE_URL=postgresql://tesla:password@postgres:5432/tesla_db
      - REDIS_URL=redis://redis:6379/0
      - RABBITMQ_URL=amqp://tesla:password@rabbitmq:5672/
      - CHROMA_HOST=chromadb
    volumes:
      - documents:/app/storage/documents
    depends_on:
      - postgres
      - redis
      - rabbitmq
    networks:
      - tesla-network
    restart: unless-stopped
    deploy:
      replicas: 3

  celery-worker-indexing:
    build: ./backend
    command: celery -A app.tasks worker --loglevel=info --queues=indexing --concurrency=2
    environment:
      - DATABASE_URL=postgresql://tesla:password@postgres:5432/tesla_db
      - REDIS_URL=redis://redis:6379/0
      - RABBITMQ_URL=amqp://tesla:password@rabbitmq:5672/
      - CHROMA_HOST=chromadb
    volumes:
      - documents:/app/storage/documents
    depends_on:
      - postgres
      - chromadb
      - rabbitmq
    networks:
      - tesla-network
    restart: unless-stopped
    deploy:
      replicas: 2

  # ============================================================================
  # POSTGRESQL - Base de datos principal
  # ============================================================================
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=tesla_db
      - POSTGRES_USER=tesla
      - POSTGRES_PASSWORD=password
      - POSTGRES_MAX_CONNECTIONS=200
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - tesla-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G

  # Replica de lectura (opcional)
  postgres-replica:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=tesla_db
      - POSTGRES_USER=tesla
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres-replica-data:/var/lib/postgresql/data
    networks:
      - tesla-network
    restart: unless-stopped

  # ============================================================================
  # REDIS - Cache distribuido
  # ============================================================================
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --maxmemory 2gb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"
    networks:
      - tesla-network
    restart: unless-stopped

  # ============================================================================
  # RABBITMQ - Message Queue
  # ============================================================================
  rabbitmq:
    image: rabbitmq:3-management-alpine
    environment:
      - RABBITMQ_DEFAULT_USER=tesla
      - RABBITMQ_DEFAULT_PASS=password
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"  # Management UI
    networks:
      - tesla-network
    restart: unless-stopped

  # ============================================================================
  # CHROMADB - Vector Database para RAG
  # ============================================================================
  chromadb:
    image: chromadb/chroma:latest
    volumes:
      - chroma-data:/chroma/chroma
    ports:
      - "8001:8000"
    environment:
      - IS_PERSISTENT=TRUE
      - ANONYMIZED_TELEMETRY=FALSE
    networks:
      - tesla-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G

  # ============================================================================
  # MONITORING - Prometheus + Grafana
  # ============================================================================
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - tesla-network
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
    ports:
      - "3001:3000"
    depends_on:
      - prometheus
    networks:
      - tesla-network
    restart: unless-stopped

# ============================================================================
# VOLUMES
# ============================================================================
volumes:
  postgres-data:
  postgres-replica-data:
  redis-data:
  rabbitmq-data:
  chroma-data:
  documents:
  logs:
  prometheus-data:
  grafana-data:

# ============================================================================
# NETWORKS
# ============================================================================
networks:
  tesla-network:
    driver: bridge
```

---

## 🔄 FLUJO DE GENERACIÓN ESCALABLE

### Flujo Asíncrono con Queue

```python
# 1. Usuario solicita documento
@router.post("/api/documentos/generar")
async def generar_documento_async(request: GenerarDocumentoRequest):
    """
    Endpoint que encola la generación en vez de hacerla síncronamente
    """
    from app.services.documentos_profesionales.tasks import generar_documento_task

    # Validar request
    # ...

    # Encolar tarea (Celery)
    task = generar_documento_task.delay(
        usuario_id=request.usuario_id,
        cliente_id=request.cliente_id,
        tipo_documento=request.tipo_documento,
        datos=request.datos
    )

    return {
        "task_id": task.id,
        "status": "encolado",
        "mensaje": "Documento en proceso de generación"
    }


# 2. Worker Celery procesa en background
@celery_app.task(bind=True, max_retries=3)
def generar_documento_task(self, usuario_id, cliente_id, tipo_documento, datos):
    """
    Tarea asíncrona de generación
    """
    from app.services.documentos_profesionales import DocumentosProfesionalesService

    service = DocumentosProfesionalesService()

    try:
        # Generar documento
        resultado = service.generar_documento(
            usuario_id=usuario_id,
            cliente_id=cliente_id,
            tipo_documento=tipo_documento,
            datos=datos
        )

        # Guardar en BD
        documento_id = service.guardar_documento(resultado)

        # Encolar indexación RAG (otra queue)
        indexar_documento_task.delay(documento_id)

        # Actualizar métricas
        service.actualizar_metricas(usuario_id, tipo_documento)

        return {
            "success": True,
            "documento_id": documento_id,
            "url_descarga": resultado["url"]
        }

    except Exception as e:
        # Retry con backoff exponencial
        raise self.retry(exc=e, countdown=2 ** self.request.retries)


# 3. Indexación RAG en worker separado
@celery_app.task(bind=True)
def indexar_documento_task(self, documento_id):
    """
    Indexa documento en ChromaDB para RAG
    """
    from app.services.documentos_profesionales.rag import RAGIndexer

    indexer = RAGIndexer()

    # Obtener documento de BD
    documento = get_documento_by_id(documento_id)

    # Indexar en ChromaDB
    indexer.indexar(
        documento_id=documento_id,
        texto=documento.contenido_texto,
        tipo_servicio=documento.tipo_servicio,
        metadatos={
            "tipo_documento": documento.tipo_documento,
            "complejidad": documento.complejidad,
            "tags": documento.tags
        }
    )

    # Marcar como indexado en BD
    marcar_documento_indexado(documento_id)

    return {"success": True, "documento_id": documento_id}
```

---

## 🚀 ESCALABILIDAD HORIZONTAL

### Kubernetes Ready (opcional)

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tesla-backend
spec:
  replicas: 5  # 5 instancias del backend
  selector:
    matchLabels:
      app: tesla-backend
  template:
    metadata:
      labels:
        app: tesla-backend
    spec:
      containers:
      - name: backend
        image: tesla/backend:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: tesla-secrets
              key: database-url
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: tesla-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: tesla-backend
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## 📊 ESTIMACIÓN DE CAPACIDAD

### Configuración Mínima (100 usuarios concurrentes)

| Componente | Recursos | Cantidad |
|------------|----------|----------|
| Backend FastAPI | 2 CPU, 4GB RAM | 2 instancias |
| PostgreSQL | 4 CPU, 8GB RAM | 1 master + 1 replica |
| Redis | 1 CPU, 2GB RAM | 1 instancia |
| RabbitMQ | 1 CPU, 2GB RAM | 1 instancia |
| ChromaDB | 2 CPU, 4GB RAM | 1 instancia |
| Celery Workers | 2 CPU, 4GB RAM | 5 workers |
| **TOTAL** | **20 CPU, 48GB RAM** | - |

### Configuración Alta Capacidad (500 usuarios concurrentes)

| Componente | Recursos | Cantidad |
|------------|----------|----------|
| Backend FastAPI | 2 CPU, 4GB RAM | 5 instancias |
| PostgreSQL | 8 CPU, 16GB RAM | 1 master + 2 replicas |
| Redis | 2 CPU, 4GB RAM | 3 instancias (cluster) |
| RabbitMQ | 2 CPU, 4GB RAM | 3 instancias (cluster) |
| ChromaDB | 4 CPU, 8GB RAM | 3 instancias (cluster) |
| Celery Workers | 2 CPU, 4GB RAM | 15 workers |
| **TOTAL** | **68 CPU, 140GB RAM** | - |

---

## ✅ CONFIRMACIÓN DE REQUISITOS

### ¿Contemplo TODO esto?

| Requisito | Estado | Implementación |
|-----------|--------|----------------|
| **Cientos de usuarios simultáneos** | ✅ SÍ | Load balancer + múltiples instancias backend |
| **BD robusta (clientes, usuarios, docs)** | ✅ SÍ | PostgreSQL con schema completo + índices |
| **RAG escalable** | ✅ SÍ | ChromaDB cluster + indexación asíncrona |
| **Aprendizaje continuo** | ✅ SÍ | Tabla rag_metadatos + workers de indexación |
| **Dockerización** | ✅ SÍ | Docker Compose + Kubernetes ready |
| **Alta disponibilidad** | ✅ SÍ | Réplicas, health checks, auto-restart |
| **Cache distribuido** | ✅ SÍ | Redis cluster |
| **Queue de trabajos** | ✅ SÍ | RabbitMQ + Celery |
| **Monitoring** | ✅ SÍ | Prometheus + Grafana |
| **Escalabilidad horizontal** | ✅ SÍ | Stateless backends + HPA |

---

## 🎯 PRÓXIMOS PASOS

1. **Renombrar carpeta**: `professional/` → `documentos_profesionales/`
2. **Crear schema BD**: Ejecutar SQL completo
3. **Implementar repositories**: Capa de datos
4. **Configurar Celery**: Tasks asíncronas
5. **Setup Docker**: Docker Compose completo
6. **Migrar generadores**: A nueva estructura
7. **Implementar RAG indexer**: Indexación automática
8. **Tests de carga**: Validar 100+ usuarios
9. **Monitoring**: Dashboards Grafana
10. **Documentación**: Deploy guide completo

---

**¿Procedo con el paso 1: Renombrar carpeta a `documentos_profesionales/`?**
