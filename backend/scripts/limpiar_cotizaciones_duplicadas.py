"""
Script para limpiar cotizaciones duplicadas y corregir numeración
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.models.cotizacion import Cotizacion

def limpiar_duplicados():
    db = SessionLocal()
    try:
        # Buscar cotizaciones con formato incorrecto
        cots_malas = db.query(Cotizacion).filter(
            Cotizacion.numero.like('COT-202512-202512%')
        ).all()
        
        print(f"Encontradas {len(cots_malas)} cotizaciones con formato incorrecto")
        
        for cot in cots_malas:
            print(f"Eliminando: {cot.numero}")
            db.delete(cot)
        
        db.commit()
        print(f"\nLimpieza completada. {len(cots_malas)} cotizaciones eliminadas.")
        
        # Verificar cotizaciones restantes
        total = db.query(Cotizacion).count()
        print(f"Total de cotizaciones en BD: {total}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    limpiar_duplicados()
