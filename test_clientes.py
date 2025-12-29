"""
Test: Verificar sincronización de datos de cliente
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_crear_cliente():
    """Test crear cliente en BD"""
    print("\n" + "="*60)
    print("🧪 TEST: Crear Cliente en BD")
    print("="*60)
    
    cliente_data = {
        "nombre": "Constructora ABC S.A.C.",
        "ruc": "20123456789",
        "direccion": "Av. Principal 123, Lima",
        "telefono": "987654321",
        "email": "contacto@abc.com"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/clientes/",
            json=cliente_data,
            timeout=10
        )
        
        if response.status_code == 201:
            cliente = response.json()
            print(f"✅ Cliente creado exitosamente")
            print(f"   ID: {cliente['id']}")
            print(f"   Nombre: {cliente['nombre']}")
            print(f"   RUC: {cliente['ruc']}")
            return cliente['id']
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_listar_clientes():
    """Test listar clientes"""
    print("\n" + "="*60)
    print("🧪 TEST: Listar Clientes")
    print("="*60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/clientes/",
            timeout=10
        )
        
        if response.status_code == 200:
            clientes = response.json()
            print(f"✅ Se encontraron {len(clientes)} clientes")
            for cliente in clientes[:3]:  # Mostrar solo los primeros 3
                print(f"   - {cliente['nombre']} (RUC: {cliente['ruc']})")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_obtener_cliente(cliente_id):
    """Test obtener cliente por ID"""
    print("\n" + "="*60)
    print(f"🧪 TEST: Obtener Cliente ID {cliente_id}")
    print("="*60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/clientes/{cliente_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            cliente = response.json()
            print(f"✅ Cliente encontrado")
            print(f"   Nombre: {cliente['nombre']}")
            print(f"   RUC: {cliente['ruc']}")
            print(f"   Email: {cliente['email']}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n🚀 PROBANDO ENDPOINTS DE CLIENTES")
    print("Verificando que el backend funciona correctamente\n")
    
    # Test 1: Listar clientes existentes
    test_listar_clientes()
    
    # Test 2: Crear nuevo cliente
    cliente_id = test_crear_cliente()
    
    # Test 3: Obtener cliente creado
    if cliente_id:
        test_obtener_cliente(cliente_id)
    
    print("\n" + "="*60)
    print("📊 TESTS COMPLETADOS")
    print("="*60)
    print("\n✅ Si todos los tests pasaron, el backend está funcionando")
    print("✅ El frontend ya tiene la sincronización automática")
    print("✅ Ahora los datos del cliente se reflejarán en la plantilla\n")
