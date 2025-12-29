"""
Script de verificación de dependencias para Tesla Cotizador v3.0
Verifica que todas las librerías necesarias estén instaladas correctamente
"""

import sys
from importlib import import_module

# Lista de dependencias críticas
DEPENDENCIES = {
    "fastapi": "FastAPI framework",
    "uvicorn": "ASGI server",
    "pydantic": "Data validation",
    "sqlalchemy": "Database ORM",
    "python-dotenv": "Environment variables (importar como 'dotenv')",
    "python-multipart": "File upload support",
    "google.generativeai": "Google Gemini AI",
    "filetype": "File type detection (reemplazo de python-magic)",
    "python-docx": "Word document generation",
    "reportlab": "PDF generation",
    "openpyxl": "Excel file handling",
    "jinja2": "Template engine",
    "aiofiles": "Async file operations",
}

# Mapeo de nombres de paquetes a nombres de importación
IMPORT_NAMES = {
    "python-dotenv": "dotenv",
    "python-multipart": "multipart",
    "python-docx": "docx",
}

def verify_dependency(package_name, description):
    """Verifica si una dependencia está instalada"""
    import_name = IMPORT_NAMES.get(package_name, package_name)
    
    try:
        module = import_module(import_name)
        version = getattr(module, "__version__", "unknown")
        print(f"✅ {package_name:25} - {description:30} (v{version})")
        return True
    except ImportError as e:
        print(f"❌ {package_name:25} - {description:30} - ERROR: {str(e)}")
        return False
    except Exception as e:
        print(f"⚠️  {package_name:25} - {description:30} - WARNING: {str(e)}")
        return True  # Consideramos que está instalado aunque haya un warning

def main():
    print("=" * 80)
    print("VERIFICACIÓN DE DEPENDENCIAS - TESLA COTIZADOR V3.0")
    print("=" * 80)
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print("=" * 80)
    print()
    
    results = {}
    for package, description in DEPENDENCIES.items():
        results[package] = verify_dependency(package, description)
    
    print()
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)
    
    installed = sum(results.values())
    total = len(results)
    
    print(f"Instaladas: {installed}/{total}")
    
    if installed == total:
        print("🎉 ¡Todas las dependencias están instaladas correctamente!")
        return 0
    else:
        print(f"⚠️  Faltan {total - installed} dependencias por instalar")
        print()
        print("Dependencias faltantes:")
        for package, is_installed in results.items():
            if not is_installed:
                print(f"  - {package}")
        print()
        print("Para instalar las dependencias faltantes, ejecuta:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    exit(main())
