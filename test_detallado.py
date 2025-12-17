import requests
import json
import random
import traceback

ruc_aleatorio = f"206019{random.randint(10000, 99999)}"

cliente_test = {
    "nombre": "TEST DETALLADO S.A.C.",
    "ruc": ruc_aleatorio,
    "direccion": "Av. Test",
    "telefono": "999999999",
    "email": "test@test.com"
}

print(f"Creando cliente con RUC: {ruc_aleatorio}\n")

try:
    response = requests.post("http://localhost:8000/api/clientes/", json=cliente_test, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    print(f"\nHeaders: {dict(response.headers)}")
    print(f"\nRaw Text: {response.text}")
    
    try:
        json_response = response.json()
        print(f"\nJSON Response:")
        print(json.dumps(json_response, indent=2, ensure_ascii=False))
        
        if 'detail' in json_response:
            print(f"\n🔍 DETAIL: {json_response['detail']}")
            
    except Exception as e:
        print(f"\nNo se pudo parsear JSON: {e}")
        
except Exception as e:
    print(f"\nError en la petición: {e}")
    traceback.print_exc()
