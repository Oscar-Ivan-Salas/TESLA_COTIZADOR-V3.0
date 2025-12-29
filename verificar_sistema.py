"""
Script de Verificación del Sistema TESLA COTIZADOR v3.0
Prueba el endpoint profesional y genera reporte
"""

import requests
import json
from datetime import datetime

print("=" * 60)
print("🔍 VERIFICACIÓN DEL SISTEMA TESLA COTIZADOR v3.0")
print("=" * 60)
print()

resultados = {
    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "pruebas": []
}

# Prueba 1: Verificar backend está corriendo
print("📡 Prueba 1: Verificando backend...")
try:
    response = requests.get("http://localhost:8000/", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Backend ACTIVO")
        print(f"   📊 Versión: {data.get('version', 'N/A')}")
        print(f"   🔧 Modo: {data.get('modo', 'N/A')}")
        print(f"   🚀 Routers avanzados: {data.get('routers_avanzados', False)}")
        resultados["pruebas"].append({
            "nombre": "Backend Status",
            "estado": "✅ PASS",
            "detalles": data
        })
    else:
        print(f"   ❌ Backend respondió con código: {response.status_code}")
        resultados["pruebas"].append({
            "nombre": "Backend Status",
            "estado": "❌ FAIL",
            "error": f"Código {response.status_code}"
        })
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    resultados["pruebas"].append({
        "nombre": "Backend Status",
        "estado": "❌ FAIL",
        "error": str(e)
    })

print()

# Prueba 2: Probar endpoint profesional
print("🤖 Prueba 2: Probando endpoint profesional /api/chat/chat-contextualizado...")
try:
    payload = {
        "tipo_flujo": "cotizacion-simple",
        "mensaje": "Cotización para casa de 100m2",
        "historial": [],
        "contexto_adicional": "",
        "generar_html": True
    }
    
    response = requests.post(
        "http://localhost:8000/api/chat/chat-contextualizado",
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Endpoint profesional FUNCIONA")
        print(f"   📝 Respuesta recibida: {data.get('respuesta', '')[:100]}...")
        print(f"   🎯 Agente activo: {data.get('agente_activo', 'N/A')}")
        
        # Verificar si generó cotización
        if data.get('cotizacion_generada'):
            cot = data['cotizacion_generada']
            items = cot.get('items', [])
            print(f"   ✅ Cotización generada con {len(items)} items")
            if items:
                print(f"   📋 Primer item: {items[0].get('descripcion', 'N/A')}")
        else:
            print(f"   ⚠️  No se generó cotización automáticamente")
        
        # Verificar HTML preview
        if data.get('html_preview'):
            print(f"   ✅ HTML preview generado ({len(data['html_preview'])} caracteres)")
        else:
            print(f"   ⚠️  No se generó HTML preview")
        
        resultados["pruebas"].append({
            "nombre": "Endpoint Profesional",
            "estado": "✅ PASS",
            "detalles": {
                "agente": data.get('agente_activo'),
                "items_generados": len(data.get('cotizacion_generada', {}).get('items', [])),
                "html_preview": bool(data.get('html_preview'))
            }
        })
    else:
        print(f"   ❌ Error: Código {response.status_code}")
        print(f"   📄 Respuesta: {response.text[:200]}")
        resultados["pruebas"].append({
            "nombre": "Endpoint Profesional",
            "estado": "❌ FAIL",
            "error": f"Código {response.status_code}",
            "respuesta": response.text[:500]
        })
        
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    resultados["pruebas"].append({
        "nombre": "Endpoint Profesional",
        "estado": "❌ FAIL",
        "error": str(e)
    })

print()

# Prueba 3: Verificar frontend
print("🌐 Prueba 3: Verificando frontend...")
try:
    response = requests.get("http://localhost:3000/", timeout=5)
    if response.status_code == 200:
        print(f"   ✅ Frontend ACTIVO")
        resultados["pruebas"].append({
            "nombre": "Frontend Status",
            "estado": "✅ PASS"
        })
    else:
        print(f"   ⚠️  Frontend respondió con código: {response.status_code}")
        resultados["pruebas"].append({
            "nombre": "Frontend Status",
            "estado": "⚠️ WARNING",
            "codigo": response.status_code
        })
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    resultados["pruebas"].append({
        "nombre": "Frontend Status",
        "estado": "❌ FAIL",
        "error": str(e)
    })

print()
print("=" * 60)
print("📊 RESUMEN DE PRUEBAS")
print("=" * 60)

total = len(resultados["pruebas"])
passed = sum(1 for p in resultados["pruebas"] if "✅" in p["estado"])
failed = sum(1 for p in resultados["pruebas"] if "❌" in p["estado"])
warnings = sum(1 for p in resultados["pruebas"] if "⚠️" in p["estado"])

print(f"Total de pruebas: {total}")
print(f"✅ Pasadas: {passed}")
print(f"❌ Fallidas: {failed}")
print(f"⚠️  Advertencias: {warnings}")
print()

# Guardar resultados
with open('verificacion_resultados.json', 'w', encoding='utf-8') as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)

print("💾 Resultados guardados en: verificacion_resultados.json")
print()

if failed == 0:
    print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
else:
    print("⚠️  Algunas pruebas fallaron. Revisar detalles arriba.")
