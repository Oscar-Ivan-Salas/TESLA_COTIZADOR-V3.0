"""
Script de Limpieza Definitiva - Cotizaciones con Formato Incorrecto
Elimina cotizaciones con números duplicados o mal formados
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.models.cotizacion import Cotizacion
import re

def limpiar_cotizaciones_malformadas():
    db = SessionLocal()
    try:
        # Patrón correcto: COT-YYYYMM-XXXX
        patron_correcto = re.compile(r'^COT-\d{6}-\d{4}$')
        
        # Obtener TODAS las cotizaciones
        todas = db.query(Cotizacion).all()
        
        cots_malas = []
        for cot in todas:
            if not patron_correcto.match(cot.numero):
                cots_malas.append(cot)
        
        print(f"Total cotizaciones: {len(todas)}")
        print(f"Cotizaciones con formato incorrecto: {len(cots_malas)}")
        print()
        
        if cots_malas:
            print("Cotizaciones a eliminar:")
            for cot in cots_malas:
                print(f"  - {cot.numero} (Cliente: {cot.cliente})")
            
            print()
            for cot in cots_malas:
                db.delete(cot)
            
            db.commit()
            print(f"\nEliminadas {len(cots_malas)} cotizaciones con formato incorrecto")
        else:
            print("No se encontraron cotizaciones con formato incorrecto")
        
        # Verificar total final
        total_final = db.query(Cotizacion).count()
        print(f"\nTotal cotizaciones en BD: {total_final}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    limpiar_cotizaciones_malformadas()
