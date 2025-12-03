"""
Script de diagnóstico exhaustivo del servidor
Verifica exactamente qué está pasando con la carga de routers
"""
import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

print("=" * 80)
print("DIAGNÓSTICO EXHAUSTIVO DEL SERVIDOR")
print("=" * 80)
print()

# Paso 1: Verificar que los módulos se pueden importar
print("📋 PASO 1: Verificando importación de módulos individuales")
print("-" * 80)

routers_to_test = {
    "chat": "app.routers.chat",
    "cotizaciones": "app.routers.cotizaciones",
    "proyectos": "app.routers.proyectos",
    "informes": "app.routers.informes",
    "documentos": "app.routers.documentos",
    "system": "app.routers.system"
}

import_results = {}

for nombre, modulo in routers_to_test.items():
    try:
        print(f"Importando {nombre}...", end=" ")
        mod = __import__(modulo, fromlist=["router"])
        
        if hasattr(mod, "router"):
            print(f"✅ OK - Router encontrado")
            import_results[nombre] = {"status": "ok", "module": mod}
        else:
            print(f"⚠️  WARNING - Módulo importado pero sin 'router'")
            import_results[nombre] = {"status": "no_router", "module": mod}
    except Exception as e:
        print(f"❌ ERROR - {type(e).__name__}: {str(e)}")
        import_results[nombre] = {"status": "error", "error": str(e)}

print()
print("=" * 80)
print("📊 RESUMEN DE IMPORTACIONES")
print("=" * 80)

ok_count = sum(1 for r in import_results.values() if r["status"] == "ok")
print(f"✅ Exitosos: {ok_count}/6")
print(f"❌ Fallidos: {6 - ok_count}/6")
print()

if ok_count < 6:
    print("⚠️  ROUTERS CON PROBLEMAS:")
    for nombre, result in import_results.items():
        if result["status"] != "ok":
            print(f"   - {nombre}: {result.get('error', result['status'])}")
    print()

# Paso 2: Simular la lógica de main.py
print("=" * 80)
print("📋 PASO 2: Simulando lógica de main.py")
print("=" * 80)
print()

routers_info = {}

for nombre, result in import_results.items():
    if result["status"] == "ok":
        routers_info[nombre] = {
            "router": result["module"].router,
            "prefix": f"/api/{nombre}",
            "tags": [nombre.capitalize()],
            "descripcion": f"Router {nombre}"
        }
        print(f"✅ {nombre} agregado a routers_info")
    else:
        print(f"⚠️  {nombre} NO agregado (status: {result['status']})")

print()
print(f"📊 Total en routers_info: {len(routers_info)}")
print(f"📋 Routers: {list(routers_info.keys())}")
print()

# Verificar condición de activación
ROUTERS_AVANZADOS_DISPONIBLES = len(routers_info) >= 1

print("=" * 80)
print("🎯 RESULTADO FINAL")
print("=" * 80)
print(f"ROUTERS_AVANZADOS_DISPONIBLES = {ROUTERS_AVANZADOS_DISPONIBLES}")
print(f"Routers disponibles: {len(routers_info)}/6")
print()

if ROUTERS_AVANZADOS_DISPONIBLES:
    print("✅ El sistema DEBERÍA estar en modo COMPLETO")
    print()
    print("Si el servidor muestra modo DEMO, el problema es:")
    print("  1. El servidor no se reinició después de los cambios")
    print("  2. Hay archivos .pyc en caché con código antiguo")
    print("  3. La variable ROUTERS_AVANZADOS_DISPONIBLES se sobrescribe después")
else:
    print("❌ El sistema está en modo DEMO porque:")
    print(f"  - Solo {len(routers_info)} routers se importaron correctamente")
    print("  - Se requiere al menos 1 router para modo completo")

print()
print("=" * 80)
