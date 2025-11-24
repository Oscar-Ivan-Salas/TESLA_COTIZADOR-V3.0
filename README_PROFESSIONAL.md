# TESLA COTIZADOR v4.0 - Sistema Profesional de Generación de Documentos

<p align="center">
  <img src="https://img.shields.io/badge/version-4.0-gold" alt="Version">
  <img src="https://img.shields.io/badge/python-3.11+-blue" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/ML-Local-purple" alt="ML Local">
  <img src="https://img.shields.io/badge/RAG-ChromaDB-orange" alt="RAG">
</p>

## 🎯 Descripción

Sistema de generación de documentos profesionales de **clase mundial** para Tesla Electricidad. Genera cotizaciones, proyectos e informes con:

- **RAG Local**: Búsqueda semántica sin internet
- **ML Local**: Clasificación automática de servicios
- **Gráficas Profesionales**: Gantt, KPIs, matrices de riesgo
- **6 Tipos de Documentos**: Simple y Complejo para cada tipo
- **100% Offline**: Funciona sin conexión a IA externa

---

## 📋 Tipos de Documentos

| Tipo | Simple | Complejo |
|------|--------|----------|
| **Cotización** | Items, totales, observaciones | Análisis de costos, cronograma, garantías |
| **Proyecto** | 5 fases básicas, recursos | PMI completo, Gantt, stakeholders, KPIs |
| **Informe** | Técnico estándar | Ejecutivo APA con gráficas, métricas, ROI |

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    DOCUMENTO GENERATOR PRO               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   FILE      │  │    RAG      │  │     ML      │     │
│  │ PROCESSOR   │  │   ENGINE    │  │   ENGINE    │     │
│  │             │  │             │  │             │     │
│  │ • PDF       │  │ • ChromaDB  │  │ • spaCy     │     │
│  │ • Word      │  │ • Embeddings│  │ • sklearn   │     │
│  │ • Excel     │  │ • Búsqueda  │  │ • NER       │     │
│  │ • OCR       │  │   semántica │  │ • Clasific. │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐                       │
│  │   CHART     │  │    WORD     │                       │
│  │   ENGINE    │  │  GENERATOR  │                       │
│  │             │  │             │                       │
│  │ • Plotly    │  │ • python-   │                       │
│  │ • Gantt     │  │   docx      │                       │
│  │ • KPIs      │  │ • Templates │                       │
│  │ • Matrices  │  │ • Estilos   │                       │
│  └─────────────┘  └─────────────┘                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.11+
- 16GB RAM (recomendado para ML)
- Tesseract OCR (para imágenes)

### Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/Oscar-Ivan-Salas/TESLA_COTIZADOR-V3.0.git
cd TESLA_COTIZADOR-V3.0

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r backend/requirements_professional.txt

# 4. Descargar modelo spaCy español
python -m spacy download es_core_news_sm

# 5. Instalar Tesseract OCR (opcional, para imágenes)
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr tesseract-ocr-spa
# macOS:
brew install tesseract tesseract-lang
# Windows: Descargar de https://github.com/UB-Mannheim/tesseract/wiki

# 6. Ejecutar tests
cd backend
python test_professional_system.py
```

---

## 🐳 Docker (Producción)

### Levantar Stack Completo

```bash
# Construir y levantar
docker-compose -f docker-compose.production.yml up -d

# Ver logs
docker-compose -f docker-compose.production.yml logs -f

# Detener
docker-compose -f docker-compose.production.yml down
```

### Servicios Incluidos

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| Backend | 8000 | API FastAPI con ML |
| Frontend | 80/443 | Nginx + React |
| PostgreSQL | 5432 | Base de datos |
| Redis | 6379 | Cache y Celery |
| Celery | - | Tareas async |

### Recursos Requeridos

- **Backend**: 4GB RAM (incluye modelos ML)
- **PostgreSQL**: 1GB RAM
- **Redis**: 512MB RAM
- **Total recomendado**: 8GB RAM

---

## 📦 Componentes del Sistema

### 1. FileProcessorPro

Procesamiento de múltiples formatos de archivos.

```python
from app.services.professional.processors import FileProcessorPro

processor = FileProcessorPro()

# Procesar PDF
result = processor.process_file("documento.pdf")
print(result["text"])
print(result["tables"])

# Procesar múltiples archivos
results = processor.process_multiple([
    "specs.pdf",
    "costos.xlsx",
    "foto.jpg"
])
```

**Formatos soportados:**
- PDF (texto y tablas con pdfplumber)
- Word (.docx)
- Excel (.xlsx, .xls, .csv)
- Imágenes (PNG, JPG, TIFF) con OCR
- JSON, TXT, XML

### 2. RAGEngine

Sistema de Retrieval Augmented Generation local.

```python
from app.services.professional.rag import RAGEngine

rag = RAGEngine()

# Agregar documentos
rag.add_document(
    "Especificaciones técnicas de instalación eléctrica...",
    metadata={"tipo": "especificaciones"}
)

# Agregar chunks
chunks = ["chunk1...", "chunk2...", "chunk3..."]
rag.add_chunks(chunks, metadata={"source": "manual"})

# Buscar información relevante
results = rag.search("instalación eléctrica residencial", n_results=5)

# Obtener contexto para documento
context = rag.get_context_for_document(
    "cotización para casa 200m2",
    document_type="cotizacion"
)
```

### 3. MLEngine

Machine Learning local para clasificación y NER.

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
    "Casa de 200 metros cuadrados, 2 pisos, presupuesto de S/15000"
)
print(entities["area_principal"])    # 200
print(entities["num_pisos"])         # 2
print(entities["precio_principal"])  # 15000

# Análisis completo
analysis = ml.analyze_text("cotizar sistema contra incendios")
print(analysis["intent"])  # "cotizacion"
```

**Servicios detectables:**
- electrico-residencial
- electrico-comercial
- electrico-industrial
- contraincendios
- domotica
- expedientes
- saneamiento
- itse
- pozo-tierra
- redes-cctv

### 4. ChartEngine

Motor de gráficas profesionales con Plotly.

```python
from app.services.professional.charts import ChartEngine

charts = ChartEngine()

# Gráfico de barras
charts.create_bar_chart(
    {"Materiales": 5000, "Mano de obra": 3000, "Equipos": 2000},
    title="Distribución de Costos"
)

# Diagrama Gantt
tasks = [
    {"nombre": "Planificación", "inicio": "2024-01-01", "fin": "2024-01-07"},
    {"nombre": "Ejecución", "inicio": "2024-01-08", "fin": "2024-01-30"},
    {"nombre": "Cierre", "inicio": "2024-01-31", "fin": "2024-02-05"}
]
charts.create_gantt_chart(tasks, title="Cronograma del Proyecto")

# Dashboard de KPIs
kpis = {
    "ROI": {"valor": 25, "meta": 20, "unidad": "%"},
    "Avance": {"valor": 75, "meta": 100, "unidad": "%"}
}
charts.create_kpi_dashboard(kpis)

# Matriz de riesgos
risks = [
    {"nombre": "Retraso materiales", "probabilidad": 3, "impacto": 4},
    {"nombre": "Cambio alcance", "probabilidad": 4, "impacto": 5}
]
charts.create_risk_matrix(risks)

# Flujo de caja
charts.create_cashflow_chart(
    inflows=[10000, 15000, 20000],
    outflows=[8000, 12000, 10000],
    periods=["Mes 1", "Mes 2", "Mes 3"]
)
```

### 5. DocumentGeneratorPro

Integración completa de todos los componentes.

```python
from app.services.professional.generators import DocumentGeneratorPro
import asyncio

generator = DocumentGeneratorPro()

# Generar documento completo
result = asyncio.run(generator.generate_document(
    message="Cotización para instalación eléctrica residencial de 200m2",
    document_type="cotizacion",
    complexity="complejo",
    uploaded_files=["specs.pdf", "planos.xlsx"],
    logo_base64="data:image/png;base64,..."
))

print(result["file_path"])
print(result["processing_steps"])

# Ver tipos disponibles
types = generator.get_available_document_types()

# Ver estado de componentes
status = generator.get_component_status()
```

---

## 🔌 API Endpoints

### Chat y Generación

```http
POST /api/chat
Content-Type: application/json

{
  "mensaje": "Necesito cotizar instalación eléctrica para casa de 150m2",
  "tipo_flujo": "cotizacion-simple",
  "historial": []
}
```

### Generación de Documentos

```http
POST /api/documentos/generar
Content-Type: application/json

{
  "mensaje": "Casa residencial de 200m2, 2 pisos",
  "tipo_documento": "cotizacion",
  "complejidad": "complejo",
  "formato": "word",
  "logo_base64": "..."
}
```

### Subida de Archivos

```http
POST /api/archivos/upload
Content-Type: multipart/form-data

files: [archivo1.pdf, archivo2.xlsx]
```

### Estado del Sistema

```http
GET /api/system/status
```

---

## 📊 Estructura de Datos

### Cotización

```json
{
  "numero": "COT-202411241230",
  "cliente": "Juan Pérez",
  "proyecto": "Instalación Eléctrica Residencial",
  "fecha": "24/11/2024",
  "vigencia": "30 días",
  "items": [
    {
      "descripcion": "Tablero eléctrico",
      "cantidad": 1,
      "unidad": "und",
      "precio_unitario": 450,
      "total": 450
    }
  ],
  "subtotal": 5000,
  "igv": 900,
  "total": 5900,
  "observaciones": "Incluye materiales y mano de obra"
}
```

### Proyecto PMI

```json
{
  "nombre": "Proyecto Instalación Industrial",
  "codigo": "PROY-202411241230-PMI",
  "cliente": "Empresa SAC",
  "fecha_inicio": "01/12/2024",
  "fecha_fin": "15/02/2025",
  "duracion_total_dias": 76,
  "presupuesto_estimado": 150000,
  "fases": [
    {
      "nombre": "Inicio y Planificación",
      "duracion_dias": 10,
      "actividades": ["..."],
      "entregable": "Project Charter"
    }
  ],
  "kpis": {
    "SPI": 1.0,
    "CPI": 1.0
  },
  "cronograma_gantt": {...}
}
```

### Informe Ejecutivo APA

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
    "tir_proyectada": 30
  },
  "graficos_sugeridos": [
    "Dashboard ejecutivo de KPIs",
    "Diagrama de Gantt",
    "Matriz de riesgos"
  ],
  "bibliografia": [...]
}
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
cd backend
python test_professional_system.py
```

### Tests Incluidos

1. **Imports de módulos**
2. **FileProcessor** - Procesamiento de archivos
3. **RAGEngine** - Indexación y búsqueda
4. **MLEngine** - Clasificación y NER
5. **ChartEngine** - Generación de gráficas
6. **DocumentGenerator** - Generación completa
7. **WordGenerator** - Creación de Word
8. **Integración** - Flujo completo

---

## 📁 Estructura del Proyecto

```
TESLA_COTIZADOR-V3.0/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── professional/           # Sistema v4.0
│   │   │   │   ├── processors/         # FileProcessorPro
│   │   │   │   ├── rag/                # RAGEngine
│   │   │   │   ├── ml/                 # MLEngine
│   │   │   │   ├── charts/             # ChartEngine
│   │   │   │   └── generators/         # DocumentGeneratorPro
│   │   │   ├── word_generator.py
│   │   │   ├── pdf_generator.py
│   │   │   └── pili_integrator.py
│   │   ├── routers/
│   │   ├── models/
│   │   └── templates/
│   ├── storage/
│   │   ├── uploads/
│   │   ├── generated/
│   │   └── embeddings/
│   ├── requirements_professional.txt
│   └── test_professional_system.py
├── frontend/
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── nginx.conf
└── docker-compose.production.yml
```

---

## ⚙️ Configuración

### Variables de Entorno

```bash
# .env
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@localhost:5432/tesla_db
REDIS_URL=redis://localhost:6379/0
STORAGE_PATH=/app/storage

# Opcional: API Key de Gemini (para modo online)
GEMINI_API_KEY=your_api_key
```

### Modos de Operación

| Modo | Descripción |
|------|-------------|
| **ONLINE** | Usa Gemini + ML local |
| **OFFLINE** | Solo ML local (100% sin internet) |
| **FALLBACK** | Plantillas predefinidas |

---

## 🔧 Dependencias Principales

### Core
- FastAPI >= 0.104.0
- SQLAlchemy >= 2.0.0
- Pydantic >= 2.5.0

### Documentos
- python-docx >= 1.1.0
- reportlab >= 4.0.0
- pdfplumber >= 0.10.0

### Visualización
- plotly >= 5.18.0
- kaleido >= 0.2.1
- matplotlib >= 3.8.0

### Machine Learning
- scikit-learn >= 1.3.0
- sentence-transformers >= 2.2.0
- spacy >= 3.7.0
- chromadb >= 0.4.0

### OCR
- pytesseract >= 0.3.10
- Pillow >= 10.1.0

---

## 📈 Rendimiento

### Consumo de Recursos

| Operación | RAM | Tiempo |
|-----------|-----|--------|
| Clasificación ML | ~500MB | <100ms |
| Búsqueda RAG | ~1GB | <500ms |
| Generación gráficas | ~200MB | 1-3s |
| Documento complejo | ~2GB | 5-10s |
| OCR imagen | ~500MB | 2-5s |

### Recomendaciones

- **Desarrollo**: 8GB RAM
- **Producción**: 16GB RAM
- **GPU**: No requerida (todo en CPU)

---

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: agregar funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es propiedad de **Tesla Electricidad y Automatización S.A.C.**

---

## 📞 Contacto

- **Email**: ingenieria.teslaelectricidad@gmail.com
- **Teléfono**: 906315961
- **Dirección**: Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL

---

## 🙏 Créditos

Desarrollado con tecnologías de clase mundial:

- [FastAPI](https://fastapi.tiangolo.com/)
- [Plotly](https://plotly.com/)
- [ChromaDB](https://www.trychroma.com/)
- [spaCy](https://spacy.io/)
- [Sentence-Transformers](https://www.sbert.net/)

---

<p align="center">
  <strong>TESLA ELECTRICIDAD v4.0</strong><br>
  Sistema Profesional de Generación de Documentos<br>
  <em>"Documentos de clase mundial, 100% offline"</em>
</p>
