# TESLA COTIZADOR v4.0 - SISTEMA PROFESIONAL DE GENERACIÓN DE DOCUMENTOS

## Sistema Inteligente con RAG, ML Local y Gráficas Profesionales

**Versión:** 4.0
**Fecha:** Noviembre 2024
**Autor:** Tesla Electricidad y Automatización S.A.C.

---

## TABLA DE CONTENIDOS

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Estructura del Proyecto](#3-estructura-del-proyecto)
4. [Componentes Profesionales](#4-componentes-profesionales)
5. [Guía de Uso para el Usuario](#5-guía-de-uso-para-el-usuario)
6. [Flujos de Trabajo](#6-flujos-de-trabajo)
7. [Casos de Uso](#7-casos-de-uso)
8. [Sistema de Documentos](#8-sistema-de-documentos)
9. [API REST Endpoints](#9-api-rest-endpoints)
10. [Instalación y Configuración](#10-instalación-y-configuración)
11. [Docker para Producción](#11-docker-para-producción)
12. [Testing](#12-testing)
13. [Ejemplos de Código](#13-ejemplos-de-código)
14. [Conclusiones](#14-conclusiones)

---

## 1. RESUMEN EJECUTIVO

### 1.1 Descripción General

TESLA COTIZADOR v4.0 es un sistema de generación de documentos de **clase mundial** que integra:

- **RAG Local**: Búsqueda semántica sin internet (ChromaDB + sentence-transformers)
- **ML Local**: Clasificación automática con spaCy + sklearn
- **Gráficas Profesionales**: Gantt, KPIs, matrices de riesgo con Plotly
- **Procesamiento de Archivos**: PDF, Word, Excel, imágenes con OCR
- **6 Tipos de Documentos**: Cotizaciones, Proyectos, Informes (simples y complejos)

### 1.2 Problema que Resuelve

| Problema | Solución v4.0 |
|----------|---------------|
| Dependencia de internet para IA | RAG + ML 100% local |
| Documentos sin gráficas profesionales | Motor Plotly completo |
| No se pueden subir archivos de referencia | Procesador multi-formato |
| Análisis manual de datos | Clasificación automática ML |
| Sin diagramas Gantt | ChartEngine profesional |

### 1.3 Tecnologías de Clase Mundial

| Componente | Tecnología | Por qué es la mejor |
|------------|------------|---------------------|
| Vector DB | ChromaDB | Estándar industria RAG |
| Embeddings | sentence-transformers | Modelos preentrenados |
| NLP | spaCy | Modelo español incluido |
| ML | scikit-learn | Algoritmos clásicos probados |
| Gráficas | Plotly | Interactivas y exportables |
| OCR | Tesseract | Estándar industria |
| Documentos | python-docx + reportlab | Control total |

### 1.4 Características Principales

- ✅ **100% Offline**: Funciona sin conexión a internet
- ✅ **6 Tipos de Documentos**: Simple y Complejo para cada tipo
- ✅ **10 Servicios**: Eléctrico, contraincendios, domótica, etc.
- ✅ **Logo Personalizado**: Cada empresa puede usar su logo
- ✅ **Gráficas Profesionales**: Gantt, KPIs, matrices, flujo de caja
- ✅ **Procesamiento de Archivos**: PDF, Word, Excel, imágenes
- ✅ **RAG Inteligente**: Busca en documentos subidos
- ✅ **Docker Ready**: Listo para producción

---

## 2. ARQUITECTURA DEL SISTEMA

### 2.1 Diagrama de Arquitectura v4.0

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                      │
│              React.js + TailwindCSS + PILI Avatar            │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE API (FastAPI)                     │
│     Routers: chat, cotizaciones, documentos, system          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              DOCUMENT GENERATOR PRO (Orquestador)            │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │    FILE      │  │     RAG      │  │      ML      │       │
│  │  PROCESSOR   │  │   ENGINE     │  │   ENGINE     │       │
│  │              │  │              │  │              │       │
│  │ • PDF        │  │ • ChromaDB   │  │ • spaCy      │       │
│  │ • Word       │  │ • Embeddings │  │ • sklearn    │       │
│  │ • Excel      │  │ • Búsqueda   │  │ • NER        │       │
│  │ • OCR        │  │   semántica  │  │ • Clasific.  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │    CHART     │  │     WORD     │                         │
│  │   ENGINE     │  │  GENERATOR   │                         │
│  │              │  │              │                         │
│  │ • Plotly     │  │ • python-    │                         │
│  │ • Gantt      │  │   docx       │                         │
│  │ • KPIs       │  │ • Templates  │                         │
│  │ • Matrices   │  │ • Estilos    │                         │
│  └──────────────┘  └──────────────┘                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  CAPA DE PERSISTENCIA                        │
│       PostgreSQL + ChromaDB + Sistema de Archivos            │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Flujo de Datos Completo

```
Usuario sube archivos (PDF, Word, Excel)
              │
              ▼
    ┌─────────────────┐
    │ FileProcessorPro │ ──► Extrae texto y tablas
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │    RAGEngine    │ ──► Indexa en ChromaDB
    └─────────────────┘
              │
              ▼
Usuario escribe mensaje
              │
              ▼
    ┌─────────────────┐
    │    MLEngine     │ ──► Clasifica servicio + extrae entidades
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │   RAG Search    │ ──► Recupera contexto relevante
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │   ChartEngine   │ ──► Genera gráficas (si es complejo)
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ WordGenerator   │ ──► Crea documento Word/PDF
    └─────────────────┘
              │
              ▼
    Usuario descarga documento profesional
```

---

## 3. ESTRUCTURA DEL PROYECTO

```
TESLA_COTIZADOR-V3.0/
│
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── professional/              # SISTEMA v4.0
│   │   │   │   ├── __init__.py
│   │   │   │   ├── processors/
│   │   │   │   │   └── file_processor_pro.py  # Procesador archivos
│   │   │   │   ├── rag/
│   │   │   │   │   └── rag_engine.py          # Motor RAG
│   │   │   │   ├── ml/
│   │   │   │   │   └── ml_engine.py           # Motor ML
│   │   │   │   ├── charts/
│   │   │   │   │   └── chart_engine.py        # Motor gráficas
│   │   │   │   └── generators/
│   │   │   │       └── document_generator_pro.py  # Orquestador
│   │   │   │
│   │   │   ├── word_generator.py          # Generador Word
│   │   │   ├── pdf_generator.py           # Generador PDF
│   │   │   ├── pili_brain.py              # IA Local
│   │   │   └── pili_integrator.py         # Integrador
│   │   │
│   │   ├── routers/                       # API Endpoints
│   │   ├── models/                        # Modelos BD
│   │   ├── schemas/                       # Pydantic
│   │   └── templates/                     # Plantillas
│   │
│   ├── storage/
│   │   ├── uploads/                       # Archivos subidos
│   │   ├── generated/                     # Documentos generados
│   │   ├── embeddings/                    # ChromaDB data
│   │   └── temp/                          # Temporales
│   │
│   ├── ml_models/                         # Modelos ML
│   ├── requirements_professional.txt      # Dependencias
│   └── test_professional_system.py        # Tests
│
├── frontend/
│   └── src/
│       ├── components/
│       └── services/
│
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── nginx.conf
│
└── docker-compose.production.yml
```

---

## 4. COMPONENTES PROFESIONALES

### 4.1 FileProcessorPro

**Ubicación:** `backend/app/services/professional/processors/file_processor_pro.py`

Procesa múltiples formatos de archivos para alimentar el sistema RAG.

**Formatos soportados:**

| Formato | Librería | Características |
|---------|----------|-----------------|
| PDF | pdfplumber | Texto + tablas |
| Word | python-docx | Párrafos + tablas |
| Excel | pandas + openpyxl | Todas las hojas |
| CSV | pandas | Datos estructurados |
| Imágenes | pytesseract | OCR español |
| JSON/TXT | nativo | Texto plano |

**Uso:**
```python
from app.services.professional.processors import FileProcessorPro

processor = FileProcessorPro()

# Procesar un archivo
result = processor.process_file("documento.pdf")
print(result["text"])     # Texto extraído
print(result["tables"])   # Tablas encontradas

# Procesar múltiples archivos
results = processor.process_multiple([
    "especificaciones.pdf",
    "costos.xlsx",
    "foto_sitio.jpg"
])

# Dividir en chunks para RAG
chunks = processor.chunk_text(result["text"], chunk_size=500)
```

### 4.2 RAGEngine

**Ubicación:** `backend/app/services/professional/rag/rag_engine.py`

Sistema de Retrieval Augmented Generation 100% local.

**Características:**
- ChromaDB como vector store
- sentence-transformers para embeddings
- Búsqueda semántica por significado
- Persiste en disco

**Uso:**
```python
from app.services.professional.rag import RAGEngine

rag = RAGEngine()

# Agregar documento
rag.add_document(
    "Las instalaciones eléctricas residenciales deben cumplir CNE...",
    metadata={"tipo": "normativa", "servicio": "electrico"}
)

# Agregar chunks de archivos procesados
rag.add_chunks(
    chunks,
    metadata={"source": "especificaciones.pdf"}
)

# Buscar información relevante
results = rag.search("requisitos instalación eléctrica", n_results=5)

# Obtener contexto para documento
context = rag.get_context_for_document(
    "cotización para casa 200m2",
    document_type="cotizacion"
)
```

### 4.3 MLEngine

**Ubicación:** `backend/app/services/professional/ml/ml_engine.py`

Machine Learning local para clasificación y extracción de entidades.

**Capacidades:**
- Clasificación de servicios (10 tipos)
- Extracción de entidades (área, cantidad, precio, pisos)
- Detección de intención
- Análisis completo de texto

**Uso:**
```python
from app.services.professional.ml import MLEngine

ml = MLEngine()

# Clasificar servicio
result = ml.classify_service(
    "Necesito cotizar instalación eléctrica para casa de 150m2"
)
print(result["service"])      # "electrico-residencial"
print(result["confidence"])   # 0.85

# Extraer entidades
entities = ml.extract_entities(
    "Casa de 200m2, 2 pisos, presupuesto S/15000"
)
print(entities["area_principal"])    # 200
print(entities["num_pisos"])         # 2
print(entities["precio_principal"])  # 15000

# Análisis completo
analysis = ml.analyze_text("cotizar sistema contra incendios")
print(analysis["intent"])    # "cotizacion"
print(analysis["service"])   # {"service": "contraincendios", ...}
```

### 4.4 ChartEngine

**Ubicación:** `backend/app/services/professional/charts/chart_engine.py`

Motor de gráficas profesionales con Plotly.

**Tipos de gráficas:**

| Tipo | Método | Uso |
|------|--------|-----|
| Barras | `create_bar_chart()` | Costos, comparativas |
| Líneas | `create_line_chart()` | Tendencias |
| Pie/Donut | `create_pie_chart()` | Distribuciones |
| Gantt | `create_gantt_chart()` | Cronogramas |
| Heatmap | `create_risk_matrix()` | Matrices riesgo |
| KPIs | `create_kpi_dashboard()` | Indicadores |
| Flujo caja | `create_cashflow_chart()` | Financiero |

**Uso:**
```python
from app.services.professional.charts import ChartEngine

charts = ChartEngine()

# Gráfico de barras
path = charts.create_bar_chart(
    {"Materiales": 5000, "Mano de obra": 3000},
    title="Distribución de Costos"
)

# Diagrama Gantt
tasks = [
    {"nombre": "Planificación", "inicio": "2024-01-01", "fin": "2024-01-07"},
    {"nombre": "Ejecución", "inicio": "2024-01-08", "fin": "2024-01-30"}
]
path = charts.create_gantt_chart(tasks)

# Dashboard KPIs
kpis = {
    "ROI": {"valor": 25, "meta": 20, "unidad": "%"},
    "Avance": {"valor": 75, "meta": 100, "unidad": "%"}
}
path = charts.create_kpi_dashboard(kpis)

# Matriz de riesgos
risks = [
    {"nombre": "Retraso", "probabilidad": 3, "impacto": 4}
]
path = charts.create_risk_matrix(risks)
```

### 4.5 DocumentGeneratorPro

**Ubicación:** `backend/app/services/professional/generators/document_generator_pro.py`

Orquestador que integra todos los componentes.

**Uso:**
```python
from app.services.professional.generators import DocumentGeneratorPro
import asyncio

generator = DocumentGeneratorPro()

# Generar documento completo
result = asyncio.run(generator.generate_document(
    message="Cotización para instalación eléctrica 200m2",
    document_type="cotizacion",
    complexity="complejo",
    uploaded_files=["specs.pdf", "planos.xlsx"],
    logo_base64="data:image/png;base64,..."
))

print(result["file_path"])
print(result["processing_steps"])
```

---

## 5. GUÍA DE USO PARA EL USUARIO

### 5.1 Inicio Rápido

#### Paso 1: Acceder a la Aplicación
```
1. Abrir navegador web
2. Ir a http://localhost:3000 (desarrollo) o tu dominio (producción)
3. Verás la interfaz de chat con PILI
```

#### Paso 2: Escribir tu Solicitud
```
Ejemplos de mensajes:

COTIZACIÓN:
"Necesito cotización para instalación eléctrica de casa de 150m2"
"Cotizar sistema contra incendios para local comercial de 300m2"
"Presupuesto para domótica en departamento de 80m2"

PROYECTO:
"Crear proyecto para instalación industrial de planta 500m2"
"Necesito proyecto PMI completo para edificio comercial"

INFORME:
"Generar informe técnico del proyecto de saneamiento"
"Informe ejecutivo con análisis ROI para inversión de $50000"
```

#### Paso 3: Subir Archivos de Referencia (Opcional)
```
1. Arrastra archivos al área de upload
2. Formatos soportados: PDF, Word, Excel, imágenes
3. El sistema extraerá información relevante
4. Se usará como contexto para tu documento
```

#### Paso 4: Revisar Vista Previa
```
1. PILI mostrará una vista previa del documento
2. Puedes ver los items generados
3. Los precios están calculados según normativa
4. Puedes editar cualquier campo
```

#### Paso 5: Editar y Personalizar
```
EDITAR ITEMS:
- Click en descripción para modificar texto
- Cambiar cantidad
- Ajustar precio unitario
- El total se recalcula automáticamente

AGREGAR LOGO:
- Click en "Subir Logo"
- Seleccionar imagen PNG o JPG
- El logo aparecerá en el encabezado
```

#### Paso 6: Generar Documento Final
```
1. Click en "Generar Word" o "Generar PDF"
2. Espera 3-5 segundos
3. El archivo se descargará automáticamente
4. Documento listo para enviar al cliente
```

### 5.2 Tipos de Documentos

#### Cotización Simple
```
QUÉ INCLUYE:
- Datos del cliente
- Lista de items con precios
- Subtotal, IGV, Total
- Observaciones básicas
- Vigencia de 30 días

CUÁNDO USAR:
- Trabajos pequeños
- Respuestas rápidas
- Presupuestos preliminares
```

#### Cotización Compleja
```
QUÉ INCLUYE:
- Todo de la simple +
- Cronograma de ejecución
- Desglose detallado por etapas
- Garantías especificadas
- Condiciones de pago
- Especificaciones técnicas ampliadas

CUÁNDO USAR:
- Proyectos medianos/grandes
- Licitaciones
- Clientes corporativos
```

#### Proyecto Simple
```
QUÉ INCLUYE:
- 5 fases principales
- Duración estimada
- Recursos básicos
- Entregables por fase
- Presupuesto total

CUÁNDO USAR:
- Proyectos estándar
- Sin requisitos PMI
- Gestión básica
```

#### Proyecto PMI (Complejo)
```
QUÉ INCLUYE:
- 6 fases (incluye Stakeholders)
- Diagrama Gantt profesional
- Matriz de riesgos
- KPIs (SPI, CPI)
- Matriz RACI
- WBS detallado
- Cronograma con dependencias

CUÁNDO USAR:
- Proyectos grandes
- Clientes que requieren PMI
- Control riguroso
```

#### Informe Técnico (Simple)
```
QUÉ INCLUYE:
- 5 secciones estándar
- Marco normativo
- Descripción técnica
- Metodología
- Resultados y conclusiones

CUÁNDO USAR:
- Informes de avance
- Documentación técnica
- Entregables de proyecto
```

#### Informe Ejecutivo APA (Complejo)
```
QUÉ INCLUYE:
- Executive Summary
- Análisis financiero (ROI, TIR, Payback)
- Métricas y KPIs
- Gráficas profesionales
- Análisis de riesgos
- Plan de implementación
- Formato APA 7ma edición
- Bibliografía

CUÁNDO USAR:
- Presentaciones a directivos
- Solicitud de inversión
- Informes finales de proyecto
```

### 5.3 Servicios Disponibles

| Servicio | Palabras Clave | Normativa |
|----------|----------------|-----------|
| Eléctrico Residencial | casa, vivienda, departamento | CNE Suministro |
| Eléctrico Comercial | tienda, oficina, local | CNE Suministro |
| Eléctrico Industrial | fábrica, planta, industria | CNE Utilización |
| Contraincendios | incendio, rociador, detector | NFPA 13, 72, 20 |
| Domótica | smart home, automatización | KNX/EIB |
| Expedientes | licencia, permiso, municipalidad | RNE |
| Saneamiento | agua, desagüe, cisterna | RNE IS.010 |
| ITSE | certificado, defensa civil | D.S. 002-2018-PCM |
| Pozo a Tierra | puesta a tierra, pararrayo | CNE Sección 250 |
| Redes/CCTV | cámaras, cableado, rack | TIA/EIA-568 |

### 5.4 Tips para Mejores Resultados

```
✅ SÉ ESPECÍFICO CON EL ÁREA:
   Malo:  "cotización para casa"
   Bueno: "cotización para casa de 150m2"

✅ MENCIONA CARACTERÍSTICAS ESPECIALES:
   "casa de 2 pisos con sótano"
   "local comercial con aire acondicionado"

✅ SUBE ARCHIVOS DE REFERENCIA:
   - Planos del arquitecto
   - Especificaciones del cliente
   - Cotizaciones anteriores

✅ USA EL TIPO CORRECTO:
   - Simple para respuestas rápidas
   - Complejo para presentaciones formales

✅ REVISA ANTES DE GENERAR:
   - Verifica items
   - Ajusta precios si es necesario
   - Agrega observaciones específicas
```

---

## 6. FLUJOS DE TRABAJO

### 6.1 Flujo: Cotización con Archivos de Referencia

```
1. Usuario sube PDF con especificaciones del cliente
                    │
                    ▼
2. FileProcessorPro extrae texto y tablas
                    │
                    ▼
3. RAGEngine indexa el contenido
                    │
                    ▼
4. Usuario escribe: "Cotización según las especificaciones"
                    │
                    ▼
5. MLEngine detecta servicio del texto
                    │
                    ▼
6. RAGEngine busca información relevante del PDF
                    │
                    ▼
7. Sistema genera cotización con datos del PDF
                    │
                    ▼
8. Usuario revisa, edita y genera documento
```

### 6.2 Flujo: Proyecto PMI Complejo

```
1. Usuario escribe: "Proyecto PMI para fábrica de 1000m2"
                    │
                    ▼
2. MLEngine:
   - Servicio: electrico-industrial
   - Área: 1000m2
   - Complejidad: complejo (por "PMI")
                    │
                    ▼
3. Sistema genera estructura PMI:
   - 6 fases con actividades
   - Cronograma Gantt
   - Matriz de riesgos
   - KPIs iniciales
                    │
                    ▼
4. ChartEngine genera gráficas:
   - Diagrama Gantt
   - Matriz probabilidad/impacto
   - Dashboard de KPIs
                    │
                    ▼
5. WordGenerator crea documento con gráficas embebidas
                    │
                    ▼
6. Usuario descarga proyecto profesional
```

### 6.3 Flujo: Informe Ejecutivo con Métricas

```
1. Usuario escribe: "Informe ejecutivo para inversión de $80000"
                    │
                    ▼
2. Sistema detecta:
   - Tipo: informe
   - Complejidad: complejo (ejecutivo)
   - Presupuesto: $80000
                    │
                    ▼
3. Sistema calcula métricas:
   - ROI: 25%
   - TIR: 30%
   - Payback: 18 meses
   - Ahorro energético anual
                    │
                    ▼
4. ChartEngine genera:
   - Dashboard de KPIs
   - Flujo de caja proyectado
   - Comparativa de escenarios
                    │
                    ▼
5. Sistema estructura en formato APA:
   - Resumen ejecutivo
   - Análisis de situación
   - Métricas y KPIs
   - Análisis financiero
   - Evaluación de riesgos
   - Plan de implementación
   - Bibliografía
                    │
                    ▼
6. Usuario obtiene informe profesional
```

---

## 7. CASOS DE USO

### CU-01: Cotización Rápida

**Actor:** Usuario
**Objetivo:** Generar cotización en menos de 1 minuto

**Flujo:**
1. Usuario escribe: "Cotización rápida para casa 120m2"
2. Sistema detecta: electrico-residencial, 120m2
3. Genera items automáticamente
4. Muestra vista previa
5. Usuario hace click en "Generar Word"
6. Descarga cotización lista

**Tiempo:** ~45 segundos

### CU-02: Cotización con Especificaciones del Cliente

**Actor:** Usuario
**Objetivo:** Cotizar según PDF del cliente

**Flujo:**
1. Usuario sube "especificaciones_cliente.pdf"
2. Sistema extrae: área, requisitos, ubicación
3. Usuario escribe: "Cotizar según especificaciones"
4. Sistema usa datos del PDF para generar items
5. Usuario revisa y ajusta precios
6. Genera documento con todos los requisitos

### CU-03: Proyecto con Diagrama Gantt

**Actor:** Usuario
**Objetivo:** Crear proyecto con cronograma visual

**Flujo:**
1. Usuario escribe: "Proyecto para local comercial 300m2, necesito Gantt"
2. Sistema genera proyecto complejo automáticamente
3. ChartEngine crea diagrama Gantt profesional
4. Documento incluye gráfica embebida
5. Usuario obtiene proyecto con cronograma visual

### CU-04: Informe con Análisis ROI

**Actor:** Usuario
**Objetivo:** Presentar informe a directivos

**Flujo:**
1. Usuario escribe: "Informe ejecutivo, inversión $100000"
2. Sistema calcula métricas financieras
3. Genera gráficas de KPIs y flujo de caja
4. Estructura en formato APA
5. Incluye bibliografía y referencias
6. Usuario presenta informe profesional a directivos

### CU-05: Trabajo Sin Internet

**Actor:** Usuario
**Objetivo:** Generar documentos offline

**Flujo:**
1. Usuario sin conexión a internet
2. Sistema detecta modo offline
3. Usa MLEngine local para clasificación
4. Usa plantillas predefinidas
5. Genera documento completo sin degradación
6. Funcionalidad 100% mantenida

### CU-06: Múltiples Archivos de Referencia

**Actor:** Usuario
**Objetivo:** Cotizar con varios documentos

**Flujo:**
1. Usuario sube: planos.pdf, costos.xlsx, fotos.jpg
2. Sistema procesa cada archivo:
   - PDF: extrae especificaciones
   - Excel: extrae datos de costos
   - Imágenes: OCR para texto
3. Indexa todo en RAG
4. Usuario pregunta sobre cualquier archivo
5. Sistema responde con contexto combinado
6. Genera cotización usando toda la información

---

## 8. SISTEMA DE DOCUMENTOS

### 8.1 Tipos y Complejidad

| Tipo | Complejidad | Secciones | Gráficas |
|------|-------------|-----------|----------|
| Cotización | Simple | 5 | No |
| Cotización | Compleja | 8 | Opcional |
| Proyecto | Simple | 5 fases | No |
| Proyecto | Complejo | 6 fases | Gantt, Riesgos |
| Informe | Simple | 5 | No |
| Informe | Complejo | 6 | KPIs, Flujo caja |

### 8.2 Estructura JSON de Cotización

```json
{
  "numero": "COT-202411241230",
  "cliente": "Juan Pérez",
  "proyecto": "Instalación Eléctrica Residencial",
  "fecha": "24/11/2024",
  "vigencia": "30 días",
  "items": [
    {
      "descripcion": "Tablero eléctrico monofásico",
      "cantidad": 1,
      "unidad": "und",
      "precio_unitario": 450.00,
      "total": 450.00
    }
  ],
  "subtotal": 5000.00,
  "igv": 900.00,
  "total": 5900.00,
  "observaciones": "Incluye materiales y mano de obra",
  "normativa_aplicable": "CNE Suministro 2011"
}
```

### 8.3 Estructura JSON de Proyecto PMI

```json
{
  "nombre": "Proyecto Instalación Industrial",
  "codigo": "PROY-202411241230-PMI",
  "cliente": "Empresa SAC",
  "fecha_inicio": "01/12/2024",
  "fecha_fin": "15/02/2025",
  "duracion_total_dias": 76,
  "presupuesto_estimado": 150000.00,
  "fases": [
    {
      "nombre": "Inicio y Planificación",
      "duracion_dias": 10,
      "actividades": [
        "Elaboración de Project Charter",
        "Definición de alcance (WBS)"
      ],
      "entregable": "Project Charter aprobado"
    }
  ],
  "kpis": {
    "SPI": 1.0,
    "CPI": 1.0,
    "EV": 75000,
    "PV": 75000,
    "AC": 75000
  },
  "cronograma_gantt": {...}
}
```

### 8.4 Estructura JSON de Informe Ejecutivo

```json
{
  "titulo": "Informe Ejecutivo - Sistema Contra Incendios",
  "codigo": "INF-202411241230-EXE",
  "autor": "Tesla Electricidad",
  "formato": "APA 7ma edición",
  "resumen_ejecutivo": "...",
  "secciones": [...],
  "metricas_clave": {
    "roi_estimado": 25,
    "payback_meses": 18,
    "tir_proyectada": 30,
    "ahorro_energetico_anual": 12000,
    "reduccion_costos_operativos": 20
  },
  "graficos_sugeridos": [
    "Dashboard ejecutivo de KPIs",
    "Diagrama de Gantt",
    "Matriz de riesgos",
    "Flujo de caja proyectado"
  ],
  "bibliografia": [
    "Ministerio de Energía y Minas. (2011). CNE Suministro. Lima.",
    "Project Management Institute. (2021). PMBOK Guide. PMI."
  ]
}
```

---

## 9. API REST ENDPOINTS

### 9.1 Chat y Generación

```http
POST /api/chat
Content-Type: application/json

{
  "mensaje": "Cotización para casa de 150m2",
  "tipo_flujo": "cotizacion-simple",
  "historial": []
}

Response:
{
  "respuesta": "He preparado una cotización...",
  "datos_generados": {...},
  "html_preview": "<div>...</div>",
  "servicio_detectado": "electrico-residencial"
}
```

### 9.2 Generación de Documentos

```http
POST /api/documentos/generar
Content-Type: application/json

{
  "mensaje": "Casa de 200m2, 2 pisos",
  "tipo_documento": "cotizacion",
  "complejidad": "complejo",
  "formato": "word",
  "logo_base64": "..."
}

Response:
{
  "success": true,
  "file_path": "/storage/generated/cotizacion_xxx.docx",
  "file_name": "cotizacion_xxx.docx"
}
```

### 9.3 Subida de Archivos

```http
POST /api/archivos/upload
Content-Type: multipart/form-data

files: [archivo1.pdf, archivo2.xlsx]

Response:
{
  "success": true,
  "processed": 2,
  "combined_text": "...",
  "rag_indexed": true
}
```

### 9.4 Estado del Sistema

```http
GET /api/system/status

Response:
{
  "version": "4.0",
  "components": {
    "file_processor": true,
    "rag_engine": true,
    "ml_engine": true,
    "chart_engine": true,
    "word_generator": true
  },
  "mode": "OFFLINE_LOCAL"
}
```

---

## 10. INSTALACIÓN Y CONFIGURACIÓN

### 10.1 Requisitos

- **Python**: 3.11+
- **RAM**: 16GB (recomendado para ML)
- **Disco**: 2GB libres
- **Tesseract**: Para OCR

### 10.2 Instalación Paso a Paso

```bash
# 1. Clonar repositorio
git clone https://github.com/Oscar-Ivan-Salas/TESLA_COTIZADOR-V3.0.git
cd TESLA_COTIZADOR-V3.0

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias profesionales
pip install -r backend/requirements_professional.txt

# 4. Descargar modelo spaCy español
python -m spacy download es_core_news_sm

# 5. Instalar Tesseract OCR
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr tesseract-ocr-spa

# macOS:
brew install tesseract tesseract-lang

# Windows: Descargar de https://github.com/UB-Mannheim/tesseract/wiki

# 6. Configurar variables de entorno
cp backend/.env.example backend/.env
# Editar .env según necesidades

# 7. Iniciar backend
cd backend
uvicorn app.main:app --reload --port 8000

# 8. Iniciar frontend (otra terminal)
cd frontend
npm install
npm start
```

### 10.3 Variables de Entorno

```env
# Entorno
ENVIRONMENT=development

# Base de datos
DATABASE_URL=sqlite:///./tesla.db

# Almacenamiento
STORAGE_PATH=./storage
UPLOAD_DIR=./storage/uploads
GENERATED_DIR=./storage/generated

# Límites
MAX_FILE_SIZE=10485760  # 10MB

# API Key Gemini (opcional, para modo online)
GEMINI_API_KEY=your_api_key

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

---

## 11. DOCKER PARA PRODUCCIÓN

### 11.1 Levantar Stack Completo

```bash
# Construir y levantar
docker-compose -f docker-compose.production.yml up -d

# Ver logs
docker-compose -f docker-compose.production.yml logs -f

# Detener
docker-compose -f docker-compose.production.yml down
```

### 11.2 Servicios

| Servicio | Puerto | RAM | Descripción |
|----------|--------|-----|-------------|
| backend | 8000 | 4GB | API + ML |
| frontend | 80 | 256MB | Nginx + React |
| postgres | 5432 | 1GB | Base de datos |
| redis | 6379 | 512MB | Cache |
| celery | - | 2GB | Tareas async |

### 11.3 Escalamiento

```yaml
# Para más capacidad, escalar workers
docker-compose -f docker-compose.production.yml up -d --scale celery_worker=3
```

---

## 12. TESTING

### 12.1 Ejecutar Tests

```bash
cd backend
python test_professional_system.py
```

### 12.2 Tests Incluidos

1. **Imports** - Verifica módulos
2. **FileProcessor** - Procesamiento de archivos
3. **RAGEngine** - Indexación y búsqueda
4. **MLEngine** - Clasificación y NER
5. **ChartEngine** - Generación de gráficas
6. **DocumentGenerator** - Generación completa
7. **WordGenerator** - Creación de Word
8. **Integración** - Flujo completo

### 12.3 Output Esperado

```
=== TESLA COTIZADOR v4.0 - TEST SUITE ===

TEST 1: IMPORTS DE MÓDULOS
✅ Componentes profesionales importados
✅ pdfplumber
✅ plotly
...

TEST 2: FILE PROCESSOR
✅ Chunking funciona: 15 chunks creados

TEST 3: RAG ENGINE
✅ Documento agregado
✅ Búsqueda funciona: 1 resultados

TEST 4: ML ENGINE
✅ Servicio detectado: electrico-residencial
✅ Área extraída: 150 m2

TEST 5: CHART ENGINE
✅ Gráfico de barras creado

...

=== RESULTADOS FINALES ===
Pasados: 8
Fallidos: 0
Advertencias: 2

🎉 TODOS LOS TESTS PASARON 🎉
```

---

## 13. EJEMPLOS DE CÓDIGO

### 13.1 Generar Cotización Completa

```python
import asyncio
from app.services.professional.generators import get_document_generator_pro

async def main():
    generator = get_document_generator_pro()

    result = await generator.generate_document(
        message="Cotización para instalación eléctrica residencial de 200m2, 2 pisos",
        document_type="cotizacion",
        complexity="complejo"
    )

    if result["success"]:
        print(f"Documento generado: {result['file_name']}")
        print(f"Ruta: {result['file_path']}")

        # Ver pasos de procesamiento
        for step in result["processing_steps"]:
            print(f"  - {step['step']}: OK")
    else:
        print(f"Error: {result['error']}")

asyncio.run(main())
```

### 13.2 Procesar Archivos y Buscar

```python
from app.services.professional.processors import get_file_processor
from app.services.professional.rag import get_rag_engine

# Procesar archivos
processor = get_file_processor()
result = processor.process_multiple([
    "especificaciones.pdf",
    "costos.xlsx"
])

# Indexar en RAG
rag = get_rag_engine()
chunks = processor.chunk_text(result["combined_text"])
rag.add_chunks(chunks, metadata={"source": "cliente"})

# Buscar información
search = rag.search("requisitos de potencia eléctrica")
for r in search["results"]:
    print(r["text"][:200])
```

### 13.3 Generar Gráficas para Informe

```python
from app.services.professional.charts import get_chart_engine

charts = get_chart_engine()

# KPIs del proyecto
kpis = {
    "ROI": {"valor": 28, "meta": 20, "unidad": "%"},
    "Avance": {"valor": 65, "meta": 100, "unidad": "%"},
    "Presupuesto": {"valor": 45000, "meta": 50000, "unidad": "$"}
}
kpi_path = charts.create_kpi_dashboard(kpis, "KPIs del Proyecto")

# Flujo de caja
inflows = [20000, 25000, 30000, 35000]
outflows = [15000, 20000, 18000, 22000]
periods = ["Q1", "Q2", "Q3", "Q4"]
cashflow_path = charts.create_cashflow_chart(inflows, outflows, periods)

print(f"KPIs: {kpi_path}")
print(f"Flujo de caja: {cashflow_path}")
```

---

## 14. CONCLUSIONES

### 14.1 Logros del Sistema v4.0

1. **100% Offline**: Funciona sin internet usando RAG + ML local
2. **Clase Mundial**: Librerías de primer nivel (Plotly, ChromaDB, spaCy)
3. **Gráficas Profesionales**: Gantt, KPIs, matrices en documentos
4. **Multi-formato**: Procesa PDF, Word, Excel, imágenes
5. **Escalable**: Docker ready para producción

### 14.2 Comparativa con v3.0

| Característica | v3.0 | v4.0 |
|----------------|------|------|
| RAG Local | ❌ | ✅ ChromaDB |
| ML Local | Básico | ✅ spaCy + sklearn |
| Gráficas | ❌ | ✅ Plotly completo |
| OCR | ❌ | ✅ Tesseract |
| Procesamiento archivos | Básico | ✅ Multi-formato |
| Docker producción | Básico | ✅ Completo |

### 14.3 Rendimiento

| Operación | Tiempo | RAM |
|-----------|--------|-----|
| Clasificación ML | <100ms | 500MB |
| Búsqueda RAG | <500ms | 1GB |
| Generar gráficas | 1-3s | 200MB |
| Documento complejo | 5-10s | 2GB |
| OCR imagen | 2-5s | 500MB |

### 14.4 Trabajo Futuro

- [ ] Más modelos de ML (BERT, transformers pequeños)
- [ ] Exportación a Excel
- [ ] Dashboard analítico
- [ ] App móvil
- [ ] Firma digital

---

## REFERENCIAS

- FastAPI: https://fastapi.tiangolo.com/
- ChromaDB: https://www.trychroma.com/
- Plotly: https://plotly.com/
- spaCy: https://spacy.io/
- sentence-transformers: https://www.sbert.net/
- python-docx: https://python-docx.readthedocs.io/
- Tesseract OCR: https://github.com/tesseract-ocr/tesseract

---

**Copyright 2024 Tesla Electricidad y Automatización S.A.C.**

**Sistema Profesional de Generación de Documentos v4.0**
*"Documentos de clase mundial, 100% offline"*
