import requests
import json

url = "http://localhost:8000/api/chat/chat-contextualizado"
# Mensaje SIN números para forzar valores None en extracción
payload = {
    "tipo_flujo": "cotizacion-simple",
    "mensaje": "Hola, quiero una cotización", 
    "historial": [],
    "contexto_adicional": "",
    "archivos_procesados": []
}

try:
    print("Enviando mensaje sin datos numéricos...")
    response = requests.post(url, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("Success:", data.get("success"))
        print("Respuesta:", data.get("respuesta")[:100] + "...")
        with open("response_error_check.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        print("Error:", response.text)

except Exception as e:
    print(f"Excepción: {e}")
