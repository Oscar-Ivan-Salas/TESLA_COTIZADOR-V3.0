"""
Script de Diagnóstico de Routers Profesionales
Identifica exactamente qué está fallando en la importación
"""

import sys
import traceback

print("=" * 60)
print("🔍 DIAGNÓSTICO DE ROUTERS PROFESIONALES")
print("=" * 60)
print()

# Agregar el path del backend
sys.path.insert(0, 'e:/TESLA_COTIZADOR-V3.0/backend')

routers_a_probar = [
    'chat',
    'cotizaciones',
    'proyectos',
    'informes',
    'documentos',
    'system',
    'auth'
]

resultados = []

for router_name in routers_a_probar:
    print(f"📦 Probando importación de: {router_name}")
    try:
        module = __import__(f'app.routers.{router_name}', fromlist=[router_name])
        print(f"   ✅ {router_name}.py importado correctamente")
        
        # Verificar que tenga el atributo 'router'
        if hasattr(module, 'router'):
            print(f"   ✅ {router_name}.router disponible")
            resultados.append((router_name, "✅ OK", None))
        else:
            print(f"   ⚠️  {router_name}.py no tiene atributo 'router'")
            resultados.append((router_name, "⚠️ NO ROUTER", "Falta atributo 'router'"))
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        print(f"   📄 Traceback:")
        traceback.print_exc()
        resultados.append((router_name, "❌ FAIL", str(e)))
    print()

print("=" * 60)
print("📊 RESUMEN")
print("=" * 60)

exitosos = sum(1 for r in resultados if r[1] == "✅ OK")
fallidos = sum(1 for r in resultados if "❌" in r[1])
advertencias = sum(1 for r in resultados if "⚠️" in r[1])

print(f"Total: {len(resultados)}")
print(f"✅ Exitosos: {exitosos}")
print(f"❌ Fallidos: {fallidos}")
print(f"⚠️  Advertencias: {advertencias}")
print()

if fallidos > 0:
    print("🔴 ROUTERS CON ERRORES:")
    for nombre, estado, error in resultados:
        if "❌" in estado:
            print(f"   - {nombre}: {error[:100]}")
    print()
    print("💡 RECOMENDACIÓN:")
    print("   Revisar las dependencias de los routers que fallaron")
    print("   Ejecutar: pip install -r backend/requirements_professional.txt")
else:
    print("🎉 ¡TODOS LOS ROUTERS SE IMPORTAN CORRECTAMENTE!")
    print()
    print("⚠️  PERO el backend reporta que no están disponibles.")
    print("   Esto sugiere un problema en main.py con el try/except")
