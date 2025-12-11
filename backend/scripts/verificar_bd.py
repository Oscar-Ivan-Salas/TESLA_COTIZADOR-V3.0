"""
Verificar y crear tabla proyectos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.database import engine, Base
from app.models.proyecto import Proyecto
from app.models.cliente import Cliente
from app.models.cotizacion import Cotizacion

# Crear todas las tablas
print("Creando tablas...")
Base.metadata.create_all(bind=engine)

# Verificar tablas
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()

print(f"\nTablas en BD:")
for table in tables:
    print(f"  - {table}")

print(f"\nTotal: {len(tables)} tablas")

# Contar registros
from app.core.database import SessionLocal
db = SessionLocal()

try:
    clientes = db.query(Cliente).count()
    cotizaciones = db.query(Cotizacion).count()
    proyectos = db.query(Proyecto).count()
    
    print(f"\nRegistros:")
    print(f"  - Clientes: {clientes}")
    print(f"  - Cotizaciones: {cotizaciones}")
    print(f"  - Proyectos: {proyectos}")
    print(f"  - TOTAL: {clientes + cotizaciones + proyectos}")
    
except Exception as e:
    print(f"\nError al contar: {e}")
finally:
    db.close()
