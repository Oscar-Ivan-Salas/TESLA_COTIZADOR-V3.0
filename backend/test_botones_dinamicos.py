"""
Test de botones dinámicos
"""
import sys
sys.path.insert(0, 'e:/TESLA_COTIZADOR-V3.0/backend')

from app.services.pili.specialist import UniversalSpecialist

s = UniversalSpecialist('itse', 'cotizacion-simple')

# Etapa 1: Categoría
r1 = s.process_message('')
print(f"ETAPA 1 - Botones: {len(r1.get('botones', []))}")
print(f"ETAPA 1 - Stage: {r1.get('stage')}")

# Etapa 2: Tipo (después de seleccionar SALUD)
r2 = s.process_message('SALUD')
print(f"\nETAPA 2 - Botones: {len(r2.get('botones', []))}")
print(f"ETAPA 2 - Stage: {r2.get('stage')}")
if r2.get('botones'):
    print(f"Primer botón: {r2['botones'][0]}")
