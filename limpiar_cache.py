"""
Script de limpieza de caché y reinicio del servidor
Limpia todos los archivos .pyc y __pycache__ del backend
"""
import os
import shutil
from pathlib import Path

def limpiar_cache(directorio):
    """Elimina todos los archivos de caché de Python"""
    contador_dirs = 0
    contador_archivos = 0
    
    print(f"🧹 Limpiando caché en: {directorio}")
    print("=" * 60)
    
    # Buscar y eliminar directorios __pycache__
    for root, dirs, files in os.walk(directorio):
        # Evitar el directorio venv
        if 'venv' in root or '.venv' in root:
            continue
            
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_path = Path(root) / dir_name
                try:
                    shutil.rmtree(pycache_path)
                    contador_dirs += 1
                    print(f"✅ Eliminado: {pycache_path}")
                except Exception as e:
                    print(f"⚠️  No se pudo eliminar {pycache_path}: {e}")
        
        # Eliminar archivos .pyc
        for file_name in files:
            if file_name.endswith('.pyc'):
                pyc_path = Path(root) / file_name
                try:
                    pyc_path.unlink()
                    contador_archivos += 1
                    print(f"✅ Eliminado: {pyc_path}")
                except Exception as e:
                    print(f"⚠️  No se pudo eliminar {pyc_path}: {e}")
    
    print("=" * 60)
    print(f"📊 Resumen:")
    print(f"   - Directorios __pycache__ eliminados: {contador_dirs}")
    print(f"   - Archivos .pyc eliminados: {contador_archivos}")
    print("=" * 60)
    print()
    print("✅ Limpieza completada!")
    print()
    print("📝 SIGUIENTE PASO:")
    print("   1. Detén el servidor actual (Ctrl+C en la terminal del servidor)")
    print("   2. Ejecuta: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    print()

if __name__ == "__main__":
    backend_dir = Path(__file__).parent / "backend"
    limpiar_cache(backend_dir)
