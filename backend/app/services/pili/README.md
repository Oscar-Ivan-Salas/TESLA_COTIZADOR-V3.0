# 🧠 PILI - Arquitectura Modular

Sistema modular basado en configuración YAML para servicios inteligentes.

## 🚀 Uso Rápido

```python
from app.services.pili.specialist import UniversalSpecialist

# Crear especialista
specialist = UniversalSpecialist('itse', 'cotizacion-simple')

# Procesar mensaje
response = specialist.process_message('', None)
```

## 📋 Servicios Disponibles

- `itse` - Certificados ITSE
- `electricidad` - Instalaciones eléctricas
- `pozo-tierra` - Pozo a tierra
- `contraincendios` - Sistemas contraincendios
- `domotica` - Domótica
- `cctv` - Sistemas CCTV
- `redes` - Redes de datos
- `saneamiento` - Saneamiento
- `automatizacion-industrial` - Automatización industrial
- `expedientes` - Expedientes técnicos

## 🔧 Configuración

### Editar Servicios

Archivos YAML en `config/services/`:
- `itse.yaml` - Configuración ITSE
- `electricidad.yaml` - Configuración electricidad
- etc.

### Estructura de YAML

```yaml
service: itse
name: "Certificado ITSE"
description: "Inspección Técnica de Seguridad"

categorias:
  SALUD:
    nombre: "Establecimientos de Salud"
    tipos:
      - "Hospital"
      - "Clínica"

documents:
  cotizacion-simple:
    etapas:
      - id: "categoria"
        type: "buttons"
        message_template: "presentacion"
```

## 🔌 Compatibilidad Legacy

Para mantener compatibilidad con código existente:

```python
from app.services.pili.adapters.legacy_adapter import LocalSpecialistFactory

# Interfaz compatible con código legacy
specialist = LocalSpecialistFactory.create('itse')
response = specialist.process_message(mensaje, state)
```

## 🧪 Tests

```bash
# Ejecutar tests
pytest app/services/pili/tests/test_integration.py -v

# Tests específicos
pytest app/services/pili/tests/test_integration.py::TestUniversalSpecialist -v
```

## 📁 Estructura

```
pili/
├── specialist.py          # UniversalSpecialist
├── config/
│   └── services/          # Configuraciones YAML
├── knowledge/             # Knowledge bases
├── adapters/              # Adapters de compatibilidad
├── tests/                 # Tests
└── README.md             # Este archivo
```

## ✅ Estado

- ✅ UniversalSpecialist implementado
- ✅ 10 servicios configurados en YAML
- ✅ Knowledge bases modulares
- ✅ Adapter de compatibilidad legacy
- ✅ Tests de integración
- ⏳ Integración con chat.py (en progreso)

## 🎯 Próximos Pasos

1. Completar integración con `chat.py`
2. Agregar multi-IA support
3. Implementar orquestador maestro
4. Agregar más servicios
