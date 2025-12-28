"""
Test directo de pili_integrator para ver el error exacto
"""
import sys
sys.path.insert(0, 'e:/TESLA_COTIZADOR-V3.0/backend')

import asyncio
from app.services.pili_integrator import pili_integrator

async def test():
    try:
        resultado = await pili_integrator.procesar_solicitud_completa(
            mensaje="Certificado ITSE",
            tipo_flujo="cotizacion-simple",
            historial=[],
            generar_documento=False
        )
        
        print("SUCCESS:", resultado.get('success'))
        print("RESPUESTA:", resultado.get('respuesta', 'N/A')[:100])
        print("AGENTE:", resultado.get('agente_pili', 'N/A'))
        print("BOTONES:", len(resultado.get('botones_sugeridos', [])))
        print("ERROR:", resultado.get('error', 'N/A'))
        
    except Exception as e:
        print(f"EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
