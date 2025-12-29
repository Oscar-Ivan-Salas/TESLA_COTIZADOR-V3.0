import sys
import os
from pathlib import Path
import traceback

# Asegurar que estamos en backend y agregarlo al path
current_dir = os.getcwd()
if not current_dir.endswith('backend'):
    print(f"⚠️ Advertencia: Ejecutando desde {current_dir}, se esperaba estar en backend")

sys.path.append(current_dir)

print(f"CWD: {current_dir}")
print("--- DIAGNÓSTICO DE IMPORTACIÓN V2 ---")

try:
    print("\n1. Intentando importar app.services.file_processor...")
    from app.services.file_processor import file_processor
    print("✅ file_processor importado correctamente")
except Exception as e:
    print(f"❌ Error importando file_processor: {e}")
    traceback.print_exc()

try:
    print("\n2. Intentando importar app.routers.documentos...")
    from app.routers import documentos
    print("✅ documentos router importado correctamente")
except Exception as e:
    print(f"❌ Error importando documentos router: {e}")
    traceback.print_exc()

try:
    print("\n3. Intentando importar todos los routers como en main.py...")
    from app.routers import chat, cotizaciones, proyectos, informes, documentos, system
    print("✅ TODOS los routers importados correctamente")
except Exception as e:
    print(f"❌ Error importando bloque de routers: {e}")
    traceback.print_exc()
