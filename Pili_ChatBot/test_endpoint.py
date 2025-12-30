# Test rápido del endpoint
import requests
import json

url = "http://localhost:8000/api/chat/pili-itse"

# Test 1: Inicio
payload = {
    "mensaje": "",
    "conversation_state": None
}

print("Test 1: Llamando endpoint...")
try:
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Respuesta: {data.get('respuesta')[:100]}...")
        print(f"Botones: {len(data.get('botones', []))}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error de conexión: {e}")
