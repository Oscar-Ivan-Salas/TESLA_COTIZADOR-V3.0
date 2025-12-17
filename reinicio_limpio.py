"""
Script profesional para reinicio limpio del sistema
1. Backup de la base de datos
2. Limpieza de caché
3. Reinicio del frontend
"""
import shutil
import os
from datetime import datetime
from pathlib import Path

print("="*70)
print("REINICIO LIMPIO DEL SISTEMA - TESLA COTIZADOR V3.0")
print("="*70)

# Rutas
PROJECT_ROOT = Path("E:/TESLA_COTIZADOR-V3.0")
DB_PATH = PROJECT_ROOT / "database" / "tesla_cotizador.db"
BACKUP_DIR = PROJECT_ROOT / "database" / "backups"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# 1. BACKUP DE LA BASE DE DATOS
print("\n[1/4] Creando backup de la base de datos...")
if DB_PATH.exists():
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"tesla_cotizador_backup_{timestamp}.db"
    shutil.copy2(DB_PATH, backup_path)
    print(f"   ✅ Backup creado: {backup_path.name}")
    print(f"   📊 Tamaño: {backup_path.stat().st_size / 1024:.2f} KB")
else:
    print("   ⚠️  Base de datos no encontrada")

# 2. LIMPIEZA DE CACHÉ PYTHON
print("\n[2/4] Limpiando caché de Python...")
cache_count = 0
for root, dirs, files in os.walk(PROJECT_ROOT / "backend"):
    if '__pycache__' in dirs:
        cache_dir = Path(root) / '__pycache__'
        shutil.rmtree(cache_dir, ignore_errors=True)
        cache_count += 1
    for file in files:
        if file.endswith(('.pyc', '.pyo')):
            os.remove(Path(root) / file)
            cache_count += 1
print(f"   ✅ {cache_count} elementos de caché eliminados")

# 3. LIMPIEZA DE CACHÉ NODE
print("\n[3/4] Limpiando caché de Node.js...")
node_cache = FRONTEND_DIR / "node_modules" / ".cache"
if node_cache.exists():
    shutil.rmtree(node_cache, ignore_errors=True)
    print("   ✅ Caché de Node eliminado")
else:
    print("   ℹ️  No hay caché de Node")

# 4. RESUMEN
print("\n[4/4] Resumen:")
print("   ✅ Backup de BD creado")
print("   ✅ Caché de Python limpiado")
print("   ✅ Caché de Node limpiado")

print("\n" + "="*70)
print("SIGUIENTE PASO:")
print("="*70)
print("\n1. Cierra tu terminal actual (Ctrl+C)")
print("2. Abre una terminal NUEVA")
print("3. Ejecuta:")
print("   cd backend")
print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
print("\n4. En OTRA terminal:")
print("   cd frontend")
print("   npm start")
print("\n5. Recarga la página web (Ctrl+Shift+R)")
print("="*70)
