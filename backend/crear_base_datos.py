#!/usr/bin/env python3
"""
🗄️ SCRIPT DE CREACIÓN DE BASE DE DATOS
==========================================
Este script GARANTIZA la creación de la base de datos en la ubicación correcta.

EJECUTAR ESTE SCRIPT ANTES DE INICIAR EL BACKEND:
    cd backend
    python crear_base_datos.py

Luego iniciar el backend:
    python -m uvicorn app.main:app --reload
"""

import sys
from pathlib import Path
import sqlite3

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent
project_root = backend_dir.parent
sys.path.insert(0, str(backend_dir))

print("=" * 70)
print("🗄️  CREACIÓN DE BASE DE DATOS - TESLA COTIZADOR V3.0")
print("=" * 70)

# ===================================================================
# PASO 1: Crear carpeta database/ en la raíz del proyecto
# ===================================================================
database_dir = project_root / "database"
database_dir.mkdir(parents=True, exist_ok=True)
print(f"\n✅ Carpeta creada/verificada: {database_dir}")

# ===================================================================
# PASO 2: Crear archivo de base de datos SQLite
# ===================================================================
db_file = database_dir / "tesla_cotizador.db"
print(f"\n📝 Creando archivo de base de datos: {db_file}")

# Crear conexión para forzar la creación del archivo
conn = sqlite3.connect(str(db_file))
conn.close()
print(f"✅ Archivo de base de datos creado: {db_file}")

# ===================================================================
# PASO 3: Importar modelos y crear tablas
# ===================================================================
print("\n🔧 Importando modelos SQLAlchemy...")

try:
    from app.core.database import Base, engine
    from app.models import Cotizacion, Proyecto, Documento, Item

    print("✅ Modelos importados correctamente")

    # Mostrar modelos registrados
    print("\n📋 Modelos registrados en Base.metadata:")
    for table_name in Base.metadata.tables.keys():
        print(f"   - {table_name}")

    # ===================================================================
    # PASO 4: Crear todas las tablas
    # ===================================================================
    print("\n🏗️  Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")

    # ===================================================================
    # PASO 5: Verificar tablas creadas
    # ===================================================================
    print("\n🔍 Verificando tablas creadas:")
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    expected_tables = ["cotizaciones", "proyectos", "documentos", "items"]
    all_ok = True

    for table in expected_tables:
        if table in tables:
            # Contar columnas
            columns = inspector.get_columns(table)
            print(f"   ✅ {table} ({len(columns)} columnas)")
        else:
            print(f"   ❌ {table} - NO ENCONTRADA")
            all_ok = False

    # ===================================================================
    # PASO 6: Resumen final
    # ===================================================================
    print("\n" + "=" * 70)
    if all_ok:
        print("🎉 BASE DE DATOS CREADA EXITOSAMENTE")
        print("=" * 70)
        print(f"\n📍 Ubicación: {db_file}")
        print(f"📊 Tablas creadas: {len(tables)}")
        print("\n✅ Ahora puedes iniciar el backend:")
        print("   cd backend")
        print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("⚠️  ALGUNAS TABLAS NO SE CREARON")
        print("=" * 70)
        print("\nRevisa los errores arriba.")

    print("\n" + "=" * 70)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nDetalles del error:")
    import traceback
    traceback.print_exc()
    sys.exit(1)
