# utils/backup.py
# Funciones para asegurar carpetas de storage/backup y mover/archivar archivos antiguos.

import os
import shutil
from datetime import datetime
from pathlib import Path

# Carpetas por defecto
DEFAULT_DIRS = ["storage", "database", "chroma_db", "storage/backup"]

def ensure_dirs(base_path: str = "."):
    """Crear las carpetas necesarias si no existen."""
    for d in DEFAULT_DIRS:
        p = Path(base_path) / d
        p.mkdir(parents=True, exist_ok=True)

def archive_file(src_path: str, dest_dir: str = "storage/backup"):
    """
    Mueve el archivo src_path a dest_dir añadiendo timestamp al nombre.
    Devuelve la ruta destino.
    """
    src = Path(src_path)
    if not src.exists():
        return None
    ensure_dirs(".")
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    dest_dir_path = Path(dest_dir)
    dest_dir_path.mkdir(parents=True, exist_ok=True)
    dest_name = f"{src.stem}_{ts}{src.suffix}"
    dest = dest_dir_path / dest_name
    shutil.move(str(src), str(dest))
    return str(dest)

def archive_all_in_dir(src_dir: str, pattern: str = "*", dest_dir: str = "storage/backup"):
    """
    Mueve todos los archivos que coincidan con pattern desde src_dir a dest_dir.
    Retorna lista de rutas movidas.
    """
    moved = []
    src_path = Path(src_dir)
    if not src_path.exists():
        return moved
    for f in src_path.glob(pattern):
        if f.is_file():
            dest = archive_file(str(f), dest_dir)
            if dest:
                moved.append(dest)
    return moved
