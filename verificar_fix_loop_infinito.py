#!/usr/bin/env python3
"""
Script de verificación del FIX del loop infinito
Verifica que el estado avance correctamente en el endpoint /pili-itse

Ejecutar: python verificar_fix_loop_infinito.py
"""

import requests
import json
from datetime import datetime

print("=" * 80)
print("🔍 VERIFICACIÓN DEL FIX - LOOP INFINITO ITSE")
print("=" * 80)
print()

# Configuración
BASE_URL = "http://localhost:8000"
ENDPOINT = f"{BASE_URL}/api/chat/pili-itse"

def hacer_request(mensaje: str, conversation_state: dict = None) -> dict:
    """Hace un request al endpoint y retorna la respuesta"""
    payload = {
        "mensaje": mensaje
    }

    if conversation_state:
        payload["conversation_state"] = conversation_state

    try:
        response = requests.post(ENDPOINT, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        print(f"❌ ERROR: No se pudo conectar al backend en {BASE_URL}")
        print(f"   Asegúrate de que el backend esté corriendo")
        return None
    except requests.exceptions.Timeout:
        print(f"❌ ERROR: Timeout al conectar con el backend")
        return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

# Test 1: Primer mensaje (sin estado)
print("📝 TEST 1: Primer mensaje (sin conversation_state)")
print("-" * 80)

response1 = hacer_request("Hola")

if not response1:
    print("\n⚠️ No se pudo realizar el test. Verifica que el backend esté corriendo.")
    exit(1)

print(f"✅ Respuesta recibida")
print(f"   Estado devuelto:")
print(f"   - etapa: {response1.get('state', {}).get('etapa')}")
print(f"   - categoria: {response1.get('state', {}).get('categoria')}")

estado_actual = response1.get('state', {})

# Verificar que el estado inicial sea correcto
if estado_actual.get('etapa') != 'categoria':
    print(f"\n❌ ERROR: Etapa inicial debería ser 'categoria', es '{estado_actual.get('etapa')}'")
    exit(1)

print()
print("=" * 80)
print("📝 TEST 2: Segundo mensaje CON conversation_state (SALUD)")
print("-" * 80)

# Test 2: Enviar categoría CON estado
response2 = hacer_request("SALUD", conversation_state=estado_actual)

if not response2:
    print("\n⚠️ No se pudo realizar el test 2")
    exit(1)

print(f"✅ Respuesta recibida")
nuevo_estado = response2.get('state', {})
print(f"   Estado enviado:")
print(f"   - etapa: {estado_actual.get('etapa')}")
print(f"   - categoria: {estado_actual.get('categoria')}")
print()
print(f"   Estado recibido:")
print(f"   - etapa: {nuevo_estado.get('etapa')}")
print(f"   - categoria: {nuevo_estado.get('categoria')}")
print(f"   - tipo: {nuevo_estado.get('tipo')}")

# VERIFICACIÓN CRÍTICA
print()
print("=" * 80)
print("🔍 VERIFICACIÓN CRÍTICA DEL FIX")
print("=" * 80)

# Verificar que el estado haya avanzado
if nuevo_estado.get('etapa') == 'tipo' and nuevo_estado.get('categoria') == 'SALUD':
    print("✅ ✅ ✅ FIX EXITOSO ✅ ✅ ✅")
    print()
    print("   🎉 El estado AVANZÓ correctamente:")
    print(f"      - Estado anterior: etapa='categoria', categoria=None")
    print(f"      - Estado nuevo: etapa='tipo', categoria='SALUD'")
    print()
    print("   ✅ El loop infinito está RESUELTO")

    # Test 3: Continuar la conversación
    print()
    print("=" * 80)
    print("📝 TEST 3: Continuar conversación (Hospital)")
    print("-" * 80)

    response3 = hacer_request("Hospital", conversation_state=nuevo_estado)

    if response3:
        estado_final = response3.get('state', {})
        print(f"✅ Respuesta recibida")
        print(f"   Estado recibido:")
        print(f"   - etapa: {estado_final.get('etapa')}")
        print(f"   - categoria: {estado_final.get('categoria')}")
        print(f"   - tipo: {estado_final.get('tipo')}")
        print(f"   - area: {estado_final.get('area')}")

        if estado_final.get('etapa') == 'area' and estado_final.get('tipo') == 'Hospital':
            print()
            print("   ✅ ✅ Estado continúa avanzando correctamente")
            print()
            print("=" * 80)
            print("🎊 TODOS LOS TESTS PASARON 🎊")
            print("=" * 80)
            print()
            print("✅ El chatbot ITSE funciona correctamente")
            print("✅ El loop infinito está completamente resuelto")
            print("✅ El estado avanza en cada mensaje")
            print()
            print("🚀 Próximo paso: Reiniciar el backend y probar en la interfaz web")
            print()
        else:
            print()
            print(f"⚠️ ADVERTENCIA: Estado no avanzó a 'area'")
            print(f"   Se esperaba: etapa='area', tipo='Hospital'")
            print(f"   Se recibió: etapa='{estado_final.get('etapa')}', tipo='{estado_final.get('tipo')}'")

else:
    print("❌ ❌ ❌ FIX NO FUNCIONÓ ❌ ❌ ❌")
    print()
    print("   🔴 El estado NO avanzó:")
    print(f"      - Estado enviado: etapa='categoria', categoria=None")
    print(f"      - Estado recibido: etapa='{nuevo_estado.get('etapa')}', categoria='{nuevo_estado.get('categoria')}'")
    print()
    print("   ❌ El loop infinito PERSISTE")
    print()
    print("   Posibles causas:")
    print("   1. El backend no se reinició después del fix")
    print("   2. Hay caché de Python (.pyc) que necesita limpiarse")
    print("   3. El schema ChatRequest no se actualizó correctamente")
    print()
    print("   Solución:")
    print("   1. Detener el backend (Ctrl+C)")
    print("   2. Limpiar caché: find . -type d -name __pycache__ -exec rm -r {} +")
    print("   3. Reiniciar: uvicorn app.main:app --reload")
    print("   4. Volver a ejecutar este script")

print()
print("=" * 80)
print("FIN DE LA VERIFICACIÓN")
print("=" * 80)
print()
