import requests
import json

# Test endpoint /mensaje
url = "http://localhost:8000/api/chat/mensaje"
payload = {
    "tipo_flujo": "cotizacion-simple",
    "mensaje": "Necesito una cotización para instalación eléctrica",
    "historial": [],
    "contexto_adicional": "",
    "cotizacion_id": None,
    "archivos_procesados": [],
    "generar_html": True
}

headers = {
    "Content-Type": "application/json"
}

print("🔍 Probando endpoint /mensaje...")
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print("\n" + "="*50 + "\n")

try:
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    print(f"✅ Status Code: {response.status_code}")
    print(f"\n📄 Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except requests.exceptions.ConnectionError:
    print("❌ ERROR: No se puede conectar al backend")
    print("Verifica que el servidor esté corriendo en http://localhost:8000")
except requests.exceptions.Timeout:
    print("❌ ERROR: Timeout - El servidor no respondió a tiempo")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    if hasattr(e, 'response'):
        print(f"Response text: {e.response.text}")
