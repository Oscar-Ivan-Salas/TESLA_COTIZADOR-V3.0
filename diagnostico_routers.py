import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path.cwd() / "backend"))

print("=" * 60)
print("DIAGNÓSTICO DE IMPORTACIÓN DE ROUTERS")
print("=" * 60)

# Test 1: Magic
print("\n1. Probando import magic...")
try:
    import magic
    m = magic.Magic(mime=True)
    print("   ✅ Magic funciona correctamente")
except Exception as e:
    print(f"   ❌ Error con magic: {e}")

# Test 2: Routers individuales
routers = ['chat', 'cotizaciones', 'proyectos', 'informes', 'documentos', 'system', 'auth']

print("\n2. Probando routers individuales...")
for router_name in routers:
    try:
        exec(f"from app.routers import {router_name}")
        print(f"   ✅ {router_name}")
    except Exception as e:
        print(f"   ❌ {router_name}: {e}")

# Test 3: Import completo
print("\n3. Probando import completo...")
try:
    from app.routers import chat, cotizaciones, proyectos, informes, documentos, system, auth
    print("   ✅ Todos los routers importados")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("DIAGNÓSTICO COMPLETADO")
print("=" * 60)
