#!/usr/bin/env python3
"""
🗄️ Script de Inicialización de Base de Datos
================================================
Crea todas las tablas necesarias para PILI v3.0

IMPORTANTE: Ejecuta este script ANTES de iniciar el servidor backend

Uso:
    cd backend
    python init_database.py

Tablas que crea:
- cotizaciones
- proyectos
- informes
- documentos
- items
"""

import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.database import engine, Base, init_db, check_db_connection
from app.models import Cotizacion, Proyecto, Documento, Item
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Inicializar base de datos"""

    print("=" * 60)
    print("🗄️  INICIALIZACIÓN DE BASE DE DATOS - PILI v3.0")
    print("=" * 60)

    # Verificar conexión
    print("\n1️⃣  Verificando conexión a base de datos...")
    if not check_db_connection():
        print("❌ Error: No se pudo conectar a la base de datos")
        return False
    print("✅ Conexión exitosa")

    # Mostrar modelos que se crearán
    print("\n2️⃣  Modelos registrados:")
    for table_name in Base.metadata.tables.keys():
        print(f"   - {table_name}")

    # Crear tablas
    print("\n3️⃣  Creando tablas...")
    try:
        init_db()
        print("✅ Todas las tablas creadas exitosamente")
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        return False

    # Verificar tablas creadas
    print("\n4️⃣  Verificando tablas creadas:")
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    expected_tables = ["cotizaciones", "proyectos", "documentos", "items"]
    all_ok = True

    for table in expected_tables:
        if table in tables:
            print(f"   ✅ {table}")
        else:
            print(f"   ❌ {table} - NO ENCONTRADA")
            all_ok = False

    print("\n" + "=" * 60)
    if all_ok:
        print("🎉 BASE DE DATOS INICIALIZADA CORRECTAMENTE")
        print("=" * 60)
        print("\n✅ Ahora puedes iniciar el servidor backend:")
        print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("⚠️  ALGUNAS TABLAS NO SE CREARON CORRECTAMENTE")
        print("=" * 60)

    return all_ok


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
