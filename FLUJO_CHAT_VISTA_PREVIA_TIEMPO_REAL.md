# 🎯 FLUJO CHAT INTELIGENTE + VISTA PREVIA EN TIEMPO REAL

> **La MAGIA de Tesla Cotizador V3.0**
> **Fecha**: 2025-12-30
> **Análisis basado en**: PiliITSEChat.jsx (código existente)

---

## 🌟 EL PLUS DE LA APPWEB (LO QUE LA HACE ÚNICA)

### Concepto:
```
Usuario chatea con PILI →
PILI recopila datos →
Datos se llenan AUTOMÁTICAMENTE en plantilla →
Usuario VE en tiempo real cómo se completa el documento →
Al final: Documento profesional listo para descargar
```

---

## 🔄 FLUJO TÉCNICO COMPLETO

### PASO 1: Usuario inicia conversación

**Frontend** (`PiliITSEChat.jsx`):
```javascript
// Mensaje inicial con BOTONES
addBotMessage(
    "¡Hola! Soy Pili. ¿Qué tipo de establecimiento es?",
    [
        { text: '🏥 Salud', value: 'SALUD' },
        { text: '🏪 Comercio', value: 'COMERCIO' },
        // ... 8 botones
    ]
);
```

**Vista del usuario**:
```
┌─────────────────────────────────────┐
│ PILI                                │
│ ¡Hola! ¿Qué tipo de establecimiento?│
│                                     │
│ [🏥 Salud]  [🏪 Comercio]           │
│ [🏨 Hospedaje]  [🏭 Industrial]      │
│ ...                                 │
└─────────────────────────────────────┘
```

---

### PASO 2: Usuario responde (OPCIÓN A: Botón)

**Frontend**:
```javascript
// Usuario clickea botón "🏪 Comercio"
handleButtonClick('COMERCIO', '🏪 Comercio')

// Agrega mensaje del usuario
addUserMessage('🏪 Comercio')

// Envía al backend
enviarMensajeBackend('COMERCIO')
```

**Request al backend**:
```javascript
POST http://localhost:8000/api/chat/pili-itse

{
  "mensaje": "COMERCIO",
  "conversation_state": {
    "etapa": "inicial",
    "datos": {}
  }
}
```

---

### PASO 3: Backend procesa (Caja Negra Chatbot)

**Backend** (`pili_itse_chatbot.py`):
```python
def procesar(mensaje, estado):
    # Etapa actual
    etapa = estado.get("etapa", "inicial")

    if etapa == "inicial":
        # Usuario seleccionó categoría
        categoria = mensaje  # "COMERCIO"

        # Obtener tipos de la categoría
        tipos = self.knowledge_base["categorias"]["COMERCIO"]["tipos"]
        # ["Tienda", "Supermercado", "Centro Comercial"]

        # Generar botones para siguiente pregunta
        botones = [
            {"text": tipo, "value": tipo}
            for tipo in tipos
        ]

        # Actualizar estado
        nuevo_estado = {
            "etapa": "tipo",
            "datos": {"categoria": "COMERCIO"}
        }

        # Retornar respuesta
        return {
            "success": True,
            "respuesta": "Perfecto, sector Comercio. ¿Qué tipo específico?",
            "botones": botones,
            "state": nuevo_estado,
            "datos_generados": {
                "CATEGORIA": "COMERCIO"  # ← DATO PARA PLANTILLA
            }
        }
```

**Response del backend**:
```json
{
  "success": true,
  "respuesta": "Perfecto, sector Comercio. ¿Qué tipo específico?",
  "botones": [
    {"text": "Tienda", "value": "Tienda"},
    {"text": "Supermercado", "value": "Supermercado"}
  ],
  "state": {
    "etapa": "tipo",
    "datos": {"categoria": "COMERCIO"}
  },
  "datos_generados": {
    "CATEGORIA": "COMERCIO",
    "SERVICIO_NOMBRE": "Certificado ITSE"
  }
}
```

---

### PASO 4: Frontend actualiza chat Y vista previa

**Frontend** (`PiliITSEChat.jsx` línea 114-131):
```javascript
const data = await response.json();

if (data.success) {
    // 1. Actualizar estado de conversación
    setConversationState(data.state);

    // 2. Mostrar nueva pregunta de PILI con botones
    addBotMessage(data.respuesta, data.botones);

    // 3. ⭐ ACTUALIZAR VISTA PREVIA ⭐
    if (data.datos_generados && onDatosGenerados) {
        console.log('📊 Datos generados:', data.datos_generados);
        onDatosGenerados(data.datos_generados);
        // ↑ Esto notifica al componente padre
    }
}
```

---

### PASO 5: App.jsx actualiza plantilla editable

**App.jsx** (lo que DEBE estar implementado):
```javascript
const [datosEditables, setDatosEditables] = useState({});

<PiliITSEChat
    onDatosGenerados={(datos) => {
        // ⭐ ACTUALIZAR DATOS EN TIEMPO REAL ⭐
        setDatosEditables(prev => ({
            ...prev,
            ...datos
        }));
    }}
    onCotizacionGenerada={(cot) => {
        setCotizacion(cot);
    }}
/>

{/* Vista previa */}
<EDITABLE_COTIZACION_SIMPLE
    datos={datosEditables}  // ← Datos actualizados en tiempo real
    onChange={setDatosEditables}
/>
```

---

### PASO 6: Plantilla editable se actualiza automáticamente

**Componente** (`EDITABLE_COTIZACION_SIMPLE.jsx`):
```javascript
const EDITABLE_COTIZACION_SIMPLE = ({ datos, onChange }) => {
    // datos = { CATEGORIA: "COMERCIO", SERVICIO_NOMBRE: "Certificado ITSE" }

    return (
        <div className="documento-preview">
            <h1>{datos.SERVICIO_NOMBRE || "..."}</h1>
            <p>Categoría: {datos.CATEGORIA || "..."}</p>
            <p>Tipo: {datos.TIPO || "..."}</p>
            <p>Área: {datos.AREA || "..."} m²</p>
            <p>Pisos: {datos.PISOS || "..."}</p>

            {/* EDITABLE: Usuario puede modificar */}
            <input
                value={datos.CLIENTE || ""}
                onChange={(e) => onChange({
                    ...datos,
                    CLIENTE: e.target.value
                })}
            />
        </div>
    );
};
```

**Vista del usuario EN TIEMPO REAL**:
```
┌────────────────────────────────────────┐
│ VISTA PREVIA - Certificado ITSE       │
├────────────────────────────────────────┤
│ Servicio: Certificado ITSE             │
│ Categoría: COMERCIO ← Actualizado!     │
│ Tipo: ...                              │
│ Área: ... m²                           │
│ Pisos: ...                             │
└────────────────────────────────────────┘
```

---

## 🎯 INTERACCIÓN DEL USUARIO: HÍBRIDO (Botones + Texto)

### OPCIÓN 1: Botones (Datos estructurados)

**Cuándo se usa**: Preguntas con opciones fijas
- Categoría de establecimiento (8 opciones)
- Tipo específico (variable por categoría)
- Número de pisos (1, 2, 3, 4+)
- Sí/No

**Ventajas**:
- ✅ Rápido para el usuario (1 click)
- ✅ Datos validados automáticamente
- ✅ No hay errores de tipeo

**Ejemplo**:
```
PILI: ¿Cuántos pisos tiene?
[Botones: 1 piso | 2 pisos | 3 pisos | 4+ pisos]

Usuario: *click* "2 pisos"
```

---

### OPCIÓN 2: Texto libre (Datos abiertos)

**Cuándo se usa**: Preguntas que requieren valores específicos
- Área en m² (150, 200.5, etc.)
- Nombre del cliente
- Dirección

**Ventajas**:
- ✅ Flexibilidad para el usuario
- ✅ Cualquier valor numérico
- ✅ Información personalizada

**Ejemplo**:
```
PILI: ¿Cuál es el área en m²?
[Input text: __________]

Usuario: *escribe* "150"
→ Backend valida: OK, es número
→ Actualiza plantilla: AREA = 150
```

---

### OPCIÓN 3: Híbrido (Botones + "Otro/Escribir")

**Cuándo se usa**: Opciones comunes + casos especiales

**Ejemplo**:
```
PILI: ¿En qué municipio?
[Botones: Huancayo | Lima | Arequipa | Otro (escribir)]

Si usuario clickea "Otro":
→ PILI: Escribe el nombre del municipio
→ Usuario escribe texto libre
```

---

## 📊 FLUJO COMPLETO (Ejemplo ITSE)

### Conversación COMPLETA con actualización de plantilla:

```
┌──────────────────────────────┬──────────────────────────────┐
│ CHAT (izquierda)             │ VISTA PREVIA (derecha)       │
├──────────────────────────────┼──────────────────────────────┤
│ PILI: ¿Tipo establecimiento? │ Servicio: Certificado ITSE   │
│ [Salud] [Comercio]...        │ Categoría: ...               │
│                              │ Tipo: ...                    │
│ Usuario: *click* Comercio    │                              │
│                              │ ↓ Actualiza automáticamente  │
│ PILI: ¿Tipo específico?      │ Categoría: COMERCIO ✅       │
│ [Tienda] [Supermercado]      │                              │
│                              │                              │
│ Usuario: *click* Tienda      │ ↓ Actualiza automáticamente  │
│                              │ Tipo: Tienda ✅              │
│ PILI: ¿Área en m²?           │                              │
│ [Input: ______]              │                              │
│                              │                              │
│ Usuario: *escribe* 150       │ ↓ Actualiza automáticamente  │
│                              │ Área: 150 m² ✅              │
│ PILI: ¿Cuántos pisos?        │                              │
│ [1] [2] [3] [4+]             │                              │
│                              │                              │
│ Usuario: *click* 2 pisos     │ ↓ Actualiza automáticamente  │
│                              │ Pisos: 2 ✅                  │
│ PILI: Calculando riesgo...   │                              │
│                              │ ↓ Backend calcula            │
│ PILI: ¡Listo! Nivel MEDIO    │ Nivel Riesgo: MEDIO ✅       │
│ Total: S/ 1,350              │ Total: S/ 1,350 ✅           │
│                              │                              │
│ [Finalizar y Generar DOC] ✅ │ [Documento completo] ✅       │
└──────────────────────────────┴──────────────────────────────┘
```

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### Backend (Caja Negra):

```python
# Pili_ChatBot/pili_itse_chatbot.py

class PILIITSEChatBot:
    def procesar(self, mensaje, estado):
        etapa = estado.get("etapa", "inicial")
        datos = estado.get("datos", {})

        # ETAPA 1: Categoría
        if etapa == "inicial":
            categoria = mensaje
            datos["categoria"] = categoria

            return {
                "respuesta": "¿Qué tipo específico?",
                "botones": self.get_tipos(categoria),
                "state": {"etapa": "tipo", "datos": datos},
                "datos_generados": {
                    "CATEGORIA": categoria,
                    "SERVICIO_NOMBRE": "Certificado ITSE"
                }
            }

        # ETAPA 2: Tipo
        elif etapa == "tipo":
            tipo = mensaje
            datos["tipo"] = tipo

            return {
                "respuesta": "¿Área en m²?",
                "botones": None,  # Input text libre
                "state": {"etapa": "area", "datos": datos},
                "datos_generados": {
                    "TIPO": tipo
                }
            }

        # ETAPA 3: Área
        elif etapa == "area":
            area = float(mensaje)
            datos["area"] = area

            return {
                "respuesta": "¿Cuántos pisos?",
                "botones": [
                    {"text": "1 piso", "value": "1"},
                    {"text": "2 pisos", "value": "2"}
                ],
                "state": {"etapa": "pisos", "datos": datos},
                "datos_generados": {
                    "AREA": area
                }
            }

        # ETAPA 4: Pisos → Generar cotización
        elif etapa == "pisos":
            pisos = int(mensaje)
            datos["pisos"] = pisos

            # CALCULAR RIESGO
            riesgo = self.calcular_riesgo(datos["categoria"], area, pisos)

            # GENERAR COTIZACIÓN COMPLETA
            cotizacion = self.generar_cotizacion(datos, riesgo)

            return {
                "respuesta": f"✅ Nivel {riesgo}\nTotal: S/ {cotizacion['total']}",
                "botones": None,
                "state": {"etapa": "completado", "datos": datos},
                "datos_generados": {
                    "PISOS": pisos,
                    "NIVEL_RIESGO": riesgo,
                    "SUBTOTAL": cotizacion['subtotal'],
                    "IGV": cotizacion['igv'],
                    "TOTAL": cotizacion['total']
                },
                "cotizacion_generada": cotizacion
            }
```

### Frontend (React):

```javascript
// App.jsx

const [datosEditables, setDatosEditables] = useState({
    SERVICIO_NOMBRE: "",
    CATEGORIA: "",
    TIPO: "",
    AREA: "",
    PISOS: "",
    NIVEL_RIESGO: "",
    TOTAL: ""
});

<div className="grid grid-cols-2 gap-4">
    {/* Chat izquierda */}
    <PiliITSEChat
        onDatosGenerados={(nuevosDatos) => {
            // ⭐ Actualizar datos en tiempo real
            setDatosEditables(prev => ({
                ...prev,
                ...nuevosDatos
            }));
            console.log("✅ Plantilla actualizada:", nuevosDatos);
        }}
        onCotizacionGenerada={(cot) => {
            setCotizacion(cot);
        }}
    />

    {/* Vista previa derecha */}
    <EDITABLE_COTIZACION_SIMPLE
        datos={datosEditables}
        onChange={setDatosEditables}
    />
</div>
```

---

## 🎯 RESPUESTA A TU PREGUNTA

> "¿Cómo va a mantener comunicación el chat? ¿Botones, texto, formulario?"

**RESPUESTA**: **HÍBRIDO** (ya implementado en PiliITSEChat.jsx)

### Interacción usuario:

1. **Botones** para opciones fijas (categoría, pisos, sí/no)
2. **Input texto** para valores libres (área, nombre, dirección)
3. **Botones + Texto** mezclados según la pregunta

### Comunicación backend ↔ frontend:

```javascript
// Frontend → Backend
{
  "mensaje": "COMERCIO",
  "conversation_state": {
    "etapa": "categoria",
    "datos": {...}
  }
}

// Backend → Frontend
{
  "respuesta": "¿Tipo específico?",
  "botones": [...],  // Puede ser null (usa input text)
  "state": {...},    // Estado actualizado
  "datos_generados": {...}  // ⭐ ACTUALIZA PLANTILLA ⭐
}
```

### Estado persistente:

- ✅ Frontend mantiene `conversationState`
- ✅ Cada mensaje lleva el estado
- ✅ Backend retorna nuevo estado
- ✅ Frontend actualiza estado local
- ✅ **Sin archivos, todo en memoria**

---

## ✅ CONCLUSIÓN

**Tu AppWeb YA tiene la arquitectura correcta**:

```
Chat (botones/texto) →
Backend (caja negra) →
Datos generados →
Plantilla actualizada EN TIEMPO REAL →
Usuario ve documento completándose →
Finalizar → Descargar Word/PDF
```

**Solo falta**:
1. ✅ Conectar `onDatosGenerados` en App.jsx
2. ✅ Integrar chatbot ITSE con backend
3. ✅ Replicar patrón a 9 servicios más

---

**FIN DEL DOCUMENTO**

