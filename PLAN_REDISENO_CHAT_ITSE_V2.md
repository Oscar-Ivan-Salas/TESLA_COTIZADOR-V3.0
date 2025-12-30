# 🎯 PLAN DE REDISEÑO CHAT ITSE V2.0

**Fecha**: 30 de Diciembre 2025
**Estado**: 📋 PLAN DE ACCIÓN - Listo para implementar
**Objetivo**: Alinear chat con plantillas REALES y frontend existente

---

## 📊 ANÁLISIS DEL FRONTEND EXISTENTE

### Componente: `PiliITSEChat.jsx`

**Ubicación**: `frontend/src/components/PiliITSEChat.jsx`

**Conexión con Backend**:
```javascript
POST http://localhost:8000/api/chat/pili-itse

Request:
{
  "mensaje": "SALUD",
  "conversation_state": {...}  // Estado de conversación
}

Response esperado:
{
  "success": true,
  "respuesta": "Texto respuesta de PILI",
  "botones_sugeridos": [...],  // o "botones"
  "state": {...},              // o "conversation_state"
  "datos_generados": {...},    // Para vista previa
  "cotizacion_generada": {...} // Cotización final
}
```

**Características del Frontend**:
- ✅ Muestra 10 botones iniciales (incluyendo "Pozo a Tierra", "Automatización")
- ✅ Renderiza botones dinámicos que vienen del backend
- ✅ Maneja estado de conversación persistente
- ✅ Notifica al padre cuando hay cotización
- ✅ Tiene botón "Finalizar y Generar DOC" (se habilita con cotización)
- ✅ Diseño profesional con colores Tesla

---

## 🎯 CAMPOS QUE DEBE RECOGER EL CHAT (ITSE)

### Basado en análisis de plantillas:

#### **CAMPOS BÁSICOS** (Cotización Simple - 12 campos):

1. **CLIENTE_NOMBRE** ← ❌ NO recoge
2. **PROYECTO_NOMBRE** ← ⚠️ Recoge parcial (tipo establecimiento)
3. **SERVICIO_NOMBRE** ← ✅ Auto: "Certificado ITSE"
4. **CATEGORIA** ← ✅ Ya recoge (Salud, Comercio, etc.)
5. **TIPO** ← ✅ Ya recoge (Hospital, Tienda, etc.)
6. **AREA_M2** ← ✅ Ya recoge
7. **PISOS** ← ✅ Ya recoge (pero no lo usa en plantilla)
8. **FECHA_COTIZACION** ← ✅ Auto: fecha actual
9. **VIGENCIA** ← ❌ NO recoge (default: "30 días")
10. **NORMATIVA_APLICABLE** ← ✅ Auto: "D.S. 002-2018-PCM"
11. **DESCRIPCION_PROYECTO** ← ❌ NO recoge
12. **NUMERO_COTIZACION** ← ✅ Auto: generar

#### **ITEMS** (tabla dinámica):
- ✅ Ya calcula: items según riesgo (TUPA + Tesla)

#### **TOTALES**:
- ✅ Ya calcula: SUBTOTAL, IGV, TOTAL

---

## 🔄 FLUJO REDISEÑADO (ITSE V2.0)

### **ETAPA 1: Bienvenida** (ya existe)

**PILI muestra**:
```
¡Hola! 👋 Soy Pili...

Selecciona tu tipo de establecimiento:
[🏥 Salud] [🎓 Educación] [🏨 Hospedaje] ... (10 botones)
```

**Estado**:
```python
{
    "etapa": "inicial",
    "servicio": "itse"
}
```

---

### **ETAPA 2: Nombre del Cliente** (NUEVO)

**Usuario selecciona**: "🏥 Salud"

**PILI pregunta**:
```
Perfecto, sector Salud.

Antes de continuar, necesito algunos datos:

¿Cuál es el nombre del cliente o empresa?

_Escribe el nombre completo_
```

**Estado actualizado**:
```python
{
    "etapa": "cliente",
    "categoria": "SALUD",
    "servicio": "itse"
}
```

---

### **ETAPA 3: Nombre del Proyecto** (NUEVO)

**Usuario escribe**: "Hospital Santa Rosa SAC"

**PILI pregunta**:
```
Gracias. Ahora, ¿cuál es el nombre del proyecto?

Ejemplo: "Certificado ITSE para Hospital Santa Rosa"

_Escribe el nombre del proyecto_
```

**Estado**:
```python
{
    "etapa": "proyecto",
    "categoria": "SALUD",
    "cliente_nombre": "Hospital Santa Rosa SAC",
    "servicio": "itse"
}
```

---

### **ETAPA 4: Tipo Específico** (ya existe)

**Usuario escribe**: "Certificado ITSE Hospital Santa Rosa - Huancayo"

**PILI muestra**:
```
Entendido. ¿Qué tipo específico de establecimiento es?

[Hospital] [Clínica] [Centro Médico] [Consultorio] [Laboratorio]
```

**Estado**:
```python
{
    "etapa": "tipo",
    "categoria": "SALUD",
    "cliente_nombre": "Hospital Santa Rosa SAC",
    "proyecto_nombre": "Certificado ITSE Hospital Santa Rosa - Huancayo"
}
```

---

### **ETAPA 5: Área en m²** (ya existe)

**Usuario selecciona**: "Hospital"

**PILI pregunta**:
```
Entendido, es un Hospital.

¿Cuál es el área total en m²?

_Escribe el número (ejemplo: 600)_
```

**Estado**:
```python
{
    "etapa": "area",
    "categoria": "SALUD",
    "cliente_nombre": "Hospital Santa Rosa SAC",
    "proyecto_nombre": "Certificado ITSE Hospital Santa Rosa - Huancayo",
    "tipo": "Hospital"
}
```

---

### **ETAPA 6: Número de Pisos** (ya existe)

**Usuario escribe**: "600"

**PILI pregunta**:
```
📐 Área: 600 m²

¿Cuántos pisos tiene el establecimiento?

_Escribe el número (ejemplo: 2)_
```

**Estado**:
```python
{
    "etapa": "pisos",
    "categoria": "SALUD",
    "cliente_nombre": "Hospital Santa Rosa SAC",
    "proyecto_nombre": "Certificado ITSE Hospital Santa Rosa - Huancayo",
    "tipo": "Hospital",
    "area_m2": 600.0
}
```

---

### **ETAPA 7: Tipo de Documento** (NUEVO - CRÍTICO)

**Usuario escribe**: "2"

**Sistema calcula**:
- Riesgo: MUY_ALTO (área > 500 y pisos >= 2)
- Precios: TUPA + Tesla

**PILI pregunta**:
```
Perfecto. He calculado tu cotización:

📊 Nivel de Riesgo: MUY ALTO
💰 Costo estimado: S/ 2,284.60 - S/ 2,884.60

Ahora, ¿qué tipo de documento necesitas?

[📄 Cotización Simple]
[📋 Proyecto Simple]
[📊 Informe Técnico]
```

**Estado**:
```python
{
    "etapa": "tipo_documento",
    "categoria": "SALUD",
    "cliente_nombre": "Hospital Santa Rosa SAC",
    "proyecto_nombre": "Certificado ITSE Hospital Santa Rosa - Huancayo",
    "tipo": "Hospital",
    "area_m2": 600.0,
    "pisos": 2,
    "riesgo": "MUY_ALTO",
    "costo_tupa": 1084.60,
    "costo_tesla_min": 1200,
    "costo_tesla_max": 1800,
    "total_min": 2284.60,
    "total_max": 2884.60
}
```

---

### **ETAPA 8A: Generar Cotización Simple**

**Usuario selecciona**: "📄 Cotización Simple"

**PILI genera datos completos**:
```python
datos_documento = {
    # Datos básicos
    "CLIENTE_NOMBRE": "Hospital Santa Rosa SAC",
    "PROYECTO_NOMBRE": "Certificado ITSE Hospital Santa Rosa - Huancayo",
    "SERVICIO_NOMBRE": "Certificado ITSE",
    "AREA_M2": 600.0,

    # Datos auto-generados
    "NUMERO_COTIZACION": "COT-ITSE-2025-001",  # Auto
    "FECHA_COTIZACION": "30/12/2025",  # Auto
    "VIGENCIA": "30 días",  # Default
    "NORMATIVA_APLICABLE": "D.S. 002-2018-PCM",  # Auto

    # Descripción generada con IA (o template)
    "DESCRIPCION_PROYECTO": f"Certificado de Inspección Técnica de Seguridad en Edificaciones (ITSE) para {datos['tipo']} de {datos['area_m2']} m², ubicado en Huancayo. Nivel de riesgo: {datos['riesgo']}.",

    # Items
    "items": [
        {
            "descripcion": f"Certificado ITSE - Nivel {datos['riesgo']}",
            "cantidad": 1,
            "unidad": "und",
            "precio_unitario": datos['costo_tupa'],
            "total": datos['costo_tupa']
        },
        {
            "descripcion": f"Servicio Técnico Tesla - Evaluación + Planos + Gestión",
            "cantidad": 1,
            "unidad": "glb",
            "precio_unitario": datos['costo_tesla_min'],
            "total": datos['costo_tesla_min']
        }
    ],

    # Totales
    "SUBTOTAL": 2284.60,
    "IGV": 411.23,
    "TOTAL": 2695.83
}
```

**PILI responde**:
```
✅ Cotización generada exitosamente

📄 COTIZACIÓN SIMPLE
Número: COT-ITSE-2025-001
Cliente: Hospital Santa Rosa SAC
Total: S/ 2,695.83 (incluye IGV)

¿Qué deseas hacer?

[📥 Ver Vista Previa HTML]
[📄 Descargar Word]
[📑 Descargar PDF]
[🔄 Nueva consulta]
```

**Estado final**:
```python
{
    "etapa": "finalizado",
    "tipo_documento": "cotizacion_simple",
    "datos_completos": datos_documento,
    "cotizacion_generada": True
}
```

---

### **ETAPA 8B: Generar Proyecto Simple**

**Si usuario selecciona**: "📋 Proyecto Simple"

**PILI pregunta datos adicionales**:
```
Para un Proyecto Simple, necesito:

¿Cuándo deseas iniciar el proyecto?

_Escribe la fecha (ejemplo: 15/01/2025)_
```

**Luego pregunta**:
```
¿Cuál es la duración esperada del proyecto?

[📅 7 días (TUPA estándar)]
[📅 15 días (con seguimiento)]
[📅 30 días (con gestión completa)]
```

**Y genera**:
```python
datos_documento = {
    # Todos los campos anteriores +
    "NOMBRE_PROYECTO": "Certificado ITSE Hospital Santa Rosa - Huancayo",
    "CODIGO_PROYECTO": "PROY-ITSE-2025-001",
    "FECHA_INICIO": "15/01/2025",
    "FECHA_FIN": "22/01/2025",  # Calculado
    "DURACION_TOTAL": 7,
    "PRESUPUESTO": 2695.83,
    "ALCANCE_PROYECTO": "Obtención de Certificado ITSE nivel MUY ALTO...",  # Generado con IA
    "DIAS_INGENIERIA": 2,
    "DIAS_EJECUCION": 5,
    "NORMATIVA_APLICABLE": "D.S. 002-2018-PCM"
}
```

---

## 📋 COMPARACIÓN: ANTES vs DESPUÉS

| Aspecto | ITSE Actual | ITSE V2.0 |
|---------|-------------|-----------|
| **Etapas** | 6 etapas | 8 etapas |
| **Campos recopilados** | 6 campos | 12+ campos |
| **Cobertura plantillas** | 50% | 100% |
| **Tipos de documento** | 1 (implícito) | 3 opciones |
| **Textos descriptivos** | No genera | ✅ Genera con IA |
| **Datos faltantes** | 6 campos | 0 campos |
| **Listo para generadores** | ❌ NO | ✅ SÍ |

---

## 🛠️ IMPLEMENTACIÓN TÉCNICA

### **CAMBIOS EN `pili_itse_chatbot.py`**

#### 1. **Actualizar `__init__` con templates de texto**

```python
def __init__(self):
    self.knowledge_base = {
        # ... precios existentes ...

        # NUEVO: Templates de descripción
        "templates_descripcion": {
            "SALUD": "Certificado ITSE nivel {riesgo} para {tipo} de {area} m², ubicado en Huancayo. Incluye evaluación técnica según D.S. 002-2018-PCM.",
            "COMERCIO": "Certificado ITSE nivel {riesgo} para {tipo} comercial de {area} m², ubicado en Huancayo.",
            # ... 8 categorías más
        }
    }
```

#### 2. **Agregar nuevas etapas**

```python
def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
    etapa = estado.get("etapa", "inicial")

    if etapa == "inicial":
        return self._etapa_inicial(estado)
    elif etapa == "cliente":  # NUEVO
        return self._etapa_cliente(mensaje, estado)
    elif etapa == "proyecto":  # NUEVO
        return self._etapa_proyecto(mensaje, estado)
    elif etapa == "categoria":
        return self._etapa_categoria(mensaje, estado)
    elif etapa == "tipo":
        return self._etapa_tipo(mensaje, estado)
    elif etapa == "area":
        return self._etapa_area(mensaje, estado)
    elif etapa == "pisos":
        return self._etapa_pisos(mensaje, estado)
    elif etapa == "tipo_documento":  # NUEVO
        return self._etapa_tipo_documento(mensaje, estado)
    elif etapa == "generar_documento":  # NUEVO
        return self._generar_documento_completo(mensaje, estado)
```

#### 3. **Implementar etapas nuevas**

```python
def _etapa_cliente(self, mensaje: str, estado: Dict) -> Dict:
    """NUEVO: Recoger nombre del cliente"""
    cliente = mensaje.strip()

    estado["cliente_nombre"] = cliente
    estado["etapa"] = "proyecto"

    return {
        'success': True,
        'respuesta': f"Gracias, {cliente}.\n\nAhora, ¿cuál es el nombre del proyecto?\n\nEjemplo: \"Certificado ITSE Hospital Santa Rosa\"",
        'botones': None,
        'estado': estado,
        'cotizacion': None
    }

def _etapa_proyecto(self, mensaje: str, estado: Dict) -> Dict:
    """NUEVO: Recoger nombre del proyecto"""
    proyecto = mensaje.strip()

    estado["proyecto_nombre"] = proyecto
    estado["etapa"] = "tipo"

    # Continuar con selección de tipo
    categoria = estado.get("categoria")
    tipos = self.knowledge_base["categorias"][categoria]["tipos"]
    botones = [{"text": t, "value": t} for t in tipos]

    return {
        'success': True,
        'respuesta': f"Perfecto. ¿Qué tipo específico de {categoria} es?",
        'botones': botones,
        'estado': estado,
        'cotizacion': None
    }
```

#### 4. **Modificar `_etapa_pisos` para ir a tipo_documento**

```python
def _etapa_pisos(self, mensaje: str, estado: Dict) -> Dict:
    """Modificado: Después de pisos, ofrecer tipo de documento"""
    try:
        pisos = int(mensaje)
        # ... validación ...

        estado["pisos"] = pisos

        # Calcular riesgo
        riesgo = self._calcular_riesgo(...)
        estado["riesgo"] = riesgo

        # Calcular precios
        precios_tupa = self.knowledge_base["precios_municipales"][riesgo]
        precios_tesla = self.knowledge_base["precios_tesla"][riesgo]

        estado["costo_tupa"] = precios_tupa["precio"]
        estado["costo_tesla_min"] = precios_tesla["min"]
        estado["costo_tesla_max"] = precios_tesla["max"]
        estado["total_min"] = precios_tupa["precio"] + precios_tesla["min"]
        estado["total_max"] = precios_tupa["precio"] + precios_tesla["max"]

        # CAMBIO: No generar cotización aún, ofrecer tipo de documento
        estado["etapa"] = "tipo_documento"

        respuesta = f"""Perfecto. He calculado tu cotización:

📊 **Nivel de Riesgo:** {riesgo.replace('_', ' ')}
💰 **Costo estimado:** S/ {estado['total_min']:,.2f} - S/ {estado['total_max']:,.2f}

Ahora, ¿qué tipo de documento necesitas?"""

        botones = [
            {"text": "📄 Cotización Simple", "value": "COT_SIMPLE"},
            {"text": "📋 Proyecto Simple", "value": "PROY_SIMPLE"},
            {"text": "📊 Informe Técnico", "value": "INF_TECNICO"}
        ]

        return {
            'success': True,
            'respuesta': respuesta,
            'botones': botones,
            'estado': estado,
            'cotizacion': None
        }

    except ValueError:
        # ... error handling ...
```

#### 5. **Implementar `_etapa_tipo_documento`**

```python
def _etapa_tipo_documento(self, mensaje: str, estado: Dict) -> Dict:
    """NUEVO: Procesar selección de tipo de documento"""
    tipo_doc = mensaje
    estado["tipo_documento"] = tipo_doc

    if tipo_doc == "COT_SIMPLE":
        # Generar inmediatamente (no necesita más datos)
        return self._generar_cotizacion_simple(estado)

    elif tipo_doc == "PROY_SIMPLE":
        # Preguntar fecha inicio
        estado["etapa"] = "proyecto_fecha_inicio"
        return {
            'success': True,
            'respuesta': "Para un Proyecto Simple, ¿cuándo deseas iniciar?\n\n_Escribe la fecha (ejemplo: 15/01/2025)_",
            'botones': None,
            'estado': estado,
            'cotizacion': None
        }

    elif tipo_doc == "INF_TECNICO":
        # Generar inmediatamente
        return self._generar_informe_tecnico(estado)
```

#### 6. **Implementar generadores por tipo**

```python
def _generar_cotizacion_simple(self, estado: Dict) -> Dict:
    """Genera cotización simple con TODOS los campos"""
    from datetime import datetime

    # Generar campos auto
    numero_cot = f"COT-ITSE-{datetime.now().year}-001"  # Mejorar con BD
    fecha_actual = datetime.now().strftime("%d/%m/%Y")

    # Generar descripción con template
    template = self.knowledge_base["templates_descripcion"][estado["categoria"]]
    descripcion = template.format(
        riesgo=estado["riesgo"],
        tipo=estado["tipo"],
        area=estado["area_m2"]
    )

    # Construir datos completos para plantilla
    datos_documento = {
        # Datos recopilados
        "CLIENTE_NOMBRE": estado.get("cliente_nombre", "Cliente ITSE"),
        "PROYECTO_NOMBRE": estado.get("proyecto_nombre", f"Certificado ITSE {estado['tipo']}"),
        "AREA_M2": estado["area_m2"],

        # Datos auto-generados
        "NUMERO_COTIZACION": numero_cot,
        "FECHA_COTIZACION": fecha_actual,
        "VIGENCIA": "30 días",
        "SERVICIO_NOMBRE": "Certificado ITSE",
        "NORMATIVA_APLICABLE": "D.S. 002-2018-PCM - Reglamento de Inspecciones Técnicas",
        "DESCRIPCION_PROYECTO": descripcion,

        # Items
        "items": [
            {
                "descripcion": f"Certificado ITSE - Nivel {estado['riesgo']}",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": estado["costo_tupa"],
                "total": estado["costo_tupa"]
            },
            {
                "descripcion": "Servicio Técnico Tesla - Evaluación + Planos + Gestión",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": estado["costo_tesla_min"],
                "total": estado["costo_tesla_min"]
            }
        ],

        # Totales
        "SUBTOTAL": estado["total_min"],
        "IGV": round(estado["total_min"] * 0.18, 2),
        "TOTAL": round(estado["total_min"] * 1.18, 2)
    }

    # Formatear respuesta
    respuesta = f"""✅ **Cotización generada exitosamente**

📄 **COTIZACIÓN SIMPLE**
Número: {numero_cot}
Cliente: {datos_documento['CLIENTE_NOMBRE']}
Total: S/ {datos_documento['TOTAL']:,.2f} (incluye IGV)

¿Qué deseas hacer?"""

    botones = [
        {"text": "📥 Ver Vista Previa", "value": "VER_PREVIEW"},
        {"text": "📄 Descargar Word", "value": "DOWNLOAD_WORD"},
        {"text": "📑 Descargar PDF", "value": "DOWNLOAD_PDF"},
        {"text": "🔄 Nueva consulta", "value": "REINICIAR"}
    ]

    return {
        'success': True,
        'respuesta': respuesta,
        'botones': botones,
        'estado': estado,
        'cotizacion': datos_documento,  # Para compatibilidad
        'datos_generados': datos_documento  # Para vista previa
    }
```

---

## 🚀 PLAN DE IMPLEMENTACIÓN (PASOS CONCRETOS)

### **PASO 1: Actualizar `pili_itse_chatbot.py`** ⏱️ 2-3 horas

1. ✅ Agregar templates de descripción en `__init__`
2. ✅ Agregar 3 nuevas etapas: `cliente`, `proyecto`, `tipo_documento`
3. ✅ Modificar `_etapa_pisos` para no generar cotización aún
4. ✅ Implementar `_etapa_tipo_documento`
5. ✅ Implementar `_generar_cotizacion_simple` (completo)
6. ✅ Implementar `_generar_proyecto_simple` (completo)
7. ✅ Implementar `_generar_informe_tecnico` (completo)

### **PASO 2: Probar localmente** ⏱️ 30 min

```bash
cd Pili_ChatBot
python pili_itse_chatbot.py

# Debería mostrar flujo completo con 8 etapas
```

### **PASO 3: Actualizar endpoint backend** ⏱️ 1 hora

**En `backend/app/routers/chat.py`** (o crear nuevo router):

```python
from Pili_ChatBot.pili_itse_chatbot import PILIITSEChatBot

# Instancia global
chatbot_itse = PILIITSEChatBot()

@router.post("/api/chat/pili-itse")
async def chat_pili_itse(request: ChatRequest):
    """Endpoint ITSE v2.0 - Alineado con plantillas"""
    resultado = chatbot_itse.procesar(
        mensaje=request.mensaje,
        estado=request.conversation_state
    )

    return {
        "success": resultado['success'],
        "respuesta": resultado['respuesta'],
        "botones_sugeridos": resultado['botones'],  # Frontend espera este nombre
        "state": resultado['estado'],  # Frontend espera este nombre
        "datos_generados": resultado.get('datos_generados'),
        "cotizacion_generada": resultado.get('cotizacion')
    }
```

### **PASO 4: Conectar con generadores** ⏱️ 2 horas

**Cuando usuario selecciona "Descargar Word"**:

```python
from backend.app.services.professional.generators.cotizaciones.simple import CotizacionSimpleGenerator

@router.post("/api/chat/pili-itse/generar-word")
async def generar_word_itse(request: GenerarDocRequest):
    """Genera documento Word desde datos de chat"""
    datos = request.datos_generados

    # Llamar al generador
    generator = CotizacionSimpleGenerator()
    archivo_path = generator.generar(
        datos=datos,
        ruta_salida=Path(f"storage/generados/{datos['NUMERO_COTIZACION']}.docx")
    )

    return FileResponse(
        path=str(archivo_path),
        filename=f"{datos['NUMERO_COTIZACION']}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
```

---

## ✅ VALIDACIÓN FINAL

**Antes de continuar con otros servicios**, validar:

1. ✅ Chat recoge los 12 campos necesarios
2. ✅ Genera datos completos para las 3 plantillas (Simple, Proyecto, Informe)
3. ✅ Frontend muestra botones correctamente
4. ✅ Generadores Word/PDF funcionan con los datos

**Una vez validado ITSE v2.0**:
→ Replicar patrón a Pozo a Tierra
→ Luego a Electricidad
→ Etc.

---

## 📋 RESUMEN EJECUTIVO

**Lo que voy a hacer**:
1. ✅ Agregar 3 etapas nuevas (cliente, proyecto, tipo_documento)
2. ✅ Recoger 12 campos (vs 6 actuales)
3. ✅ Generar textos descriptivos con templates
4. ✅ Ofrecer 3 tipos de documentos
5. ✅ Conectar con generadores Word/PDF

**Tiempo estimado**: 5-6 horas

**¿Procedo con la implementación?** 🚀

---

**Documento creado**: 30 de Diciembre 2025
**Autor**: Claude Code (Sonnet 4.5)
**Estado**: ✅ PLAN LISTO - Esperando confirmación para implementar
