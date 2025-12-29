"""
Test Final - Verificar respuesta exacta del backend
"""

import requests
import json

print("\n" + "="*70)
print("TEST FINAL - RESPUESTA DEL BACKEND")
print("="*70 + "\n")

endpoint = "http://localhost:8000/api/chat/chat-contextualizado"

payload = {
    "tipo_flujo": "cotizacion-simple",
    "mensaje": "Hola PILI, necesito una cotizacion ITSE",
    "historial": [],
    "contexto_adicional": "Servicio: itse",
    "datos_cliente": {
        "nombre": "Juan Perez",
        "ruc": "20601138787",
        "direccion": "Lima",
        "telefono": "999888777",
        "email": "juan@test.com"
    },
    "generar_html": True
}

try:
    print("Enviando peticion...")
    print(f"Endpoint: {endpoint}")
    print(f"Payload: {json.dumps(payload, indent=2)}\n")
    
    response = requests.post(endpoint, json=payload, timeout=15)
    
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        
        print("RESPUESTA COMPLETA DEL BACKEND:")
        print("="*70)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("="*70)
        
        print("\nANALISIS:")
        print("-"*70)
        print(f"success: {data.get('success')}")
        print(f"respuesta: {data.get('respuesta', 'N/A')[:100]}...")
        print(f"mensaje: {data.get('mensaje', 'N/A')[:100]}...")
        print(f"agente_pili: {data.get('agente_pili', 'N/A')}")
        print(f"modo: {data.get('modo', 'N/A')}")
        print(f"stage: {data.get('stage', 'N/A')}")
        print(f"progreso: {data.get('progreso', 'N/A')}")
        print(f"botones_sugeridos: {len(data.get('botones_sugeridos', []))} botones")
        print(f"botones_contextuales: {len(data.get('botones_contextuales', []))} botones")
        print(f"datos_generados: {bool(data.get('datos_generados'))}")
        print(f"html_preview: {bool(data.get('html_preview'))}")
        
        print("\n" + "="*70)
        print("DIAGNOSTICO FINAL:")
        print("="*70)
        
        if data.get('stage'):
            print("\n[OK] Backend usa NUEVA ARQUITECTURA MODULAR")
            print("     UniversalSpecialist esta activo")
        elif data.get('agente_pili'):
            print("\n[OK] Backend usa PILIIntegrator")
        else:
            print("\n[WARN] Backend responde sin arquitectura modular")
            print("       Posible fallback a modo basico")
        
        if not data.get('botones_sugeridos') and not data.get('botones_contextuales'):
            print("\n[PROBLEMA] No hay botones en la respuesta")
            print("           Frontend mostrara modo demo")
        
    else:
        print(f"[ERROR] Status {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70 + "\n")
