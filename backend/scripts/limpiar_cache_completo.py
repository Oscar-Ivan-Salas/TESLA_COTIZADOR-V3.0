# ============================================================
# SCRIPT DE LIMPIEZA COMPLETA DE CACHE
# Sistema Tesla Cotizador V3.0
# ============================================================
# 
# USO:
#   python limpiar_cache_completo.py
#
# QUE HACE:
#   1. Elimina todos los directorios __pycache__
#   2. Elimina todos los archivos .pyc y .pyo
#   3. Limpia cache de pytest (si existe)
#   4. Limpia cache de mypy (si existe)
#
# DESPUES DE EJECUTAR:
#   Reinicia manualmente los servidores desde tu entorno virtual
# ============================================================

import os
import shutil
from pathlib import Path

def limpiar_cache_completo(directorio_raiz):
    """
    Limpia TODOS los archivos de cache de Python
    """
    
    stats = {
        'pycache_dirs': 0,
        'pyc_files': 0,
        'pytest_cache': 0,
        'mypy_cache': 0,
        'errores': []
    }
    
    print("=" * 70)
    print("LIMPIEZA COMPLETA DE CACHE - TESLA COTIZADOR")
    print("=" * 70)
    print(f"Directorio raiz: {directorio_raiz}")
    print()
    
    # 1. Limpiar __pycache__ y archivos .pyc
    print("1. Eliminando __pycache__ y archivos .pyc/.pyo...")
    print("-" * 70)
    
    for root, dirs, files in os.walk(directorio_raiz):
        # Saltar directorios de entornos virtuales
        if 'venv' in root or 'env' in root or '.venv' in root:
            continue
            
        # Eliminar directorios __pycache__
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                stats['pycache_dirs'] += 1
                print(f"  [OK] {pycache_path}")
            except Exception as e:
                stats['errores'].append(f"Error en {pycache_path}: {e}")
        
        # Eliminar archivos .pyc y .pyo
        for file in files:
            if file.endswith('.pyc') or file.endswith('.pyo'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    stats['pyc_files'] += 1
                except Exception as e:
                    stats['errores'].append(f"Error en {file_path}: {e}")
    
    # 2. Limpiar .pytest_cache
    print()
    print("2. Eliminando .pytest_cache...")
    print("-" * 70)
    pytest_cache = os.path.join(directorio_raiz, '.pytest_cache')
    if os.path.exists(pytest_cache):
        try:
            shutil.rmtree(pytest_cache)
            stats['pytest_cache'] = 1
            print(f"  [OK] {pytest_cache}")
        except Exception as e:
            stats['errores'].append(f"Error en pytest_cache: {e}")
    else:
        print("  [SKIP] No existe .pytest_cache")
    
    # 3. Limpiar .mypy_cache
    print()
    print("3. Eliminando .mypy_cache...")
    print("-" * 70)
    mypy_cache = os.path.join(directorio_raiz, '.mypy_cache')
    if os.path.exists(mypy_cache):
        try:
            shutil.rmtree(mypy_cache)
            stats['mypy_cache'] = 1
            print(f"  [OK] {mypy_cache}")
        except Exception as e:
            stats['errores'].append(f"Error en mypy_cache: {e}")
    else:
        print("  [SKIP] No existe .mypy_cache")
    
    # 4. Resumen
    print()
    print("=" * 70)
    print("RESUMEN DE LIMPIEZA")
    print("=" * 70)
    print(f"Directorios __pycache__ eliminados: {stats['pycache_dirs']}")
    print(f"Archivos .pyc/.pyo eliminados: {stats['pyc_files']}")
    print(f"Cache pytest eliminado: {'SI' if stats['pytest_cache'] else 'NO'}")
    print(f"Cache mypy eliminado: {'SI' if stats['mypy_cache'] else 'NO'}")
    
    if stats['errores']:
        print()
        print("ERRORES ENCONTRADOS:")
        for error in stats['errores']:
            print(f"  - {error}")
    
    print("=" * 70)
    print()
    print("LIMPIEZA COMPLETADA!")
    print()
    print("SIGUIENTE PASO:")
    print("  Reinicia los servidores desde tu entorno virtual")
    print("=" * 70)

if __name__ == "__main__":
    # Obtener directorio raiz del proyecto
    script_dir = Path(__file__).parent
    proyecto_raiz = script_dir.parent.parent  # Subir 2 niveles desde scripts/
    
    limpiar_cache_completo(proyecto_raiz)
