"""
Test para ver exactamente qué devuelve _generar_respuesta_chat
"""
import sys
sys.path.insert(0, 'e:/TESLA_COTIZADOR-V3.0/backend')

import asyncio
from app.services.pili_integrator import pili_integrator

async def test():
    # Llamar directamente a _generar_respuesta_chat
    respuesta = await pili_integrator._generar_respuesta_chat(
        mensaje="Certificado ITSE",
        tipo_flujo="cotizacion-simple",
        historial=[],
        servicio="itse",
        datos_acumulados={}
    )
    
    print("RESPUESTA COMPLETA:")
    print(respuesta)
    print("\nCAMPOS:")
    for key, value in respuesta.items():
        if key == "botones":
            print(f"  {key}: {len(value)} botones")
        else:
            val_str = str(value)[:100] if isinstance(value, str) else value
            print(f"  {key}: {val_str}")

asyncio.run(test())
