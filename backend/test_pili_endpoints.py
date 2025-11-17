"""
🧪 TEST ENDPOINTS PILI
Verifica que todos los endpoints de PILI estén funcionando
"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 80)
print("🧪 TEST ENDPOINTS PILI")
print("=" * 80)

tests_passed = 0
tests_failed = 0

# Test 1: Health Check
print("\n1️⃣ TEST: Health Check...")
try:
    response = requests.get(f"{BASE_URL}/api/chat/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Status: {data.get('status')}")
        print(f"   ✅ PILI Version: {data.get('pili_version')}")
        print(f"   ✅ Agentes disponibles: {data.get('agentes_disponibles')}")
        tests_passed += 1
    else:
        print(f"   ❌ Error: Status {response.status_code}")
        tests_failed += 1
except Exception as e:
    print(f"   ❌ Error: {e}")
    print(f"   ⚠️  ¿Está corriendo el backend? (uvicorn app.main:app --reload)")
    tests_failed += 1

# Test 2: Presentación PILI
print("\n2️⃣ TEST: Presentación PILI...")
try:
    response = requests.get(f"{BASE_URL}/api/chat/pili/presentacion", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Mensaje: {data.get('mensaje')[:50]}...")
        print(f"   ✅ Servicios: {len(data.get('servicios_disponibles', []))}")
        print(f"   ✅ Version: {data.get('version')}")
        tests_passed += 1
    else:
        print(f"   ❌ Error: Status {response.status_code}")
        tests_failed += 1
except Exception as e:
    print(f"   ❌ Error: {e}")
    tests_failed += 1

# Test 3: Botones Contextuales
print("\n3️⃣ TEST: Botones Contextuales...")
try:
    response = requests.get(
        f"{BASE_URL}/api/chat/botones-contextuales/cotizacion-simple",
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ PILI Activa: {data.get('pili_activa')}")
        print(f"   ✅ Botones: {len(data.get('botones', []))}")
        print(f"   ✅ Personalidad: {data.get('personalidad')[:50]}...")
        tests_passed += 1
    else:
        print(f"   ❌ Error: Status {response.status_code}")
        tests_failed += 1
except Exception as e:
    print(f"   ❌ Error: {e}")
    tests_failed += 1

# Test 4: Chat Contextualizado
print("\n4️⃣ TEST: Chat Contextualizado...")
try:
    payload = {
        "tipo_flujo": "cotizacion-simple",
        "mensaje": "Necesito una cotización para instalación eléctrica residencial",
        "historial": [],
        "contexto_adicional": "Prueba de PILI"
    }
    response = requests.post(
        f"{BASE_URL}/api/chat/chat-contextualizado",
        json=payload,
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Agente Activo: {data.get('agente_activo')}")
        print(f"   ✅ Respuesta: {data.get('respuesta')[:80]}...")
        print(f"   ✅ Botones: {len(data.get('botones_contextuales', []))}")
        tests_passed += 1
    else:
        print(f"   ❌ Error: Status {response.status_code}")
        print(f"   ❌ Response: {response.text[:200]}")
        tests_failed += 1
except Exception as e:
    print(f"   ❌ Error: {e}")
    tests_failed += 1

# Test 5: PILIBrain Offline
print("\n5️⃣ TEST: PILIBrain Offline...")
try:
    from app.services.pili_brain import pili_brain

    # Test detección de servicio
    servicio = pili_brain.detectar_servicio("instalación eléctrica residencial 150m²")
    print(f"   ✅ Servicio detectado: {servicio}")

    # Test generación cotización
    resultado = pili_brain.generar_cotizacion(
        mensaje="instalación eléctrica residencial 150m²",
        servicio=servicio,
        complejidad="simple"
    )

    print(f"   ✅ Conversación: {resultado['conversacion'][:50]}...")
    print(f"   ✅ Items generados: {len(resultado['datos']['items'])}")
    print(f"   ✅ Total: S/ {resultado['datos']['total']:.2f}")
    tests_passed += 1
except Exception as e:
    print(f"   ❌ Error: {e}")
    tests_failed += 1

# Resumen
print("\n" + "=" * 80)
print(f"📊 RESUMEN:")
print(f"   ✅ Tests exitosos: {tests_passed}")
print(f"   ❌ Tests fallidos: {tests_failed}")
print(f"   📈 Total: {tests_passed + tests_failed}")

if tests_failed == 0:
    print("\n🎉 TODOS LOS TESTS PASARON - PILI ESTÁ FUNCIONANDO CORRECTAMENTE")
else:
    print(f"\n⚠️  {tests_failed} TESTS FALLARON - REVISA LOS ERRORES ARRIBA")

print("=" * 80)
