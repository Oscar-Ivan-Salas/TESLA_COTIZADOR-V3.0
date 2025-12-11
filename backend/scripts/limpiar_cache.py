"""
Script de Limpieza de Cache - Sistema Tesla Cotizador
Limpia todos los archivos de cache de Python para forzar recarga completa
"""
import os
import shutil
from pathlib import Path

def limpiar_cache_python(directorio_raiz):
    """Elimina todos los archivos __pycache__ y .pyc"""
    
    archivos_eliminados = 0
    directorios_eliminados = 0
    
    print("Iniciando limpieza de cache...")
    print("-" * 60)
    
    # Buscar y eliminar directorios __pycache__
    for root, dirs, files in os.walk(directorio_raiz):
        # Eliminar directorios __pycache__
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                directorios_eliminados += 1
                print(f"Eliminado: {pycache_path}")
            except Exception as e:
                print(f"Error eliminando {pycache_path}: {e}")
        
        # Eliminar archivos .pyc individuales
        for file in files:
            if file.endswith('.pyc') or file.endswith('.pyo'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    archivos_eliminados += 1
                    print(f"Eliminado: {file_path}")
                except Exception as e:
                    print(f"Error eliminando {file_path}: {e}")
    
    print("-" * 60)
    print(f"Limpieza completada:")
    print(f"  - Directorios __pycache__ eliminados: {directorios_eliminados}")
    print(f"  - Archivos .pyc/.pyo eliminados: {archivos_eliminados}")
    print("-" * 60)

if __name__ == "__main__":
    # Directorio del backend
    backend_dir = Path(__file__).parent.parent
    
    print("=" * 60)
    print("LIMPIEZA DE CACHE - TESLA COTIZADOR")
    print("=" * 60)
    print(f"Directorio: {backend_dir}")
    print()
    
    limpiar_cache_python(backend_dir)
    
    print()
    print("LISTO! Ahora puedes reiniciar el servidor.")
    print()
    print("Comando para reiniciar:")
    print("  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    print("=" * 60)
