import sys
from pathlib import Path
import traceback

# Add backend to sys.path
backend_path = Path("backend")
sys.path.append(str(backend_path.absolute()))

print("Checking imports for advanced routers...")

modules_to_check = [
    "app.routers.chat",
    "app.routers.cotizaciones",
    "app.routers.proyectos",
    "app.routers.informes",
    "app.routers.documentos",
    "app.routers.system",
    "app.routers.auth"
]

for module in modules_to_check:
    try:
        __import__(module)
        print(f"✅ Successfully imported {module}")
    except ImportError as e:
        print(f"❌ Failed to import {module}: {e}")
    except Exception as e:
        print(f"❌ Error importing {module}: {e}")
        traceback.print_exc()
