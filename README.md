# 🚀 Tesla Cotizador V3

Sistema de cotización inteligente con IA (Gemini 1.5 Pro) para generación automática de cotizaciones profesionales.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green)
![React](https://img.shields.io/badge/React-18+-61dafb)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791)
![License](https://img.shields.io/badge/License-Proprietary-red)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Documentation](#-api-documentation)
- [Contribución](#-contribución)

---

## ✨ Características

### 🤖 Inteligencia Artificial
- ✅ Generación automática de cotizaciones con Gemini 1.5 Pro
- ✅ Chat conversacional para refinar cotizaciones
- ✅ Análisis inteligente de documentos
- ✅ Sugerencias de servicios y precios

### 📄 Procesamiento de Documentos
- ✅ Upload y análisis de PDF, Word, Excel
- ✅ OCR para imágenes y documentos escaneados
- ✅ Extracción automática de información
- ✅ Búsqueda semántica con RAG (ChromaDB)

### 📊 Gestión Completa
- ✅ CRUD de cotizaciones y proyectos
- ✅ Estados de cotización (borrador, enviada, aprobada, rechazada)
- ✅ Dashboard con estadísticas
- ✅ Historial y versionado

### 📥 Exportación Profesional
- ✅ Generación de PDF profesional
- ✅ Documentos Word editables
- ✅ Informes ejecutivos
- ✅ Plantillas personalizables

---

## 🏗️ Arquitectura
```
TESLA-COTIZADOR-V3/
│
├── frontend/          # React + Tailwind CSS
├── backend/           # FastAPI + Python
├── database/          # PostgreSQL Scripts
└── docker-compose.yml # Orquestación de servicios
```

### Stack Tecnológico

**Frontend:**
- React 18
- Tailwind CSS
- Lucide Icons
- Fetch API

**Backend:**
- FastAPI
- SQLAlchemy (ORM)
- Pydantic (Validación)
- Google Gemini AI
- ChromaDB (Vector DB)
- Python-docx / ReportLab

**Database:**
- PostgreSQL 15
- Full-text search
- JSON fields

**Infraestructura:**
- Docker & Docker Compose
- Nginx (Producción)

---

## 📦 Requisitos

### Desarrollo Local

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Tesseract OCR
- API Key de Gemini

### Docker (Recomendado)

- Docker 24+
- Docker Compose 2.20+

---

## 🚀 Instalación

### Opción 1: Docker (Recomendado)
```bash
# 1. Clonar repositorio
git clone <repo-url>
cd TESLA-COTIZADOR-V3

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY

# 3. Levantar servicios
docker-compose up -d

# 4. Verificar servicios
docker-compose ps

# Acceder a:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - ChromaDB: http://localhost:8001
```

### Opción 2: Instalación Manual

#### Backend
```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env

# Inicializar base de datos
cd ../database
psql -U postgres -f init.sql

# Ejecutar backend
cd ../backend
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables
echo "REACT_APP_API_URL=http://localhost:8000" > .env.local

# Ejecutar frontend
npm start
```

---

## 🎯 Uso

### 1. Crear una Cotización Rápida
```bash
# Desde la interfaz web
1. Clic en "Cotización Rápida"
2. Describe tu proyecto
3. La IA generará automáticamente los items
4. Edita si es necesario
5. Exporta a PDF o Word
```

### 2. Chat Conversacional
```bash
# Refinamiento iterativo
1. Clic en "Cotización Compleja"
2. Sube documentos relevantes (opcional)
3. Chatea con la IA para refinar
4. La cotización se actualiza en tiempo real
```

### 3. Gestión de Proyectos
```bash
1. Crear proyecto
2. Subir documentos
3. Generar múltiples cotizaciones
4. Ver dashboard con estadísticas
5. Exportar informes ejecutivos
```

---

## 📁 Estructura del Proyecto
```
TESLA-COTIZADOR-V3/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   │   ├── ChatIA.jsx
│   │   │   ├── UploadZone.jsx
│   │   │   ├── CotizacionEditor.jsx
│   │   │   ├── VistaPrevia.jsx
│   │   │   └── Alerta.jsx
│   │   ├── services/
│   │   │   └── api.js        # Cliente API
│   │   ├── App.jsx           # Componente principal
│   │   └── index.js
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── core/             # Configuración
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/           # Modelos SQLAlchemy
│   │   │   ├── cotizacion.py
│   │   │   ├── proyecto.py
│   │   │   ├── documento.py
│   │   │   └── item.py
│   │   ├── schemas/          # Schemas Pydantic
│   │   ├── services/         # Lógica de negocio
│   │   │   ├── gemini_service.py
│   │   │   ├── word_generator.py
│   │   │   ├── pdf_generator.py
│   │   │   ├── file_processor.py
│   │   │   └── rag_service.py
│   │   ├── routers/          # Endpoints API
│   │   │   ├── cotizaciones.py
│   │   │   ├── proyectos.py
│   │   │   ├── documentos.py
│   │   │   ├── chat.py
│   │   │   └── informes.py
│   │   ├── utils/            # Utilidades
│   │   │   ├── ocr.py
│   │   │   └── helpers.py
│   │   └── main.py
│   ├── storage/              # Archivos
│   ├── templates/            # Plantillas Word
│   ├── requirements.txt
│   └── Dockerfile
│
├── database/
│   ├── init.sql              # Script inicial
│   └── migrations/           # Migraciones
│
├── docker-compose.yml
├── .gitignore
├── .env.example
└── README.md
```

---

## 📚 API Documentation

### Endpoints Principales

#### Cotizaciones
```
POST   /api/cotizaciones/              # Crear cotización
GET    /api/cotizaciones/              # Listar cotizaciones
GET    /api/cotizaciones/{id}          # Obtener cotización
PUT    /api/cotizaciones/{id}          # Actualizar cotización
DELETE /api/cotizaciones/{id}          # Eliminar cotización
POST   /api/cotizaciones/{id}/duplicar # Duplicar cotización
```

#### Chat IA
```
POST   /api/chat/generar-cotizacion        # Chat conversacional
POST   /api/chat/generar-cotizacion-rapida # Generación rápida
POST   /api/chat/refinar-cotizacion        # Refinar existente
```

#### Documentos
```
POST   /api/documentos/upload          # Subir documento
GET    /api/documentos/                # Listar documentos
GET    /api/documentos/buscar/semantica # Búsqueda RAG
```

#### Informes
```
POST   /api/informes/generar-pdf/{id}  # Generar PDF
POST   /api/informes/generar-word/{id} # Generar Word
```

**Documentación completa:** http://localhost:8000/docs

---

## 🧪 Testing
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

---

## 🔒 Seguridad

- ✅ Validación de archivos subidos
- ✅ Sanitización de inputs
- ✅ Rate limiting en endpoints
- ✅ Tokens JWT (preparado para autenticación)
- ✅ Variables de entorno para secretos

---

## 🚀 Deployment

### Producción con Docker
```bash
# Build para producción
docker-compose -f docker-compose.prod.yml up -d

# Con Nginx reverse proxy
# Ver documentación en /docs/deployment.md
```

---

## 📝 Licencia

Propietario - Tesla Cotizador © 2025

---

## 👥 Equipo

Desarrollado con ❤️ por el equipo de Tesla Cotizador

---

## 📞 Soporte

- 📧 Email: soporte@teslacotizador.com
- 📱 WhatsApp: +51 999 888 777
- 🌐 Web: www.teslacotizador.com

---

## 🎯 Roadmap

- [ ] Autenticación multi-usuario
- [ ] Integración con WhatsApp
- [ ] Dashboard analytics avanzado
- [ ] App móvil (React Native)
- [ ] Integración con sistemas contables
- [ ] Firma digital de cotizaciones












# 🚀 TESLA COTIZADOR V3.0

Sistema profesional de cotización y gestión de proyectos con IA integrada.

## 📋 Descripción

Sistema completo para generar cotizaciones, gestionar proyectos e informes técnicos profesionales usando:
- **IA Gemini 1.5 Pro** para análisis inteligente
- **RAG** para aprender de proyectos históricos
- **Generación automática** de documentos Word/PDF
- **Chat conversacional** para guiar al usuario

## 🎯 Características

### ⚡ Cotizaciones
- **Cotización Rápida**: Proceso simplificado (5-15 min)
- **Cotización Compleja**: Análisis detallado con IA

### 📁 Proyectos
- **Proyecto Simple**: Gestión básica
- **Proyecto Complejo**: Con carpetas automáticas, Gantt, hitos

### 📄 Informes
- **Informe Simple**: PDF básico
- **Informe Ejecutivo**: Word con formato APA, tablas y gráficos

## 🛠️ Stack Tecnológico

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy
- Google Gemini 1.5 Pro
- ChromaDB (Vector Database)
- python-docx / ReportLab

### Frontend
- React 18
- Tailwind CSS
- Lucide Icons

### Base de Datos
- SQLite (desarrollo)
- PostgreSQL (producción)

## 📦 Instalación

### 1. Requisitos Previos
```bash
- Python 3.11 o superior
- Node.js 18 o superior
- pip y npm actualizados
```

### 2. Configuración Backend
```bash
# Activar entorno virtual
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Instalar dependencias (ya instaladas por el script)
# pip install -r backend/requirements.txt

# Configurar .env
# Edita backend/.env y agrega tu GEMINI_API_KEY
```

### 3. Configuración Frontend
```bash
cd frontend
npm install
```

### 4. Ejecutar Aplicación

**Backend:**
```bash
# Desde la raíz del proyecto
# Windows:
venv\Scripts\python backend/app/main.py

# Linux/Mac:
venv/bin/python backend/app/main.py

# O con uvicorn directamente:
# Windows:
venv\Scripts\uvicorn backend.app.main:app --reload

# Linux/Mac:
venv/bin/uvicorn backend.app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm start
```

## 🌐 Acceso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 📁 Estructura del Proyecto

```
TESLA_COTIZADOR-V3.0/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── core/        # Configuración
│   │   ├── models/      # Modelos BD
│   │   ├── schemas/     # Schemas Pydantic
│   │   ├── services/    # Lógica de negocio
│   │   ├── routers/     # Endpoints API
│   │   └── utils/       # Utilidades
│   ├── templates/       # Plantillas Word
│   ├── storage/         # Archivos subidos/generados
│   └── .env            # Configuración
├── frontend/            # React App
├── database/            # Scripts SQL
├── venv/               # Entorno virtual Python
└── docs/               # Documentación

```

## 🔐 Configuración de Variables de Entorno

Edita `backend/.env` y configura:

```env
# API KEY DE GEMINI (OBLIGATORIO)
GEMINI_API_KEY=tu_api_key_aqui

# Otras configuraciones están listas por defecto
```

## 🚀 Próximos Pasos

1. ✅ Estructura creada
2. ⏳ Implementar routers del backend
3. ⏳ Integrar Gemini API
4. ⏳ Crear generadores Word/PDF
5. ⏳ Implementar RAG
6. ⏳ Conectar frontend con backend

## 📞 Soporte

TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.
- Email: ingenieria.teslaelectricidad@gmail.com
- Teléfono: 906315961

---

**Versión**: 3.0.0  
**Fecha**: Octubre 2025  
**Estado**: En Desarrollo - Estructura Base Completada
