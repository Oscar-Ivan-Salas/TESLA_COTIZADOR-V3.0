# 📊 INFORME EXHAUSTIVO: CÓDIGO PILI EXISTENTE

## 🔍 BÚSQUEDA COMPLETA REALIZADA

He analizado **TODO** el código PILI existente en el repositorio.

---

## 📁 ARCHIVOS ENCONTRADOS (4,638 líneas totales)

| Archivo | Líneas | Propósito | Estado |
|---------|--------|-----------|--------|
| **pili_brain.py** | 1,614 | Cerebro - Lógica de negocio, cálculos | ✅ COMPLETO |
| **pili_cotizadora.py** | 382 | Conversación cotizaciones paso a paso | ✅ FUNCIONAL |
| **pili_proyectos.py** | 1,004 | Conversación proyectos | ✅ FUNCIONAL |
| **pili_informes.py** | 905 | Conversación informes | ✅ FUNCIONAL |
| **pili_orchestrator.py** | 733 | Enrutador/orquestador | ✅ FUNCIONAL |
| **pili_integrator.py** | 30KB | Integración servicios | ✅ FUNCIONAL |

---

## ✅ LO QUE YA EXISTE Y FUNCIONA

### 1. **PILI Brain** (1,614 líneas)

**Ubicación**: `backend/app/services/pili_brain.py`

**Funcionalidades completas**:
- ✅ 10 servicios configurados (eléctrico, ITSE, contraincendios, etc.)
- ✅ Detección inteligente de servicio por keywords
- ✅ Extracción de datos (área, pisos, cantidades, potencia)
- ✅ Cálculos según normativas (CNE 2011, NFPA, RNE)
- ✅ Generación de items específicos por servicio
- ✅ Precios realistas mercado peruano 2025
- ✅ Generación de cotizaciones, proyectos e informes
- ✅ JSON estructurado

**Ejemplo de código existente**:
```python
class PILIBrain:
    def detectar_servicio(self, mensaje: str) -> str:
        """Detecta qué servicio necesita el usuario"""
        # Analiza keywords y retorna servicio

    def extraer_datos(self, mensaje: str, servicio: str) -> Dict:
        """Extrae área, pisos, cantidades automáticamente"""

    def generar_cotizacion(self, mensaje, servicio, complejidad):
        """Genera cotización completa con cálculos"""

    def _items_contraincendios(self, datos):
        """Items específicos contra incendios según NFPA"""
        # Rociadores, detectores, bomba, etc.
```

---

### 2. **PILI Cotizadora** (382 líneas)

**Ubicación**: `backend/app/services/pili_cotizadora.py`

**Funcionalidades conversacionales YA IMPLEMENTADAS**:

#### ✅ Conversación Paso a Paso

```python
def procesar(self, mensaje: str, historial: List[Dict]) -> Dict[str, Any]:
    # 1. DETECTAR SERVICIO
    servicio = self._detectar_servicio_contexto(mensaje, historial)

    # 2. EXTRAER DATOS DEL HISTORIAL
    datos_recopilados = self._extraer_datos_historial(historial, mensaje)

    # 3. VERIFICAR QUÉ DATOS FALTAN Y HACER PREGUNTAS
    pregunta = self._siguiente_pregunta(servicio, datos_recopilados)

    if pregunta:
        # AÚN FALTAN DATOS → PREGUNTA
        return pregunta

    # 4. YA TENEMOS TODO → GENERAR
    return self._generar_cotizacion_final(servicio, datos_recopilados)
```

#### ✅ Preguntas Específicas por Servicio

**Ejemplo: Instalaciones Eléctricas**
```python
def _siguiente_pregunta(self, servicio: str, datos: Dict) -> Optional[Dict]:
    if servicio.startswith("electrico"):

        if not datos.get("tipo_instalacion"):
            return {
                "mensaje_pili": "¿Es instalación **residencial**, **comercial** o **industrial**?",
                "botones": ["🏠 Residencial", "🏢 Comercial", "🏭 Industrial"]
            }

        if not datos.get("area_m2"):
            return {
                "mensaje_pili": "¿Cuántos **metros cuadrados (m²)** tiene el área?",
                "tipo_input": "numero"
            }

        if not datos.get("puntos_luz"):
            return {
                "mensaje_pili": "¿Cuántos **puntos de luz** necesitas?",
                "tipo_input": "numero"
            }

        # ... más preguntas

        return None  # Ya tiene todo
```

**Ejemplo: Sistema Contra Incendios**
```python
elif servicio == "contraincendios":

    if not datos.get("tipo_local"):
        return {
            "mensaje_pili": "¿Qué tipo de local es?",
            "campo_esperado": "tipo_local"
        }

    if not datos.get("area_m2"):
        return {
            "mensaje_pili": "¿Cuántos metros cuadrados tiene?",
            "tipo_input": "numero"
        }

    if not datos.get("riesgo"):
        return {
            "mensaje_pili": "¿Es riesgo **bajo**, **medio** o **alto**?",
            "botones": ["🟢 Bajo", "🟡 Medio", "🔴 Alto"]
        }
```

#### ✅ Extracción de Datos del Historial

```python
def _extraer_datos_historial(self, historial: List[Dict], mensaje_actual: str) -> Dict:
    """NO vuelve a preguntar lo ya dicho"""
    datos = {}

    # Combinar historial completo
    todos_mensajes = " ".join([msg["content"] for msg in historial]) + mensaje_actual

    # Extraer con regex
    datos["cliente"] = self._extraer_cliente(todos_mensajes)
    datos["area_m2"] = self._extraer_numero(todos_mensajes, ["metros", "m2", "m²"])
    datos["puntos_luz"] = self._extraer_numero(todos_mensajes, ["luces", "luminarias"])
    datos["tomacorrientes"] = self._extraer_numero(todos_mensajes, ["tomas", "enchufes"])

    return datos
```

---

### 3. **PILI Proyectos** (1,004 líneas)

**Ubicación**: `backend/app/services/pili_proyectos.py`

**Funcionalidades**:
- ✅ Conversación guiada para proyectos
- ✅ Proyectos simples y complejos PMI
- ✅ Generación de cronogramas Gantt
- ✅ Análisis de riesgos
- ✅ Plan de recursos
- ✅ Fases del proyecto

---

### 4. **PILI Informes** (905 líneas)

**Ubicación**: `backend/app/services/pili_informes.py`

**Funcionalidades**:
- ✅ Informes técnicos
- ✅ Informes ejecutivos APA
- ✅ Bibliografía formato APA 7ma
- ✅ Secciones estructuradas
- ✅ Conclusiones y recomendaciones

---

### 5. **PILI Orchestrator** (733 líneas)

**Ubicación**: `backend/app/services/pili_orchestrator.py`

**Funcionalidades**:
- ✅ Enruta a especialista correcto
- ✅ Integra con servicios existentes
- ✅ Maneja 6 tipos de flujos

---

## 🎯 LO QUE FUNCIONA BIEN

| Aspecto | Estado | Ubicación |
|---------|--------|-----------|
| **Detección de servicio** | ✅ EXCELENTE | pili_brain.py, pili_cotizadora.py |
| **Extracción de datos** | ✅ BUENA | pili_cotizadora.py:152-168 |
| **Cálculos CNE/NFPA** | ✅ PROFESIONAL | pili_brain.py:400-780 |
| **Preguntas paso a paso** | ✅ IMPLEMENTADO | pili_cotizadora.py:212-360 |
| **Memoria conversacional** | ✅ FUNCIONA | Usa historial completo |
| **Generación de items** | ✅ COMPLETO | 10 servicios con items |
| **JSON estructurado** | ✅ PERFECTO | Retorna JSON correcto |

---

## ⚠️ LO QUE NECESITA MEJORAR

### Problema 1: NO es Conversacional Como EXPERTO

**Actual**:
```
PILI: "¿Cuántos metros cuadrados tiene?"
Usuario: "200 m²"
PILI: "¿Cuántos puntos de luz?"
```

**Lo que quieres (EXPERTO)**:
```
PILI: "¡Perfecto! Sistema contra incendios.
Primero cuéntame: ¿Qué tipo de local es?
¿Comercial, industrial, residencial u oficinas?"

Usuario: "Comercial, un restaurante"

PILI: "Restaurante, entendido. Eso requiere atención ESPECIAL
por las cocinas. ¿Cuántos m² tiene el local?"

Usuario: "200 m²"

PILI: "200m² comercial - restaurante. Perfecto.
¿Tienen cocina a gas o eléctrica?
(Es IMPORTANTE para el tipo de sistema)"

Usuario: "Gas"

PILI: "Cocina a gas, eso requiere sistema ESPECIAL anti-explosión.
¿Cuántos ambientes tiene? ¿Cocina, comedor, almacén?"
```

**Diferencia**:
- ❌ Actual: Preguntas secas, como formulario
- ✅ Necesitas: Conversación EXPERTA, explica el "por qué"

### Problema 2: Falta Contexto Experto

**Actual**:
```python
if not datos.get("tipo_cocina"):
    return {
        "mensaje_pili": "¿Qué tipo de cocina tiene?"
    }
```

**Necesitas**:
```python
if not datos.get("tipo_cocina"):
    return {
        "mensaje_pili": """Perfecto, restaurante de 200m².

🔥 **Es CRÍTICO saber el tipo de cocina:**
¿Tienen cocina a gas o eléctrica?

💡 **¿Por qué pregunto?**
- Cocina a GAS → Requiere sistema especial clase K (aceites)
- Cocina ELÉCTRICA → Sistema estándar ABC

¿Cuál es su caso?""",
        "botones": ["🔥 Gas", "⚡ Eléctrica", "🔥⚡ Mixta"]
    }
```

### Problema 3: No Hace Sugerencias Proactivas

**Actual**: Solo pregunta lo que falta

**Necesitas**:
```
PILI: "Veo que tienes 200m² con cocina a gas.

✅ Te RECOMIENDO incluir:
- Detectores de humo (8 unidades mínimo según NFPA)
- Rociadores automáticos (16 unidades para 200m²)
- Sistema ESPECIAL para campana de cocina
- Extintores clase K para aceites

¿Te parece bien o prefieres ajustar algo?"
```

---

## 🔧 PLAN DE MEJORA (Sin Crear Código Nuevo)

### OPCIÓN A: Mejorar Mensajes en Código Existente

**Archivo**: `pili_cotizadora.py`

**Modificar**: Función `_siguiente_pregunta()` (línea 212-360)

**Cambio**:
```python
# ANTES (línea 232-240)
if not datos.get("area_m2"):
    return {
        "mensaje_pili": "¿Cuántos **metros cuadrados (m²)** tiene el área?"
    }

# DESPUÉS (conversacional experto)
if not datos.get("area_m2"):
    tipo = datos.get("tipo_instalacion", "")

    # Contexto experto según tipo
    if tipo == "residencial":
        contexto = """Como es instalación **residencial**, el área determina:
        - Número de circuitos (1 cada 25m² según CNE)
        - Cantidad de puntos de luz
        - Carga eléctrica total"""
    elif tipo == "comercial":
        contexto = """En **comercial** el área es CRÍTICA porque:
        - Define la carga eléctrica (30 VA/m² según CNE)
        - Número de circuitos dedicados
        - Tipo de tablero (monofásico o trifásico)"""
    else:
        contexto = "El área determina la capacidad del sistema."

    return {
        "mensaje_pili": f"""{contexto}

📐 **¿Cuántos metros cuadrados (m²) tiene?**

_Ejemplo: 150 m² o 150 metros cuadrados_""",
        "campo_esperado": "area_m2"
    }
```

### OPCIÓN B: Agregar Sistema de "Explicaciones Expertas"

**Nuevo archivo**: `pili_conocimiento_experto.py`

**Contenido**: Base de conocimiento por servicio

```python
CONOCIMIENTO_EXPERTO = {
    "contraincendios": {
        "restaurante": {
            "cocina_gas": {
                "explicacion": "Cocinas a gas requieren sistema clase K según NFPA 17A para fuegos de aceites y grasas",
                "riesgos": ["Explosión", "Incendio grasa"],
                "sistema_recomendado": "Supresión automática en campana + detectores térmicos"
            }
        }
    }
}
```

**Integrar en**: `pili_cotizadora.py`

---

## 💡 RECOMENDACIÓN FINAL

### LO QUE DEBES HACER:

**NO crear código nuevo**, sino **MEJORAR** lo existente:

1. ✅ **Mantener** toda la lógica de `pili_brain.py` (cálculos, items)
2. ✅ **Mantener** la estructura conversacional de `pili_cotizadora.py`
3. ✅ **Mejorar** los mensajes en `_siguiente_pregunta()` para que sean EXPERTOS
4. ✅ **Agregar** contexto y explicaciones del "por qué"
5. ✅ **Agregar** sugerencias proactivas

### Ejemplo Concreto:

**Archivo a modificar**: `backend/app/services/pili_cotizadora.py`

**Función**: `_siguiente_pregunta()` (líneas 212-360)

**Cambio**: Cada pregunta debe incluir:
1. ✅ Contexto experto
2. ✅ Explicación del "por qué"
3. ✅ Opciones claras con botones
4. ✅ Sugerencias proactivas

---

## 📊 RESUMEN EJECUTIVO

### CÓDIGO EXISTENTE:
- ✅ **4,638 líneas** de código PILI funcional
- ✅ **Sistema conversacional** ya implementado
- ✅ **10 servicios** configurados
- ✅ **Cálculos profesionales** según normativas
- ✅ **Extracción de datos** del historial

### LO QUE FALTA:
- ⚠️ **Conversación experta** (no solo preguntas secas)
- ⚠️ **Contexto explicativo** (el "por qué" de cada pregunta)
- ⚠️ **Sugerencias proactivas** (recomendar, no solo preguntar)

### SOLUCIÓN:
- 🔧 **NO crear código nuevo**
- 🔧 **Mejorar mensajes** en funciones existentes
- 🔧 **Agregar conocimiento experto** por servicio
- 🔧 **Mantener** toda la lógica de cálculos y estructura

---

**¿Quieres que proceda a MEJORAR el código existente con esta lógica conversacional experta?**

Solo dime:
1. ¿Por qué servicio empiezo? (contraincendios, eléctrico, etc.)
2. ¿Mejoro SOLO los mensajes o también agrego base de conocimiento?
3. ¿Trabajamos en `pili_cotizadora.py` o también en los otros?

---

**Archivos completos analizados:**
- ✅ pili_brain.py (1,614 líneas)
- ✅ pili_cotizadora.py (382 líneas)
- ✅ pili_proyectos.py (1,004 líneas)
- ✅ pili_informes.py (905 líneas)
- ✅ pili_orchestrator.py (733 líneas)
- ✅ pili_multi_ia.py (actualizado con modo offline)

**Total analizado: ~5,000 líneas de código PILI**
