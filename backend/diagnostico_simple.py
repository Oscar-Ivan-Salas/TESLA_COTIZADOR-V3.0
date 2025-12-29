"""
Script Simple de Diagnóstico PILI
Encuentra el problema rápidamente
"""

import requests

print("\n" + "="*60)
print("DIAGNOSTICO RAPIDO - PILI")
print("="*60 + "\n")

# Test 1: Backend corriendo
print("1. Verificando backend...")
try:
    r = requests.get("http://localhost:8000/health", timeout=3)
    print(f"   [OK] Backend corriendo (status {r.status_code})")
except:
    print("   [ERROR] Backend NO responde")
    print("   SOLUCION: Reiniciar backend")
    exit(1)

# Test 2: Encontrar endpoint de chat
print("\n2. Buscando endpoint de chat...")
endpoints = ["/api/chat", "/chat", "/api/pili/chat"]
endpoint_found = None

for ep in endpoints:
    try:
        payload = {"mensaje": "test", "tipo_flujo": "cotizacion-simple", "historial": []}
        r = requests.post(f"http://localhost:8000{ep}", json=payload, timeout=5)
        if r.status_code == 200:
            endpoint_found = ep
            print(f"   [OK] Endpoint encontrado: {ep}")
            break
    except:
        pass

if not endpoint_found:
    print("   [ERROR] No se encontro endpoint de chat")
    print("   SOLUCION: Verificar rutas en backend")
    exit(1)

# Test 3: Probar respuesta
print("\n3. Probando respuesta de PILI...")
try:
    payload = {
        "mensaje": "Hola PILI, necesito cotizacion ITSE",
        "tipo_flujo": "cotizacion-simple",
        "historial": []
    }
    r = requests.post(f"http://localhost:8000{endpoint_found}", json=payload, timeout=10)
    data = r.json()
    
    print(f"   Modo: {data.get('modo', 'N/A')}")
    print(f"   Agente: {data.get('agente_pili', data.get('agente', 'N/A'))}")
    print(f"   Stage: {data.get('stage', 'N/A')}")
    print(f"   Botones: {len(data.get('botones', []))} opciones")
    
    # Diagnóstico
    print("\n" + "="*60)
    print("DIAGNOSTICO:")
    print("="*60)
    
    modo = data.get('modo', '')
    if 'demo' in modo.lower() or 'basico' in modo.lower():
        print("\nPROBLEMA: PILI esta en modo DEMO")
        print("\nCAUSAS POSIBLES:")
        print("1. Frontend tiene modo demo hardcodeado")
        print("2. Frontend no esta llamando al backend")
        print("3. Cache del navegador")
        print("\nSOLUCIONES:")
        print("1. Revisar App.jsx y buscar 'modo: demo'")
        print("2. Limpiar cache del navegador (Ctrl+Shift+Delete)")
        print("3. Verificar que frontend use http://localhost:8000")
    elif not data.get('stage'):
        print("\nPROBLEMA: Backend no retorna 'stage'")
        print("\nSOLUCION:")
        print("Verificar que pili_integrator este usando UniversalSpecialist")
    elif not data.get('botones'):
        print("\nPROBLEMA: Backend no retorna botones")
        print("\nSOLUCION:")
        print("Verificar que UniversalSpecialist genere botones en YAMLs")
    else:
        print("\n[OK] Backend funciona correctamente")
        print("\nSi aun ves modo demo en frontend:")
        print("1. Limpia cache del navegador")
        print("2. Verifica que frontend llame a http://localhost:8000")
        print("3. Revisa consola del navegador (F12) para ver errores")
    
except Exception as e:
    print(f"   [ERROR] {e}")

print("\n" + "="*60 + "\n")
