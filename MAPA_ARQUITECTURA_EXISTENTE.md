# 🗺️ MAPA COMPLETO DE LA ARQUITECTURA EXISTENTE

**Fecha**: 2025-12-03
**Análisis**: Sistema Tesla Cotizador V3.0 - Estado Actual
**Propósito**: Entender qué YA EXISTE antes de hacer cambios

---

## 📊 RESUMEN EJECUTIVO

### Lo que REALMENTE tenemos:

```
┌─────────────────────────────────────────────────────────────┐
│                  TESLA COTIZADOR V3.0                       │
│                   ARQUITECTURA ACTUAL                        │
└─────────────────────────────────────────────────────────────┘

FRONTEND (App.jsx):
- 6 TIPOS DE DOCUMENTOS definidos
- 8 SERVICIOS mostrados en UI
- 8 INDUSTRIAS definidas

BACKEND (pili_brain.py):
- 10 SERVICIOS completos implementados
- 3 MÉTODOS de generación (cotización, proyecto, informe)

BACKEND (chat.py):
- Endpoints para chat contextualizado
- Vista previa HTML editable
- Integración con PILI
```

---

## 🎯 LOS 6 TIPOS DE DOCUMENTOS (Frontend App.jsx)

**Ubicación**: `frontend/src/App.jsx` líneas 936-941

### Categoría 1: COTIZACIONES

| # | Tipo | ID en código | Descripción | Tiempo |
|---|------|-------------|-------------|--------|
| 1 | **Cotización Simple** | `cotizacion-simple` | Vista previa en tiempo real | 5-15 min |
| 2 | **Cotización Compleja** | `cotizacion-compleja` | Análisis detallado con edición avanzada | 20-45 min |

**Código Frontend (líneas 798-820)**:
```javascript
<button onClick={() => iniciarFlujo('cotizacion-simple')}>
  Cotización Simple
</button>

<button onClick={() => iniciarFlujo('cotizacion-compleja')}>
  Cotización Compleja
</button>
```

### Categoría 2: PROYECTOS

| # | Tipo | ID en código | Descripción | Características |
|---|------|-------------|-------------|-----------------|
| 3 | **Proyecto Simple** | `proyecto-simple` | Gestión básica con vista previa | Sin Gantt |
| 4 | **Proyecto Complejo** | `proyecto-complejo` | Gantt, hitos y seguimiento avanzado | Con cronograma |

**Código Frontend (líneas 844-866)**:
```javascript
<button onClick={() => iniciarFlujo('proyecto-simple')}>
  Proyecto Simple
</button>

<button onClick={() => iniciarFlujo('proyecto-complejo')}>
  Proyecto Complejo
</button>
```

### Categoría 3: INFORMES

| # | Tipo | ID en código | Descripción | Formato |
|---|------|-------------|-------------|---------|
| 5 | **Informe Simple** | `informe-simple` | PDF básico con vista previa editable | PDF |
| 6 | **Informe Ejecutivo** | `informe-ejecutivo` | Word APA, tablas y gráficos automáticos | Word (APA) |

**Código Frontend (líneas 890-915)**:
```javascript
<button onClick={() => iniciarFlujo('informe-simple')}>
  Informe Simple
</button>

<button onClick={() => iniciarFlujo('informe-ejecutivo')}>
  Informe Ejecutivo
</button>
```

---

## ⚙️ LOS 10 SERVICIOS (Backend pili_brain.py)

**Ubicación**: `backend/app/services/pili_brain.py` líneas 38-117

### Tabla Completa de Servicios

| # | ID Backend | Nombre | Keywords | Normativa | En Frontend |
|---|-----------|---------|----------|-----------|-------------|
| 1 | `electrico-residencial` | Instalaciones Eléctricas Residenciales | residencial, casa, vivienda | CNE Suministro 2011 | ✅ (como "electricidad") |
| 2 | `electrico-comercial` | Instalaciones Eléctricas Comerciales | comercial, tienda, oficina | CNE Suministro 2011 | ✅ (como "electricidad") |
| 3 | `electrico-industrial` | Instalaciones Eléctricas Industriales | industrial, fábrica, planta | CNE 2011 + Utilización | ✅ (como "electricidad") |
| 4 | `contraincendios` | Sistemas Contra Incendios | contraincendios, sprinkler | NFPA 13, 72, 20 | ✅ |
| 5 | `domotica` | Domótica y Automatización | domótica, smart, knx, iot | KNX/EIB, Z-Wave | ✅ |
| 6 | **`expedientes`** | Expedientes Técnicos de Edificación | expediente, licencia | RNE, Municipal | ❌ **FALTA** |
| 7 | **`saneamiento`** | Sistemas de Agua y Desagüe | saneamiento, agua, desagüe | RNE IS.010, IS.020 | ❌ **FALTA** |
| 8 | `itse` | Certificaciones ITSE | itse, certificación, seguridad | D.S. 002-2018-PCM | ✅ |
| 9 | `pozo-tierra` | Sistemas de Puesta a Tierra | pozo, tierra, aterramiento | CNE Sección 250 | ✅ (como "puesta-tierra") |
| 10 | `redes-cctv` | Redes y CCTV | red, cctv, cámara, ethernet | TIA/EIA-568 | ✅ (separado: "redes" y "cctv") |

### ⚠️ DISCREPANCIA DETECTADA

El backend tiene **10 servicios**, pero el frontend solo muestra **8**:

**FALTAN EN FRONTEND:**
- ❌ Expedientes Técnicos de Edificación
- ❌ Sistemas de Agua y Desagüe (Saneamiento)

**SERVICIOS QUE SE DIVIDEN:**
- Backend: `redes-cctv` (1 servicio)
- Frontend: `redes` + `cctv` (2 servicios separados)

---

## 🔄 LOS 3 MÉTODOS DE GENERACIÓN (Backend pili_brain.py)

**Ubicación**: `backend/app/services/pili_brain.py`

### 1. generar_cotizacion() - Línea 318

```python
def generar_cotizacion(
    self,
    mensaje: str,
    servicio: str,
    complejidad: str = "simple"  # "simple" o "compleja"
) -> Dict[str, Any]:
    """
    Genera una cotización completa con cálculos realistas

    Returns:
        {
            "accion": "cotizacion_generada",
            "datos": {
                "numero": "COT-20251203-001",
                "cliente": "...",
                "items": [...],
                "subtotal": 2500.00,
                "igv": 450.00,
                "total": 2950.00
            },
            "conversacion": {
                "mensaje_pili": "...",
                "preguntas_pendientes": [...]
            }
        }
    """
```

**Usado para:**
- ✅ Tipo 1: Cotización Simple (complejidad="simple")
- ✅ Tipo 2: Cotización Compleja (complejidad="compleja")

### 2. generar_proyecto() - Línea 878

```python
def generar_proyecto(
    self,
    mensaje: str,
    servicio: str,
    complejidad: str = "simple"  # "simple" o "complejo"
) -> Dict[str, Any]:
    """
    Genera un proyecto completo con cronograma, fases y recursos

    Returns:
        {
            "accion": "proyecto_generado",
            "datos": {
                "numero": "PROY-20251203-001",
                "cliente": "...",
                "fases": [...],
                "cronograma": [...],
                "recursos": {...},
                "presupuesto": 45000.00
            },
            "conversacion": {
                "mensaje_pili": "...",
                "preguntas_pendientes": [...]
            }
        }
    """
```

**Usado para:**
- ✅ Tipo 3: Proyecto Simple (complejidad="simple")
- ✅ Tipo 4: Proyecto Complejo (complejidad="complejo")

### 3. generar_informe() - Línea 1272

```python
def generar_informe(
    self,
    mensaje: str,
    servicio: str,
    complejidad: str = "simple",  # "simple" o "compleja"
    proyecto_base: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Genera un informe técnico o ejecutivo

    Returns:
        {
            "accion": "informe_generado",
            "datos": {
                "numero": "INF-20251203-001",
                "titulo": "...",
                "resumen_ejecutivo": "...",
                "desarrollo": [...],
                "conclusiones": [...],
                "recomendaciones": [...]
            },
            "conversacion": {
                "mensaje_pili": "...",
                "preguntas_pendientes": [...]
            }
        }
    """
```

**Usado para:**
- ✅ Tipo 5: Informe Simple (complejidad="simple")
- ✅ Tipo 6: Informe Ejecutivo (complejidad="compleja")

---

## 🔌 ENDPOINTS DEL BACKEND (chat.py)

**Ubicación**: `backend/app/routers/chat.py`

### Endpoint Principal: `/chat-contextualizado` (Línea 1277)

```python
@router.post("/chat-contextualizado")
async def chat_contextualizado(
    tipo_flujo: str = Body(...),  # ej: "cotizacion-simple", "proyecto-complejo"
    mensaje: str = Body(...),
    historial: Optional[List[Dict]] = Body([]),
    contexto_adicional: Optional[str] = Body(""),
    cotizacion_id: Optional[int] = Body(None),
    archivos_procesados: Optional[List[Dict]] = Body([]),
    generar_html: Optional[bool] = Body(False),
    db: Session = Depends(get_db)
)
```

**¿Qué hace?**
1. Recibe el `tipo_flujo` (uno de los 6 tipos)
2. Llama a PILIBrain para generar estructura según el tipo
3. Retorna los campos específicos:
   - `cotizacion_generada` si tipo_flujo contiene "cotizacion"
   - `proyecto_generado` si tipo_flujo contiene "proyecto"
   - `informe_generado` si tipo_flujo contiene "informe"

### Otros Endpoints Importantes

| Endpoint | Método | Propósito |
|----------|--------|-----------|
| `/iniciar-flujo-inteligente` | POST | Inicia conversación con PILI |
| `/botones-contextuales/{tipo_flujo}` | GET | Obtiene botones inteligentes |
| `/generar-documento-directo` | POST | Genera doc sin guardar en BD |

---

## 🔄 FLUJO COMPLETO DE GENERACIÓN

### Flujo Actual (Lo que YA EXISTE)

```
1. USUARIO EN FRONTEND
   ↓
   Usuario hace clic en uno de los 6 botones
   Ejemplo: "Cotización Simple"
   ↓

2. FUNCIÓN iniciarFlujo() (App.jsx línea 154)
   ↓
   setTipoFlujo('cotizacion-simple')
   setPantallaActual('flujo-pasos')
   ↓

3. USUARIO CHATEA CON PILI
   ↓
   handleEnviarMensajeChat() (App.jsx línea 183)
   ↓
   POST a http://localhost:8000/api/chat/chat-contextualizado
   Body: {
     tipo_flujo: "cotizacion-simple",
     mensaje: "Necesito instalación eléctrica para oficina 100m2",
     generar_html: true
   }
   ↓

4. BACKEND PROCESA (chat.py línea 1338)
   ↓
   Detecta que tipo_flujo contiene "cotizacion"
   ↓
   servicio_detectado = pili_brain.detectar_servicio(mensaje)
   // Retorna: "electrico-comercial"
   ↓
   complejidad = "simple"  // porque es "cotizacion-simple"
   ↓
   documento_data = pili_brain.generar_cotizacion(
     mensaje,
     "electrico-comercial",
     "simple"
   )
   ↓
   datos_generados = documento_data['datos']
   html_preview = generar_preview_html_editable(datos_generados)
   ↓

5. BACKEND RETORNA RESPUESTA
   ↓
   {
     "success": true,
     "cotizacion_generada": {
       "numero": "COT-20251203-001",
       "cliente": "Cliente Demo",
       "items": [...],
       "total": 2950.00
     },
     "html_preview": "<html>...</html>",
     "respuesta": "He generado una cotización..."
   }
   ↓

6. FRONTEND RECIBE RESPUESTA (App.jsx línea 229)
   ↓
   if (data.cotizacion_generada) {
     setCotizacion(data.cotizacion_generada)
     setDatosEditables(data.cotizacion_generada)
   }
   ↓
   setHtmlPreview(data.html_preview)
   setMostrarPreview(true)
   ↓

7. USUARIO VE VISTA PREVIA HTML
   ↓
   Puede editar datos
   ↓

8. USUARIO HACE CLIC "DESCARGAR WORD"
   ↓
   handleDescargar() (App.jsx línea 530)
   ↓
   Usa datosEditables para generar documento
   ↓
   Llama a /api/generar-documento-directo
   ↓
   ✅ DOCUMENTO WORD DESCARGADO
```

---

## 📁 ESTRUCTURA DE DATOS POR TIPO

### Tipo 1 y 2: COTIZACIONES

```json
{
  "numero": "COT-20251203-001",
  "cliente": "Empresa ABC S.A.C.",
  "proyecto": "Instalación Eléctrica Comercial",
  "fecha": "03/12/2025",
  "vigencia": "30 días calendario",
  "items": [
    {
      "descripcion": "Punto de luz LED 18W empotrado",
      "cantidad": 12,
      "unidad": "pto",
      "precio_unitario": 30.00,
      "total": 360.00
    },
    {
      "descripcion": "Tomacorriente doble polarizado",
      "cantidad": 8,
      "unidad": "pto",
      "precio_unitario": 35.00,
      "total": 280.00
    }
  ],
  "subtotal": 2500.00,
  "igv": 450.00,
  "total": 2950.00,
  "observaciones": [
    "Incluye materiales y mano de obra",
    "Garantía de 12 meses"
  ],
  "normativa_aplicable": "CNE Suministro 2011"
}
```

### Tipo 3 y 4: PROYECTOS

```json
{
  "numero": "PROY-20251203-001",
  "cliente": "Industria XYZ S.A.",
  "nombre": "Automatización Industrial con PLC",
  "descripcion": "...",
  "fases": [
    {
      "numero": 1,
      "nombre": "Planificación",
      "duracion_dias": 15,
      "hitos": [
        "Levantamiento de información",
        "Diseño preliminar"
      ]
    },
    {
      "numero": 2,
      "nombre": "Implementación",
      "duracion_dias": 45,
      "hitos": [
        "Instalación de equipos",
        "Programación de PLC"
      ]
    }
  ],
  "cronograma": [
    {
      "actividad": "Instalación tableros",
      "inicio": "2025-12-10",
      "fin": "2025-12-15",
      "responsable": "Ing. Juan Pérez"
    }
  ],
  "recursos": {
    "personal": [
      {"rol": "Ingeniero Eléctrico", "cantidad": 2},
      {"rol": "Técnico", "cantidad": 4}
    ],
    "equipos": [
      {"nombre": "PLC Siemens S7-1200", "cantidad": 2}
    ],
    "materiales": [
      {"nombre": "Cable THW 12 AWG", "cantidad": "500m"}
    ]
  },
  "presupuesto": 45000.00
}
```

### Tipo 5 y 6: INFORMES

```json
{
  "numero": "INF-20251203-001",
  "titulo": "Informe Técnico de Instalación Eléctrica",
  "tipo": "tecnico",  // o "ejecutivo"
  "fecha": "03/12/2025",
  "cliente": "Empresa ABC",
  "resumen_ejecutivo": "...",
  "desarrollo": [
    {
      "seccion": "1. Introducción",
      "contenido": "..."
    },
    {
      "seccion": "2. Alcance del Proyecto",
      "contenido": "..."
    },
    {
      "seccion": "3. Metodología",
      "contenido": "..."
    }
  ],
  "conclusiones": [
    "Conclusión 1...",
    "Conclusión 2..."
  ],
  "recomendaciones": [
    "Recomendación 1...",
    "Recomendación 2..."
  ],
  "anexos": [
    {"nombre": "Anexo A: Planos", "descripcion": "..."}
  ]
}
```

---

## 🎨 ESTADOS DEL FRONTEND (App.jsx)

**Ubicación**: `frontend/src/App.jsx` líneas 8-60

### Estados Principales

```javascript
// NAVEGACIÓN
const [pantallaActual, setPantallaActual] = useState('inicio');
  // Valores: 'inicio', 'flujo-pasos'

const [tipoFlujo, setTipoFlujo] = useState(null);
  // Valores: 'cotizacion-simple', 'cotizacion-compleja',
  //          'proyecto-simple', 'proyecto-complejo',
  //          'informe-simple', 'informe-ejecutivo'

// MENÚS EXPANDIBLES
const [menuCotizaciones, setMenuCotizaciones] = useState(false);
const [menuProyectos, setMenuProyectos] = useState(false);
const [menuInformes, setMenuInformes] = useState(false);

// CONVERSACIÓN
const [conversacion, setConversacion] = useState([]);
const [inputChat, setInputChat] = useState('');
const [analizando, setAnalizando] = useState(false);

// VISTA PREVIA
const [htmlPreview, setHtmlPreview] = useState('');
const [mostrarPreview, setMostrarPreview] = useState(false);
const [datosEditables, setDatosEditables] = useState(null);  // ← CRÍTICO

// DATOS POR TIPO
const [cotizacion, setCotizacion] = useState(null);
const [proyecto, setProyecto] = useState(null);
const [informe, setInforme] = useState(null);
```

---

## ✅ LO QUE FUNCIONA ACTUALMENTE

```
✅ Frontend muestra los 6 tipos de documentos
✅ Botones de inicio funcionan (iniciarFlujo)
✅ Chat con PILI está integrado
✅ Backend tiene 10 servicios completos
✅ PILIBrain tiene 3 métodos de generación
✅ Endpoint /chat-contextualizado existe
✅ Vista previa HTML se genera
✅ Estados de React están definidos
✅ Colores institucionales rojos aplicados
```

---

## ❌ PROBLEMAS DETECTADOS

### 1. Discrepancia de Servicios

**Problema**: Backend tiene 10 servicios, frontend muestra solo 8

**Servicios faltantes en frontend:**
- Expedientes Técnicos de Edificación
- Sistemas de Agua y Desagüe (Saneamiento)

### 2. División de Servicios

**Problema**: Backend tiene `redes-cctv` como 1 servicio, frontend los separa en 2

**Backend**: `redes-cctv`
**Frontend**: `redes` + `cctv`

---

## 🎯 CONCLUSIONES

### Lo que YA TENEMOS y FUNCIONA:

1. ✅ **6 tipos de documentos** bien definidos en frontend
2. ✅ **10 servicios** completos en backend
3. ✅ **3 métodos** de generación en PILIBrain (cotización, proyecto, informe)
4. ✅ **Endpoint principal** `/chat-contextualizado` implementado
5. ✅ **Vista previa HTML** editable con colores institucionales
6. ✅ **Estados de React** correctamente estructurados
7. ✅ **Flujo completo** desde inicio hasta descarga

### Lo que NECESITA AJUSTARSE:

1. ⚠️ Sincronizar servicios entre frontend (8) y backend (10)
2. ⚠️ Decidir si `redes-cctv` debe ser 1 o 2 servicios
3. ⚠️ Verificar que los 6 tipos llamen al método PILIBrain correcto

---

**FIN DEL MAPA**

_Este documento NO agrega código nuevo, solo documenta lo que YA EXISTE_
_Última actualización: 2025-12-03 17:30 UTC_
