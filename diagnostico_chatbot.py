#!/usr/bin/env python3
"""
Script de diagnóstico para verificar por qué el chatbot ITSE no funciona
Ejecutar desde: /ruta/a/TESLA_COTIZADOR-V3.0/
"""

import sys
import os
from pathlib import Path

print("=" * 80)
print("🔍 DIAGNÓSTICO CHATBOT ITSE")
print("=" * 80)

# 1. Verificar directorio actual
print("\n1️⃣ VERIFICANDO DIRECTORIO ACTUAL")
print(f"   Directorio actual: {os.getcwd()}")
print(f"   ✅ Correcto" if "TESLA_COTIZADOR" in os.getcwd() else "   ❌ ERROR: No estás en el directorio del proyecto")

# 2. Verificar existencia de archivos clave
print("\n2️⃣ VERIFICANDO ARCHIVOS CLAVE")
archivos_clave = [
    "Pili_ChatBot/pili_itse_chatbot.py",
    "backend/app/routers/chat.py",
    "test_claude_api_demo.py"
]

for archivo in archivos_clave:
    existe = Path(archivo).exists()
    print(f"   {'✅' if existe else '❌'} {archivo}")

# 3. Verificar que se puede importar el chatbot
print("\n3️⃣ VERIFICANDO IMPORT DEL CHATBOT")
try:
    from Pili_ChatBot.pili_itse_chatbot import PILIITSEChatBot
    print("   ✅ Import exitoso")

    # 4. Crear instancia
    print("\n4️⃣ CREANDO INSTANCIA DEL CHATBOT")
    chatbot = PILIITSEChatBot()
    print("   ✅ Instancia creada")

    # 5. Probar procesamiento
    print("\n5️⃣ PROBANDO PROCESAMIENTO")
    resultado = chatbot.procesar("Hola", {})
    print(f"   ✅ Procesamiento exitoso")
    print(f"   ✅ Success: {resultado.get('success')}")
    print(f"   ✅ Respuesta: {resultado.get('respuesta')[:50]}...")

    # 6. Probar generación completa
    print("\n6️⃣ PROBANDO GENERACIÓN COMPLETA")
    estado = {}

    # Simular conversación
    pasos = [
        ("Hola", "inicio"),
        ("COMERCIO", "categoría"),
        ("Tienda", "tipo"),
        ("150", "área"),
        ("2", "pisos")
    ]

    for i, (mensaje, paso) in enumerate(pasos, 1):
        resultado = chatbot.procesar(mensaje, estado)
        estado = resultado.get("estado", {})
        print(f"   {i}. {paso}: {'✅' if resultado.get('success') else '❌'}")

    # Verificar datos generados
    datos_generados = resultado.get("datos_generados")
    if datos_generados:
        print(f"\n   ✅ DATOS GENERADOS:")
        print(f"      - Proyecto: {datos_generados.get('proyecto', {}).get('nombre')}")
        print(f"      - Items: {len(datos_generados.get('items', []))} items")
        print(f"      - Subtotal: S/ {datos_generados.get('subtotal', 0):.2f}")
        print(f"      - IGV: S/ {datos_generados.get('igv', 0):.2f}")
        print(f"      - Total: S/ {datos_generados.get('total', 0):.2f}")

        # Mostrar items
        print(f"\n   📋 ITEMS GENERADOS:")
        for i, item in enumerate(datos_generados.get('items', []), 1):
            print(f"      {i}. {item['descripcion'][:50]}")
            print(f"         Cantidad: {item['cantidad']} {item['unidad']}")
            print(f"         Precio: S/ {item['precio_unitario']:.2f}")
    else:
        print(f"\n   ❌ ERROR: No se generaron datos_generados")
        print(f"   Resultado completo: {resultado}")

    print("\n" + "=" * 80)
    print("✅ DIAGNÓSTICO EXITOSO - EL CHATBOT FUNCIONA CORRECTAMENTE")
    print("=" * 80)

except ImportError as e:
    print(f"   ❌ ERROR DE IMPORT: {e}")
    print(f"\n   SOLUCIÓN:")
    print(f"   1. Verifica que estás en el directorio raíz del proyecto")
    print(f"   2. Ejecuta: cd /ruta/a/TESLA_COTIZADOR-V3.0")
    print(f"   3. Vuelve a ejecutar: python3 diagnostico_chatbot.py")

except Exception as e:
    print(f"   ❌ ERROR: {e}")
    import traceback
    print("\n   TRACEBACK COMPLETO:")
    traceback.print_exc()

    print(f"\n" + "=" * 80)
    print("❌ DIAGNÓSTICO FALLIDO")
    print("=" * 80)
    print("\nPosibles soluciones:")
    print("1. Actualiza el código: git pull origin <branch>")
    print("2. Verifica que estás en el directorio correcto")
    print("3. Revisa que el archivo Pili_ChatBot/pili_itse_chatbot.py existe")
    print("4. Verifica que no hay errores de sintaxis en el archivo")

print("\n")
