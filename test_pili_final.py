import requests
import json

url = "http://localhost:8000/api/chat/chat-contextualizado"
payload = {
    "tipo_flujo": "cotizacion-simple",
    "mensaje": "Necesito cotizar una instalación eléctrica para una casa de 120m2",
    "historial": [],
    "contexto_adicional": "",
    "archivos_procesados": []
}

try:
    response = requests.post(url, json=payload, timeout=10)
    with open("final_response.json", "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=2, ensure_ascii=False)
    print("Response saved to final_response.json")
except Exception as e:
    print(f"Error: {e}")
