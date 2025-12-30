# 🎯 ANÁLISIS COMPLETO - MATRIZ SERVICIOS × DOCUMENTOS

**Fecha**: 30 de Diciembre 2025
**Estado**: 📋 ANÁLISIS - NO escribir código hasta validar
**Objetivo**: Diseñar flujos conversacionales alineados con plantillas REALES

---

## ⚠️ PROBLEMA IDENTIFICADO POR EL USUARIO

**El chat ITSE actual pregunta datos genéricos** que NO están alineados con lo que las plantillas realmente necesitan.

**Ejemplo**:
- ITSE pregunta: "categoría, tipo, área, pisos"
- Pero plantillas necesitan: "cliente, proyecto, servicio, normativa, presupuesto, fechas, etc."

**Resultado**: Datos recopilados ≠ Datos necesarios para rellenar plantillas

---

## 📊 ANÁLISIS DE LAS 6 PLANTILLAS

### Campos Identificados por Plantilla:

#### 1️⃣ **Cotización Simple** (`PLANTILLA_HTML_COTIZACION_SIMPLE.html`)

**Campos obligatorios**:
- `NUMERO_COTIZACION` - Número de cotización
- `CLIENTE_NOMBRE` - Nombre del cliente
- `PROYECTO_NOMBRE` - Nombre del proyecto
- `AREA_M2` - Área en metros cuadrados
- `FECHA_COTIZACION` - Fecha de emisión
- `VIGENCIA` - Vigencia de la cotización (ej: "30 días")
- `SERVICIO_NOMBRE` - Nombre del servicio (ITSE, Electricidad, etc.)
- `DESCRIPCION_PROYECTO` - Descripción breve del proyecto
- `NORMATIVA_APLICABLE` - Normativa técnica (ej: "CNE 2011")
- `SUBTOTAL` - Subtotal sin IGV
- `IGV` - Impuesto General a las Ventas (18%)
- `TOTAL` - Total con IGV

**Items de cotización** (tabla dinámica):
- Cada item tiene: descripción, cantidad, unidad, precio unitario, total

**Total de campos**: **12 campos básicos** + items

---

#### 2️⃣ **Cotización Compleja** (`PLANTILLA_HTML_COTIZACION_COMPLEJA.html`)

**Campos obligatorios** (incluye todos de Cotización Simple +):
- `DIAS_INGENIERIA` - Días de ingeniería
- `DIAS_ADQUISICIONES` - Días de adquisiciones
- `DIAS_INSTALACION` - Días de instalación
- `DIAS_PRUEBAS` - Días de pruebas y puesta en marcha

**Secciones adicionales**:
- Alcance del servicio (más detallado)
- Cronograma por fases
- Exclusiones
- Garantías

**Total de campos**: **16 campos básicos** + items

---

#### 3️⃣ **Proyecto Simple** (`PLANTILLA_HTML_PROYECTO_SIMPLE.html`)

**Campos obligatorios**:
- `NOMBRE_PROYECTO` - Nombre del proyecto
- `CODIGO_PROYECTO` - Código único (ej: "PROY-2025-001")
- `CLIENTE` - Nombre del cliente
- `DURACION_TOTAL` - Duración total en días
- `FECHA_INICIO` - Fecha de inicio
- `FECHA_FIN` - Fecha de fin
- `PRESUPUESTO` - Presupuesto total
- `ALCANCE_PROYECTO` - Alcance del proyecto
- `DIAS_INGENIERIA` - Días fase ingeniería
- `DIAS_EJECUCION` - Días fase ejecución
- `NORMATIVA_APLICABLE` - Normativa técnica

**Total de campos**: **11 campos**

---

#### 4️⃣ **Proyecto Complejo PMI** (`PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html`)

**Campos obligatorios** (incluye todos de Proyecto Simple +):
- `SPI` - Schedule Performance Index
- `CPI` - Cost Performance Index
- `EV_K` - Earned Value (en miles)
- `PV_K` - Planned Value (en miles)
- `AC_K` - Actual Cost (en miles)

**Secciones adicionales**:
- KPIs PMI
- Diagrama de Gantt
- Gestión de stakeholders
- Análisis de riesgos

**Total de campos**: **16 campos** + KPIs PMI

---

#### 5️⃣ **Informe Técnico** (`PLANTILLA_HTML_INFORME_TECNICO.html`)

**Campos obligatorios**:
- `TITULO_INFORME` - Título del informe
- `CODIGO_INFORME` - Código del informe (ej: "INF-TEC-2025-001")
- `CLIENTE` - Nombre del cliente
- `FECHA` - Fecha del informe
- `RESUMEN_EJECUTIVO` - Resumen ejecutivo (texto largo)
- `SERVICIO_NOMBRE` - Servicio técnico
- `NORMATIVA_APLICABLE` - Normativa aplicable

**Total de campos**: **7 campos**

---

#### 6️⃣ **Informe Ejecutivo APA** (`PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html`)

**Campos obligatorios**:
- `TITULO_PROYECTO` - Título del proyecto
- `CLIENTE` - Nombre del cliente
- `FECHA` - Fecha
- `CODIGO_INFORME` - Código del informe
- `RESUMEN_EJECUTIVO` - Resumen ejecutivo
- `PRESUPUESTO` - Presupuesto total
- `ROI_ESTIMADO` - ROI estimado (%)
- `PAYBACK_MESES` - Período de retorno (meses)
- `TIR_PROYECTADA` - TIR proyectada (%)
- `AHORRO_ANUAL_K` - Ahorro anual en miles
- `AHORRO_ENERGETICO` - Ahorro energético
- `INVERSION_EQUIPOS` - Inversión en equipos
- `INVERSION_MANO_OBRA` - Inversión en mano de obra
- `CAPITAL_TRABAJO` - Capital de trabajo
- `SERVICIO_NOMBRE` - Servicio
- `NORMATIVA_APLICABLE` - Normativa

**Total de campos**: **16 campos** + análisis financiero

---

## 📋 CAMPOS COMUNES vs ESPECÍFICOS

### Campos COMUNES (aparecen en casi todas las plantillas):

| Campo | Aparece en | Obligatorio |
|-------|-----------|-------------|
| `CLIENTE` o `CLIENTE_NOMBRE` | 6/6 plantillas | ✅ SÍ |
| `FECHA` o `FECHA_COTIZACION` | 6/6 plantillas | ✅ SÍ |
| `SERVICIO_NOMBRE` | 6/6 plantillas | ✅ SÍ |
| `NORMATIVA_APLICABLE` | 6/6 plantillas | ✅ SÍ |
| `PRESUPUESTO` o `TOTAL` | 5/6 plantillas | ✅ SÍ |
| `PROYECTO_NOMBRE` o `NOMBRE_PROYECTO` | 4/6 plantillas | ⚠️ Según tipo |
| `CODIGO_PROYECTO` o `CODIGO_INFORME` | 4/6 plantillas | ⚠️ Según tipo |

### Campos ESPECÍFICOS por Tipo de Documento:

| Tipo Documento | Campos Específicos |
|----------------|-------------------|
| **Cotizaciones** | NUMERO_COTIZACION, VIGENCIA, AREA_M2, items (tabla), SUBTOTAL, IGV |
| **Cotización Compleja** | + DIAS_INGENIERIA, DIAS_ADQUISICIONES, DIAS_INSTALACION, DIAS_PRUEBAS |
| **Proyectos** | CODIGO_PROYECTO, DURACION_TOTAL, FECHA_INICIO, FECHA_FIN, ALCANCE_PROYECTO |
| **Proyecto PMI** | + SPI, CPI, EV_K, PV_K, AC_K (métricas PMI) |
| **Informes** | CODIGO_INFORME, TITULO_INFORME, RESUMEN_EJECUTIVO |
| **Informe Ejecutivo APA** | + ROI_ESTIMADO, PAYBACK_MESES, TIR_PROYECTADA, AHORRO_ANUAL_K, métricas financieras |

---

## 🎯 MATRIZ: 10 SERVICIOS × 6 DOCUMENTOS

### Propuesta de "Pesos" (Complejidad/Frecuencia):

| Servicio | Cot. Simple | Cot. Compleja | Proy. Simple | Proy. PMI | Inf. Técnico | Inf. Ejecutivo APA | **Complejidad Total** |
|----------|:-----------:|:-------------:|:------------:|:---------:|:------------:|:------------------:|:---------------------:|
| **1. ITSE** | ✅ Alta | ⚠️ Baja | ✅ Media | ❌ No aplica | ✅ Media | ❌ No aplica | **Simple** |
| **2. Instalaciones Eléctricas** | ✅ Alta | ✅ Alta | ✅ Alta | ✅ Media | ✅ Alta | ✅ Media | **Muy Complejo** |
| **3. Pozo a Tierra** | ✅ Alta | ✅ Media | ⚠️ Baja | ❌ No aplica | ✅ Alta | ⚠️ Baja | **Medio** |
| **4. Contraincendios** | ✅ Alta | ✅ Alta | ✅ Alta | ✅ Media | ✅ Alta | ✅ Media | **Muy Complejo** |
| **5. Domótica** | ✅ Alta | ✅ Alta | ✅ Media | ✅ Media | ✅ Media | ✅ Alta | **Muy Complejo** |
| **6. CCTV** | ✅ Alta | ✅ Media | ✅ Media | ⚠️ Baja | ✅ Media | ⚠️ Baja | **Medio** |
| **7. Redes de Datos** | ✅ Alta | ✅ Media | ✅ Media | ⚠️ Baja | ✅ Alta | ⚠️ Baja | **Medio** |
| **8. Automatización Industrial** | ✅ Alta | ✅ Alta | ✅ Alta | ✅ Alta | ✅ Alta | ✅ Alta | **Muy Complejo** |
| **9. Expedientes Técnicos** | ⚠️ Baja | ⚠️ Baja | ✅ Alta | ✅ Alta | ✅ Alta | ✅ Alta | **Complejo** |
| **10. Saneamiento** | ✅ Alta | ✅ Media | ✅ Media | ⚠️ Baja | ✅ Alta | ⚠️ Baja | **Medio** |

**Leyenda**:
- ✅ **Alta**: Muy frecuente, necesario
- ✅ **Media**: Frecuente
- ⚠️ **Baja**: Poco frecuente
- ❌ **No aplica**: No se usa

---

## 🔍 ANÁLISIS DE DATOS POR SERVICIO

### **Servicio #1: ITSE** (SIMPLE)

**Datos específicos que debe preguntar el chat**:

**Para Cotización Simple**:
1. ✅ Cliente (nombre/empresa)
2. ✅ Proyecto (tipo establecimiento) ← Ya lo pregunta
3. ✅ Categoría (Salud, Comercio, etc.) ← Ya lo pregunta
4. ✅ Tipo específico (Hospital, Tienda, etc.) ← Ya lo pregunta
5. ✅ Área en m² ← Ya lo pregunta
6. ✅ Número de pisos ← Ya lo pregunta
7. ❌ **FALTA**: Vigencia de cotización
8. ❌ **FALTA**: Normativa aplicable (autocompletar: "D.S. 002-2018-PCM")

**Para Proyecto Simple**:
1. ✅ Datos anteriores +
2. ❌ **FALTA**: Fecha inicio deseada
3. ❌ **FALTA**: Duración esperada (calcular automático: 7 días TUPA + trabajo)
4. ❌ **FALTA**: Alcance del proyecto (generar con IA)

**Para Informe Técnico**:
1. ✅ Datos anteriores +
2. ❌ **FALTA**: Código de informe (generar automático)
3. ❌ **FALTA**: Resumen ejecutivo (generar con IA)

**CONCLUSIÓN ITSE**:
El chat actual recoge **6/12 campos** necesarios. Faltan:
- Cliente (nombre completo)
- Vigencia
- Normativa (autocompletar)
- Fechas (calcular)
- Códigos (autogenerar)
- Textos largos (generar con IA)

---

### **Servicio #2: Instalaciones Eléctricas** (MUY COMPLEJO)

**Datos específicos que debe preguntar**:

**Base común**:
1. Cliente
2. Proyecto (nombre descriptivo)
3. Tipo de instalación:
   - **Residencial** (casa, departamento)
   - **Comercial** (oficinas, tiendas)
   - **Industrial** (fábricas, plantas)

**Datos técnicos específicos**:
4. Potencia requerida (kW)
5. Número de circuitos
6. Tipo de tablero (monofásico, trifásico)
7. Área de instalación (m²)
8. Número de pisos
9. Tipo de acabado (empotrado, superficial)

**Para Cotización Compleja** (+ 4 fases):
- Días de ingeniería (calcular según potencia)
- Días de adquisiciones (calcular)
- Días de instalación (calcular según área)
- Días de pruebas (fijo: 2-3 días)

**Para Proyecto PMI** (+ KPIs):
- SPI, CPI (calcular automático)
- EV, PV, AC (calcular según avance)

**Normativa**: CNE 2011 (Código Nacional de Electricidad)

---

### **Servicio #3: Pozo a Tierra** (MEDIO)

**Datos específicos**:
1. Cliente
2. Proyecto
3. Tipo de sistema:
   - **Simple** (residencial < 25 Ohms)
   - **Complejo** (industrial, datacenters < 10 Ohms)
4. Resistividad del suelo (Ohm·m)
5. Resistencia objetivo (Ohms)
6. Área disponible (m²)
7. Tipo de electrodo (copperwell, acero)

**Normativa**: CNE 2011 - Sección 5: Puesta a Tierra

---

## 🎯 PROPUESTA DE PLAN DE ACCIÓN

### FASE 0: Análisis y Validación (ACTUAL - NO ESCRIBIR CÓDIGO)

**Tareas**:
1. ✅ Identificar campos de las 6 plantillas
2. ✅ Crear matriz 10 servicios × 6 documentos
3. 📋 **PENDIENTE**: Validar con usuario:
   - ¿La matriz de "pesos" es correcta?
   - ¿Qué servicios priorizamos primero?
   - ¿Tenemos los datos técnicos (normativas, fórmulas)?

---

### FASE 1: Rediseñar Chat ITSE (PRIMERO)

**Objetivo**: Alinear chat ITSE con plantillas reales

**Preguntas que DEBE hacer el chat** (orden):
1. **Datos del cliente**:
   - ¿Cuál es el nombre del cliente? (empresa/persona)
   - ¿Cuál es el nombre del proyecto? (ej: "Local comercial Av. Huancavelica")

2. **Datos técnicos** (ya los tiene):
   - Categoría de establecimiento
   - Tipo específico
   - Área en m²
   - Número de pisos

3. **Datos de cotización**:
   - ¿Vigencia de cotización? (default: 30 días)
   - Normativa (autocompletar: "D.S. 002-2018-PCM")

4. **Tipo de documento a generar**:
   - Mostrar botones:
     - "📄 Cotización Simple" (más frecuente)
     - "📋 Proyecto Simple" (si necesita cronograma)
     - "📊 Informe Técnico" (si necesita informe)

5. **Datos adicionales según tipo elegido**:
   - **Si Proyecto**: ¿Fecha inicio deseada?
   - **Si Informe**: Generar código automático

**Resultado**: Chat recoge TODOS los datos necesarios para rellenar plantillas

---

### FASE 2: Crear Servicios Complejos (SEGUNDO)

**Orden sugerido por complejidad**:

1. **Pozo a Tierra** (Medio) - Bueno para probar flujo técnico
2. **CCTV** (Medio) - Similar a Pozo a Tierra
3. **Redes de Datos** (Medio)
4. **Saneamiento** (Medio)
5. **Instalaciones Eléctricas** (Muy Complejo) - El más importante
6. **Contraincendios** (Muy Complejo)
7. **Domótica** (Muy Complejo)
8. **Automatización Industrial** (Muy Complejo)
9. **Expedientes Técnicos** (Complejo)

---

### FASE 3: Integrar Generación de Documentos

**Objetivo**: Que el chat llame a los generadores en `professional/generators/`

**Flujo**:
```
Chat recoge datos → Valida completitud → Llama a generador → Retorna documento
```

**Generadores a usar** (ya existen en `backend/app/services/professional/generators/`):
- `cotizaciones/simple.py`
- `cotizaciones/compleja.py`
- `proyectos/simple.py`
- `proyectos/complejo_pmi.py`
- `informes/tecnico.py`
- `informes/ejecutivo_apa.py`

---

## ❓ PREGUNTAS CRÍTICAS PARA EL USUARIO

Antes de continuar, **necesito que respondas**:

### 1️⃣ **Sobre la Matriz de Servicios × Documentos**

¿La matriz de "pesos" es correcta?

**Ejemplo dudas**:
- ¿ITSE realmente NO usa Proyecto PMI ni Informe Ejecutivo APA?
- ¿Electricidad SÍ usa los 6 tipos de documentos?
- ¿Expedientes Técnicos usa más Proyectos que Cotizaciones?

**Acción**: Revisar la tabla y corregir

---

### 2️⃣ **Sobre Datos Técnicos de Cada Servicio**

¿Tienes definido para cada servicio?:
- Normativa aplicable
- Fórmulas de cálculo (precio, duración, etc.)
- Datos técnicos que se deben preguntar

**Ejemplo**:
- **ITSE**: Ya está (D.S. 002-2018-PCM, precios TUPA, cálculo de riesgo)
- **Electricidad**: ¿CNE 2011? ¿Fórmula de cálculo según potencia?
- **Pozo Tierra**: ¿CNE 2011 Sección 5? ¿Fórmula de resistividad?

---

### 3️⃣ **Sobre Prioridad de Implementación**

¿En qué orden quieres que implemente los servicios?

**Opciones**:
- **A)** Por frecuencia de uso (los más solicitados primero)
- **B)** Por complejidad ascendente (Simple → Complejo)
- **C)** Orden personalizado (tú defines)

**Mi sugerencia**:
1. Rediseñar ITSE (alinear con plantillas)
2. Pozo a Tierra (medio, probar flujo técnico)
3. Electricidad (muy complejo, muy importante)
4. Resto según frecuencia

---

### 4️⃣ **Sobre Generación Automática de Textos**

Algunos campos necesitan textos largos:
- `DESCRIPCION_PROYECTO`
- `ALCANCE_PROYECTO`
- `RESUMEN_EJECUTIVO`

¿Quieres que?:
- **A)** El chat pregunte al usuario (más trabajo para usuario)
- **B)** Generar automático con IA (usando datos recopilados)
- **C)** Plantillas predefinidas por servicio

**Mi sugerencia**: Generar con IA usando los datos recopilados

---

## 📋 DECISIÓN REQUERIDA

**NO escribiré código hasta que confirmes**:

1. ✅ Matriz de servicios × documentos validada
2. ✅ Datos técnicos (normativas, fórmulas) por servicio
3. ✅ Orden de prioridad de implementación
4. ✅ Estrategia para campos de texto largo

**Una vez validado**:
→ Rediseño chat ITSE (versión 2.0 alineada con plantillas)
→ Implemento servicios según prioridad
→ Integro con generadores de documentos

---

**¿Cuáles son tus respuestas a las 4 preguntas críticas?** 🎯

---

**Documento creado**: 30 de Diciembre 2025
**Autor**: Claude Code (Sonnet 4.5)
**Estado**: ⏸️ ANÁLISIS COMPLETO - Esperando validación del usuario
