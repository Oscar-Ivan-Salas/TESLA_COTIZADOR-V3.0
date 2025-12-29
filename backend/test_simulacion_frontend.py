"""
Test Final - Simular exactamente lo que hace el frontend
"""

import requests
import json

print("\n" + "="*70)
print("TEST FINAL - SIMULACION EXACTA DEL FRONTEND")
print("="*70 + "\n")

# Exactamente como lo envía el frontend
payload = {
    "tipo_flujo": "cotizacion-simple",  # Frontend envía esto
    "mensaje": "Certificado ITSE",  # Usuario selecciona este servicio
    "historial": [],
    "contexto_adicional": "Servicio: itse, Industria: , Contexto: ",
    "datos_cliente": {
        "nombre": "",
        "ruc": "",
        "direccion": "",
        "telefono": "",
        "email": ""
    },
    "archivos_procesados": [],
    "generar_html": True
}

try:
    print("Enviando peticion al endpoint...")
    print(f"Payload:\n{json.dumps(payload, indent=2)}\n")
    
    response = requests.post(
        "http://localhost:8000/api/chat/chat-contextualizado",
        json=payload,
        timeout=15
    )
    
    print(f"Status: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        
        print("RESPUESTA:")
        print("="*70)
        
        # Campos clave
        print(f"success: {data.get('success')}")
        print(f"mensaje/respuesta: {data.get('mensaje', data.get('respuesta', 'N/A'))[:150]}...")
        print(f"\nagente_pili: {data.get('agente_pili', 'N/A')}")
        print(f"modo: {data.get('modo', 'N/A')}")
        print(f"stage: {data.get('stage', 'N/A')}")
        print(f"progreso: {data.get('progreso', 'N/A')}")
        
        # Botones
        botones = data.get('botones_sugeridos') or data.get('botones_contextuales') or []
        print(f"\nBotones: {len(botones)}")
        if botones:
            for i, btn in enumerate(botones[:3], 1):
                if isinstance(btn, dict):
                    print(f"  {i}. {btn.get('text', btn.get('label', btn))}")
                else:
                    print(f"  {i}. {btn}")
        
        print("\n" + "="*70)
        print("DIAGNOSTICO:")
        print("="*70)
        
        if data.get('stage'):
            print("\n[OK] NUEVA ARQUITECTURA ACTIVA")
            print("     Sistema usando UniversalSpecialist")
            print("     PILI deberia funcionar correctamente")
        else:
            print("\n[PROBLEMA] Nueva arquitectura NO activa")
            print("           Sistema usando fallback")
            print("           Por eso frontend muestra modo demo")
            
            # Mostrar que campos faltan
            print("\nCampos faltantes:")
            if not data.get('stage'):
                print("  - stage (indica etapa de conversacion)")
            if not botones:
                print("  - botones (opciones para el usuario)")
            if not data.get('progreso'):
                print("  - progreso (indicador de avance)")
        
    else:
        print(f"[ERROR] {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70 + "\n")
