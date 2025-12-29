"""
Script de diagnóstico para probar el endpoint de chat ITSE directamente
"""
import requests
import json

url = "http://localhost:8000/api/chat/chat-contextualizado"

payload = {
    "tipo_flujo": "cotizacion-simple",
    "mensaje": "Hola",
    "historial": [],
    "contexto_adicional": "Servicio: itse",
    "generar_html": True,
    "conversation_state": None
}

print("=" * 80)
print("DIAGNÓSTICO: Probando endpoint chat-contextualizado")
print("=" * 80)
print(f"\nURL: {url}")
print(f"\nPayload enviado:")
print(json.dumps(payload, indent=2, ensure_ascii=False))
print("\n" + "=" * 80)

try:
    response = requests.post(url, json=payload, timeout=10)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"\nRespuesta del servidor:")
    print("=" * 80)
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        print("\n" + "=" * 80)
        print("ANÁLISIS DE LA RESPUESTA:")
        print("=" * 80)
        
        if data.get("success"):
            print("✅ Success: True")
            respuesta_texto = data.get("respuesta", "")
            print(f"\n📝 Texto de respuesta (primeros 200 caracteres):")
            print(respuesta_texto[:200])
            
            if "ITSE" in respuesta_texto or "Salud" in respuesta_texto:
                print("\n✅ CORRECTO: La respuesta contiene contenido de ITSE")
            elif "Eléctric" in respuesta_texto or "CNE" in respuesta_texto:
                print("\n❌ ERROR: La respuesta contiene contenido de ELECTRICIDAD")
            
            if data.get("botones_sugeridos"):
                print(f"\n🔘 Botones sugeridos: {len(data['botones_sugeridos'])} botones")
                for btn in data.get("botones_sugeridos", [])[:3]:
                    print(f"   - {btn}")
        else:
            print(f"❌ Success: False")
            print(f"Error: {data.get('error', 'No error message')}")
    else:
        print(f"❌ Error HTTP {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ EXCEPCIÓN: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
