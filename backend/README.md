# Tesla Cotizador V3 - Backend

Sistema de cotización inteligente con IA (Gemini 1.5 Pro) para generación automática de cotizaciones profesionales.

## 🚀 Características

- ✅ Generación de cotizaciones con IA
- ✅ Chat conversacional para refinar cotizaciones
- ✅ Procesamiento de documentos (PDF, Word, Excel, imágenes)
- ✅ OCR para extracción de texto
- ✅ Búsqueda semántica (RAG con ChromaDB)
- ✅ Exportación a PDF y Word profesional
- ✅ API RESTful con FastAPI
- ✅ Base de datos PostgreSQL

## 📋 Requisitos

- Python 3.11+
- PostgreSQL 15+
- Tesseract OCR
- API Key de Gemini

## 🛠️ Instalación

### 1. Clonar repositorio
```bash
git clone <repo>
cd backend
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### 5. Inicializar base de datos
```bash
psql -U postgres -f database/init.sql
```

### 6. Ejecutar aplicación
```bash
uvicorn app.main:app --reload
```

## 🐳 Docker (Recomendado)
```bash
docker-compose up -d
```

## 📚 Documentación API

Una vez ejecutado, accede a:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🗂️ Estructura
```
backend/
├── app/
│   ├── core/          # Configuración y DB
│   ├── models/        # Modelos SQLAlchemy
│   ├── schemas/       # Schemas Pydantic
│   ├── services/      # Lógica de negocio
│   ├── routers/       # Endpoints API
│   └── utils/         # Utilidades
├── storage/           # Archivos subidos
├── templates/         # Plantillas Word
└── database/          # Scripts SQL
```

## 🧪 Testing
```bash
pytest
```

## 📝 Licencia

Propietario - Tesla Cotizador 2025





TESLA-COTIZADOR-V3/
│
├── frontend/              # React App
├── backend/               # FastAPI App
├── database/              # ← INDEPENDIENTE (scripts SQL)
│   ├── init.sql
│   ├── migrations/
│   └── README.md
│
├── docker-compose.yml     # ← Orquesta TODOS los servicios
├── .gitignore
└── README.md
```

### ✅ VENTAJAS:
- **Separación clara de responsabilidades**
- **Modular**: Puedes cambiar backend sin tocar DB
- **Equipo**: Diferentes desarrolladores pueden trabajar independientemente
- **Docker**: Cada servicio en su propio contenedor
- **Versionado**: Migraciones de DB independientes del código
- **CI/CD**: Puedes deployar DB, backend y frontend por separado

### ❌ DESVENTAJAS:
- Más carpetas en la raíz del proyecto
- Requiere configuración explícita de conexión

---

## 🏗️ OPCIÓN 2: Database dentro de Backend
```
TESLA-COTIZADOR-V3/
│
├── frontend/
├── backend/
│   ├── app/
│   ├── database/          # ← DENTRO del backend
│   │   ├── init.sql
│   │   └── migrations/
│   └── ...
│
└── docker-compose.yml
```

### ✅ VENTAJAS:
- Todo lo relacionado al backend en un solo lugar
- Más fácil de empaquetar el backend completo

### ❌ DESVENTAJAS:
- Menos modular
- Mezcla código de aplicación con esquema de base de datos
- Dificulta trabajo en equipo separado (DBA vs Backend Dev)

---

## 🎯 MI RECOMENDACIÓN COMO ARQUITECTO DE SOFTWARE

**MANTENER LA ARQUITECTURA ORIGINAL** (Opción 1) por estas razones críticas:

1. **🔐 Principio de Separación de Concerns**: Base de datos es infraestructura, no código de aplicación
2. **📦 Microservicios-ready**: Si en el futuro quieres escalar, ya está preparado
3. **👥 Trabajo en equipo**: DBA puede gestionar DB sin tocar código Python
4. **🔄 Versionado independiente**: Migraciones de DB tienen su propio ciclo de vida
5. **🐳 Docker best practices**: Cada servicio (DB, Backend, Frontend) es independiente

---

## 📁 ESTRUCTURA FINAL CORRECTA (Arquitectura Original)
```
TESLA-COTIZADOR-V3/
│
├── frontend/                          # React Application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/                           # Python FastAPI
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── routers/
│   │   ├── utils/
│   │   └── main.py
│   ├── storage/
│   ├── templates/
│   ├── requirements.txt
│   ├── .env.example
│   ├── Dockerfile
│   └── README.md
│
├── database/                          # ← INDEPENDIENTE
│   ├── init.sql
│   ├── migrations/
│   │   └── README.md
│   └── README.md
│
├── docker-compose.yml                 # Orquesta TODO
├── .gitignore
├── .env.example
└── README.md                          # Principal del proyecto