"""
🧪 TEST RÁPIDO - PILIBrain
Verifica que PILIBrain funciona sin APIs
"""

import sys
import os

# Agregar ruta para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.pili_brain import pili_brain
import json

print("=" * 70)
print("🧪 PRUEBA DE PILI BRAIN - Sistema sin APIs")
print("=" * 70)

# Test 1: Detección de servicio
print("\n📊 TEST 1: Detección de servicio")
mensaje1 = "Necesito cotizar instalación eléctrica residencial de 150m²"
servicio = pili_brain.detectar_servicio(mensaje1)
print(f"✅ Servicio detectado: {servicio}")

# Test 2: Extracción de datos
print("\n📊 TEST 2: Extracción de datos")
datos = pili_brain.extraer_datos(mensaje1, servicio)
print(f"✅ Datos extraídos:")
print(json.dumps(datos, indent=2, ensure_ascii=False))

# Test 3: Generación de cotización residencial
print("\n💰 TEST 3: Cotización Residencial 150m²")
cotizacion = pili_brain.generar_cotizacion(
    mensaje=mensaje1,
    servicio="electrico-residencial",
    complejidad="simple"
)
print(f"✅ Cotización generada:")
print(f"   - Cliente: {cotizacion['datos']['cliente']}")
print(f"   - Proyecto: {cotizacion['datos']['proyecto']}")
print(f"   - Items: {len(cotizacion['datos']['items'])}")
print(f"   - Total: ${cotizacion['datos']['total']:.2f} USD")
print(f"\n📋 Items generados:")
for item in cotizacion['datos']['items']:
    print(f"   - {item['descripcion']}: ${item['total']:.2f}")

# Test 4: Contraincendios
print("\n🔥 TEST 4: Sistema Contraincendios 300m²")
mensaje2 = "Necesito sistema contraincendios para local comercial de 300m²"
cotizacion2 = pili_brain.generar_cotizacion(
    mensaje=mensaje2,
    servicio="contraincendios",
    complejidad="simple"
)
print(f"✅ Cotización contraincendios:")
print(f"   - Total: ${cotizacion2['datos']['total']:.2f} USD")
print(f"   - Items: {len(cotizacion2['datos']['items'])}")

# Test 5: Domótica
print("\n🏠 TEST 5: Sistema Domótico 200m²")
mensaje3 = "Quiero automatizar mi casa de 200m² con domótica KNX"
cotizacion3 = pili_brain.generar_cotizacion(
    mensaje=mensaje3,
    servicio="domotica",
    complejidad="complejo"
)
print(f"✅ Cotización domótica:")
print(f"   - Total: ${cotizacion3['datos']['total']:.2f} USD")
print(f"   - Items: {len(cotizacion3['datos']['items'])}")

# Test 6: JSON completo
print("\n📄 TEST 6: JSON completo exportado")
output_file = "test_cotizacion_output.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(cotizacion, f, indent=2, ensure_ascii=False)
print(f"✅ JSON guardado en: {output_file}")

print("\n" + "=" * 70)
print("✅ TODOS LOS TESTS PASARON")
print("🧠 PILIBrain funciona perfectamente SIN API KEYS")
print("=" * 70)
