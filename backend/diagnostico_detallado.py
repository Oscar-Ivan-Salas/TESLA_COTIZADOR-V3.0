"""
Script de Diagnóstico con Logs Detallados
"""

import sys
sys.path.insert(0, 'e:/TESLA_COTIZADOR-V3.0/backend')

import logging
logging.basicConfig(level=logging.DEBUG)

print("\n" + "="*70)
print("DIAGNOSTICO CON LOGS DETALLADOS")
print("="*70 + "\n")

# 1. Verificar imports
print("1. Verificando imports...")
try:
    from app.services.pili.specialist import UniversalSpecialist
    print("   [OK] UniversalSpecialist importado")
except Exception as e:
    print(f"   [ERROR] No se pudo importar UniversalSpecialist: {e}")
    exit(1)

try:
    from app.services.pili_integrator import pili_integrator, NUEVA_ARQUITECTURA_DISPONIBLE, SERVICIOS_MIGRADOS
    print(f"   [OK] pili_integrator importado")
    print(f"   NUEVA_ARQUITECTURA_DISPONIBLE = {NUEVA_ARQUITECTURA_DISPONIBLE}")
    print(f"   SERVICIOS_MIGRADOS = {SERVICIOS_MIGRADOS}")
except Exception as e:
    print(f"   [ERROR] No se pudo importar pili_integrator: {e}")
    exit(1)

# 2. Probar detección de servicio
print("\n2. Probando detección de servicio...")
from app.services.pili_brain import PILIBrain
pili_brain = PILIBrain()

mensaje = "Certificado ITSE"
servicio_detectado = pili_brain.detectar_servicio(mensaje)
print(f"   Mensaje: '{mensaje}'")
print(f"   Servicio detectado: '{servicio_detectado}'")
print(f"   ¿Está en SERVICIOS_MIGRADOS? {servicio_detectado in SERVICIOS_MIGRADOS}")

# 3. Probar UniversalSpecialist directamente
print("\n3. Probando UniversalSpecialist directamente...")
try:
    specialist = UniversalSpecialist(servicio_detectado, "cotizacion-simple")
    print(f"   [OK] Specialist creado para '{servicio_detectado}'")
    
    response = specialist.process_message("Hola")
    print(f"   [OK] Mensaje procesado")
    print(f"   Respuesta: {response.get('texto', '')[:100]}...")
    print(f"   Stage: {response.get('stage')}")
    print(f"   Botones: {len(response.get('botones', []))}")
except Exception as e:
    print(f"   [ERROR] {e}")
    import traceback
    traceback.print_exc()

# 4. Probar pili_integrator
print("\n4. Probando pili_integrator...")
import asyncio

async def test_integrator():
    try:
        resultado = await pili_integrator.procesar_solicitud_completa(
            mensaje="Certificado ITSE",
            tipo_flujo="cotizacion-simple",
            historial=[],
            generar_documento=False
        )
        
        print(f"   [OK] pili_integrator respondió")
        print(f"   success: {resultado.get('success')}")
        print(f"   respuesta: {resultado.get('respuesta', '')[:100]}...")
        print(f"   agente_pili: {resultado.get('agente_pili')}")
        print(f"   modo: {resultado.get('modo')}")
        
        # Verificar si tiene campos de nueva arquitectura
        if 'stage' in resultado or 'progreso' in resultado:
            print("\n   [OK] NUEVA ARQUITECTURA ACTIVA")
        else:
            print("\n   [PROBLEMA] Nueva arquitectura NO activa")
            print(f"   Campos en resultado: {list(resultado.keys())}")
        
        return resultado
    except Exception as e:
        print(f"   [ERROR] {e}")
        import traceback
        traceback.print_exc()
        return None

resultado = asyncio.run(test_integrator())

print("\n" + "="*70)
print("CONCLUSION:")
print("="*70)

if resultado and resultado.get('success'):
    if 'stage' in resultado:
        print("\n[OK] Sistema funcionando con nueva arquitectura")
    else:
        print("\n[PROBLEMA] Sistema funciona pero usa fallback")
        print("Revisar logs arriba para ver el error")
else:
    print("\n[ERROR] Sistema no funciona")

print("\n" + "="*70 + "\n")
