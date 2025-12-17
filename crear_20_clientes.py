"""
Script para crear 20 clientes con RUCs únicos y diferentes
"""
import requests
import random

API_URL = "http://localhost:8000/api/clientes/"

# Generar 20 clientes con RUCs únicos
clientes = []
for i in range(1, 21):
    ruc = f"2060{random.randint(1000000, 9999999)}"  # RUC único de 11 dígitos
    cliente = {
        "nombre": f"EMPRESA TEST {i:02d} S.A.C.",
        "ruc": ruc,
        "direccion": f"Av. Test {i*100}, Huancayo",
        "telefono": f"96{random.randint(1000000, 9999999)}",
        "email": f"empresa{i:02d}@test.com"
    }
    clientes.append(cliente)

print("="*70)
print("CREACIÓN DE 20 CLIENTES DE PRUEBA")
print("="*70)

exitosos = 0
fallidos = 0
errores = []

for i, cliente in enumerate(clientes, 1):
    try:
        print(f"\n[{i}/20] Creando: {cliente['nombre']}")
        print(f"        RUC: {cliente['ruc']}")
        
        response = requests.post(API_URL, json=cliente, timeout=10)
        
        if response.status_code in [200, 201]:
            exitosos += 1
            print(f"        ✅ Creado exitosamente")
        else:
            fallidos += 1
            error_msg = response.text[:100]
            print(f"        ❌ Error {response.status_code}: {error_msg}")
            errores.append(f"Cliente {i}: {error_msg}")
            
    except Exception as e:
        fallidos += 1
        print(f"        ❌ Error: {str(e)[:100]}")
        errores.append(f"Cliente {i}: {str(e)[:100]}")

print("\n" + "="*70)
print("RESUMEN FINAL")
print("="*70)
print(f"✅ Exitosos: {exitosos}")
print(f"❌ Fallidos: {fallidos}")
print(f"📊 Total: {exitosos + fallidos}")

if errores:
    print(f"\n⚠️  Errores encontrados:")
    for error in errores[:5]:  # Mostrar solo los primeros 5
        print(f"   - {error}")

print("="*70)
