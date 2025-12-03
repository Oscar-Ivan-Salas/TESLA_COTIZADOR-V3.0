import sys
import os
import traceback

# Agregar el directorio actual al path
sys.path.append(os.getcwd())

print("--- DIAGNÓSTICO DE IMPORTACIÓN ---")

try:
    print("1. Intentando importar file_processor...")
    from app.services.file_processor import file_processor
    print("✅ file_processor importado correctamente")
except Exception as e:
    print(f"❌ Error importando file_processor: {e}")
    traceback.print_exc()

try:
    print("\n2. Intentando importar chat router...")
    from app.routers import chat
    print("✅ chat router importado correctamente")
except Exception as e:
    print(f"❌ Error importando chat router: {e}")
    traceback.print_exc()

try:
    print("\n3. Intentando importar todos los routers desde __init__...")
    from app.routers import chat_router, documentos_router
    print("✅ Routers desde __init__ importados correctamente")
except Exception as e:
    print(f"❌ Error importando routers desde __init__: {e}")
    traceback.print_exc()
