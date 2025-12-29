# 🔧 SCRIPT PARA CORREGIR LÓGICA DE DETECCIÓN DE CATEGORÍAS EN ITSE
import re

file_path = r'e:\TESLA_COTIZADOR-V3.0\backend\app\services\pili_local_specialists.py'

# Leer archivo
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar y reemplazar la función _process_itse
# Patrón: desde "def _process_itse" hasta el siguiente "elif stage == "
old_pattern = r'(    def _process_itse\(self, message: str\) -> Dict:\r?\n        stage = self\.conversation_state\["stage"\]\r?\n        data = self\.conversation_state\["data"\]\r?\n        \r?\n        if stage == "initial":)'

new_code = '''    def _process_itse(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        # 🔥 CRÍTICO: Detectar selección de categoría PRIMERO (antes de verificar stage)
        message_upper = message.upper().strip()
        if message_upper in self.kb["categorias"].keys():
            # Usuario seleccionó una categoría válida
            data["categoria"] = message_upper
            self.conversation_state["stage"] = "tipo_especifico"
            tipos = self.kb["categorias"][message_upper]["tipos"]
            
            return {
                "texto": f"""Perfecto, sector **{self.kb["categorias"][message_upper]["nombre"]}**. 

¿Qué tipo específico es tu establecimiento?""",
                "botones": [{"text": t, "value": t} for t in tipos],
                "stage": "tipo_especifico",
                "state": self.conversation_state,
                "progreso": "2/5"
            }
        
        # Si no es una categoría, procesar según el stage actual
        if stage == "initial":'''

# Reemplazar
content_new = re.sub(old_pattern, new_code, content)

if content_new == content:
    print("❌ NO SE ENCONTRÓ EL PATRÓN - Intentando método alternativo...")
    
    # Método alternativo: buscar línea por línea
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def _process_itse(self, message: str) -> Dict:' in line:
            print(f"✅ Encontrado en línea {i+1}")
            # Insertar código después de las primeras 3 líneas de la función
            insert_pos = i + 4  # Después de stage, data, y línea vacía
            
            new_lines = [
                "        ",
                "        # 🔥 CRÍTICO: Detectar selección de categoría PRIMERO (antes de verificar stage)",
                "        message_upper = message.upper().strip()",
                '        if message_upper in self.kb["categorias"].keys():',
                "            # Usuario seleccionó una categoría válida",
                '            data["categoria"] = message_upper',
                '            self.conversation_state["stage"] = "tipo_especifico"',
                '            tipos = self.kb["categorias"][message_upper]["tipos"]',
                "            ",
                "            return {",
                '                "texto": f"""Perfecto, sector **{self.kb["categorias"][message_upper]["nombre"]}**. ',
                "",
                '¿Qué tipo específico es tu establecimiento?""",',
                '                "botones": [{"text": t, "value": t} for t in tipos],',
                '                "stage": "tipo_especifico",',
                '                "state": self.conversation_state,',
                '                "progreso": "2/5"',
                "            }",
                "        ",
                "        # Si no es una categoría, procesar según el stage actual"
            ]
            
            # Insertar nuevas líneas
            lines = lines[:insert_pos] + new_lines + lines[insert_pos:]
            content_new = '\n'.join(lines)
            break
    else:
        print("❌ NO SE ENCONTRÓ LA FUNCIÓN _process_itse")
        exit(1)

# Escribir archivo
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content_new)

print("✅ Lógica de detección de categorías corregida")
print("📝 Ahora detecta categorías ANTES de verificar el stage")
