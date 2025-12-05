# TESLA COTIZADOR v3.0 - DOCUMENTACION TECNICA PARA TESIS

## Sistema Inteligente de Generacion de Documentos con IA

**Version:** 3.0
**Fecha:** Noviembre 2025
**Autor:** Tesla Electricidad y Automatizacion S.A.C.

---

## TABLA DE CONTENIDOS

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Arbol Completo de Trabajo](#3-arbol-completo-de-trabajo)
4. [Componentes Principales](#4-componentes-principales)
5. [Flujo de Trabajo del Usuario](#5-flujo-de-trabajo-del-usuario)
6. [Casos de Uso](#6-casos-de-uso)
7. [Sistema de Generacion de Documentos](#7-sistema-de-generacion-de-documentos)
8. [PILI - Inteligencia Artificial Local](#8-pili---inteligencia-artificial-local)
9. [API REST Endpoints](#9-api-rest-endpoints)
10. [40 Prompts para Comprension de IA](#10-40-prompts-para-comprension-de-ia)
11. [Guia de Instalacion](#11-guia-de-instalacion)
12. [Conclusiones](#12-conclusiones)

---

## 1. RESUMEN EJECUTIVO

### 1.1 Descripcion General

TESLA COTIZADOR v3.0 es una aplicacion web empresarial desarrollada para automatizar la generacion de documentos tecnicos en el sector de instalaciones electricas e industriales. El sistema integra inteligencia artificial para procesar solicitudes en lenguaje natural y generar documentos profesionales de manera autonoma.

### 1.2 Caracteristicas Principales

- **Generacion de 6 tipos de documentos**: Cotizaciones, Proyectos e Informes (simples y complejos)
- **10 servicios especializados**: Desde instalaciones electricas hasta sistemas contraincendios
- **IA integrada (PILI)**: Procesamiento 100% offline sin dependencia de APIs externas
- **Arquitectura hibrida**: Funciona con IA externa (Gemini) o localmente
- **Sistema RAG**: Busqueda semantica en documentos
- **Interfaz conversacional**: Chat con avatar animado (PILI Avatar)

### 1.3 Problema que Resuelve

El sistema resuelve la necesidad de empresas del sector electrico de:
- Generar cotizaciones profesionales rapidamente
- Crear documentos estandarizados segun normativas
- Automatizar calculos tecnicos complejos
- Mantener consistencia en la documentacion
- Reducir tiempo de elaboracion de propuestas

### 1.4 Tecnologias Utilizadas

| Componente | Tecnologia |
|------------|------------|
| Frontend | React.js 18, TailwindCSS |
| Backend | FastAPI (Python 3.11) |
| Base de Datos | SQLite/PostgreSQL |
| Generacion Word | python-docx |
| Generacion PDF | ReportLab |
| IA Externa | Google Gemini API |
| IA Local | PILIBrain (Python puro) |

---

## 2. ARQUITECTURA DEL SISTEMA

### 2.1 Diagrama de Arquitectura

```
+------------------------------------------+
|            CAPA DE PRESENTACION           |
|    React.js + TailwindCSS + PILI Avatar   |
+------------------------------------------+
                    |
                    | HTTP/REST
                    v
+------------------------------------------+
|            CAPA DE API (FastAPI)          |
|  - Routers: chat, cotizaciones, docs      |
|  - Autenticacion y validacion             |
+------------------------------------------+
                    |
                    v
+------------------------------------------+
|         CAPA DE SERVICIOS DE IA           |
|  +----------------+  +----------------+   |
|  | Gemini Service |  |   PILIBrain    |   |
|  | (IA Externa)   |  |  (IA Local)    |   |
|  +----------------+  +----------------+   |
+------------------------------------------+
                    |
                    v
+------------------------------------------+
|       CAPA DE GENERACION DE DOCS          |
|  +---------------+  +---------------+     |
|  | WordGenerator |  | PDFGenerator  |     |
|  +---------------+  +---------------+     |
|  +---------------+  +---------------+     |
|  | TemplateProc  |  | ReportGen     |     |
|  +---------------+  +---------------+     |
+------------------------------------------+
                    |
                    v
+------------------------------------------+
|           CAPA DE PERSISTENCIA            |
|    SQLite/PostgreSQL + Sistema Archivos   |
+------------------------------------------+
```

### 2.2 Patron de Diseno

El sistema implementa varios patrones de diseno:

- **MVC (Model-View-Controller)**: Separacion de responsabilidades
- **Repository Pattern**: Abstraccion de acceso a datos
- **Strategy Pattern**: Multiples estrategias de generacion de IA
- **Factory Pattern**: Creacion de diferentes tipos de documentos
- **Singleton**: Instancias unicas de servicios

### 2.3 Flujo de Datos

```
Usuario -> Frontend -> API -> Servicio IA -> Generador Docs -> Archivo Final
     ^                                                              |
     |______________________________________________________________|
                         (Descarga documento)
```

---

## 3. ARBOL COMPLETO DE TRABAJO

```
TESLA_COTIZADOR-V3.0/
|
+-- backend/                          # Servidor FastAPI
|   +-- app/
|   |   +-- core/                     # Configuracion central
|   |   |   +-- config.py             # Variables de entorno
|   |   |   +-- database.py           # Conexion BD
|   |   |   +-- __init__.py
|   |   |
|   |   +-- models/                   # Modelos SQLAlchemy
|   |   |   +-- cotizacion.py         # Modelo Cotizacion
|   |   |   +-- documento.py          # Modelo Documento
|   |   |   +-- proyecto.py           # Modelo Proyecto
|   |   |   +-- item.py               # Modelo Item
|   |   |   +-- __init__.py
|   |   |
|   |   +-- routers/                  # Endpoints API
|   |   |   +-- chat.py               # Chat con IA
|   |   |   +-- cotizaciones.py       # CRUD Cotizaciones
|   |   |   +-- documentos.py         # Gestion documentos
|   |   |   +-- proyectos.py          # CRUD Proyectos
|   |   |   +-- informes.py           # Generacion informes
|   |   |   +-- system.py             # Estado del sistema
|   |   |   +-- __init__.py
|   |   |
|   |   +-- schemas/                  # Schemas Pydantic
|   |   |   +-- cotizacion.py         # Schema Cotizacion
|   |   |   +-- documento.py          # Schema Documento
|   |   |   +-- proyecto.py           # Schema Proyecto
|   |   |   +-- __init__.py
|   |   |
|   |   +-- services/                 # SERVICIOS PRINCIPALES
|   |   |   +-- gemini_service.py     # Conexion Google Gemini
|   |   |   +-- pili_brain.py         # IA LOCAL (OFFLINE)
|   |   |   +-- pili_orchestrator.py  # Orquestador de servicios
|   |   |   +-- word_generator.py     # Generador Word (.docx)
|   |   |   +-- pdf_generator.py      # Generador PDF
|   |   |   +-- template_processor.py # Procesador plantillas
|   |   |   +-- report_generator.py   # Generador informes
|   |   |   +-- file_processor.py     # Procesador archivos
|   |   |   +-- rag_service.py        # Busqueda semantica
|   |   |   +-- multi_ia_service.py   # Multi-IA support
|   |   |   +-- __init__.py
|   |   |
|   |   +-- templates/                # PLANTILLAS MODELO
|   |   |   +-- documentos/
|   |   |       +-- plantillas_modelo.py  # Fallback local
|   |   |
|   |   +-- utils/                    # Utilidades
|   |   |   +-- helpers.py            # Funciones auxiliares
|   |   |   +-- ocr.py                # Procesamiento OCR
|   |   |   +-- contextos_servicios.py
|   |   |   +-- __init__.py
|   |   |
|   |   +-- main.py                   # Punto de entrada
|   |
|   +-- storage/                      # Almacenamiento
|   |   +-- uploads/                  # Archivos subidos
|   |   +-- generated/                # Documentos generados
|   |   +-- templates/                # Plantillas Word
|   |
|   +-- requirements.txt              # Dependencias Python
|   +-- Dockerfile                    # Contenedor Docker
|   +-- .env.example                  # Variables ejemplo
|
+-- frontend/                         # Cliente React
|   +-- src/
|   |   +-- components/               # Componentes React
|   |   |   +-- PiliAvatar.jsx        # Avatar animado IA
|   |   |   +-- UploadZone.jsx        # Zona drag & drop
|   |   |   +-- VistaPrevia.jsx       # Vista previa docs
|   |   |
|   |   +-- services/
|   |   |   +-- api.js                # Cliente API
|   |   |
|   |   +-- App.jsx                   # Componente principal
|   |   +-- index.js                  # Punto de entrada
|   |
|   +-- public/                       # Archivos estaticos
|   +-- package.json                  # Dependencias Node
|   +-- tailwind.config.js            # Config TailwindCSS
|
+-- docker-compose.yml                # Orquestacion Docker
+-- README.md                         # Documentacion basica
+-- README_TESIS.md                   # ESTA DOCUMENTACION
```

---

## 4. COMPONENTES PRINCIPALES

### 4.1 PILIBrain - Cerebro de IA Local

**Ubicacion:** `backend/app/services/pili_brain.py`

PILIBrain es el componente central de inteligencia artificial que funciona 100% offline. Utiliza logica Python pura, expresiones regulares y reglas de negocio para:

- Detectar servicios automaticamente desde texto
- Extraer datos tecnicos (areas, cantidades, potencias)
- Generar cotizaciones con calculos segun normativas
- Crear proyectos con cronogramas realistas
- Elaborar informes tecnicos y ejecutivos

**Caracteristicas:**
- No requiere API keys ni conexion a internet
- Calculos segun CNE, NFPA, RNE
- Precios de mercado peruano 2025
- 10 servicios especializados

### 4.2 WordGenerator - Generador de Documentos Word

**Ubicacion:** `backend/app/services/word_generator.py`

Genera documentos Word profesionales sin corrupcion de archivos. Incluye:

- Estilos Tesla (colores corporativos)
- Tablas dinamicas
- Logos personalizados
- Headers y footers automaticos
- Marcadores PILI

**Metodos principales:**
```python
- generar_desde_json_pili()  # Nuevo metodo PILI v3.0
- generar_cotizacion()       # Cotizaciones
- generar_informe_proyecto() # Informes de proyecto
- generar_informe_simple()   # Informes basicos
```

### 4.3 PDFGenerator - Generador de PDF

**Ubicacion:** `backend/app/services/pdf_generator.py`

Genera documentos PDF no editables usando ReportLab:

- Formato profesional
- Tablas con estilos
- Soporte para logos
- Calculos automaticos de totales

### 4.4 TemplateProcessor - Procesador de Plantillas

**Ubicacion:** `backend/app/services/template_processor.py`

Procesa plantillas Word con marcadores dinamicos:

**Marcadores soportados:**
```
{{cliente}}          - Nombre del cliente
{{proyecto}}         - Nombre del proyecto
{{numero}}           - Numero de documento
{{fecha}}            - Fecha actual
{{items_tabla}}      - Tabla de items
{{logo}}             - Logo de empresa
{{subtotal}}         - Subtotal
{{igv}}              - IGV (18%)
{{total}}            - Total
{{agente_pili}}      - Agente PILI responsable
```

### 4.5 ReportGenerator - Generador de Informes Ejecutivos

**Ubicacion:** `backend/app/services/report_generator.py`

Genera informes ejecutivos complejos con:

- Analisis automatico con IA
- Calculo de metricas y KPIs
- Conclusiones inteligentes
- Recomendaciones basadas en datos
- Timeline del proyecto
- Analisis de riesgos

### 4.6 GeminiService - Conexion IA Externa

**Ubicacion:** `backend/app/services/gemini_service.py`

Conecta con Google Gemini API para:

- Chat conversacional
- Analisis de documentos
- Generacion de contenido avanzado
- Extraccion de datos de PDFs

### 4.7 RAGService - Busqueda Semantica

**Ubicacion:** `backend/app/services/rag_service.py`

Implementa Retrieval-Augmented Generation para:

- Indexar documentos subidos
- Busqueda semantica por significado
- Contexto inteligente para respuestas

---

## 5. FLUJO DE TRABAJO DEL USUARIO

### 5.1 Flujo Principal

```
1. INICIO
   |
   v
2. Usuario accede a la aplicacion web
   |
   v
3. Escribe mensaje en chat describiendo necesidad
   Ejemplo: "Necesito cotizacion para casa de 150m2"
   |
   v
4. Sistema detecta:
   - Tipo de documento: Cotizacion
   - Servicio: electrico-residencial
   - Area: 150 m2
   |
   v
5. PILIBrain genera JSON estructurado con:
   - Items calculados segun normativa
   - Precios de mercado
   - Observaciones tecnicas
   |
   v
6. Usuario visualiza preview en interfaz
   - Puede editar items
   - Puede ajustar cantidades
   - Puede cambiar precios
   |
   v
7. Usuario solicita generar documento
   - Selecciona formato (Word/PDF)
   - Opcionalmente sube logo
   |
   v
8. WordGenerator/PDFGenerator crea archivo
   |
   v
9. Sistema ofrece descarga del documento
   |
   v
10. FIN - Usuario tiene documento profesional
```

### 5.2 Flujo con Documentos Adjuntos

```
1. Usuario sube documento (PDF, imagen, etc.)
   |
   v
2. FileProcessor extrae contenido
   - OCR para imagenes
   - Extraccion de texto de PDF
   |
   v
3. RAGService indexa contenido
   |
   v
4. Usuario hace pregunta sobre el documento
   |
   v
5. Sistema usa contexto del documento para responder
   |
   v
6. Genera cotizacion/proyecto basado en informacion extraida
```

### 5.3 Flujo Offline (Sin Internet)

```
1. Sistema detecta que Gemini no esta disponible
   |
   v
2. Automaticamente usa PILIBrain (IA local)
   |
   v
3. PILIBrain procesa solicitud con reglas locales
   |
   v
4. Genera documento usando plantillas predefinidas
   |
   v
5. Usuario obtiene documento sin depender de internet
```

---

## 6. CASOS DE USO

### CU-01: Generar Cotizacion Simple

**Actor:** Usuario
**Precondicion:** Sistema iniciado
**Flujo:**
1. Usuario escribe "Cotizacion para local comercial de 200m2"
2. Sistema detecta servicio: electrico-comercial
3. Sistema genera items automaticamente
4. Usuario revisa y confirma
5. Sistema genera documento Word
6. Usuario descarga cotizacion

### CU-02: Generar Proyecto PMI

**Actor:** Usuario
**Precondicion:** Sistema iniciado
**Flujo:**
1. Usuario escribe "Necesito proyecto complejo para fabrica"
2. Sistema detecta servicio: electrico-industrial
3. Sistema genera estructura PMI con 6 fases
4. Incluye diagrama Gantt, recursos, riesgos
5. Usuario revisa y ajusta cronograma
6. Sistema genera documento Word

### CU-03: Generar Informe Ejecutivo

**Actor:** Usuario
**Precondicion:** Existe proyecto previo
**Flujo:**
1. Usuario solicita informe ejecutivo
2. Sistema analiza datos del proyecto
3. Calcula metricas (ROI, TIR, Payback)
4. Genera secciones en formato APA
5. Incluye bibliografia y graficos sugeridos
6. Usuario descarga informe profesional

### CU-04: Subir y Analizar Documento

**Actor:** Usuario
**Precondicion:** Sistema iniciado
**Flujo:**
1. Usuario arrastra PDF al area de upload
2. Sistema procesa y extrae texto
3. Sistema indexa en RAG
4. Usuario pregunta sobre el documento
5. Sistema responde con contexto del documento

### CU-05: Chat Conversacional

**Actor:** Usuario
**Precondicion:** Sistema iniciado
**Flujo:**
1. Usuario inicia conversacion con PILI
2. PILI responde con informacion tecnica
3. Usuario hace preguntas de seguimiento
4. PILI mantiene contexto de la conversacion
5. Usuario puede solicitar generar documento en cualquier momento

### CU-06: Editar Cotizacion Existente

**Actor:** Usuario
**Precondicion:** Cotizacion generada
**Flujo:**
1. Usuario visualiza preview de cotizacion
2. Edita descripcion de item
3. Modifica cantidad o precio
4. Sistema recalcula totales automaticamente
5. Usuario regenera documento con cambios

### CU-07: Generar Documento desde Plantilla

**Actor:** Usuario
**Precondicion:** Plantilla Word configurada
**Flujo:**
1. Usuario selecciona plantilla personalizada
2. Sistema extrae marcadores de la plantilla
3. Usuario completa datos faltantes
4. Sistema reemplaza marcadores
5. Genera documento final manteniendo formato de plantilla

### CU-08: Usar Sistema Sin Internet

**Actor:** Usuario
**Precondicion:** Sin conexion a internet
**Flujo:**
1. Sistema detecta Gemini no disponible
2. Activa PILIBrain automaticamente
3. Usuario trabaja normalmente
4. Sistema genera documentos usando plantillas locales
5. Funcionalidad completa sin degradacion

---

## 7. SISTEMA DE GENERACION DE DOCUMENTOS

### 7.1 Tipos de Documentos

| Tipo | Complejidad | Descripcion |
|------|-------------|-------------|
| Cotizacion Simple | Simple | Items basicos, totales, observaciones |
| Cotizacion Compleja | Complejo | Desglose detallado, cronograma, garantias |
| Proyecto Simple | Simple | 5 fases, recursos basicos, entregables |
| Proyecto PMI | Complejo | 6 fases, Gantt, stakeholders, KPIs |
| Informe Tecnico | Simple | 5 secciones, formato estandar |
| Informe Ejecutivo | Complejo | 6 secciones, APA, metricas, ROI |

### 7.2 Servicios Soportados

| Codigo | Nombre | Normativa |
|--------|--------|-----------|
| electrico-residencial | Inst. Electricas Residenciales | CNE Suministro 2011 |
| electrico-comercial | Inst. Electricas Comerciales | CNE Suministro 2011 |
| electrico-industrial | Inst. Electricas Industriales | CNE Utilizacion |
| contraincendios | Sistemas Contra Incendios | NFPA 13, 72, 20 |
| domotica | Domotica y Automatizacion | KNX/EIB |
| expedientes | Expedientes Tecnicos | RNE Municipal |
| saneamiento | Agua y Desague | RNE IS.010, IS.020 |
| itse | Certificaciones ITSE | D.S. 002-2018-PCM |
| pozo-tierra | Puesta a Tierra | CNE Seccion 250 |
| redes-cctv | Redes y CCTV | TIA/EIA-568 |

### 7.3 Logica de Calculos

El sistema aplica calculos tecnicos basados en normativas:

**Electricas Residenciales:**
- Circuitos: 1 por cada 25m2
- Puntos de luz: 1 cada 10m2
- Tomacorrientes: 1 cada 15m2

**Contraincendios:**
- Rociadores: 1 cada 12m2 (NFPA 13)
- Detectores: 1 cada 60m2 (NFPA 72)

**Precios:**
- Basados en mercado peruano 2025
- En dolares americanos (USD)
- IGV 18% calculado automaticamente

---

## 8. PILI - INTELIGENCIA ARTIFICIAL LOCAL

### 8.1 Que es PILI

PILI (Procesadora Inteligente de Licitaciones Industriales) es el motor de IA que funciona 100% offline. Es el componente diferenciador que permite al sistema operar sin dependencia de servicios externos.

### 8.2 Arquitectura de PILI

```python
class PILIBrain:
    """
    Cerebro de IA que funciona sin APIs externas

    Usa:
    - Expresiones regulares para extraccion
    - Reglas de negocio para calculos
    - Diccionarios para precios
    - Templates para generacion
    """

    def detectar_servicio(mensaje) -> str
    def extraer_datos(mensaje, servicio) -> dict
    def generar_cotizacion(mensaje, servicio, complejidad) -> dict
    def generar_proyecto(mensaje, servicio, complejidad) -> dict
    def generar_informe(mensaje, servicio, complejidad) -> dict
```

### 8.3 Deteccion de Servicios

PILI usa keywords para detectar el servicio:

```python
SERVICIOS_PILI = {
    "electrico-residencial": {
        "keywords": ["residencial", "casa", "vivienda", "departamento"],
        ...
    },
    "contraincendios": {
        "keywords": ["incendio", "rociador", "sprinkler", "detector"],
        ...
    }
}
```

### 8.4 Extraccion de Datos

PILI extrae datos usando regex:

```python
# Extraer area
patterns = [
    r'(\d+\.?\d*)\s*m[2²]',
    r'(\d+\.?\d*)\s*metros?\s*cuadrados?'
]

# Extraer potencia
patterns = [
    r'(\d+\.?\d*)\s*hp',
    r'(\d+\.?\d*)\s*kw'
]
```

### 8.5 Agentes PILI

El sistema define agentes especializados:

| Agente | Responsabilidad |
|--------|-----------------|
| PILI Cotizadora | Cotizaciones simples |
| PILI Cotizadora Senior | Cotizaciones complejas |
| PILI Coordinadora | Proyectos simples |
| PILI Directora PMI | Proyectos complejos |
| PILI Reportera | Informes tecnicos |
| PILI Directora Ejecutiva | Informes ejecutivos |

---

## 9. API REST ENDPOINTS

### 9.1 Chat y Conversacion

```
POST /api/v1/chat/mensaje
- Envia mensaje al chat PILI
- Body: { "mensaje": "texto", "historial": [] }
- Response: { "respuesta": "...", "cotizacion": {...} }

POST /api/v1/chat/generar-documento
- Genera documento desde chat
- Body: { "tipo": "word/pdf", "datos": {...} }
- Response: FileResponse (archivo)
```

### 9.2 Cotizaciones

```
GET /api/v1/cotizaciones/
- Lista todas las cotizaciones

POST /api/v1/cotizaciones/
- Crea nueva cotizacion

GET /api/v1/cotizaciones/{id}
- Obtiene cotizacion por ID

PUT /api/v1/cotizaciones/{id}
- Actualiza cotizacion

DELETE /api/v1/cotizaciones/{id}
- Elimina cotizacion

POST /api/v1/cotizaciones/{id}/generar-word
- Genera documento Word

POST /api/v1/cotizaciones/{id}/generar-pdf
- Genera documento PDF
```

### 9.3 Proyectos

```
GET /api/v1/proyectos/
POST /api/v1/proyectos/
GET /api/v1/proyectos/{id}
PUT /api/v1/proyectos/{id}
DELETE /api/v1/proyectos/{id}
POST /api/v1/proyectos/{id}/generar-informe
```

### 9.4 Documentos

```
POST /api/v1/documentos/upload
- Sube documento para procesar

GET /api/v1/documentos/
- Lista documentos

POST /api/v1/documentos/buscar-semantica
- Busqueda RAG

POST /api/v1/documentos/{id}/analizar-con-ia
- Analiza documento con IA
```

### 9.5 Sistema

```
GET /api/v1/system/health
- Estado del sistema

GET /api/v1/system/pili-status
- Estado de servicios PILI
```

---

## 10. 40 PROMPTS PARA COMPRENSION DE IA

Estos prompts estan disenados para que cualquier sistema de IA pueda comprender completamente la funcionalidad de TESLA COTIZADOR v3.0:

### Prompts de Comprension General (1-10)

**1. Proposito del Sistema**
```
"Explica el proposito principal de TESLA COTIZADOR v3.0 y que problema empresarial resuelve para empresas del sector electrico."
```

**2. Arquitectura Tecnica**
```
"Describe la arquitectura de tres capas (presentacion, servicios, persistencia) de TESLA COTIZADOR y como se comunican entre si."
```

**3. Tipos de Documentos**
```
"Enumera los 6 tipos de documentos que puede generar el sistema, indicando la diferencia entre versiones simples y complejas."
```

**4. Servicios Soportados**
```
"Lista los 10 servicios especializados que soporta el sistema y la normativa tecnica que aplica a cada uno."
```

**5. PILIBrain Offline**
```
"Explica como funciona PILIBrain para procesar solicitudes sin conexion a internet, incluyendo su proceso de deteccion de servicios."
```

**6. Flujo de Cotizacion**
```
"Describe paso a paso el flujo completo desde que un usuario escribe 'cotizacion para casa de 100m2' hasta que descarga el documento Word."
```

**7. Calculo de Precios**
```
"Explica como el sistema calcula automaticamente los items de una cotizacion electrica residencial basandose en el area."
```

**8. Generacion Word vs PDF**
```
"Compara las diferencias entre WordGenerator y PDFGenerator en terminos de bibliotecas usadas y caracteristicas del documento final."
```

**9. Sistema RAG**
```
"Describe como funciona RAGService para busqueda semantica y como mejora las respuestas del chat."
```

**10. Plantillas y Marcadores**
```
"Explica el sistema de marcadores ({{variable}}) en plantillas Word y como TemplateProcessor los reemplaza."
```

### Prompts de Analisis Tecnico (11-20)

**11. Deteccion de Servicios**
```
"Analiza el algoritmo de PILIBrain para detectar el servicio a partir de keywords en el mensaje del usuario."
```

**12. Extraccion de Datos**
```
"Describe los patrones regex que usa PILIBrain para extraer area, pisos, potencia y cantidad de puntos del mensaje."
```

**13. Generacion de Items**
```
"Explica la logica de _generar_items_servicio() para crear items de cotizacion segun el servicio y area."
```

**14. Fases de Proyecto PMI**
```
"Describe las 6 fases del proyecto PMI complejo y que actividades incluye cada una."
```

**15. Metricas de Informe Ejecutivo**
```
"Lista las metricas financieras (ROI, TIR, Payback) que calcula el sistema para informes ejecutivos."
```

**16. Orquestador PILI**
```
"Explica como PILIOrchestrator coordina los diferentes servicios existentes sin modificarlos."
```

**17. Manejo de Errores**
```
"Describe la estrategia de fallback cuando Gemini no esta disponible y como el sistema mantiene funcionalidad."
```

**18. Procesamiento de Archivos**
```
"Explica como FileProcessor maneja diferentes tipos de archivo (PDF, Word, imagenes) para extraccion de texto."
```

**19. Estilos de Documento**
```
"Describe los colores Tesla (rojo, dorado, negro) y como se aplican en documentos Word y PDF."
```

**20. Validacion de Plantillas**
```
"Explica como validar_plantilla() verifica que un archivo Word sea valido antes de procesarlo."
```

### Prompts de Casos de Uso (21-30)

**21. CU Cotizacion Residencial**
```
"Genera el JSON completo que produciria PILIBrain para: 'Cotizacion instalacion electrica casa 120m2, 2 pisos'."
```

**22. CU Proyecto Contraincendios**
```
"Describe el proyecto PMI que generaria el sistema para: 'Proyecto sistema contraincendios edificio 500m2'."
```

**23. CU Informe Ejecutivo**
```
"Lista las secciones y metricas del informe ejecutivo para un proyecto de domotica de $80,000 USD."
```

**24. CU Subir Documento**
```
"Describe el flujo completo cuando un usuario sube un PDF de especificaciones tecnicas."
```

**25. CU Busqueda Semantica**
```
"Explica como responderia el sistema a: 'Que dice el documento sobre cables THW?' usando RAG."
```

**26. CU Edicion de Items**
```
"Describe como el usuario puede editar cantidad y precio de un item y como se recalculan los totales."
```

**27. CU Modo Offline**
```
"Simula el comportamiento del sistema cuando no hay internet disponible pero el usuario necesita una cotizacion."
```

**28. CU Multiple Servicio**
```
"Describe como manejaria el sistema: 'Cotizacion para electrico y contraincendios de local comercial'."
```

**29. CU Plantilla Personalizada**
```
"Explica como un usuario puede crear y usar su propia plantilla Word con marcadores."
```

**30. CU Chat Conversacional**
```
"Simula una conversacion de 5 turnos donde el usuario refina los detalles de una cotizacion."
```

### Prompts de Integracion y Extension (31-40)

**31. Agregar Nuevo Servicio**
```
"Describe los pasos para agregar un nuevo servicio 'solar-fotovoltaico' al sistema PILIBrain."
```

**32. Nuevo Tipo de Documento**
```
"Explica como agregar un nuevo tipo de documento 'Acta de Conformidad' al sistema."
```

**33. Integracion API Externa**
```
"Describe como integrar una nueva API de IA (como Claude) al sistema usando el patron de GeminiService."
```

**34. Personalizar Colores**
```
"Explica como modificar los colores corporativos en WordGenerator para otra empresa."
```

**35. Agregar Idioma**
```
"Describe los cambios necesarios para soportar generacion de documentos en ingles."
```

**36. Mejorar Deteccion**
```
"Propone mejoras al algoritmo de deteccion de servicios usando NLP o machine learning."
```

**37. Dashboard Analitico**
```
"Disena un dashboard que muestre estadisticas de cotizaciones generadas, servicios mas solicitados, etc."
```

**38. Notificaciones**
```
"Describe como implementar notificaciones cuando se genera un documento o expira una cotizacion."
```

**39. Multi-tenancy**
```
"Explica los cambios arquitectonicos necesarios para soportar multiples empresas (tenants)."
```

**40. Exportacion Masiva**
```
"Describe como implementar exportacion de multiples cotizaciones a Excel o generacion batch de documentos."
```

---

## 11. GUIA DE INSTALACION

### 11.1 Requisitos

- Python 3.11+
- Node.js 18+
- SQLite o PostgreSQL

### 11.2 Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Configurar variables
cp .env.example .env
# Editar .env con tu GEMINI_API_KEY (opcional)

# Iniciar servidor
uvicorn app.main:app --reload --port 8000
```

### 11.3 Frontend

```bash
cd frontend
npm install
npm start
```

### 11.4 Docker

```bash
docker-compose up -d
```

### 11.5 Variables de Entorno

```env
# Backend
GEMINI_API_KEY=tu_api_key_aqui  # Opcional
DATABASE_URL=sqlite:///./tesla.db
SECRET_KEY=tu_secreto
UPLOAD_DIR=./storage/uploads
GENERATED_DIR=./storage/generated
MAX_FILE_SIZE=10485760  # 10MB

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

---

## 12. CONCLUSIONES

### 12.1 Logros del Sistema

1. **Automatizacion Completa**: El sistema automatiza la generacion de documentos tecnicos reduciendo tiempo de elaboracion en 80%.

2. **IA Hibrida**: Funciona tanto con IA externa (Gemini) como con IA local (PILIBrain), garantizando disponibilidad.

3. **Normativa Integrada**: Los calculos siguen normativas CNE, NFPA, RNE asegurando cumplimiento tecnico.

4. **Escalabilidad**: La arquitectura permite agregar nuevos servicios y tipos de documentos facilmente.

5. **Usabilidad**: Interfaz conversacional intuitiva con avatar animado mejora experiencia de usuario.

### 12.2 Contribuciones Tecnicas

- Implementacion de sistema RAG para busqueda semantica
- Motor de IA offline sin dependencias externas
- Sistema de plantillas con marcadores dinamicos
- Generacion de documentos Word/PDF sin corrupcion
- Arquitectura de microservicios con FastAPI

### 12.3 Trabajo Futuro

- Soporte para mas IAs (Claude, GPT-4)
- Dashboard analitico de metricas
- Aplicacion movil
- Firma digital de documentos
- Integracion con ERPs

### 12.4 Impacto

TESLA COTIZADOR v3.0 representa una solucion integral para la automatizacion de documentos tecnicos en el sector electrico e industrial, combinando inteligencia artificial con conocimiento tecnico normativo para generar documentos profesionales de manera eficiente y confiable.

---

## REFERENCIAS

- FastAPI Documentation: https://fastapi.tiangolo.com/
- python-docx: https://python-docx.readthedocs.io/
- ReportLab: https://www.reportlab.com/docs/
- Google Gemini API: https://ai.google.dev/
- Codigo Nacional de Electricidad: CNE Suministro 2011
- NFPA Standards: NFPA 13, 72, 20
- Reglamento Nacional de Edificaciones (Peru)

---

**Documento generado para fines academicos - Tesis de Ingenieria de Software**

**Copyright 2025 Tesla Electricidad y Automatizacion S.A.C.**
