# ARQUITECTURA: Caja Negra YAML vs Caja Negra Simple

> **Comparación de dos enfoques para chatbots PILI**
> **Fecha**: 2025-12-30
> **Contexto**: Decidir cuál usar para los 10 servicios

---

## 📊 TABLA COMPARATIVA

| Aspecto | CAJA NEGRA YAML (pili/) | CAJA NEGRA SIMPLE (Pili_ChatBot/) |
|---------|------------------------|-----------------------------------|
| **Archivos por servicio** | 1 YAML + 1 Python compartido | 1 Python único |
| **Líneas de código** | ~500 YAML + 0 Python nuevo | ~400-500 Python total |
| **Configuración** | Externa (YAML) | Interna (diccionarios Python) |
| **Reusabilidad** | Alta (UniversalSpecialist) | Baja (código duplicado) |
| **Similitud con N8N** | ✅ MUY ALTA (nodos → etapas) | ❌ BAJA |
| **Curva de aprendizaje** | Media (aprender YAML) | Baja (solo Python) |
| **Mantenimiento** | Fácil (cambiar YAML) | Medio (cambiar código) |
| **Testing** | Difícil (lógica distribuida) | Fácil (todo en un archivo) |
| **Velocidad desarrollo** | Rápida (copiar YAML) | Media (escribir código) |
| **Validación** | ✅ Engines especializados | ⚠️ Manual en código |
| **Escalabilidad** | ✅ Alta (agregar servicios = YAML) | ❌ Baja (cada servicio = código nuevo) |
| **Debugging** | Difícil (saltar entre archivos) | Fácil (todo en un archivo) |

---

## 🏗️ ARQUITECTURA 1: CAJA NEGRA YAML (Actual en `pili/`)

### Estructura de Archivos

```
backend/app/services/pili/
├── config/
│   ├── itse.yaml              # Configuración ITSE
│   ├── pozo-tierra.yaml       # Configuración Pozo a Tierra
│   ├── electricidad.yaml      # Configuración Electricidad
│   └── ... (10 servicios)
│
├── core/
│   ├── conversation_engine.py # Motor de conversación
│   ├── calculation_engine.py  # Motor de cálculos
│   └── validation_engine.py   # Motor de validación
│
├── knowledge/
│   └── itse_kb.py             # Knowledge base (opcional)
│
├── templates/
│   └── messages.yaml          # Plantillas de mensajes
│
└── specialist.py              # UniversalSpecialist (ÚNICO)
```

### Flujo de Funcionamiento

```
┌─────────────────────────────────────────────────────┐
│ 1. Usuario envía mensaje                            │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 2. UniversalSpecialist carga YAML del servicio      │
│    specialist = UniversalSpecialist("itse")         │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 3. Lee etapa actual desde YAML                      │
│    etapa = config['documents']['cotizacion-simple'] │
│            ['etapas'][stage_index]                  │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 4. ConversationEngine renderiza mensaje             │
│    texto = engine.render_message("itse",            │
│                "presentacion", **datos)             │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 5. ValidationEngine valida entrada                  │
│    if etapa['validacion']:                          │
│        ValidationEngine.validate(...)               │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 6. CalculationEngine calcula cotización             │
│    if etapa['type'] == 'generate_quote':            │
│        CalculationEngine.calculate(...)             │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 7. Retorna respuesta con siguiente etapa            │
│    return {                                         │
│        "texto": "...",                              │
│        "botones": [...],                            │
│        "stage": next_stage                          │
│    }                                                │
└─────────────────────────────────────────────────────┘
```

### Ejemplo YAML (itse.yaml)

```yaml
service: itse
name: "Certificado ITSE"

# Knowledge base inline
precios_municipales:
  BAJO:
    precio: 168.30
    dias: 7

# Flujo de conversación (como N8N)
documents:
  cotizacion-simple:
    etapas:
      # NODO 1: Botones de categoría
      - id: categoria
        type: buttons
        message_template: presentacion
        data_source: kb.categorias
        next: tipo

      # NODO 2: Botones de tipo
      - id: tipo
        type: buttons
        message_template: confirm_categoria
        data_source: kb.categorias.{categoria}.tipos
        next: area

      # NODO 3: Input de área
      - id: area
        type: input_number
        message_template: ask_area
        next: pisos
        validacion:
          min: 10
          max: 10000

      # NODO 4: Input de pisos
      - id: pisos
        type: input_number
        message_template: ask_pisos
        next: quotation

      # NODO 5: Generar cotización
      - id: quotation
        type: generate_quote
        calculator: calculate_itse_quote
        message_template: cotizacion
```

### Código Python (UniversalSpecialist)

```python
class UniversalSpecialist:
    def __init__(self, service_name: str):
        # Cargar YAML
        self.config = yaml.safe_load(open(f'config/{service_name}.yaml'))
        self.stages = self.config['documents']['cotizacion-simple']['etapas']

    def procesar(self, mensaje: str, estado: Dict) -> Dict:
        # Obtener etapa actual
        current_stage = estado.get('stage', 'initial')
        etapa = self._get_stage(current_stage)

        # Procesar según tipo de etapa
        if etapa['type'] == 'buttons':
            return self._process_buttons(etapa, mensaje, estado)
        elif etapa['type'] == 'input_number':
            return self._process_input_number(etapa, mensaje, estado)
        elif etapa['type'] == 'generate_quote':
            return self._process_quote(etapa, estado)
```

### ✅ VENTAJAS

1. **Escalabilidad**: Agregar servicio = copiar YAML, NO código
2. **Mantenimiento**: Cambiar precios/mensajes = editar YAML
3. **Separación de responsabilidades**: Lógica (Python) vs Configuración (YAML)
4. **Reutilización**: UniversalSpecialist sirve para TODOS los servicios
5. **No duplicación**: 0% código repetido
6. **Similar a N8N**: Flujo visual de etapas
7. **Fácil de entender**: Ver YAML = entender flujo completo

### ❌ DESVENTAJAS

1. **Complejidad**: Múltiples archivos (YAML, engines, specialist)
2. **Debugging difícil**: Saltar entre archivos para entender flujo
3. **Curva de aprendizaje**: Requiere entender YAML + engines
4. **Menos flexible**: Lógica personalizada requiere modificar engines
5. **Testing complejo**: Necesitas mockear YAML + engines
6. **Dependencia YAML**: Si YAML falla, todo falla

---

## 🏗️ ARQUITECTURA 2: CAJA NEGRA SIMPLE (Patrón actual `pili_itse_chatbot.py`)

### Estructura de Archivos

```
backend/app/services/Pili_ChatBot/
├── pili_itse_chatbot.py           # Caja negra ITSE
├── pili_pozo_tierra_chatbot.py    # Caja negra Pozo a Tierra
├── pili_electricidad_chatbot.py   # Caja negra Electricidad
└── ... (10 archivos)
```

### Flujo de Funcionamiento

```
┌─────────────────────────────────────────────────────┐
│ 1. Usuario envía mensaje                            │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 2. Instanciar caja negra                            │
│    chatbot = PILIITSEChatBot()                      │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 3. Procesar mensaje (TODO EN UN MÉTODO)             │
│    resultado = chatbot.procesar(mensaje, estado)    │
│                                                     │
│    - Identifica etapa actual                        │
│    - Valida entrada                                 │
│    - Actualiza estado                               │
│    - Calcula cotización si aplica                   │
│    - Genera respuesta                               │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 4. Retorna respuesta                                │
│    return {                                         │
│        "success": True,                             │
│        "respuesta": "...",                          │
│        "botones": [...],                            │
│        "estado": {...}                              │
│    }                                                │
└─────────────────────────────────────────────────────┘
```

### Código Python Completo (pili_itse_chatbot.py)

```python
class PILIITSEChatBot:
    """
    Caja negra ITSE - TODO en un archivo
    INPUT: mensaje + estado
    OUTPUT: respuesta + nuevo_estado + cotización
    """

    def __init__(self):
        # Knowledge base INLINE (no archivos externos)
        self.knowledge_base = {
            "precios_municipales": {
                "BAJO": {
                    "precio": 168.30,
                    "renovacion": 90.30,
                    "dias": 7
                },
                "MEDIO": {
                    "precio": 208.60,
                    "renovacion": 109.40,
                    "dias": 7
                },
                "ALTO": {
                    "precio": 703.00,
                    "renovacion": 417.40,
                    "dias": 7
                },
                "MUY_ALTO": {
                    "precio": 1084.60,
                    "renovacion": 629.20,
                    "dias": 7
                }
            },
            "categorias": {
                "SALUD": {
                    "nombre": "Salud",
                    "tipos": ["Hospital", "Clínica", "Centro Médico"],
                    "riesgo_default": "ALTO"
                },
                "EDUCACION": {
                    "nombre": "Educación",
                    "tipos": ["Colegio", "Universidad", "Instituto"],
                    "riesgo_default": "MEDIO"
                }
                # ... 8 categorías más
            }
        }

    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        """
        Método principal - Máquina de estados

        INPUT: mensaje del usuario + estado actual
        OUTPUT: respuesta + nuevo estado + datos generados
        """
        # Inicializar estado si no existe
        if estado is None:
            estado = {"etapa": "inicial", "datos": {}}

        etapa = estado.get("etapa", "inicial")

        # MÁQUINA DE ESTADOS (6 etapas)
        if etapa == "inicial":
            return self._etapa_inicial(estado)

        elif etapa == "categoria":
            return self._etapa_categoria(mensaje, estado)

        elif etapa == "tipo":
            return self._etapa_tipo(mensaje, estado)

        elif etapa == "area":
            return self._etapa_area(mensaje, estado)

        elif etapa == "pisos":
            return self._etapa_pisos(mensaje, estado)

        elif etapa == "cotizacion":
            return self._etapa_cotizacion(estado)

        else:
            return self._error("Etapa desconocida")

    def _etapa_inicial(self, estado: Dict) -> Dict:
        """Etapa 1: Mostrar botones de categorías"""
        botones = [
            {"text": "🏥 Salud", "value": "SALUD"},
            {"text": "🎓 Educación", "value": "EDUCACION"},
            {"text": "🏪 Comercio", "value": "COMERCIO"},
            # ... 8 botones total
        ]

        return {
            "success": True,
            "respuesta": "¡Hola! Soy PILI. ¿Qué tipo de establecimiento es?",
            "botones": botones,
            "estado": {"etapa": "categoria", "datos": {}},
            "cotizacion": None
        }

    def _etapa_categoria(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 2: Procesar categoría y mostrar tipos"""
        categoria = mensaje.upper()

        if categoria not in self.knowledge_base["categorias"]:
            return self._error("Categoría inválida")

        # Obtener tipos de la categoría
        tipos = self.knowledge_base["categorias"][categoria]["tipos"]
        botones = [{"text": tipo, "value": tipo} for tipo in tipos]

        # Actualizar estado
        estado["datos"]["categoria"] = categoria
        estado["etapa"] = "tipo"

        return {
            "success": True,
            "respuesta": f"Perfecto, sector {categoria}. ¿Qué tipo específico?",
            "botones": botones,
            "estado": estado,
            "cotizacion": None
        }

    def _etapa_area(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 4: Procesar área"""
        try:
            area = float(mensaje)

            if area < 10 or area > 10000:
                return self._error("Área debe estar entre 10 y 10,000 m²")

            # Actualizar estado
            estado["datos"]["area"] = area
            estado["etapa"] = "pisos"

            return {
                "success": True,
                "respuesta": f"📐 Área: {area} m². ¿Cuántos pisos tiene?",
                "botones": None,
                "estado": estado,
                "cotizacion": None
            }

        except ValueError:
            return self._error("Por favor ingresa un número válido")

    def _calcular_riesgo(self, categoria: str, area: float, pisos: int) -> str:
        """Calcula nivel de riesgo según D.S. 002-2018-PCM"""

        # Reglas especiales por categoría
        if categoria == "SALUD":
            if area > 500 or pisos >= 2:
                return "MUY_ALTO"
            return "ALTO"

        elif categoria == "EDUCACION":
            if area > 1000 or pisos >= 3:
                return "ALTO"
            return "MEDIO"

        elif categoria == "COMERCIO":
            if area > 500:
                return "ALTO"
            return "MEDIO"

        # ... más reglas

        return "MEDIO"  # Default

    def _generar_cotizacion(self, datos: Dict) -> Dict:
        """Genera cotización completa"""

        # Calcular riesgo
        riesgo = self._calcular_riesgo(
            datos["categoria"],
            datos["area"],
            datos["pisos"]
        )

        # Obtener precios
        precios_muni = self.knowledge_base["precios_municipales"][riesgo]

        # Calcular total
        costo_tupa = precios_muni["precio"]
        costo_tesla_min = 450 if riesgo == "MEDIO" else 800
        costo_tesla_max = 650 if riesgo == "MEDIO" else 1200

        total_min = costo_tupa + costo_tesla_min
        total_max = costo_tupa + costo_tesla_max

        return {
            "categoria": datos["categoria"],
            "tipo": datos["tipo"],
            "area": datos["area"],
            "pisos": datos["pisos"],
            "riesgo": riesgo,
            "costo_tupa": costo_tupa,
            "costo_tesla_min": costo_tesla_min,
            "costo_tesla_max": costo_tesla_max,
            "total_min": total_min,
            "total_max": total_max,
            "dias": precios_muni["dias"]
        }

    def _error(self, mensaje: str) -> Dict:
        """Retorna error"""
        return {
            "success": False,
            "respuesta": f"❌ Error: {mensaje}",
            "botones": None,
            "estado": None,
            "cotizacion": None
        }
```

### ✅ VENTAJAS

1. **Simplicidad**: TODO en un archivo, fácil de entender
2. **Debugging fácil**: Ver todo el flujo en un solo lugar
3. **No dependencias**: No requiere YAML, engines, etc.
4. **Testing simple**: Mockear solo el chatbot
5. **Flexibilidad**: Lógica personalizada fácil de agregar
6. **Autocontenido**: 0 dependencias externas
7. **Patrón validado**: Ya funciona en producción (ITSE)

### ❌ DESVENTAJAS

1. **Duplicación**: Cada servicio replica estructura similar
2. **Mantenimiento**: Cambiar precio = editar código Python
3. **Escalabilidad**: 10 servicios = 10 archivos casi idénticos
4. **Acoplamiento**: Configuración mezclada con lógica
5. **Difícil cambiar mensajes**: Requiere tocar código

---

## 🤔 ¿CUÁL USAR?

### RECOMENDACIÓN: **HÍBRIDO** 🎯

Combinar lo mejor de ambos mundos:

```python
# pili_pozo_tierra_chatbot.py

import yaml
from pathlib import Path

class PILIPozoTierraChatBot:
    """Caja negra híbrida: Código simple + YAML para configuración"""

    def __init__(self):
        # Cargar configuración YAML (precios, mensajes)
        self.config = self._load_config()
        self.kb = self.config["knowledge_base"]
        self.mensajes = self.config["mensajes"]

    def _load_config(self) -> Dict:
        """Carga YAML solo para configuración, NO para flujo"""
        config_path = Path(__file__).parent / "config" / "pozo_tierra_config.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def procesar(self, mensaje: str, estado: Dict) -> Dict:
        """Lógica del flujo en Python (no YAML)"""

        etapa = estado.get("etapa", "inicial")

        # FLUJO EN CÓDIGO (como caja negra simple)
        if etapa == "inicial":
            return self._etapa_inicial()

        elif etapa == "aplicacion":
            return self._etapa_aplicacion(mensaje, estado)

        # ... etc

    def _etapa_inicial(self) -> Dict:
        # Mensaje desde YAML
        texto = self.mensajes["presentacion"]

        # Botones desde knowledge base YAML
        botones = [
            {"text": opt["label"], "value": opt["value"]}
            for opt in self.kb["aplicaciones"]
        ]

        return {
            "success": True,
            "respuesta": texto,
            "botones": botones,
            "estado": {"etapa": "aplicacion"}
        }
```

### YAML Híbrido (pozo_tierra_config.yaml)

```yaml
# Solo configuración, NO flujo de etapas

knowledge_base:
  aplicaciones:
    - label: "🏠 Residencial"
      value: "RESIDENCIAL"
    - label: "🏢 Comercial"
      value: "COMERCIAL"

  resistividades:
    ARCILLOSO:
      rho: 100
      descripcion: "Terreno arcilloso/húmedo"
    ARENOSO:
      rho: 1000
      descripcion: "Terreno arenoso/seco"

  precios:
    varilla_copperweld_24m: 85.00
    conector_grapa: 12.00
    cable_desnudo_25mm: 18.00

mensajes:
  presentacion: |
    ¡Hola! Voy a cotizar tu sistema de pozo a tierra.

    ¿Para qué tipo de instalación es?

  ask_resistencia: |
    ¿Qué valor de resistencia necesitas alcanzar?

    Recomendaciones:
    - ≤25Ω: Mínimo legal CNE
    - ≤5Ω: Buena práctica NFPA
```

### ✅ VENTAJAS DEL HÍBRIDO

1. ✅ Simplicidad del código (flujo en Python)
2. ✅ Facilidad de mantenimiento (precios en YAML)
3. ✅ Debugging fácil (lógica visible)
4. ✅ Configuración externa (YAML para datos)
5. ✅ Escalable (duplicar archivo + cambiar YAML)
6. ✅ Testing simple (código + mockear YAML)

---

## 📊 DECISIÓN FINAL

### Para los 10 servicios de Tesla Electricidad:

**USAR PATRÓN HÍBRIDO**:

```
✅ CÓDIGO: Caja negra simple (1 archivo .py por servicio)
✅ CONFIGURACIÓN: YAML ligero (precios, mensajes, knowledge base)
❌ NO USAR: UniversalSpecialist con flujo completo en YAML
```

### Razones:

1. **Simplicidad > Complejidad**: El equipo prefiere ver flujo en código
2. **Debugging más fácil**: Un archivo Python vs saltar entre YAML + engines
3. **Patrón validado**: `pili_itse_chatbot.py` ya funciona
4. **Flexibilidad**: Lógica personalizada por servicio
5. **YAML solo para datos**: Precios, mensajes, opciones (fácil de cambiar)
6. **Escalabilidad suficiente**: 10 servicios no es un número enorme

---

## 🚀 PLAN DE IMPLEMENTACIÓN

### FASE 1: Crear 4 chatbots híbridos (Cotizaciones Simples)

```python
# 1. pili_pozo_tierra_chatbot.py + pozo_tierra_config.yaml
# 2. pili_cctv_chatbot.py + cctv_config.yaml
# 3. pili_redes_chatbot.py + redes_config.yaml
# 4. pili_itse_chatbot.py (ya existe, migrar a YAML config)
```

### Estructura de cada chatbot:

```python
class PILI{Servicio}ChatBot:
    def __init__(self):
        self.config = yaml.safe_load(open("config/{servicio}_config.yaml"))
        self.kb = self.config["knowledge_base"]
        self.mensajes = self.config["mensajes"]
        self.precios = self.config["precios"]

    def procesar(self, mensaje, estado) -> Dict:
        # FLUJO EN CÓDIGO (máquina de estados)
        if etapa == "inicial":
            return self._etapa_inicial()
        elif etapa == "...":
            return self._etapa_...(mensaje, estado)

    def _calcular_cotizacion(self, datos) -> Dict:
        # LÓGICA DE CÁLCULO
        # Usa self.precios desde YAML
        pass

    def _generar_items(self, datos) -> List[Dict]:
        # GENERA ITEMS DE COTIZACIÓN
        pass
```

---

**FIN DEL DOCUMENTO**

