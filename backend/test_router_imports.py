"""
Script de verificación de importación de routers
Verifica que todos los routers del backend se puedan importar correctamente
"""

import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

print("=" * 80)
print("VERIFICACIÓN DE IMPORTACIÓN DE ROUTERS")
print("=" * 80)
print(f"Backend path: {backend_path}")
print()

routers_to_test = [
    "app.routers.chat",
    "app.routers.cotizaciones",
    "app.routers.proyectos",
    "app.routers.informes",
    "app.routers.documentos",
    "app.routers.system"
]

results = {}

for router_module in routers_to_test:
    router_name = router_module.split(".")[-1]
    try:
        print(f"Probando {router_name}...", end=" ")
        module = __import__(router_module, fromlist=["router"])
        
        # Verificar que tenga el objeto router
        if hasattr(module, "router"):
            print(f"✅ OK - Router encontrado")
            results[router_name] = {"status": "ok", "error": None}
        else:
            print(f"⚠️  WARNING - Módulo importado pero no tiene objeto 'router'")
            results[router_name] = {"status": "warning", "error": "No router object"}
            
    except Exception as e:
        print(f"❌ ERROR - {type(e).__name__}: {str(e)}")
        results[router_name] = {"status": "error", "error": str(e)}

print()
print("=" * 80)
print("RESUMEN")
print("=" * 80)

ok_count = sum(1 for r in results.values() if r["status"] == "ok")
warning_count = sum(1 for r in results.values() if r["status"] == "warning")
error_count = sum(1 for r in results.values() if r["status"] == "error")

print(f"✅ OK: {ok_count}")
print(f"⚠️  WARNING: {warning_count}")
print(f"❌ ERROR: {error_count}")
print()

if error_count > 0:
    print("ROUTERS CON ERRORES:")
    for name, result in results.items():
        if result["status"] == "error":
            print(f"  - {name}: {result['error']}")
    print()
    exit(1)
elif warning_count > 0:
    print("⚠️  Algunos routers tienen advertencias pero se importaron")
    exit(0)
else:
    print("🎉 ¡Todos los routers se importaron correctamente!")
    exit(0)
