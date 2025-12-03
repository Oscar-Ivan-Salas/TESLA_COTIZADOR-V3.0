import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para poder importar app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    print("Intentando importar app.routers.generar_directo...")
    from app.routers import generar_directo
    print("✅ Importación exitosa!")
except Exception as e:
    print(f"❌ Error al importar: {e}")
    import traceback
    traceback.print_exc()
