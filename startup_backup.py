# startup_backup.py
# Script pequeño para ejecutar en el arranque (o manualmente) que asegura las carpetas necesarias.
from utils.backup import ensure_dirs

# Llamar a ensure_dirs en el arranque del backend
ensure_dirs('.');

# No ejecutar más nada aquí; main.py puede importar este módulo para asegurar carpetas al iniciar.