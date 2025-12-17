"""
Script de diagnóstico para verificar el estado del router de clientes
"""
import sys
sys.path.insert(0, 'E:/TESLA_COTIZADOR-V3.0/backend')

print("="*60)
print("DIAGNÓSTICO DEL ROUTER DE CLIENTES")
print("="*60)

# Test 1: Importar el router directamente
print("\n1. Intentando importar router de clientes...")
try:
    from app.routers import clientes
    print("   ✅ Import exitoso")
    print(f"   Router: {clientes.router}")
    print(f"   Prefix esperado: /api/clientes")
except Exception as e:
    print(f"   ❌ Error en import: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Verificar schemas
print("\n2. Verificando schemas de cliente...")
try:
    from app.schemas.cliente import ClienteCreate, ClienteUpdate
    print("   ✅ Schemas importados correctamente")
except Exception as e:
    print(f"   ❌ Error en schemas: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Verificar modelo
print("\n3. Verificando modelo Cliente...")
try:
    from app.models.cliente import Cliente
    print("   ✅ Modelo importado correctamente")
    print(f"   Tabla: {Cliente.__tablename__}")
except Exception as e:
    print(f"   ❌ Error en modelo: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Verificar endpoint
print("\n4. Verificando endpoint en servidor...")
import requests
try:
    r = requests.get('http://localhost:8000/api/clientes/', timeout=5)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   ✅ Endpoint funcionando - {len(r.json())} clientes")
    else:
        print(f"   ❌ Endpoint devuelve: {r.status_code}")
        print(f"   Response: {r.text[:200]}")
except requests.exceptions.ConnectionError:
    print("   ❌ No se puede conectar al servidor")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
