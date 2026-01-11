import os
import re

# Directorio de componentes
COMPONENTS_DIR = r"e:\TESLA_COTIZADOR-V3.0\frontend\src\components"

# Lista de chats a verificar (patrón de nombre)
CHAT_PATTERNS = ["Pili", "Chat.jsx"]

# Componente a insertar
TOGGLE_COMPONENT = "                    <ViewToggleButtons viewMode={viewMode} setViewMode={setViewMode} />\n"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Verificar si ya tiene el componente
    if "<ViewToggleButtons" in content:
        print(f"✅ Ya tiene botones: {os.path.basename(file_path)}")
        return False

    # 2. Verificar si tiene el import, si no, agregarlo
    if "import ViewToggleButtons" not in content:
        content = content.replace("import { PiliAvatarLarge }", "import { PiliAvatarLarge } from './PiliAvatar';\nimport ViewToggleButtons from './ViewToggleButtons';")
        content = content.replace("import { PiliAvatarLarge } from './PiliAvatar';", "") # Evitar duplicado si el replace anterior no fue exacto, ajustando logica:
        # Mejor estrategia para import: Buscar el último import y agregar luego
        # Pero asumimos que PiliAvatarLarge siempre está. Vamos a simplificar:
        if "import ViewToggleButtons" not in content: # Re-check
             # Fallback simple
             lines = content.split('\n')
             for i, line in enumerate(lines):
                 if "import" in line and "from" in line:
                     last_import_idx = i
             lines.insert(last_import_idx + 1, "import ViewToggleButtons from './ViewToggleButtons';")
             content = '\n'.join(lines)

    print(f"🔧 Reparando: {os.path.basename(file_path)}")
    
    # 3. Estrategias de inserción
    inserted = False
    
    # Estrategia 1: Buscar botón ArrowLeft (común en chats modernos)
    if not inserted and '<ArrowLeft' in content:
        # Buscar el contenedor padre del botón ArrowLeft o el botón mismo para insertar ANTES
        # Patrón: {onBack && ( ... <button ... ArrowLeft ... </button> ... )}
        # Intentar insertar antes del bloque {onBack &&
        pattern = r'(\{onBack &&)'
        if re.search(pattern, content):
            content = re.sub(pattern, TOGGLE_COMPONENT + r'\1', content, count=1)
            inserted = True
            print("  -> Estrategia: Antes de {onBack &&")

    # Estrategia 2: Buscar texto "Volver" (chats antiguos)
    if not inserted and 'Volver' in content:
        pattern = r'(<button[^>]*>.*?Volver.*?</button>)'
        # Insertar antes del botón
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, TOGGLE_COMPONENT + r'\1', content, count=1, flags=re.DOTALL)
            inserted = True
            print("  -> Estrategia: Antes de botón Volver")
            
    # Estrategia 3: PiliITSEChat (Header específico con estilos en línea)
    # Busca el cierre del div del header que contiene el Avatar
    if not inserted and "PiliAvatarLarge" in content:
        # Buscar el div que cierra el bloque del Avatar y Título en el header
        # PiliITSEChat tiene un estructura compleja. 
        # Buscaremos 'Tesla Electricidad • Huancayo' y cerraremos divs hasta encontrar el lugar.
        target_str = "Tesla Electricidad • Huancayo"
        if target_str in content:
            # En PiliITSEChat, esto está dentro de un p -> div -> div (flex row) -> div (header container)
            # Queremos ponerlo en el 'header container' a la derecha.
            # El header container tiene 'justifyContent: space-between'.
            # El primer hijo es el div del avatar+titulo.
            # El segundo hijo será nuestro componente.
            
            # Buscar el cierre del div que envuelve al avatar y texto
            # Es difícil con regex. Vamos a usar un str replace específico para este archivo conocido.
            context_str = """                            Tesla Electricidad • Huancayo
                        </p>
                    </div>
                </div>"""
            if context_str in content:
                content = content.replace(context_str, context_str + "\n" + TOGGLE_COMPONENT)
                inserted = True
                print("  -> Estrategia: PiliITSEChat Contexto Específico")

    # Estrategia 4: Fallback genérico - Buscar cierre del primer div header (suponiendo clase bg-gradient o similar)
    if not inserted:
        print("  ⚠️ No se encontró patrón seguro de inserción. Saltando.")
        return False

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

# Ejecutar
count = 0
for filename in os.listdir(COMPONENTS_DIR):
    if filename.startswith("Pili") and filename.endswith("Chat.jsx"):
        if process_file(os.path.join(COMPONENTS_DIR, filename)):
            count += 1

print(f"\n✅ Total archivos reparados: {count}")
