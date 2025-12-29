import requests
import json

url_root = "http://localhost:8000/"
url_gen = "http://localhost:8000/api/generar-documento-directo?formato=word"

try:
    print(f"Consultando estado del servidor en {url_root}...")
    response = requests.get(url_root)
    if response.status_code == 200:
        data = response.json()
        print("✅ Estado del servidor:")
        print(json.dumps(data, indent=2))
        
        routers = data.get("routers_cargados", [])
        if "generar_directo" in routers:
            print("✅ Router 'generar_directo' está cargado!")
        else:
            print("❌ Router 'generar_directo' NO está en la lista de cargados.")
    else:
        print(f"❌ Error al consultar raíz: {response.status_code}")

    print(f"\nProbando endpoint {url_gen}...")
    # Datos mínimos para prueba
    payload = {"items": []} 
    response = requests.post(url_gen, json=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 404:
        print("✅ Endpoint encontrado (aunque devuelva error de validación)")
    else:
        print("❌ Endpoint sigue dando 404")

except Exception as e:
    print(f"❌ Excepción: {e}")
