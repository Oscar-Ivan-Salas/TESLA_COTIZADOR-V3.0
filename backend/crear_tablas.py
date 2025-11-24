#!/usr/bin/env python3
"""
🗄️ CREAR TABLAS EN BASE DE DATOS - MÉTODO DIRECTO
====================================================
Este script crea las tablas directamente con SQL puro.
NO requiere dependencias de Python.

EJECUTAR:
    cd backend
    python crear_tablas.py
"""

import sqlite3
from pathlib import Path

# Ruta de la base de datos
project_root = Path(__file__).parent.parent
db_file = project_root / "database" / "tesla_cotizador.db"

print("=" * 70)
print("🗄️  CREANDO TABLAS - TESLA COTIZADOR V3.0")
print("=" * 70)
print(f"\n📍 Base de datos: {db_file}")

# Verificar que el archivo existe
if not db_file.exists():
    print(f"\n❌ ERROR: Archivo de base de datos no encontrado: {db_file}")
    print("\nPrimero ejecuta: python crear_base_datos.py")
    exit(1)

# Conectar a la base de datos
conn = sqlite3.connect(str(db_file))
cursor = conn.cursor()

print("\n🏗️  Creando tablas...")

# ===================================================================
# TABLA: proyectos
# ===================================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS proyectos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    cliente VARCHAR(200),
    descripcion TEXT,
    estado VARCHAR(50) DEFAULT 'planificacion',
    presupuesto_estimado DECIMAL(12, 2),
    duracion_meses INTEGER,
    tipo VARCHAR(100),
    metadata_adicional TEXT,
    fecha_inicio DATETIME,
    fecha_fin DATETIME,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
print("   ✅ proyectos")

# ===================================================================
# TABLA: cotizaciones
# ===================================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS cotizaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero VARCHAR(50) UNIQUE NOT NULL,
    cliente VARCHAR(200) NOT NULL,
    proyecto VARCHAR(200) NOT NULL,
    descripcion TEXT,
    subtotal DECIMAL(10, 2) DEFAULT 0.00,
    igv DECIMAL(10, 2) DEFAULT 0.00,
    total DECIMAL(10, 2) DEFAULT 0.00,
    observaciones TEXT,
    vigencia VARCHAR(100) DEFAULT '30 días',
    estado VARCHAR(50) DEFAULT 'borrador',
    items TEXT,
    metadata_adicional TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    proyecto_id INTEGER,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE SET NULL
)
""")
print("   ✅ cotizaciones")

# Crear índices para cotizaciones
cursor.execute("CREATE INDEX IF NOT EXISTS idx_cotizaciones_numero ON cotizaciones(numero)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_cotizaciones_cliente ON cotizaciones(cliente)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_cotizaciones_estado ON cotizaciones(estado)")

# ===================================================================
# TABLA: documentos
# ===================================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS documentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_archivo VARCHAR(255) NOT NULL,
    tipo VARCHAR(50),
    ruta VARCHAR(500),
    tamanio INTEGER,
    contenido_extraido TEXT,
    metadata TEXT,
    fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP,
    proyecto_id INTEGER,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE
)
""")
print("   ✅ documentos")

# ===================================================================
# TABLA: items
# ===================================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    cantidad DECIMAL(10, 2) DEFAULT 0,
    unidad VARCHAR(20) DEFAULT 'und',
    precio_unitario DECIMAL(10, 2) DEFAULT 0.00,
    total DECIMAL(10, 2) DEFAULT 0.00,
    categoria VARCHAR(100),
    metadata TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    cotizacion_id INTEGER,
    proyecto_id INTEGER,
    FOREIGN KEY (cotizacion_id) REFERENCES cotizaciones(id) ON DELETE CASCADE,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE
)
""")
print("   ✅ items")

# Guardar cambios
conn.commit()

# ===================================================================
# VERIFICAR TABLAS CREADAS
# ===================================================================
print("\n🔍 Verificando tablas creadas:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

expected_tables = ["cotizaciones", "proyectos", "documentos", "items"]
all_ok = True

for expected in expected_tables:
    found = any(expected == t[0] for t in tables)
    if found:
        # Contar columnas
        cursor.execute(f"PRAGMA table_info({expected})")
        columns = cursor.fetchall()
        print(f"   ✅ {expected} ({len(columns)} columnas)")
    else:
        print(f"   ❌ {expected} - NO ENCONTRADA")
        all_ok = False

# Cerrar conexión
conn.close()

# ===================================================================
# RESUMEN FINAL
# ===================================================================
print("\n" + "=" * 70)
if all_ok:
    print("🎉 TODAS LAS TABLAS CREADAS EXITOSAMENTE")
    print("=" * 70)
    print(f"\n📍 Base de datos: {db_file}")
    print(f"📊 Tablas creadas: {len(expected_tables)}")
    print("\n✅ Ahora puedes iniciar el backend:")
    print("   cd E:\\TESLA_COTIZADOR-V3.0\\backend")
    print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("\n✅ O ejecutar directamente desde PowerShell:")
    print("   cd E:\\TESLA_COTIZADOR-V3.0")
    print("   git pull")
    print("   # Luego reinicia el backend")
else:
    print("⚠️  ALGUNAS TABLAS NO SE CREARON")
    print("=" * 70)

print("\n" + "=" * 70)
