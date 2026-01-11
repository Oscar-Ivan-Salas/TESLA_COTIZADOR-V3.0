import os
import re

COMPONENTS_DIR = r"e:\TESLA_COTIZADOR-V3.0\frontend\src\components"

# Lista de archivos que sabemos que tienen problemas de IMPORT
IMPORT_FILES = [
    "PiliAutomatizacionChat.jsx",
    "PiliAutomatizacionComplejoChat.jsx",
    "PiliContraIncendiosComplejoChat.jsx",
    "PiliExpedientesChat.jsx",
    "PiliSaneamientoChat.jsx"
]

def fix_import_props_issue(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Problema: 
    # Line 1: import ...; const Comp = ({ ... ,
    # Line 2: import ViewToggleButtons...
    # Line 3: ...
    #
    # Solución: 
    # 1. Extraer 'import ViewToggleButtons ...;' de donde esté.
    # 2. Insertarlo limpio al inicio (después de otros imports).
    
    if "import ViewToggleButtons" not in content:
        return
        
    # Verificar si está mal posicionado (dentro de props)
    # Una heurística simple: Si está DESPUÉS de "const Pili" y ANTES de "=> {", está mal.
    
    const_pattern = r'(const\s+Pili\w+\s*=\s*\(\{)'
    view_toggle_import = r'(import\s+ViewToggleButtons\s+from\s+[\'"]\./ViewToggleButtons[\'"];?)'
    
    match_const = re.search(const_pattern, content)
    match_import = re.search(view_toggle_import, content)
    
    if match_const and match_import:
        if match_import.start() > match_const.start():
            print(f"🔧 Reparando import mal posicionado en: {os.path.basename(file_path)}")
            
            # Quitar el import incorrecto
            content = content.replace(match_import.group(0), "")
            
            # Insertar al principio, antes de la constante
            # Buscamos el último ';' de los imports iniciales o simplemente antes de 'const Pili'
            
            # Mejor: Insertar justo antes de 'const Pili'
            content = content.replace(match_const.group(0), "import ViewToggleButtons from './ViewToggleButtons';\n\n" + match_const.group(0))
            
            # Limpieza extra: Si quedaron líneas vacías raras o comas flotando
            content = content.replace(",\n\n    viewMode,", ", viewMode,") # Posible residuo de mi edit anterior
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print(f"✅ Import parece correcto en: {os.path.basename(file_path)}")

# Ejecutar
for f in IMPORT_FILES:
    path = os.path.join(COMPONENTS_DIR, f)
    if os.path.exists(path):
        fix_import_props_issue(path)
