import requests
import json
import random

# Generar RUC aleatorio para evitar duplicados
ruc_aleatorio = f"206019{random.randint(10000, 99999)}"

cliente_test = {
    "nombre": "CLIENTE FINAL PRUEBA S.A.C.",
    "ruc": ruc_aleatorio,
    "direccion": "Av. Final 999",
    "telefono": "999666555",
    "email": "final@prueba.com"
}

print(f"Creando cliente con RUC: {ruc_aleatorio}")
response = requests.post("http://localhost:8000/api/clientes/", json=cliente_test)

print(f"\nStatus: {response.status_code}")

if response.status_code == 200 or response.status_code == 201:
    print("\n✅ ¡ÉXITO! Cliente creado correctamente")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
else:
    print(f"\n❌ Error: {response.text}")
