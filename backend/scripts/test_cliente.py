"""
Test minimal de inserción de cliente
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.cliente import Cliente

def test_insert():
    db = SessionLocal()
    try:
        print("Intentando insertar un cliente de prueba...")
        
        cliente = Cliente(
            nombre="Empresa Test",
            ruc="20600000001",
            direccion="Av. Test 123",
            telefono="999999999",
            email="test@test.com",
            ciudad="Lima",
            industria="Mineria",
            contacto_nombre="Juan Perez"
        )
        
        db.add(cliente)
        db.commit()
        
        print(f"OK - Cliente creado con ID: {cliente.id}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_insert()
