import requests
import json

url = "http://localhost:8000/api/generar-documento-directo?formato=word"

datos = {
    "cliente": "Cliente Prueba",
    "proyecto": "Proyecto Verificación",
    "items": [
        {"descripcion": "Item 1", "cantidad": 1, "precioUnitario": 100.0}
    ]
}

try:
    print(f"Probando endpoint: {url}")
    response = requests.post(url, json=datos)
    
    if response.status_code == 200:
        print("✅ ÉXITO: Endpoint activo y respondiendo")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        with open("prueba_generada.docx", "wb") as f:
            f.write(response.content)
        print("📄 Archivo guardado como prueba_generada.docx")
    else:
        print(f"❌ ERROR: Status {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ EXCEPCIÓN: {e}")
