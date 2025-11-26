# 🤖 README - Flujo de Generación de Documentos con PILI

> **Guía completa del proceso de generación de documentos inteligente**
> Versión: 3.0
> Última actualización: 2025-11-26

---

## 📋 Índice

1. [Problema Identificado](#-problema-identificado)
2. [Flujo Ideal vs Flujo Actual](#-flujo-ideal-vs-flujo-actual)
3. [Arquitectura del Sistema](#-arquitectura-del-sistema)
4. [Cómo Debe Funcionar PILI](#-cómo-debe-funcionar-pili)
5. [Endpoints Disponibles](#-endpoints-disponibles)
6. [Proceso de Generación Paso a Paso](#-proceso-de-generación-paso-a-paso)
7. [Componentes Frontend](#-componentes-frontend)
8. [Componentes Backend](#-componentes-backend)
9. [Solución al Problema](#-solución-al-problema)

---

## 🔴 Problema Identificado

### Síntoma
PILI está enviando un **chat larguísimo** en lugar de:
- Hacer preguntas cortas e inteligentes
- Guiar al usuario paso a paso
- Generar vista previa HTML editable
- Permitir confirmación antes de crear documentos

### Causa Raíz
El componente `ChatIA.jsx` está llamando al **endpoint INCORRECTO**:

```javascript
// ❌ ACTUAL (INCORRECTO)
const response = await fetch('/api/chat/conversacional', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    mensaje: inputMensaje,
    contexto: mensajes
  })
});
```

Este endpoint (`/chat/conversacional`) es **básico** y solo llama a Gemini directamente, generando respuestas largas sin estructura.

### Endpoint Correcto
Debería usar `/api/chat/chat-contextualizado` que tiene:
- ✅ Personalidades PILI especializadas
- ✅ Generación de JSON estructurado
- ✅ Vista previa HTML editable
- ✅ Botones contextuales inteligentes
- ✅ Detección automática de servicios con PILIBrain

---

## 🎯 Flujo Ideal vs Flujo Actual

### Flujo IDEAL (Como Debe Ser)

```
┌─────────────────────────────────────────────────────────────┐
│                   FLUJO COMPLETO PILI 3.0                   │
└─────────────────────────────────────────────────────────────┘

1️⃣ INICIO - Usuario selecciona tipo de documento
   └─> Frontend: Establece tipo_flujo (cotizacion-simple, proyecto-complejo, etc.)
   └─> Backend: Carga contexto PILI específico del servicio

2️⃣ CHAT INTELIGENTE - Conversación guiada
   ┌───────────────────────────────────────────────────┐
   │ Usuario: "Necesito cotizar instalación eléctrica" │
   │                                                    │
   │ PILI: "¡Hola! 🤖 Soy PILI Cotizadora.            │
   │        ¿Qué tipo de instalación necesitas?        │
   │        [🏠 Residencial] [🏢 Comercial]            │
   │        [🏭 Industrial]"                           │
   │                                                    │
   │ Usuario: "Residencial"                            │
   │                                                    │
   │ PILI: "Perfecto. ¿Cuántos metros cuadrados       │
   │        tiene el área?"                            │
   │                                                    │
   │ Usuario: "120 m2"                                 │
   │                                                    │
   │ PILI: "Excelente. ¿Aproximadamente cuántos       │
   │        puntos de luz necesitas?"                  │
   │                                                    │
   │ Usuario: "25 puntos"                              │
   └───────────────────────────────────────────────────┘

   📌 CARACTERÍSTICAS:
   - Preguntas cortas (1-2 líneas)
   - Botones contextuales según el servicio
   - Máximo 5-7 preguntas esenciales
   - Guía clara y directa

3️⃣ GENERACIÓN DE DATOS - PILIBrain procesa
   └─> PILIBrain.detectar_servicio(mensaje_completo)
   └─> PILIBrain.generar_cotizacion(servicio, complejidad)
   └─> Genera JSON estructurado con items calculados

4️⃣ VISTA PREVIA HTML - Usuario revisa y edita
   ┌────────────────────────────────────────────────┐
   │  VISTA PREVIA - COTIZACIÓN COT-202511-0001    │
   │  ────────────────────────────────────────────  │
   │  Cliente: [Editable] _____________________     │
   │  Proyecto: [Editable] ____________________     │
   │                                                │
   │  Items:                                        │
   │  1. Punto luz empotrado     25 und  S/. 375   │
   │  2. Tomacorriente doble     15 und  S/. 270   │
   │  3. Cable THW 2.5mm²       350 m    S/. 700   │
   │                                                │
   │  Subtotal:                         S/. 5,850  │
   │  IGV (18%):                        S/. 1,053  │
   │  TOTAL:                            S/. 6,903  │
   │                                                │
   │  [✏️ Editar] [👁️ Ocultar IGV]                 │
   │  [✅ Confirmar] [🔄 Regenerar]                 │
   └────────────────────────────────────────────────┘

5️⃣ CONFIRMACIÓN - Usuario aprueba
   └─> Usuario hace clic en "Confirmar"
   └─> Frontend envía JSON a backend

6️⃣ GENERACIÓN DE DOCUMENTO - Python crea archivo
   └─> Backend recibe JSON
   └─> WordGenerator.generar_cotizacion(datos)
   └─> Guarda en storage/generados/COT-202511-0001.docx
   └─> Retorna URL de descarga

7️⃣ DESCARGA - Usuario obtiene archivo
   └─> Frontend muestra botón de descarga
   └─> Usuario descarga Word
   └─> (Opcional) Convierte a PDF desde Word
```

### Flujo ACTUAL (Incorrecto)

```
❌ PROBLEMA ACTUAL

1️⃣ Usuario: "Necesito cotizar instalación eléctrica residencial de 120m2"

2️⃣ PILI envía respuesta LARGA (500+ caracteres):
   "¡Hola! Soy PILI, tu asistente especializada en cotizaciones
   eléctricas. Para generar una cotización precisa para tu
   instalación eléctrica residencial de 120m2, necesito la
   siguiente información adicional:

   1. Distribución de espacios: ¿Cuántas habitaciones, baños,
      cocina tiene la vivienda?
   2. Puntos de iluminación: ¿Cuántos puntos de luz necesitas
      en total?
   3. Tomacorrientes: ¿Cuántos tomacorrientes requieres?
   4. Tablero eléctrico: ¿Necesitas tablero nuevo?
   5. Cableado existente: ¿Es instalación nueva o hay cableado?
   6. Normativa: ¿Requieres certificación?

   Con esta información podré prepararte una cotización detallada..."

❌ PROBLEMAS:
- Texto demasiado largo
- Hace todas las preguntas de una vez
- No usa botones contextuales
- No genera vista previa HTML
- No estructura datos en JSON
- Usuario se confunde
```

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                      ARQUITECTURA PILI                       │
└─────────────────────────────────────────────────────────────┘

FRONTEND (React)
├── App.jsx                          # Orquestador principal
│   ├── Estado: tipoFlujo            # cotizacion-simple, proyecto-complejo, etc.
│   ├── Estado: conversacion         # Array de mensajes
│   ├── Estado: htmlPreview          # Vista previa HTML
│   ├── Estado: datosEditables       # Datos del documento
│   └── función: enviarMensaje()     # Comunica con backend
│
├── ChatIA.jsx                       # Componente de chat
│   ├── Estado: mensajes             # Historial del chat
│   ├── Estado: cargando             # Loading state
│   └── función: enviarMensaje()     # ⚠️ USA ENDPOINT INCORRECTO
│
└── PiliAvatar.jsx                   # Avatar animado
    └── Estados: idle, thinking, speaking

BACKEND (FastAPI)
├── routers/chat.py                  # Endpoints PILI
│   │
│   ├── /chat/conversacional         # ❌ ENDPOINT BÁSICO (problema actual)
│   │   └── Llama directamente a gemini_service.chat()
│   │   └── No tiene lógica PILI
│   │   └── Genera respuestas largas
│   │
│   ├── /chat/chat-contextualizado   # ✅ ENDPOINT CORRECTO
│   │   ├── Carga contexto PILI del servicio
│   │   ├── Usa personalidades especializadas
│   │   ├── Llama a PILIBrain para generar datos
│   │   ├── Genera vista previa HTML
│   │   └── Retorna botones contextuales
│   │
│   └── /chat/botones-contextuales/{tipo_flujo}
│       └── Retorna botones según etapa
│
├── services/
│   ├── pili_brain.py                # 🧠 CEREBRO OFFLINE
│   │   ├── detectar_servicio()      # Identifica tipo de servicio
│   │   ├── generar_cotizacion()     # Crea JSON con items
│   │   ├── calcular_precios()       # Precios según normativa
│   │   └── extraer_datos()          # Extrae info del mensaje
│   │
│   ├── gemini_service.py            # Cliente Gemini AI
│   │   └── chat()                   # Conversación con Gemini
│   │
│   ├── word_generator.py            # Generador Word
│   │   └── generar_cotizacion()     # JSON → Word
│   │
│   └── pdf_generator.py             # Generador PDF
│       └── generar_desde_word()     # Word → PDF

STORAGE
└── generados/
    ├── COT-202511-0001.docx         # Documentos Word
    └── COT-202511-0001.pdf          # Documentos PDF
```

---

## 🤖 Cómo Debe Funcionar PILI

### Personalidades PILI Especializadas

PILI tiene **6 agentes especializados** según el tipo de servicio:

| Agente | Tipo Flujo | Personalidad | Preguntas Típicas |
|--------|-----------|--------------|-------------------|
| **PILI Cotizadora** | `cotizacion-simple` | Rápida y directa (5-15 min) | ¿Tipo instalación? ¿Área m²? ¿Puntos luz? |
| **PILI Analista** | `cotizacion-compleja` | Detallista con OCR | ¿Tienes planos? ¿Normativa? ¿Especificaciones? |
| **PILI Coordinadora** | `proyecto-simple` | Práctica y organizada | ¿Nombre? ¿Cliente? ¿Presupuesto? ¿Duración? |
| **PILI PM** | `proyecto-complejo` | Profesional PMI | ¿Fases? ¿Hitos? ¿Recursos? ¿Cronograma? |
| **PILI Reportera** | `informe-simple` | Técnica y clara | ¿Proyecto? ¿Datos? ¿Métricas? |
| **PILI Analista Senior** | `informe-ejecutivo` | Ejecutiva y estratégica | ¿KPIs? ¿ROI? ¿Análisis financiero? |

### Ejemplo de Conversación CORRECTA

```
🤖 PILI Cotizadora (cotizacion-simple)
───────────────────────────────────────

Usuario: "Necesito cotizar instalación eléctrica"

PILI: "¡Hola! 🤖 Soy PILI Cotizadora.
       ¿Qué tipo de instalación necesitas?"

       [🏠 Residencial] [🏢 Comercial] [🏭 Industrial]

Usuario: [Clic en Residencial]

PILI: "Perfecto. ¿Cuántos m² tiene el área?"

Usuario: "120 m2"

PILI: "Excelente. ¿Cuántos puntos de luz aproximadamente?"

Usuario: "25 puntos"

PILI: "Entendido. ¿Cuántos tomacorrientes necesitas?"

Usuario: "15 tomacorrientes"

PILI: "¡Listo! Ya tengo toda la info.
       ¿Quieres ver la vista previa?"

       [✅ Ver Vista Previa] [➕ Agregar más detalles]
```

### Características de las Respuestas PILI

✅ **BUENAS RESPUESTAS (1-3 líneas)**
```
"¿Qué tipo de instalación necesitas?"
"Perfecto. ¿Cuántos m² tiene el área?"
"Excelente. ¿Cuántos puntos de luz aproximadamente?"
```

❌ **MALAS RESPUESTAS (demasiado largas)**
```
"¡Hola! Soy PILI, tu asistente especializada en cotizaciones
eléctricas. Para generar una cotización precisa para tu instalación
eléctrica residencial de 120m2, necesito la siguiente información
adicional: 1. Distribución de espacios... 2. Puntos de iluminación...
3. Tomacorrientes... 4. Tablero eléctrico... 5. Cableado existente..."
```

---

## 🔌 Endpoints Disponibles

### 1. `/api/chat/chat-contextualizado` ✅ CORRECTO

**Propósito**: Chat inteligente con contexto PILI especializado

**Request**:
```json
{
  "tipo_flujo": "cotizacion-simple",
  "mensaje": "120 m2",
  "historial": [
    {"role": "assistant", "content": "¿Cuántos m² tiene el área?"},
    {"role": "user", "content": "120 m2"}
  ],
  "contexto_adicional": "Instalación residencial",
  "generar_html": true
}
```

**Response**:
```json
{
  "success": true,
  "agente_activo": "PILI Cotizadora",
  "respuesta": "Excelente. ¿Cuántos puntos de luz aproximadamente?",
  "botones_contextuales": ["15-20 puntos", "20-30 puntos", "30+ puntos"],
  "etapa_actual": "refinamiento",
  "html_preview": "<div class='cotizacion'>...</div>",
  "cotizacion_generada": {
    "cliente": "Cliente",
    "items": [
      {
        "descripcion": "Punto luz empotrado",
        "cantidad": 25,
        "precio_unitario": 15.0,
        "subtotal": 375.0
      }
    ],
    "subtotal": 5850.0,
    "igv": 1053.0,
    "total": 6903.0
  }
}
```

### 2. `/api/chat/conversacional` ❌ INCORRECTO

**Problema**: Solo llama a Gemini sin estructura PILI

**Request**:
```json
{
  "mensaje": "Necesito cotizar instalación",
  "contexto": []
}
```

**Response**:
```json
{
  "respuesta": "¡Hola! Soy PILI, tu asistente... [500+ caracteres]",
  "sugerencias": [],
  "accion_recomendada": null
}
```

❌ No tiene:
- Personalidad PILI
- Botones contextuales
- Vista previa HTML
- Datos estructurados JSON
- Detección de servicio

### 3. `/api/chat/botones-contextuales/{tipo_flujo}`

**Propósito**: Obtener botones para la etapa actual

**Request**:
```http
GET /api/chat/botones-contextuales/cotizacion-simple?etapa=inicial
```

**Response**:
```json
{
  "success": true,
  "pili_activa": "PILI Cotizadora",
  "personalidad": "¡Hola! 🤖 Soy PILI Cotizadora...",
  "tipo_flujo": "cotizacion-simple",
  "etapa": "inicial",
  "botones": [
    "🏠 Instalación Residencial",
    "🏢 Instalación Comercial",
    "🏭 Instalación Industrial"
  ]
}
```

---

## 📝 Proceso de Generación Paso a Paso

### Fase 1: Inicialización

```javascript
// Frontend: App.jsx
const iniciarFlujo = (tipoFlujo) => {
  setTipoFlujo(tipoFlujo); // 'cotizacion-simple'
  setPantallaActual('chat');

  // Obtener botones iniciales
  fetch(`/api/chat/botones-contextuales/${tipoFlujo}?etapa=inicial`)
    .then(res => res.json())
    .then(data => {
      setBotonesContextuales(data.botones);
      setConversacion([{
        role: 'assistant',
        content: data.personalidad
      }]);
    });
};
```

### Fase 2: Conversación Iterativa

```javascript
// Frontend: App.jsx
const enviarMensaje = async (mensaje) => {
  // Agregar mensaje del usuario
  const nuevoMensaje = { role: 'user', content: mensaje };
  setConversacion(prev => [...prev, nuevoMensaje]);

  setAnalizando(true);

  try {
    const response = await fetch('/api/chat/chat-contextualizado', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tipo_flujo: tipoFlujo,
        mensaje: mensaje,
        historial: conversacion,
        contexto_adicional: contextoUsuario,
        generar_html: conversacion.length >= 3 // Generar HTML después de 3 mensajes
      })
    });

    const data = await response.json();

    // Agregar respuesta de PILI
    setConversacion(prev => [...prev, {
      role: 'assistant',
      content: data.respuesta
    }]);

    // Actualizar botones
    setBotonesContextuales(data.botones_contextuales);

    // Si generó HTML preview
    if (data.html_preview) {
      setHtmlPreview(data.html_preview);
      setDatosEditables(data.cotizacion_generada);
      setMostrarPreview(true);
    }

  } catch (error) {
    setError('Error al procesar mensaje');
  } finally {
    setAnalizando(false);
  }
};
```

### Fase 3: Vista Previa HTML

```javascript
// Frontend: App.jsx - Renderizado de vista previa
{mostrarPreview && (
  <div className="preview-container">
    <h3>Vista Previa del Documento</h3>

    <div dangerouslySetInnerHTML={{ __html: htmlPreview }} />

    <div className="controles-preview">
      <button onClick={() => setModoEdicion(true)}>
        ✏️ Editar
      </button>
      <button onClick={() => setOcultarIGV(!ocultarIGV)}>
        👁️ {ocultarIGV ? 'Mostrar' : 'Ocultar'} IGV
      </button>
      <button onClick={confirmarGeneracion}>
        ✅ Confirmar y Generar Documento
      </button>
      <button onClick={regenerarDatos}>
        🔄 Regenerar con PILI
      </button>
    </div>
  </div>
)}
```

### Fase 4: Edición de Datos

```javascript
// Frontend: App.jsx - Modo edición
const actualizarDatosEditables = (campo, valor) => {
  setDatosEditables(prev => ({
    ...prev,
    [campo]: valor
  }));
};

const actualizarItem = (index, campo, valor) => {
  setDatosEditables(prev => {
    const nuevosItems = [...prev.items];
    nuevosItems[index] = {
      ...nuevosItems[index],
      [campo]: valor
    };

    // Recalcular totales
    const subtotal = nuevosItems.reduce((sum, item) =>
      sum + (item.cantidad * item.precio_unitario), 0
    );
    const igv = subtotal * 0.18;
    const total = subtotal + igv;

    return {
      ...prev,
      items: nuevosItems,
      subtotal,
      igv,
      total
    };
  });
};
```

### Fase 5: Confirmación y Generación

```javascript
// Frontend: App.jsx - Confirmar generación
const confirmarGeneracion = async () => {
  setAnalizando(true);

  try {
    const response = await fetch('/api/cotizaciones/generar-documento', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tipo_flujo: tipoFlujo,
        datos: datosEditables,
        opciones: {
          mostrarIGV: !ocultarIGV,
          mostrarPreciosUnitarios: !ocultarPreciosUnitarios,
          incluirLogo: true
        }
      })
    });

    const data = await response.json();

    if (data.success) {
      // Mostrar enlace de descarga
      setExito('¡Documento generado exitosamente!');
      setUrlDescarga(data.url_descarga);
      setCotizacion(data.cotizacion);
    }

  } catch (error) {
    setError('Error al generar documento');
  } finally {
    setAnalizando(false);
  }
};
```

### Fase 6: Descarga

```javascript
// Frontend: App.jsx - Descargar documento
const descargarDocumento = async (formato) => {
  setDescargando(formato);

  try {
    const response = await fetch(`/api/cotizaciones/${cotizacion.id}/descargar-${formato}`);
    const blob = await response.blob();

    // Crear enlace de descarga
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${cotizacion.numero}.${formato}`;
    link.click();

    setExito(`Documento ${formato.toUpperCase()} descargado`);

  } catch (error) {
    setError('Error al descargar');
  } finally {
    setDescargando(null);
  }
};
```

---

## 🎨 Componentes Frontend

### App.jsx - Orquestador Principal

**Responsabilidades**:
1. Gestionar estados globales (pantalla, flujo, conversación)
2. Comunicar con backend mediante fetch
3. Renderizar componentes según pantalla actual
4. Gestionar vista previa HTML editable
5. Manejar generación y descarga de documentos

**Estados Clave**:
```javascript
const [pantallaActual, setPantallaActual] = useState('inicio');
const [tipoFlujo, setTipoFlujo] = useState(null);
const [conversacion, setConversacion] = useState([]);
const [htmlPreview, setHtmlPreview] = useState('');
const [datosEditables, setDatosEditables] = useState(null);
const [botonesContextuales, setBotonesContextuales] = useState([]);
const [mostrarPreview, setMostrarPreview] = useState(false);
```

### ChatIA.jsx - Componente de Chat

**Estado Actual (INCORRECTO)**:
```javascript
// ❌ Llama al endpoint básico
const response = await fetch('/api/chat/conversacional', {
  method: 'POST',
  body: JSON.stringify({
    mensaje: inputMensaje,
    contexto: mensajes
  })
});
```

**Debería Ser (CORRECTO)**:
```javascript
// ✅ Llamar al endpoint contextualizado
const response = await fetch('/api/chat/chat-contextualizado', {
  method: 'POST',
  body: JSON.stringify({
    tipo_flujo: props.tipoFlujo,
    mensaje: inputMensaje,
    historial: mensajes,
    contexto_adicional: props.contextoAdicional,
    generar_html: mensajes.length >= 3
  })
});

const data = await response.json();

// Actualizar conversación
setMensajes(prev => [...prev, {
  role: 'assistant',
  content: data.respuesta
}]);

// Actualizar botones (pasar a componente padre)
if (props.onBotonesActualizados) {
  props.onBotonesActualizados(data.botones_contextuales);
}

// Mostrar vista previa si está disponible
if (data.html_preview && props.onPreviewGenerado) {
  props.onPreviewGenerado({
    html: data.html_preview,
    datos: data.cotizacion_generada || data.proyecto_generado
  });
}
```

---

## ⚙️ Componentes Backend

### PILIBrain - Cerebro Inteligente Offline

**Ubicación**: `backend/app/services/pili_brain.py`

**Funciones Clave**:

```python
class PILIBrain:

    def detectar_servicio(self, mensaje: str) -> str:
        """
        Detecta el servicio basándose en keywords

        Ejemplo:
        >>> detectar_servicio("instalación residencial 120m2")
        'electrico-residencial'
        """

    def generar_cotizacion(
        self,
        mensaje: str,
        servicio: str,
        complejidad: str = "simple"
    ) -> dict:
        """
        Genera cotización completa con items calculados

        Returns:
        {
          "success": True,
          "datos": {
            "cliente": "Cliente",
            "proyecto": "Instalación Residencial 120m²",
            "items": [
              {
                "descripcion": "Punto luz empotrado",
                "cantidad": 25,
                "unidad": "und",
                "precio_unitario": 15.0,
                "subtotal": 375.0
              },
              ...
            ],
            "subtotal": 5850.0,
            "igv": 1053.0,
            "total": 6903.0
          }
        }
        """
```

### WordGenerator - Generador de Documentos Word

**Ubicación**: `backend/app/services/word_generator.py`

**Función Principal**:

```python
class WordGenerator:

    def generar_cotizacion(
        self,
        datos: dict,
        ruta_salida: Path,
        opciones: dict = None,
        logo_base64: str = None
    ) -> Path:
        """
        Genera documento Word profesional

        Args:
            datos: {
              "numero": "COT-202511-0001",
              "fecha": "26/11/2025",
              "cliente": "Cliente ABC",
              "proyecto": "Instalación Residencial",
              "items": [...],
              "subtotal": 5850.0,
              "igv": 1053.0,
              "total": 6903.0
            }

            opciones: {
              "mostrarIGV": True,
              "mostrarPreciosUnitarios": True,
              "incluirLogo": True
            }

        Returns:
            Path al archivo generado
        """
```

---

## 🔧 Solución al Problema

### Paso 1: Actualizar ChatIA.jsx

**Archivo**: `frontend/src/components/ChatIA.jsx`

**Cambios Necesarios**:

```javascript
// 1. Agregar props necesarios
const ChatIA = ({
  tipoFlujo,                    // NUEVO
  contextoAdicional,            // NUEVO
  onBotonesActualizados,        // NUEVO
  onPreviewGenerado             // NUEVO
}) => {

  // 2. Modificar función enviarMensaje
  const enviarMensaje = async () => {
    if (!inputMensaje.trim() || cargando) return;

    const nuevoMensaje = {
      role: 'user',
      content: inputMensaje
    };

    setMensajes(prev => [...prev, nuevoMensaje]);
    setInputMensaje('');
    setCargando(true);

    try {
      // ✅ CAMBIAR ENDPOINT
      const response = await fetch('/api/chat/chat-contextualizado', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tipo_flujo: tipoFlujo,                    // NUEVO
          mensaje: inputMensaje,
          historial: mensajes,
          contexto_adicional: contextoAdicional,    // NUEVO
          generar_html: mensajes.length >= 3        // NUEVO
        })
      });

      const data = await response.json();

      // Agregar respuesta de PILI
      setMensajes(prev => [...prev, {
        role: 'assistant',
        content: data.respuesta
      }]);

      // ✅ NUEVO: Actualizar botones contextuales
      if (data.botones_contextuales && onBotonesActualizados) {
        onBotonesActualizados(data.botones_contextuales);
      }

      // ✅ NUEVO: Mostrar vista previa si existe
      if (data.html_preview && onPreviewGenerado) {
        onPreviewGenerado({
          html: data.html_preview,
          datos: data.cotizacion_generada || data.proyecto_generado
        });
      }

    } catch (error) {
      console.error('Error al enviar mensaje:', error);
      setMensajes(prev => [...prev, {
        role: 'assistant',
        content: 'Disculpa, hubo un error. ¿Puedes intentarlo de nuevo?'
      }]);
    } finally {
      setCargando(false);
    }
  };
};
```

### Paso 2: Actualizar App.jsx

**Archivo**: `frontend/src/App.jsx`

**Cambios en el uso de ChatIA**:

```javascript
// En la función donde se renderiza ChatIA
<ChatIA
  tipoFlujo={tipoFlujo}
  contextoAdicional={contextoUsuario}
  onBotonesActualizados={(botones) => {
    setBotonesContextuales(botones);
  }}
  onPreviewGenerado={(preview) => {
    setHtmlPreview(preview.html);
    setDatosEditables(preview.datos);
    setMostrarPreview(true);
  }}
/>
```

### Paso 3: Verificar Endpoints Backend

**Archivo**: `backend/app/routers/chat.py`

**Verificar que existe**:
```python
@router.post("/chat-contextualizado")
async def chat_contextualizado(...):
    # Este endpoint ya existe y funciona
    # Solo necesitamos que el frontend lo use
    pass
```

### Paso 4: Probar el Flujo

1. **Iniciar conversación**:
   ```
   Usuario: "Necesito cotizar instalación eléctrica"
   PILI: "¡Hola! 🤖 ¿Qué tipo de instalación?"
   [Botones: Residencial, Comercial, Industrial]
   ```

2. **Responder preguntas**:
   ```
   Usuario: "Residencial"
   PILI: "Perfecto. ¿Cuántos m²?"

   Usuario: "120 m2"
   PILI: "Excelente. ¿Cuántos puntos de luz?"
   ```

3. **Después de 3+ mensajes**:
   - Backend genera HTML preview automáticamente
   - Frontend muestra vista previa editable
   - Usuario puede editar, confirmar o regenerar

4. **Confirmar y descargar**:
   - Usuario confirma → Backend crea Word
   - Usuario descarga documento final

---

## 📊 Diagrama de Secuencia Completo

```
Usuario          Frontend           Backend            PILIBrain         WordGen
  │                 │                  │                   │                │
  │─Select Flujo──>│                  │                   │                │
  │                 │─Get Botones────>│                   │                │
  │                 │<────Botones─────│                   │                │
  │<─Show Buttons───│                  │                   │                │
  │                 │                  │                   │                │
  │─"120 m2"──────>│                  │                   │                │
  │                 │─Chat Context───>│                   │                │
  │                 │                  │─Detect Service──>│                │
  │                 │                  │<──Service Type───│                │
  │                 │                  │─Generate Data───>│                │
  │                 │                  │<──JSON + Items───│                │
  │                 │<──Response+HTML──│                   │                │
  │<─Show Preview───│                  │                   │                │
  │                 │                  │                   │                │
  │─Edit Data────>│                  │                   │                │
  │─Confirm───────>│                  │                   │                │
  │                 │─Create Doc─────>│                   │                │
  │                 │                  │─Generate Word──────────────────>│
  │                 │                  │<────Word Path──────────────────────│
  │                 │<─Download URL────│                   │                │
  │<─Download Link──│                  │                   │                │
  │                 │                  │                   │                │
  │─Download──────>│─Fetch File─────>│                   │                │
  │<──Word File─────│<────File Blob────│                   │                │
```

---

## ✅ Checklist de Implementación

### Frontend
- [ ] Actualizar `ChatIA.jsx` para usar `/api/chat/chat-contextualizado`
- [ ] Agregar props: `tipoFlujo`, `contextoAdicional`, `onBotonesActualizados`, `onPreviewGenerado`
- [ ] Modificar `enviarMensaje()` para enviar datos correctos
- [ ] Actualizar `App.jsx` para pasar props correctos a ChatIA
- [ ] Implementar renderizado de vista previa HTML
- [ ] Implementar modo edición de datos
- [ ] Agregar botones de confirmación y regeneración

### Backend
- [ ] Verificar que endpoint `/chat-contextualizado` funciona
- [ ] Verificar que PILIBrain genera datos correctamente
- [ ] Verificar generación de HTML preview
- [ ] Verificar WordGenerator crea archivos
- [ ] Agregar endpoint `/cotizaciones/generar-documento` si no existe
- [ ] Agregar endpoint `/cotizaciones/{id}/descargar-word`
- [ ] Agregar endpoint `/cotizaciones/{id}/descargar-pdf`

### Testing
- [ ] Probar flujo completo de cotización simple
- [ ] Probar flujo completo de cotización compleja
- [ ] Probar flujo completo de proyecto
- [ ] Probar flujo completo de informe
- [ ] Verificar que respuestas PILI son cortas (1-3 líneas)
- [ ] Verificar que botones contextuales aparecen
- [ ] Verificar que vista previa HTML se genera
- [ ] Verificar que datos son editables
- [ ] Verificar que Word se descarga correctamente
- [ ] Verificar que PDF se genera desde Word

---

## 🎓 Conclusión

**El problema principal es**:
- Frontend usa endpoint `/chat/conversacional` (básico)
- Debería usar `/chat/chat-contextualizado` (completo con PILI)

**La solución es**:
1. Actualizar `ChatIA.jsx` para usar endpoint correcto
2. Pasar props necesarios desde `App.jsx`
3. Implementar vista previa HTML editable
4. Implementar confirmación y generación de documentos

**Resultado esperado**:
- PILI hace preguntas cortas e inteligentes
- Muestra botones contextuales
- Genera vista previa HTML después de 3+ mensajes
- Usuario puede editar antes de confirmar
- Genera Word/PDF profesional
- Usuario descarga documento final

---

**Versión**: 3.0
**Autor**: Tesla Electricidad y Automatización S.A.C.
**Última actualización**: 2025-11-26
