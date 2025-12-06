# CLAUDE.md - Tesla Cotizador V3.0

> **Guía completa para asistentes de IA trabajando en este repositorio**
> Última actualización: 2025-12-04
> Versión del proyecto: 3.0.0

---

## 📋 Tabla de Contenidos

- [Visión General del Proyecto](#-visión-general-del-proyecto)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Estructura de Directorios](#-estructura-de-directorios)
- [Stack Tecnológico](#-stack-tecnológico)
- [Convenciones de Código](#-convenciones-de-código)
- [Flujos de Trabajo de Desarrollo](#-flujos-de-trabajo-de-desarrollo)
- [Componentes Clave](#-componentes-clave)
- [Base de Datos](#-base-de-datos)
- [Servicios de IA](#-servicios-de-ia)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Notas Importantes para IA](#-notas-importantes-para-ia)

---

## 🎯 Visión General del Proyecto

**Tesla Cotizador V3.0** es un sistema profesional de cotización y gestión de proyectos para **TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.**, una empresa especializada en servicios eléctricos y de automatización en Perú.

### Propósito Principal

El sistema permite:
1. **Generar cotizaciones automáticas** usando IA (Gemini 1.5 Pro)
2. **Gestionar proyectos complejos** con documentos, cronogramas y recursos
3. **Crear informes profesionales** en formato Word y PDF
4. **Interacción conversacional** con PILI, el agente IA integrado
5. **Análisis de documentos** con OCR y búsqueda semántica (RAG)

### Usuarios Objetivo

- Ingenieros y técnicos de Tesla Electricidad
- Gerentes de proyectos
- Personal de ventas
- Clientes (vía interfaz web)

### Servicios que Cotiza

- ⚡ Instalaciones eléctricas
- 📋 Certificados ITSE
- 🔌 Puestas a tierra
- 🔥 Sistemas contra incendios
- 🏠 Domótica
- 📹 CCTV
- 🌐 Redes de datos
- ⚙️ Automatización industrial

---

## 🏗️ Arquitectura del Sistema

### Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    TESLA COTIZADOR V3.0                     │
│                   Arquitectura de 3 Capas                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐      ┌─────────────────┐      ┌──────────────┐
│   FRONTEND      │◄────►│    BACKEND      │◄────►│   STORAGE    │
│                 │ HTTP │                 │ I/O  │              │
│  React 18       │      │  FastAPI        │      │ File System  │
│  Tailwind CSS   │      │  SQLAlchemy     │      │ SQLite/PG    │
│  Lucide Icons   │      │  Pydantic       │      │ ChromaDB     │
└─────────────────┘      └─────────────────┘      └──────────────┘
                                │
                                │ API Calls
                                ▼
                    ┌───────────────────────┐
                    │    SERVICIOS IA       │
                    │                       │
                    │  - Gemini 1.5 Pro    │
                    │  - ChromaDB (RAG)    │
                    │  - Sentence Trans.   │
                    │  - Multi-IA Support  │
                    └───────────────────────┘
```

### Flujo de Datos Principal

```
1. Usuario → Frontend (React) → Solicitud HTTP
2. Backend (FastAPI) → Valida y procesa
3. Servicios IA → Genera contenido inteligente
4. Base de Datos → Persiste información
5. Generadores → Crea documentos (Word/PDF)
6. Backend → Retorna respuesta JSON
7. Frontend → Renderiza vista previa
8. Usuario → Descarga documento final
```

### Patrón de Arquitectura

**Arquitectura Híbrida:**
- **Microservicios internos**: Servicios especializados (Gemini, RAG, generadores)
- **Monolito modular**: Backend FastAPI con routers separados
- **SPA**: Frontend React de una sola página
- **Event-driven**: Chat conversacional con historial
- **Degradación elegante**: Sistema funciona incluso si algunos routers no cargan (modo fallback)
- **Carga dinámica de routers**: Cada router se importa individualmente con manejo robusto de errores

---

## 📁 Estructura de Directorios

### Estructura Completa

```
TESLA_COTIZADOR-V3.0/
│
├── backend/                      # Backend FastAPI
│   ├── app/
│   │   ├── core/                # Configuración central
│   │   │   ├── config.py       # Settings con Pydantic
│   │   │   ├── database.py     # SQLAlchemy setup
│   │   │   └── __init__.py
│   │   │
│   │   ├── models/              # Modelos SQLAlchemy (ORM)
│   │   │   ├── cotizacion.py   # Modelo Cotización
│   │   │   ├── item.py         # Modelo Item (líneas de cotización)
│   │   │   ├── proyecto.py     # Modelo Proyecto
│   │   │   ├── documento.py    # Modelo Documento
│   │   │   └── __init__.py
│   │   │
│   │   ├── schemas/             # Schemas Pydantic (validación)
│   │   │   ├── cotizacion.py
│   │   │   ├── proyecto.py
│   │   │   ├── documento.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── routers/             # Endpoints API (controladores)
│   │   │   ├── chat.py         # PILI - Chat IA (~84KB, endpoint principal)
│   │   │   ├── cotizaciones.py # CRUD cotizaciones (~12KB)
│   │   │   ├── proyectos.py    # CRUD proyectos (~26KB)
│   │   │   ├── informes.py     # Generación de informes
│   │   │   ├── documentos.py   # Upload y análisis (~24KB)
│   │   │   ├── generar_directo.py # Generación directa Word/PDF
│   │   │   ├── auth.py         # Autenticación (básico)
│   │   │   ├── system.py       # Health checks
│   │   │   └── __init__.py
│   │   │
│   │   ├── services/            # Lógica de negocio
│   │   │   ├── gemini_service.py        # Cliente Gemini AI
│   │   │   ├── multi_ia_service.py      # Soporte multi-IA
│   │   │   ├── pili_brain.py            # Cerebro de PILI
│   │   │   ├── pili_orchestrator.py     # Orquestador PILI
│   │   │   ├── pili_integrator.py       # Integración PILI
│   │   │   ├── word_generator.py        # Generador Word
│   │   │   ├── pdf_generator.py         # Generador PDF
│   │   │   ├── file_processor.py        # Procesador archivos
│   │   │   ├── rag_service.py           # RAG con ChromaDB
│   │   │   ├── template_processor.py    # Procesador plantillas
│   │   │   ├── report_generator.py      # Generador informes
│   │   │   │
│   │   │   └── professional/            # Servicios avanzados
│   │   │       ├── ml/                  # Machine Learning
│   │   │       ├── rag/                 # RAG avanzado
│   │   │       ├── processors/          # Procesadores pro
│   │   │       ├── charts/              # Generador gráficos
│   │   │       └── generators/          # Generadores pro
│   │   │
│   │   ├── utils/               # Utilidades
│   │   │   ├── ocr.py          # OCR para imágenes
│   │   │   ├── helpers.py      # Funciones auxiliares
│   │   │   └── __init__.py
│   │   │
│   │   ├── templates/           # Plantillas HTML/Jinja2
│   │   └── main.py             # Aplicación FastAPI principal
│   │
│   ├── storage/                 # Almacenamiento de archivos
│   │   ├── documentos/         # Archivos subidos
│   │   └── generados/          # Documentos generados
│   │
│   ├── logs/                    # Logs de la aplicación
│   ├── requirements.txt         # Dependencias Python
│   ├── Dockerfile              # Docker backend
│   ├── .env.example            # Variables de entorno ejemplo
│   └── README.md
│
├── frontend/                    # Frontend React
│   ├── public/
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   │
│   ├── src/
│   │   ├── components/          # Componentes React
│   │   │   ├── ChatIA.jsx      # Componente chat PILI
│   │   │   ├── PiliAvatar.jsx  # Avatar animado PILI
│   │   │   ├── UploadZone.jsx  # Zona de carga archivos
│   │   │   ├── CotizacionEditor.jsx  # Editor cotizaciones
│   │   │   ├── VistaPrevia.jsx # Vista previa documentos
│   │   │   └── Alerta.jsx      # Componente alertas
│   │   │
│   │   ├── services/
│   │   │   └── api.js          # Cliente API (Fetch)
│   │   │
│   │   ├── App.jsx             # Componente principal
│   │   ├── index.js            # Entry point
│   │   ├── index.css           # Estilos globales
│   │   └── setupProxy.js       # Proxy para desarrollo
│   │
│   ├── package.json
│   ├── tailwind.config.js      # Configuración Tailwind
│   ├── .eslintrc.json          # Configuración ESLint
│   ├── .prettierrc             # Configuración Prettier
│   └── Dockerfile
│
├── storage/                     # Storage raíz del proyecto
│   ├── documentos/             # Documentos subidos
│   ├── generados/              # Documentos generados
│   ├── templates/              # Plantillas Word/HTML
│   ├── chroma_db/              # Base de datos ChromaDB
│   └── proyectos/              # Carpetas de proyectos
│       └── proyecto_1/
│           ├── documentos/
│           ├── cotizaciones/
│           ├── informes/
│           └── archivos_originales/
│
├── database/                    # Base de datos SQLite
│   └── tesla_cotizador.db
│
├── docker/                      # Configuración Docker
├── docs/                        # Documentación adicional
│
├── docker-compose.yml           # Orquestación Docker
├── docker-compose.production.yml
├── .gitignore
├── .env.example
├── README.md                    # README principal
├── README_PROFESSIONAL.md       # README profesional
├── README_TESIS.md             # README para tesis
├── INSTRUCCIONES_INSTALACION.md
├── INSTRUCCIONES_MULTI_IA.md
└── CLAUDE.md                   # Este archivo
```

### Directorios Importantes

| Directorio | Propósito | Notas |
|------------|-----------|-------|
| `backend/app/routers/` | Endpoints API | Cada router maneja un dominio específico |
| `backend/app/services/` | Lógica de negocio | Servicios reutilizables, desacoplados |
| `backend/app/models/` | Modelos de datos | Definición de tablas SQLAlchemy |
| `backend/app/schemas/` | Validación | Schemas Pydantic para request/response |
| `frontend/src/components/` | UI React | Componentes reutilizables |
| `storage/` | Archivos | **NUNCA** commitear a git |

---

## 🛠️ Stack Tecnológico

### Backend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.11+ / 3.12 | Lenguaje principal (compatible con ambas versiones) |
| **FastAPI** | 0.115.6 | Framework web moderno y rápido |
| **Uvicorn** | 0.34.0 | Servidor ASGI de alto rendimiento |
| **SQLAlchemy** | 2.0.36 | ORM para base de datos |
| **Pydantic** | 2.10.6 | Validación de datos con type hints |
| **google-generativeai** | 0.8.3 | Cliente oficial Gemini AI |
| **chromadb** | 0.5.23 | Base de datos vectorial (RAG) |
| **sentence-transformers** | 3.4.0 | Embeddings para búsqueda semántica |
| **python-docx** | 1.1.2 | Generación de documentos Word |
| **reportlab** | 4.4.5 | Generación de documentos PDF |
| **weasyprint** | 63.1 | Conversión HTML a PDF profesional |
| **pypdf** | 5.2.0 | Procesamiento y manipulación de PDFs |
| **pytest** | 8.3.5 | Framework de testing |
| **httpx** | 0.28.1 | Cliente HTTP asíncrono |

### Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **React** | 18.2.0 | Framework UI |
| **react-scripts** | 5.0.1 | Toolchain React |
| **Tailwind CSS** | 3.3.6 | Framework CSS utility-first |
| **lucide-react** | 0.294.0 | Librería de iconos |
| **ESLint** | 8.55.0 | Linter JavaScript |
| **Prettier** | 3.1.1 | Formateador código |

### Base de Datos

- **Desarrollo**: SQLite 3 (archivo `database/tesla_cotizador.db`)
- **Producción**: PostgreSQL 15+ (configurable)
- **Vector DB**: ChromaDB (para RAG)

### Infraestructura

- **Docker** & **Docker Compose** para contenedores
- **Nginx** para reverse proxy en producción
- **Git** para control de versiones

---

## 📐 Convenciones de Código

### Python (Backend)

#### Estilo de Código

```python
# Seguir PEP 8
# - Indentación: 4 espacios
# - Línea máxima: 100 caracteres
# - Imports ordenados: stdlib, third-party, local

# ✅ BUENO
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.models.cotizacion import Cotizacion
from app.schemas.cotizacion import CotizacionCreate
from app.core.database import get_db

# ❌ MALO
from app.models.cotizacion import Cotizacion
from pathlib import Path
from fastapi import APIRouter, HTTPException
```

#### Nomenclatura

```python
# Archivos: snake_case
# archivo: gemini_service.py

# Clases: PascalCase
class CotizacionService:
    pass

# Funciones y variables: snake_case
def generar_cotizacion(datos: dict) -> Cotizacion:
    total_items = calcular_total(datos)
    return total_items

# Constantes: UPPER_CASE
MAX_UPLOAD_SIZE = 10 * 1024 * 1024
API_VERSION = "3.0.0"

# Variables privadas: prefijo _
class MiClase:
    def __init__(self):
        self._variable_privada = 10
```

#### Docstrings

```python
def generar_cotizacion(
    datos: dict,
    incluir_igv: bool = True
) -> dict:
    """
    Genera una cotización a partir de datos estructurados.

    Args:
        datos: Diccionario con información del cliente y servicios
        incluir_igv: Si True, incluye IGV en el cálculo (default: True)

    Returns:
        dict: Cotización generada con estructura completa

    Raises:
        ValueError: Si los datos no tienen estructura válida

    Example:
        >>> datos = {"cliente": "ABC", "items": [...]}
        >>> cotizacion = generar_cotizacion(datos)
    """
    pass
```

#### Type Hints

```python
# Siempre usar type hints
from typing import List, Dict, Optional, Union

def procesar_items(
    items: List[Dict[str, Union[str, float]]],
    descuento: Optional[float] = None
) -> float:
    total: float = 0.0
    for item in items:
        cantidad: int = int(item["cantidad"])
        precio: float = float(item["precio"])
        total += cantidad * precio

    if descuento:
        total *= (1 - descuento)

    return total
```

### JavaScript/React (Frontend)

#### Estilo de Código

```javascript
// Seguir estándares ES6+
// - Indentación: 2 espacios
// - Usar const/let, NO var
// - Arrow functions cuando sea apropiado
// - Destructuring cuando mejore legibilidad

// ✅ BUENO
const handleSubmit = async (event) => {
  event.preventDefault();
  const { nombre, email } = formData;

  try {
    const response = await api.crearCotizacion({ nombre, email });
    setExito(true);
  } catch (error) {
    setError(error.message);
  }
};

// ❌ MALO
var handleSubmit = function(event) {
  event.preventDefault();
  var nombre = formData.nombre;
  var email = formData.email;
  // ...
};
```

#### Nomenclatura React

```javascript
// Componentes: PascalCase
const CotizacionEditor = () => { /* ... */ };

// Hooks personalizados: prefijo "use"
const useFormValidation = (initialValues) => { /* ... */ };

// Funciones y variables: camelCase
const handleClick = () => {};
const userName = "Tesla";

// Constantes: UPPER_CASE
const API_BASE_URL = "http://localhost:8000";
const MAX_FILE_SIZE = 10 * 1024 * 1024;

// Props: camelCase
<CotizacionEditor
  cotizacionId={1}
  onSave={handleSave}
  isEditable={true}
/>
```

#### Estructura de Componentes

```javascript
import React, { useState, useEffect } from 'react';
import { Upload, Save } from 'lucide-react';

/**
 * Componente para editar cotizaciones
 * @param {Object} props - Props del componente
 * @param {number} props.cotizacionId - ID de la cotización
 * @param {Function} props.onSave - Callback al guardar
 */
const CotizacionEditor = ({ cotizacionId, onSave }) => {
  // 1. Estados
  const [datos, setDatos] = useState(null);
  const [loading, setLoading] = useState(false);

  // 2. Effects
  useEffect(() => {
    cargarCotizacion();
  }, [cotizacionId]);

  // 3. Funciones auxiliares
  const cargarCotizacion = async () => {
    // ...
  };

  const handleSubmit = async (e) => {
    // ...
  };

  // 4. Renderizado
  return (
    <div className="p-4">
      {/* JSX */}
    </div>
  );
};

export default CotizacionEditor;
```

### Tailwind CSS

```javascript
// Orden de clases Tailwind (recomendado):
// 1. Layout (flex, grid, etc.)
// 2. Spacing (p-, m-, etc.)
// 3. Sizing (w-, h-, etc.)
// 4. Typography (text-, font-, etc.)
// 5. Colors (bg-, text-, border-)
// 6. Effects (shadow-, opacity-, etc.)
// 7. Interactions (hover:, focus:, etc.)

<div className="flex flex-col p-4 w-full max-w-lg text-lg font-semibold text-gray-800 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
  Contenido
</div>
```

### Git Commits

```bash
# Formato de commits:
# tipo(alcance): descripción breve

# Tipos:
# - feat: Nueva funcionalidad
# - fix: Corrección de bug
# - docs: Documentación
# - style: Formato (sin cambio de código)
# - refactor: Refactorización
# - test: Tests
# - chore: Tareas de mantenimiento

# Ejemplos:
git commit -m "feat(cotizaciones): agregar generación automática de Word"
git commit -m "fix(chat): corregir error al enviar mensaje vacío"
git commit -m "docs(readme): actualizar instrucciones de instalación"
git commit -m "refactor(services): separar lógica de Gemini en módulo"
```

---

## 🔄 Flujos de Trabajo de Desarrollo

### Información Importante sobre Branches

**IMPORTANTE para Asistentes de IA**:
- Cuando trabajes en este proyecto, siempre verifica el branch actual con `git branch`
- Los branches de Claude Code siguen el patrón: `claude/claude-md-{id}-{session-id}`
- **NUNCA** hagas push a main/master directamente
- **SIEMPRE** usa el branch designado para tu sesión de trabajo
- Al finalizar cambios importantes, se debe crear un Pull Request para revisión

**Branch actual de trabajo**: Verificar con `git status` o `git branch`

### Flujo de Desarrollo Local

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd TESLA_COTIZADOR-V3.0

# 2. Backend - Crear entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias backend
cd backend
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar GEMINI_API_KEY

# 5. Frontend - Instalar dependencias
cd ../frontend
npm install

# 6. Ejecutar backend (terminal 1)
cd ../backend
uvicorn app.main:app --reload
# Backend disponible en http://localhost:8000

# 7. Ejecutar frontend (terminal 2)
cd frontend
npm start
# Frontend disponible en http://localhost:3000
```

### Flujo con Docker

```bash
# 1. Configurar .env
cp .env.example .env
# Editar .env

# 2. Levantar servicios
docker-compose up -d

# 3. Ver logs
docker-compose logs -f

# 4. Detener servicios
docker-compose down
```

### Workflow de Features

```bash
# 1. Crear rama desde main
git checkout main
git pull origin main
git checkout -b feature/nombre-feature

# 2. Desarrollar feature
# ... hacer cambios ...

# 3. Commit frecuentes
git add .
git commit -m "feat(modulo): descripción clara"

# 4. Push a repositorio
git push origin feature/nombre-feature

# 5. Crear Pull Request
# En GitHub, crear PR desde feature/nombre-feature a main

# 6. Code review y merge
# Esperar aprobación y merge
```

### Workflow de Bugfix

```bash
# 1. Crear rama bugfix
git checkout -b fix/descripcion-bug

# 2. Reproducir y corregir bug
# ... hacer cambios ...

# 3. Agregar tests si es posible
pytest tests/test_correccion.py

# 4. Commit
git commit -m "fix(modulo): corregir problema X"

# 5. Push y PR
git push origin fix/descripcion-bug
# Crear PR en GitHub
```

---

## 🧩 Componentes Clave

### Backend - Routers

#### chat.py - PILI (Agente IA)

**Ubicación**: `backend/app/routers/chat.py`

**Propósito**: Endpoints para interacción con PILI, el agente IA conversacional.

**Endpoints principales**:
- `POST /api/chat/mensaje` - Chat conversacional general con PILI
- `POST /api/chat/generar-cotizacion-rapida` - Generación rápida (5-15 min)
- `POST /api/chat/generar-cotizacion-compleja` - Generación compleja con análisis
- `POST /api/chat/generar-proyecto` - Creación de proyectos
- `POST /api/chat/generar-informe` - Generación de informes
- `GET /api/chat/botones-contextuales/{tipo_flujo}` - Botones inteligentes contextuales
- `POST /api/generar-documento-directo` - Generación directa de documentos sin BD

**Servicios que utiliza**:
- `gemini_service` - Cliente Gemini AI
- `pili_brain` - Cerebro de PILI
- `rag_service` - Búsqueda semántica

#### cotizaciones.py

**Ubicación**: `backend/app/routers/cotizaciones.py`

**Propósito**: CRUD completo de cotizaciones.

**Endpoints**:
- `POST /api/cotizaciones/` - Crear cotización
- `GET /api/cotizaciones/` - Listar cotizaciones
- `GET /api/cotizaciones/{id}` - Obtener cotización específica
- `PUT /api/cotizaciones/{id}` - Actualizar cotización
- `DELETE /api/cotizaciones/{id}` - Eliminar cotización
- `POST /api/cotizaciones/{id}/generar-word` - Generar documento Word
- `POST /api/cotizaciones/{id}/generar-pdf` - Generar documento PDF
- `GET /api/cotizaciones/{id}/exportar/{formato}` - Exportar en Word/PDF/JSON

#### proyectos.py

**Ubicación**: `backend/app/routers/proyectos.py`

**Propósito**: Gestión de proyectos complejos.

**Funcionalidades**:
- Creación de proyectos con estructura de carpetas automática
- Asignación de recursos y cronogramas
- Gestión de hitos y fases
- Vinculación con múltiples cotizaciones

#### informes.py

**Ubicación**: `backend/app/routers/informes.py`

**Propósito**: Generación de informes ejecutivos y técnicos.

**Tipos de informes**:
- Informe simple (PDF básico)
- Informe ejecutivo (Word con formato APA)
- Informe técnico (con gráficos y tablas)

#### documentos.py

**Ubicación**: `backend/app/routers/documentos.py`

**Propósito**: Upload, análisis y búsqueda de documentos.

**Funcionalidades**:
- Upload de múltiples formatos (PDF, Word, Excel, imágenes)
- OCR para documentos escaneados
- Indexación en ChromaDB para RAG
- Búsqueda semántica

### Backend - Services

#### gemini_service.py

**Ubicación**: `backend/app/services/gemini_service.py`

**Propósito**: Cliente para Google Gemini AI.

**Clase principal**: `GeminiService`

**Métodos importantes**:
```python
async def chat_conversacional(
    mensaje: str,
    contexto: str,
    historial: List[dict]
) -> dict:
    """Chat conversacional con historial"""

async def generar_cotizacion_estructurada(
    descripcion: str,
    archivos_contexto: List[str]
) -> dict:
    """Genera cotización estructurada desde descripción"""

async def analizar_documento(
    texto: str,
    tipo_analisis: str
) -> dict:
    """Analiza documentos con IA"""
```

#### pili_brain.py

**Ubicación**: `backend/app/services/pili_brain.py`

**Propósito**: Cerebro de PILI - Lógica de razonamiento del agente.

**Funcionalidades**:
- Comprensión de intención del usuario
- Generación de respuestas contextuales
- Gestión de flujos conversacionales
- Aprendizaje de proyectos históricos

#### word_generator.py

**Ubicación**: `backend/app/services/word_generator.py`

**Propósito**: Generación de documentos Word profesionales.

**Clase principal**: `WordGenerator`

**Método principal**:
```python
def generar_cotizacion(
    datos: dict,
    ruta_salida: Path,
    opciones: dict = None,
    logo_base64: str = None
) -> Path:
    """
    Genera cotización en Word

    Args:
        datos: Datos de cotización (cliente, items, totales)
        ruta_salida: Ruta donde guardar el archivo
        opciones: Configuración de visualización
            - mostrarPreciosUnitarios: bool
            - mostrarPreciosTotales: bool
            - mostrarIGV: bool
            - incluirLogo: bool
        logo_base64: Logo en base64 (opcional)

    Returns:
        Path al archivo generado
    """
```

#### rag_service.py

**Ubicación**: `backend/app/services/rag_service.py`

**Propósito**: Retrieval-Augmented Generation con ChromaDB.

**Funcionalidades**:
- Indexación de documentos en ChromaDB
- Búsqueda semántica por similitud
- Recuperación de contexto para IA
- Gestión de colecciones vectoriales

### Frontend - Componentes

#### App.jsx

**Ubicación**: `frontend/src/App.jsx`

**Propósito**: Componente principal de la aplicación.

**Estados principales**:
```javascript
const [pantallaActual, setPantallaActual] = useState('inicio');
const [tipoFlujo, setTipoFlujo] = useState(null);
const [conversacion, setConversacion] = useState([]);
const [cotizacion, setCotizacion] = useState(null);
const [proyecto, setProyecto] = useState(null);
const [informe, setInforme] = useState(null);
```

**Pantallas**:
- `inicio` - Dashboard principal
- `cotizacion-rapida` - Flujo rápido de cotización
- `cotizacion-compleja` - Flujo complejo con chat
- `proyecto-simple` - Creación de proyecto básico
- `proyecto-complejo` - Proyecto con Gantt y recursos
- `informe-simple` - Informe PDF básico
- `informe-ejecutivo` - Informe Word profesional

#### ChatIA.jsx

**Ubicación**: `frontend/src/components/ChatIA.jsx`

**Propósito**: Componente de chat con PILI.

**Props**:
```javascript
{
  mensajes: Array<{role: 'user'|'assistant', content: string}>,
  onEnviarMensaje: (mensaje: string) => void,
  cargando: boolean,
  botonesContextuales: Array<string>
}
```

#### PiliAvatar.jsx

**Ubicación**: `frontend/src/components/PiliAvatar.jsx`

**Propósito**: Avatar animado de PILI con animaciones CSS.

**Estados**:
- `idle` - En espera
- `listening` - Escuchando usuario
- `thinking` - Procesando
- `speaking` - Respondiendo

#### CotizacionEditor.jsx

**Ubicación**: `frontend/src/components/CotizacionEditor.jsx`

**Propósito**: Editor visual de cotizaciones.

**Funcionalidades**:
- Edición inline de items
- Cálculo automático de totales
- Agregar/eliminar items
- Vista previa en tiempo real

---

## 🗄️ Base de Datos

### Modelos SQLAlchemy

#### Cotizacion

**Ubicación**: `backend/app/models/cotizacion.py`

**Tabla**: `cotizaciones`

**Campos**:
```python
class Cotizacion(Base):
    __tablename__ = "cotizaciones"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(50), unique=True, index=True)  # COT-202511-0001
    cliente = Column(String(200))
    proyecto = Column(String(200))
    descripcion = Column(Text, nullable=True)

    # Relaciones
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=True)

    # Fechas
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, onupdate=datetime.utcnow)
    fecha_vencimiento = Column(Date, nullable=True)

    # Estado
    estado = Column(String(50), default="borrador")  # borrador, enviada, aprobada, rechazada

    # Totales
    subtotal = Column(Float, default=0.0)
    igv = Column(Float, default=0.0)
    total = Column(Float, default=0.0)

    # Relaciones
    items = relationship("Item", back_populates="cotizacion", cascade="all, delete-orphan")
    proyecto_rel = relationship("Proyecto", back_populates="cotizaciones")
```

#### Item

**Ubicación**: `backend/app/models/item.py`

**Tabla**: `items`

**Campos**:
```python
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    cotizacion_id = Column(Integer, ForeignKey("cotizaciones.id"))

    descripcion = Column(String(500))
    cantidad = Column(Float)
    unidad = Column(String(20), default="und")  # und, m, m2, m3, kg, etc.
    precio_unitario = Column(Float)

    # Calculado
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    # Relaciones
    cotizacion = relationship("Cotizacion", back_populates="items")
```

#### Proyecto

**Ubicación**: `backend/app/models/proyecto.py`

**Tabla**: `proyectos`

**Campos**:
```python
class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200))
    cliente = Column(String(200))
    descripcion = Column(Text, nullable=True)

    # Gestión
    presupuesto_estimado = Column(Float, nullable=True)
    duracion_meses = Column(Integer, nullable=True)

    # Estado
    estado = Column(String(50), default="planificacion")  # planificacion, ejecucion, finalizado

    # Fechas
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    cotizaciones = relationship("Cotizacion", back_populates="proyecto_rel")
    documentos = relationship("Documento", back_populates="proyecto")
```

#### Documento

**Ubicación**: `backend/app/models/documento.py`

**Tabla**: `documentos`

**Campos**:
```python
class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200))
    ruta = Column(String(500))
    tipo = Column(String(50))  # pdf, docx, xlsx, imagen

    # Contenido extraído
    contenido_texto = Column(Text, nullable=True)

    # Metadata
    tamano_bytes = Column(Integer)
    fecha_upload = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=True)
    proyecto = relationship("Proyecto", back_populates="documentos")
```

### Migraciones

El proyecto usa **Alembic** para migraciones de base de datos.

```bash
# Crear migración
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migración
alembic upgrade head

# Revertir migración
alembic downgrade -1
```

---

## 🤖 Servicios de IA

### Gemini 1.5 Pro

**Configuración**: `backend/.env`

```env
GEMINI_API_KEY=tu_api_key_aqui
GEMINI_MODEL=gemini-1.5-pro
TEMPERATURE=0.3
MAX_TOKENS=4000
```

**Usos principales**:
1. **Chat conversacional** con PILI
2. **Generación de cotizaciones** desde lenguaje natural
3. **Análisis de documentos** técnicos
4. **Sugerencias inteligentes** de items y precios

### Soporte Multi-IA

El sistema soporta múltiples proveedores de IA:

**Ubicación**: `backend/app/services/multi_ia_service.py`

**Proveedores soportados**:
- ✅ **Gemini** (Google) - Por defecto, recomendado
- ⚠️ **OpenAI** (ChatGPT) - Opcional, requiere API key
- ⚠️ **Anthropic** (Claude) - Opcional, requiere API key
- ⚠️ **Groq** (Llama) - Opcional, **GRATIS**
- ⚠️ **Together AI** - Opcional, **GRATIS**
- ⚠️ **Cohere** - Opcional, **GRATIS**

**Configuración en .env**:
```env
# Seleccionar proveedor (por defecto: gemini)
AI_PROVIDER=gemini

# API Keys (solo si usas otros proveedores)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GROQ_API_KEY=gsk_...
```

### ChromaDB (RAG)

**Propósito**: Base de datos vectorial para búsqueda semántica.

**Ubicación de datos**: `storage/chroma_db/`

**Modelo de embeddings**: `sentence-transformers/all-MiniLM-L6-v2`

**Flujo RAG**:
```
1. Documento subido → Texto extraído (OCR si necesario)
2. Texto dividido en chunks
3. Chunks → Embeddings con sentence-transformers
4. Embeddings guardados en ChromaDB
5. Consulta usuario → Embedding de consulta
6. Búsqueda de similitud en ChromaDB
7. Top-K chunks más relevantes → Contexto para IA
8. IA genera respuesta con contexto
```

---

## 🧪 Testing

### Backend Tests

**Framework**: pytest

**Ubicación**: `backend/tests/`

**Ejecutar tests**:
```bash
cd backend
pytest

# Con coverage
pytest --cov=app tests/

# Tests específicos
pytest tests/test_cotizaciones.py
pytest tests/test_gemini.py -v
```

**Estructura de tests**:
```
backend/tests/
├── test_cotizaciones.py     # Tests CRUD cotizaciones
├── test_proyectos.py        # Tests CRUD proyectos
├── test_gemini.py           # Tests integración Gemini
├── test_word_generator.py   # Tests generación Word
├── test_rag.py              # Tests RAG/ChromaDB
└── conftest.py              # Fixtures comunes
```

**Ejemplo de test**:
```python
# tests/test_cotizaciones.py
import pytest
from app.models.cotizacion import Cotizacion

def test_crear_cotizacion(client, db):
    """Test crear cotización vía API"""
    data = {
        "cliente": "Cliente Test",
        "proyecto": "Proyecto Test",
        "items": [
            {
                "descripcion": "Item 1",
                "cantidad": 10,
                "precio_unitario": 100
            }
        ]
    }

    response = client.post("/api/cotizaciones/", json=data)
    assert response.status_code == 200
    assert response.json()["cliente"] == "Cliente Test"

    # Verificar en BD
    cotizacion = db.query(Cotizacion).first()
    assert cotizacion is not None
    assert len(cotizacion.items) == 1
```

### Frontend Tests

**Framework**: React Testing Library + Jest

**Ejecutar tests**:
```bash
cd frontend
npm test

# Con coverage
npm test -- --coverage
```

---

## 🚀 Deployment

### Desarrollo Local

Ver [Flujos de Trabajo de Desarrollo](#-flujos-de-trabajo-de-desarrollo)

### Producción con Docker

**Archivo**: `docker-compose.production.yml`

```bash
# 1. Configurar .env para producción
cp .env.example .env
# Editar .env:
# - ENVIRONMENT=production
# - PROD_DATABASE_URL=postgresql://user:pass@host:5432/dbname
# - GEMINI_API_KEY=tu_api_key_real

# 2. Build de imágenes
docker-compose -f docker-compose.production.yml build

# 3. Levantar servicios
docker-compose -f docker-compose.production.yml up -d

# 4. Ver logs
docker-compose -f docker-compose.production.yml logs -f

# 5. Ejecutar migraciones
docker-compose -f docker-compose.production.yml exec backend alembic upgrade head
```

### Nginx Reverse Proxy

**Configuración sugerida**: `/etc/nginx/sites-available/tesla-cotizador`

```nginx
server {
    listen 80;
    server_name teslacotizador.com www.teslacotizador.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Archivos estáticos
    location /storage/ {
        alias /home/user/TESLA_COTIZADOR-V3.0/storage/generados/;
    }
}
```

### Variables de Entorno Importantes

**IMPORTANTE**:
- Copia `backend/.env.example` a `backend/.env` antes de configurar
- **NUNCA** commitees el archivo `.env` con API keys reales
- El archivo `.env.example` es la plantilla oficial

**Desarrollo** (`backend/.env`):
```env
# Entorno
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# IA (configura AL MENOS una)
GEMINI_API_KEY=tu_gemini_api_key_aqui
GEMINI_MODEL=gemini-1.5-pro
TEMPERATURE=0.3
MAX_TOKENS=4000

# Alternativas (opcional)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GROQ_API_KEY=gsk_...  # GRATIS
# TOGETHER_API_KEY=...   # GRATIS
# COHERE_API_KEY=...     # GRATIS

# Servidor
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000

# Seguridad
SECRET_KEY=cambia-esto-en-produccion-por-algo-muy-seguro
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Archivos
ALLOWED_EXTENSIONS=pdf,docx,xlsx,png,jpg,jpeg
MAX_UPLOAD_SIZE_MB=10
```

**Producción** (`backend/.env`):
```env
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING

GEMINI_API_KEY=tu_gemini_api_key_produccion
PROD_DATABASE_URL=postgresql://user:password@host:5432/tesla_cotizador
SECRET_KEY=clave-secreta-muy-segura-cambiar-con-valor-aleatorio
FRONTEND_URL=https://teslacotizador.com

BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

ALLOWED_EXTENSIONS=pdf,docx,xlsx,png,jpg,jpeg
MAX_UPLOAD_SIZE_MB=10
```

---

## 🤖 Notas Importantes para IA

### Primeros Pasos para Asistentes de IA

**Antes de comenzar cualquier tarea**:

1. **Verifica el branch actual**: `git branch` o `git status`
2. **Revisa la estructura real**: El proyecto puede tener archivos `copy` o backups (ej. `main copy.py`, `chat copy.py`) que NO deben modificarse
3. **Archivos principales a modificar**:
   - `backend/app/main.py` - Aplicación principal FastAPI (~1000 líneas)
   - `backend/app/routers/*.py` - Routers sin sufijo "copy"
   - `backend/app/services/*.py` - Servicios sin sufijo "copy"
   - `frontend/src/App.jsx` - Aplicación principal React
   - `frontend/src/components/*.jsx` - Componentes React

4. **Archivos que NO debes modificar**:
   - Cualquier archivo con sufijo `copy`, `copy 2`, etc.
   - Archivos en carpeta `_backup/`
   - Archivos en `storage/generados/`
   - Archivos `.env` (solo modificar `.env.example` si es necesario)
   - Base de datos directamente (usar SQLAlchemy)

5. **Antes de hacer cambios importantes**:
   - Lee el código existente primero
   - Verifica que no haya duplicados o versiones antiguas
   - Asegúrate de entender el flujo completo
   - Considera el impacto en otras partes del sistema

### Problemas Comunes y Soluciones

**Problema #1: Router no registrado** ⚠️
- **Síntoma**: Endpoint devuelve 404 Not Found
- **Causa**: Router existe pero no está registrado en `main.py`
- **Solución**:
  ```python
  # En backend/app/main.py, agregar:
  from app.routers import nuevo_router
  routers_info["nuevo_router"] = {
      "router": nuevo_router.router,
      "prefix": "/api/nuevo",
      "tags": ["NuevoRouter"]
  }
  ```

**Problema #2: Generación de documentos falla** ⚠️
- **Síntoma**: Botones de descarga no generan archivos
- **Causa**: Estructura de datos incorrecta o falta endpoint
- **Solución**: Verificar estructura de datos y endpoint `/api/generar-documento-directo`
- **Referencia**: Ver `DIAGNOSTICO_ERRORES_GENERACION_DOCUMENTOS.md`

**Problema #3: Cache del navegador** ⚠️
- **Síntoma**: Cambios en frontend no se ven reflejados
- **Solución**: Limpiar cache del navegador (Ctrl+Shift+R) o modo incógnito

**Problema #4: CORS errors** ⚠️
- **Síntoma**: Frontend no puede conectar con backend
- **Solución**: Verificar configuración CORS en `main.py` y que backend esté corriendo

### Contexto del Negocio

**Empresa**: TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.
- **Ubicación**: Huancayo, Junín, Perú
- **Sector**: Electricidad y automatización
- **RUC**: 20601138787
- **Email**: ingenieria.teslaelectricidad@gmail.com

**Contexto cultural**:
- Moneda: Soles peruanos (S/)
- IGV: 18% (impuesto peruano)
- Formato de números: 1,234.56 (punto decimal, coma miles)
- Fechas: DD/MM/YYYY

### Reglas de Negocio Críticas

1. **Cálculo de Totales**:
   ```python
   subtotal = sum(item.cantidad * item.precio_unitario for item in items)
   igv = subtotal * 0.18
   total = subtotal + igv
   ```

2. **Numeración de Cotizaciones**:
   - Formato: `COT-YYYYMM-XXXX`
   - Ejemplo: `COT-202511-0001`
   - Autoincremental por mes

3. **Estados de Cotización**:
   - `borrador` → `enviada` → `aprobada` | `rechazada`
   - Solo se puede editar en estado `borrador`

4. **Validaciones de Items**:
   - Cantidad > 0
   - Precio unitario >= 0
   - Descripción no vacía

### Patrones Comunes

#### Crear Cotización desde IA

```python
# 1. Usuario describe proyecto en lenguaje natural
descripcion = "Necesito instalación eléctrica para oficina de 100m2"

# 2. Gemini analiza y extrae información
response = await gemini_service.generar_cotizacion_estructurada(descripcion)

# 3. Sistema crea estructura en BD
cotizacion = Cotizacion(
    cliente=response["cliente"],
    proyecto=response["proyecto"],
    numero=generar_numero_cotizacion()
)
db.add(cotizacion)

# 4. Crear items
for item_data in response["items"]:
    item = Item(
        cotizacion_id=cotizacion.id,
        descripcion=item_data["descripcion"],
        cantidad=item_data["cantidad"],
        precio_unitario=item_data["precio_unitario"]
    )
    db.add(item)

# 5. Calcular totales
cotizacion.subtotal = sum(item.subtotal for item in cotizacion.items)
cotizacion.igv = cotizacion.subtotal * 0.18
cotizacion.total = cotizacion.subtotal + cotizacion.igv

db.commit()
```

#### Generar Documento Word

```python
from app.services.word_generator import WordGenerator

# 1. Obtener cotización de BD
cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()

# 2. Preparar datos
datos = {
    "numero": cotizacion.numero,
    "fecha": cotizacion.fecha_creacion.strftime("%d/%m/%Y"),
    "cliente": cotizacion.cliente,
    "proyecto": cotizacion.proyecto,
    "items": [
        {
            "descripcion": item.descripcion,
            "cantidad": item.cantidad,
            "unidad": item.unidad,
            "precio_unitario": item.precio_unitario,
            "subtotal": item.subtotal
        }
        for item in cotizacion.items
    ],
    "subtotal": cotizacion.subtotal,
    "igv": cotizacion.igv,
    "total": cotizacion.total
}

# 3. Generar documento
generator = WordGenerator()
ruta_archivo = Path(f"storage/generados/{cotizacion.numero}.docx")

opciones = {
    "mostrarPreciosUnitarios": True,
    "mostrarPreciosTotales": True,
    "mostrarIGV": True,
    "incluirLogo": True
}

generator.generar_cotizacion(
    datos=datos,
    ruta_salida=ruta_archivo,
    opciones=opciones,
    logo_base64=logo_base64  # Opcional
)

# 4. Retornar archivo
return FileResponse(
    path=str(ruta_archivo),
    filename=f"{cotizacion.numero}.docx",
    media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
```

### Errores Comunes a Evitar

1. **NO** commitear archivos en `storage/` al repositorio
2. **NO** hardcodear API keys en código
3. **NO** olvidar validar inputs del usuario
4. **NO** usar `var` en JavaScript, usar `const`/`let`
5. **NO** olvidar type hints en Python
6. **NO** crear migraciones manualmente, usar Alembic
7. **NO** modificar base de datos directamente, usar SQLAlchemy
8. **NO** hacer push directo a main/master - siempre usar branches de trabajo
9. **NO** eliminar archivos `.env.example` - son plantillas importantes
10. **NO** commitear archivos `.env` con API keys reales
11. **NO** olvidar registrar nuevos routers en `backend/app/main.py`
12. **NO** modificar archivos con sufijo "copy" o en carpeta `_backup`

### Debugging

**Backend**:
```python
# Logging
import logging
logger = logging.getLogger(__name__)

logger.debug("Mensaje de debug")
logger.info("Información general")
logger.warning("Advertencia")
logger.error("Error")
logger.critical("Error crítico")

# Logs en: backend/logs/app.log
```

**Frontend**:
```javascript
// Console
console.log("Debug general");
console.warn("Advertencia");
console.error("Error");

// React DevTools en Chrome/Firefox
```

### Recursos Útiles

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Gemini API**: https://ai.google.dev/docs
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/

---

## 📞 Contacto y Soporte

**Equipo de Desarrollo**:
- Email: ingenieria.teslaelectricidad@gmail.com
- Teléfono: +51 906 315 961

**Documentación Adicional**:
- `README.md` - Información general del proyecto
- `README_PROFESSIONAL.md` - Documentación profesional completa (v4.0)
- `README_TESIS.md` - Documentación para tesis
- `README_FLUJO_PILI.md` - Documentación detallada del flujo PILI
- `INSTRUCCIONES_INSTALACION.md` - Guía de instalación paso a paso
- `INSTRUCCIONES_MULTI_IA.md` - Configuración multi-IA
- `DIAGNOSTICO_ERRORES_GENERACION_DOCUMENTOS.md` - Diagnóstico de errores comunes
- `MANUAL_USUARIO_TESLA_COTIZADOR_V3.md` - Manual de usuario
- `AUDITORIA_ARQUITECTURA_BACKEND.md` - Auditoría técnica del backend
- `INFORME_AUDITORIA_TECNICA.md` - Informe de auditoría técnica completa

---

## 📝 Changelog

### [3.0.0] - 2025-11-XX

**Agregado**:
- Sistema PILI (agente IA conversacional)
- Soporte multi-IA (Gemini, OpenAI, Claude, Groq, Together AI, Cohere)
- Generación automática de documentos Word/PDF
- RAG con ChromaDB para búsqueda semántica
- Sistema de proyectos complejos
- Dashboard con estadísticas
- Documentación completa (README_PROFESSIONAL.md, CLAUDE.md, README_TESIS.md)
- Plantillas de documentos profesionales
- Sistema de upload y análisis de documentos con OCR

**Cambiado**:
- Migración de arquitectura monolítica a modular
- Actualización a React 18
- Actualización a FastAPI 0.115+
- Nueva UI con Tailwind CSS
- Mejoras en el sistema de configuración con .env.example

**Deprecado**:
- Versiones anteriores (V1.0, V2.0)

### Actualizaciones Recientes - Diciembre 2025

- **2025-12-04**: Actualización completa de CLAUDE.md con estado actual del proyecto
- **2025-12-03**: Diagnóstico exhaustivo de errores de generación de documentos
- **2025-12-03**: Implementación de generación híbrida de documentos (Word/PDF)
- **2025-12-02**: Corrección de router generar_directo.py y registro en main.py
- **2025-11-26**: Actualización de CLAUDE.md con información práctica para asistentes de IA
- **2025-11-25**: Creación inicial de CLAUDE.md con guía completa del proyecto

---

## 🚀 Referencia Rápida para IA

### Comandos Más Comunes

```bash
# Ver estado actual
git status
git branch

# Ejecutar backend
cd backend
uvicorn app.main:app --reload

# Ejecutar frontend
cd frontend
npm start

# Instalar dependencias backend
cd backend
pip install -r requirements.txt

# Instalar dependencias frontend
cd frontend
npm install

# Tests
cd backend
pytest
```

### Archivos Clave para Modificar

| Archivo | Propósito | Cuándo Modificar |
|---------|-----------|------------------|
| `backend/app/main.py` | App principal FastAPI (~1000 líneas) | Agregar routers, middleware, CORS |
| `backend/app/routers/chat.py` | Chat con PILI (~84KB) | Modificar lógica de conversación |
| `backend/app/routers/generar_directo.py` | Generación directa | Modificar generación de documentos |
| `backend/app/services/gemini_service.py` | Cliente Gemini (~36KB) | Cambiar prompts o configuración IA |
| `backend/app/services/word_generator.py` | Generador Word (~37KB) | Modificar plantillas Word |
| `backend/app/services/pili_brain.py` | Cerebro PILI (~63KB) | Modificar lógica de razonamiento |
| `frontend/src/App.jsx` | App principal React | Agregar pantallas, cambiar flujo |
| `frontend/src/components/ChatIA.jsx` | Componente chat (~18KB) | Modificar UI del chat |
| `backend/.env` | Configuración | **NO commitear** - solo local |
| `backend/.env.example` | Plantilla config | Agregar nuevas variables |

### Rutas API Principales

```
POST   /api/chat/mensaje                    - Chat con PILI
POST   /api/chat/generar-cotizacion-rapida  - Cotización rápida
POST   /api/generar-documento-directo       - Generar Word/PDF directo
GET    /api/cotizaciones/                   - Listar cotizaciones
POST   /api/cotizaciones/                   - Crear cotización
GET    /api/cotizaciones/{id}/exportar/{formato} - Exportar cotización
GET    /api/proyectos/                      - Listar proyectos
POST   /api/documentos/upload               - Subir documentos
GET    /api/system/health                   - Health check
```

### Estructura de Response Típica

```json
{
  "exito": true,
  "mensaje": "Operación exitosa",
  "datos": { /* ... */ },
  "error": null
}
```

---

---

## 📊 Estado Actual del Proyecto (Diciembre 2025)

### ✅ Funcionalidades Completadas

- [x] Sistema PILI conversacional totalmente funcional
- [x] Generación de cotizaciones con IA (rápida y compleja)
- [x] Generación de documentos Word/PDF profesionales
- [x] Sistema de proyectos con gestión completa
- [x] Upload y análisis de documentos con OCR
- [x] RAG con ChromaDB para búsqueda semántica
- [x] API REST completa con FastAPI
- [x] Frontend React con Tailwind CSS
- [x] Soporte multi-IA (Gemini, OpenAI, Claude, Groq, etc.)
- [x] Arquitectura híbrida con degradación elegante
- [x] Sistema de routers dinámicos con manejo de errores robusto

### 🔧 En Desarrollo

- [ ] Autenticación completa con JWT
- [ ] Dashboard de estadísticas avanzado
- [ ] Sistema de notificaciones en tiempo real
- [ ] Integración con ERP externo
- [ ] Versionamiento de cotizaciones

### 🎯 Métricas del Proyecto

- **Líneas de código backend**: ~150,000+
- **Líneas de código frontend**: ~20,000+
- **Routers implementados**: 8
- **Servicios de IA**: 12+
- **Modelos de base de datos**: 4 principales
- **Endpoints API**: 40+
- **Componentes React**: 6 principales
- **Documentación**: 15+ archivos MD

---

**Fin de CLAUDE.md**

_Documento vivo - Actualizar cuando haya cambios significativos en arquitectura o convenciones._

**Versión**: 3.0.0
**Última revisión**: 2025-12-04
**Mantenido por**: Tesla Electricidad y Automatización S.A.C.
**Revisado por**: Claude Code (Sonnet 4.5)
