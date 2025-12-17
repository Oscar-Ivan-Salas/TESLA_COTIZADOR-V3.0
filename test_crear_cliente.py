"""
Script para probar la creación de cliente directamente con la API
y ver el error exacto
"""
import requests
import json

# Datos de prueba (exactamente como los envía el frontend)
cliente_test = {
    "nombre": "EMPRESA DE PRUEBA S.A.C.",
    "ruc": "20601888888",
    "direccion": "Av. Test 123",
    "telefono": "999888777",
    "email": "test@empresa.com"
}

print("="*60)
print("PRUEBA DE CREACIÓN DE CLIENTE")
print("="*60)
print(f"\nDatos a enviar:")
print(json.dumps(cliente_test, indent=2))

try:
    response = requests.post(
        "http://localhost:8000/api/clientes/",
        json=cliente_test,
        timeout=10
    )
    
    print(f"\n{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"{'='*60}")
    
    if response.status_code == 200 or response.status_code == 201:
        print("\n✅ ÉXITO!")
        print(json.dumps(response.json(), indent=2))
    else:
        print("\n❌ ERROR!")
        print(f"Response Text: {response.text}")
        try:
            print(f"\nJSON Error: {json.dumps(response.json(), indent=2)}")
        except:
            pass
            
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: No se puede conectar al servidor")
    print("Asegúrate de que el backend esté corriendo en http://localhost:8000")
except Exception as e:
    print(f"\n❌ ERROR INESPERADO: {str(e)}")
