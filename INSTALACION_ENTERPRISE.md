# 🚀 INSTALACIÓN ENTERPRISE - TESLA COTIZADOR V4.0
## Guía Completa de Instalación en Entorno Virtual

**Fecha**: 29 de Diciembre 2025
**Versión**: Enterprise 4.0
**Python**: 3.11 o 3.12
**Sistema Operativo**: Linux, Windows, macOS

---

## 📋 TABLA DE CONTENIDOS

1. [Pre-requisitos del Sistema](#1-pre-requisitos-del-sistema)
2. [Instalación de Dependencias del Sistema](#2-instalación-de-dependencias-del-sistema)
3. [Configuración del Entorno Virtual Python](#3-configuración-del-entorno-virtual-python)
4. [Instalación de Paquetes Python](#4-instalación-de-paquetes-python)
5. [Configuración de Base de Datos](#5-configuración-de-base-de-datos)
6. [Configuración de Redis y Celery](#6-configuración-de-redis-y-celery)
7. [Variables de Entorno](#7-variables-de-entorno)
8. [Verificación de Instalación](#8-verificación-de-instalación)
9. [Instalación con Docker](#9-instalación-con-docker-recomendado)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. PRE-REQUISITOS DEL SISTEMA

### Verificar Versión de Python

```bash
# Linux/Mac
python3 --version

# Windows
python --version
```

**Requerido**: Python 3.11+ o 3.12

### Instalar Python si no está presente

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

#### Windows
Descargar desde: https://www.python.org/downloads/
- ✅ Marcar "Add Python to PATH"
- ✅ Instalar pip

#### macOS
```bash
brew install python@3.12
```

---

## 2. INSTALACIÓN DE DEPENDENCIAS DEL SISTEMA

### 2.1 PostgreSQL

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib libpq-dev
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Windows
1. Descargar desde: https://www.postgresql.org/download/windows/
2. Ejecutar instalador
3. Configurar password para usuario `postgres`

#### macOS
```bash
brew install postgresql@15
brew services start postgresql@15
```

### 2.2 Redis

#### Ubuntu/Debian
```bash
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

#### Windows
```powershell
# Opción 1: WSL
wsl --install
# Dentro de WSL: sudo apt install redis-server

# Opción 2: Memurai (Redis para Windows)
# Descargar desde: https://www.memurai.com/
```

#### macOS
```bash
brew install redis
brew services start redis
```

### 2.3 Tesseract OCR

#### Ubuntu/Debian
```bash
sudo apt install tesseract-ocr tesseract-ocr-spa
sudo apt install libtesseract-dev libleptonica-dev
```

#### Windows
1. Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Instalar
3. Agregar a PATH: `C:\Program Files\Tesseract-OCR`

#### macOS
```bash
brew install tesseract tesseract-lang
```

### 2.4 Librerías del Sistema (Opcional pero Recomendado)

#### Ubuntu/Debian
```bash
# Para procesamiento de imágenes
sudo apt install libjpeg-dev libpng-dev libtiff-dev

# Para WeasyPrint (PDF)
sudo apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev

# Para compilación de paquetes
sudo apt install build-essential python3-dev

# Para libmagic (detección de tipos de archivo)
sudo apt install libmagic1
```

### 2.5 RabbitMQ (Opcional - para producción)

#### Ubuntu/Debian
```bash
sudo apt install rabbitmq-server
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server
```

#### Windows
Descargar desde: https://www.rabbitmq.com/download.html

#### macOS
```bash
brew install rabbitmq
brew services start rabbitmq
```

---

## 3. CONFIGURACIÓN DEL ENTORNO VIRTUAL PYTHON

### 3.1 Crear Entorno Virtual

```bash
# Navegar a la carpeta del proyecto
cd TESLA_COTIZADOR-V3.0/backend

# Crear entorno virtual
python3 -m venv venv

# Windows (alternativa)
python -m venv venv
```

### 3.2 Activar Entorno Virtual

#### Linux/Mac
```bash
source venv/bin/activate
```

#### Windows (CMD)
```cmd
venv\Scripts\activate.bat
```

#### Windows (PowerShell)
```powershell
venv\Scripts\Activate.ps1

# Si hay error de ejecución de scripts:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3.3 Verificar Activación

Deberías ver `(venv)` al inicio de la línea de comandos:
```
(venv) user@machine:~/TESLA_COTIZADOR-V3.0/backend$
```

### 3.4 Actualizar pip

```bash
pip install --upgrade pip setuptools wheel
```

---

## 4. INSTALACIÓN DE PAQUETES PYTHON

### 4.1 Instalar Dependencias Enterprise

```bash
# IMPORTANTE: Asegurarse de que el entorno virtual está activado
# Verificar: which python (Linux/Mac) o where python (Windows)

# Instalar todas las dependencias
pip install -r requirements_enterprise.txt

# Esto puede tomar 5-15 minutos dependiendo de la conexión
```

### 4.2 Instalar Modelo spaCy Español

```bash
# Descargar modelo de idioma español
python -m spacy download es_core_news_md

# Verificar instalación
python -c "import spacy; nlp = spacy.load('es_core_news_md'); print('✅ spaCy modelo español instalado')"
```

### 4.3 Verificar Instalaciones Críticas

```bash
# Verificar FastAPI
python -c "import fastapi; print(f'✅ FastAPI {fastapi.__version__}')"

# Verificar SQLAlchemy
python -c "import sqlalchemy; print(f'✅ SQLAlchemy {sqlalchemy.__version__}')"

# Verificar ChromaDB
python -c "import chromadb; print(f'✅ ChromaDB {chromadb.__version__}')"

# Verificar Celery
python -c "import celery; print(f'✅ Celery {celery.__version__}')"

# Verificar Redis
python -c "import redis; print('✅ Redis client instalado')"

# Verificar sentence-transformers
python -c "from sentence_transformers import SentenceTransformer; print('✅ Sentence Transformers instalado')"

# Verificar Plotly
python -c "import plotly; print(f'✅ Plotly {plotly.__version__}')"
```

---

## 5. CONFIGURACIÓN DE BASE DE DATOS

### 5.1 Crear Base de Datos PostgreSQL

#### Opción 1: Usando psql (Linux/Mac)

```bash
# Conectar a PostgreSQL
sudo -u postgres psql

# Dentro de psql:
CREATE DATABASE tesla_db;
CREATE USER tesla WITH PASSWORD 'tesla_password_2024';
GRANT ALL PRIVILEGES ON DATABASE tesla_db TO tesla;

# Habilitar extensiones necesarias
\c tesla_db
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Para búsqueda full-text

# Salir
\q
```

#### Opción 2: Usando pgAdmin (Windows/cualquier SO)

1. Abrir pgAdmin
2. Click derecho en "Databases" → Create → Database
3. Nombre: `tesla_db`
4. Owner: crear usuario `tesla` con password

### 5.2 Configurar URL de Conexión

Editar `.env`:
```env
DATABASE_URL=postgresql://tesla:tesla_password_2024@localhost:5432/tesla_db
```

### 5.3 Ejecutar Migraciones

```bash
# Ir a carpeta backend (si no estás ahí)
cd backend

# Inicializar Alembic (solo primera vez)
alembic init migrations

# Crear migración inicial
alembic revision --autogenerate -m "Initial schema empresarial"

# Aplicar migraciones
alembic upgrade head
```

---

## 6. CONFIGURACIÓN DE REDIS Y CELERY

### 6.1 Verificar Redis

```bash
# Probar conexión a Redis
redis-cli ping
# Debería responder: PONG
```

### 6.2 Configurar Celery

Crear archivo `backend/app/celeryconfig.py`:

```python
from celery import Celery
import os

celery_app = Celery(
    "tesla_cotizador",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Lima',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    worker_max_tasks_per_child=1000,
)
```

### 6.3 Iniciar Worker Celery (Terminal separada)

```bash
# Activar entorno virtual primero
source venv/bin/activate

# Iniciar worker
celery -A app.tasks worker --loglevel=info
```

---

## 7. VARIABLES DE ENTORNO

### 7.1 Crear archivo .env

```bash
# Copiar template
cp .env.example .env

# Editar con tu editor favorito
nano .env  # o code .env, vim .env, etc.
```

### 7.2 Configuración Mínima (.env)

```env
# ============================================================================
# ENTORNO
# ============================================================================
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# ============================================================================
# BASE DE DATOS
# ============================================================================
DATABASE_URL=postgresql://tesla:tesla_password_2024@localhost:5432/tesla_db

# Pool de conexiones
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# ============================================================================
# REDIS
# ============================================================================
REDIS_URL=redis://localhost:6379/0
REDIS_MAX_CONNECTIONS=50

# ============================================================================
# CELERY
# ============================================================================
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# ============================================================================
# CHROMADB (RAG)
# ============================================================================
CHROMA_HOST=localhost
CHROMA_PORT=8001
CHROMA_PERSIST_DIRECTORY=storage/chroma_db

# ============================================================================
# INTELIGENCIA ARTIFICIAL
# ============================================================================
# Google Gemini (RECOMENDADO)
GEMINI_API_KEY=tu_api_key_aqui
GEMINI_MODEL=gemini-1.5-pro
TEMPERATURE=0.3
MAX_TOKENS=4000

# OpenAI (Opcional)
# OPENAI_API_KEY=

# Anthropic (Opcional)
# ANTHROPIC_API_KEY=

# Groq (Opcional - GRATIS)
# GROQ_API_KEY=

# ============================================================================
# SERVIDOR
# ============================================================================
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000

# Workers
WORKERS=4

# ============================================================================
# SEGURIDAD
# ============================================================================
SECRET_KEY=cambia-esto-por-algo-muy-seguro-en-produccion-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# ============================================================================
# ARCHIVOS
# ============================================================================
UPLOAD_DIR=storage/uploads
DOCUMENTS_DIR=storage/documents
MAX_UPLOAD_SIZE_MB=25
ALLOWED_EXTENSIONS=pdf,docx,xlsx,png,jpg,jpeg,txt

# ============================================================================
# LOGGING
# ============================================================================
LOG_FILE=logs/app.log
LOG_ROTATION=1 day
LOG_RETENTION=30 days

# ============================================================================
# PERFORMANCE
# ============================================================================
CACHE_TTL=3600
ENABLE_RESPONSE_CACHE=True
```

---

## 8. VERIFICACIÓN DE INSTALACIÓN

### 8.1 Script de Verificación Automática

Crear `backend/verificar_instalacion.py`:

```python
#!/usr/bin/env python3
"""Script de verificación de instalación"""
import sys

def verificar_componente(nombre, func):
    try:
        func()
        print(f"✅ {nombre}: OK")
        return True
    except Exception as e:
        print(f"❌ {nombre}: ERROR - {e}")
        return False

def main():
    resultados = []

    # FastAPI
    resultados.append(verificar_componente(
        "FastAPI",
        lambda: __import__('fastapi')
    ))

    # PostgreSQL
    def test_postgres():
        import sqlalchemy
        from sqlalchemy import create_engine
        import os
        engine = create_engine(os.getenv('DATABASE_URL'))
        with engine.connect() as conn:
            conn.execute(sqlalchemy.text("SELECT 1"))

    resultados.append(verificar_componente("PostgreSQL", test_postgres))

    # Redis
    def test_redis():
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()

    resultados.append(verificar_componente("Redis", test_redis))

    # ChromaDB
    resultados.append(verificar_componente(
        "ChromaDB",
        lambda: __import__('chromadb')
    ))

    # Sentence Transformers
    resultados.append(verificar_componente(
        "Sentence Transformers",
        lambda: __import__('sentence_transformers')
    ))

    # spaCy
    def test_spacy():
        import spacy
        nlp = spacy.load('es_core_news_md')

    resultados.append(verificar_componente("spaCy (modelo español)", test_spacy))

    # Plotly
    resultados.append(verificar_componente(
        "Plotly",
        lambda: __import__('plotly')
    ))

    # Celery
    resultados.append(verificar_componente(
        "Celery",
        lambda: __import__('celery')
    ))

    # python-docx
    resultados.append(verificar_componente(
        "python-docx",
        lambda: __import__('docx')
    ))

    # Tesseract
    def test_tesseract():
        import pytesseract
        pytesseract.get_tesseract_version()

    resultados.append(verificar_componente("Tesseract OCR", test_tesseract))

    # Resumen
    print("\n" + "="*50)
    total = len(resultados)
    exitosos = sum(resultados)
    print(f"Resultado: {exitosos}/{total} componentes instalados correctamente")
    print("="*50)

    if exitosos == total:
        print("\n🎉 ¡Instalación completa y verificada!")
        return 0
    else:
        print("\n⚠️  Algunos componentes requieren atención")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

Ejecutar:
```bash
python verificar_instalacion.py
```

---

## 9. INSTALACIÓN CON DOCKER (RECOMENDADO)

### 9.1 Instalar Docker

#### Ubuntu
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### Windows/Mac
Descargar Docker Desktop: https://www.docker.com/products/docker-desktop

### 9.2 Levantar Servicios

```bash
# Desde la raíz del proyecto
cd TESLA_COTIZADOR-V3.0

# Levantar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

---

## 10. TROUBLESHOOTING

### Error: "pg_config executable not found"
```bash
# Ubuntu/Debian
sudo apt install libpq-dev

# macOS
brew install postgresql
```

### Error: "Microsoft Visual C++ 14.0 is required" (Windows)
Instalar Build Tools: https://visualstudio.microsoft.com/downloads/

### Error: "Unable to find vcvarsall.bat" (Windows)
Instalar Visual Studio Build Tools con C++ workload

### Error: "Tesseract is not installed"
```bash
# Verificar instalación
tesseract --version

# Ubuntu/Debian
sudo apt install tesseract-ocr

# Agregar a PATH si está instalado pero no se encuentra
```

### Error: "Cannot connect to Redis"
```bash
# Verificar que Redis está corriendo
sudo systemctl status redis

# Iniciar Redis
sudo systemctl start redis

# Windows: Iniciar servicio desde Services
```

### Error: "psycopg2 installation failed"
```bash
# Usar binary en vez de source
pip uninstall psycopg2
pip install psycopg2-binary
```

---

## ✅ CHECKLIST DE INSTALACIÓN

- [ ] Python 3.11+ o 3.12 instalado
- [ ] PostgreSQL instalado y corriendo
- [ ] Redis instalado y corriendo
- [ ] Tesseract OCR instalado
- [ ] Entorno virtual creado y activado
- [ ] requirements_enterprise.txt instalado
- [ ] spaCy modelo español descargado
- [ ] Base de datos `tesla_db` creada
- [ ] Usuario `tesla` configurado en PostgreSQL
- [ ] Archivo `.env` creado y configurado
- [ ] Migraciones ejecutadas (alembic upgrade head)
- [ ] Script de verificación ejecutado y todo ✅
- [ ] Celery worker probado
- [ ] Backend FastAPI inicia correctamente

---

## 🚀 SIGUIENTE PASO

Una vez completada la instalación:

```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Abrir navegador: http://localhost:8000/docs

---

**Instalación completada por**: Claude Code (Sonnet 4.5)
**Fecha**: 29 de Diciembre 2025
**Versión**: Enterprise 4.0
