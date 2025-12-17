import requests
import json

cliente_test = {
    "nombre": "EMPRESA TEST 2 S.A.C.",
    "ruc": "20601777777",
    "direccion": "Av. Test 456",
    "telefono": "999777666",
    "email": "test2@empresa.com"
}

print("Enviando POST...")
response = requests.post("http://localhost:8000/api/clientes/", json=cliente_test)

print(f"\nStatus: {response.status_code}")
print(f"\nResponse completo:")
print(response.text)

if response.status_code != 200 and response.status_code != 201:
    try:
        error_json = response.json()
        print(f"\nError JSON formateado:")
        print(json.dumps(error_json, indent=2, ensure_ascii=False))
    except:
        print("No se pudo parsear como JSON")
