"""
Debug de data_source dinámico
"""
import sys
sys.path.insert(0, 'e:/TESLA_COTIZADOR-V3.0/backend')

from app.services.pili.specialist import UniversalSpecialist

s = UniversalSpecialist('itse', 'cotizacion-simple')

# Etapa 1
r1 = s.process_message('')
print(f"Etapa 1: {r1.get('stage')}")
print(f"Data: {s.conversation_state.get('data')}")

# Seleccionar SALUD
r2 = s.process_message('SALUD')
print(f"\nEtapa 2: {r2.get('stage')}")
print(f"Data: {s.conversation_state.get('data')}")

# Ver la etapa actual
current_stage = s._find_stage('tipo')
print(f"\nEtapa 'tipo' config:")
print(f"  data_source: {current_stage.get('data_source')}")

# Intentar obtener botones manualmente
import re
data_source = current_stage.get('data_source', '')
print(f"\nProcesando data_source: '{data_source}'")

# Reemplazar placeholders
placeholders = re.findall(r'\{(\w+)\}', data_source)
print(f"Placeholders encontrados: {placeholders}")

for placeholder in placeholders:
    value = s.conversation_state.get('data', {}).get(placeholder, '')
    print(f"  Reemplazando {{{placeholder}}} con '{value}'")
    data_source = data_source.replace(f'{{{placeholder}}}', value)

print(f"Data source después de reemplazar: '{data_source}'")

# Parsear path
path = data_source.replace('kb.', '').split('.')
print(f"Path: {path}")

# Navegar por el config
data = s.config
for key in path:
    print(f"  Buscando '{key}' en {type(data).__name__}")
    if isinstance(data, dict) and key in data:
        data = data[key]
        print(f"    Encontrado: {type(data).__name__}")
    else:
        print(f"    NO encontrado")
        data = None
        break

print(f"\nData final: {data}")
