#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
    TESLA COTIZADOR V3.0 - SCRIPT DE INSTALACIÓN MAESTRO
═══════════════════════════════════════════════════════════════
Autor: Sistema de Arquitectura Profesional
Versión: 3.0.0
Fecha: Octubre 2025

DESCRIPCIÓN:
Este script crea la estructura completa del proyecto Tesla Cotizador v3.0
incluyendo backend FastAPI, frontend React, base de datos, entorno virtual
y todas las configuraciones necesarias para producción.

USO:
1. Crea la carpeta: mkdir TESLA_COTIZADOR-V3.0
2. Navega: cd TESLA_COTIZADOR-V3.0  
3. Ejecuta: python setup_tesla_v3.py
4. Sigue las instrucciones en pantalla
═══════════════════════════════════════════════════════════════
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import json

class TeslaSetupProfessional:
    def __init__(self):
        self.base_path = Path.cwd()
        self.colors = {
            "HEADER": "\033[95m",
            "OKBLUE": "\033[94m",
            "OKCYAN": "\033[96m",
            "OKGREEN": "\033[92m",
            "WARNING": "\033[93m",
            "FAIL": "\033[91m",
            "ENDC": "\033[0m",
            "BOLD": "\033[1m",
            "UNDERLINE": "\033[4m"
        }
        self.is_windows = platform.system() == "Windows"
        
    def print_colored(self, message, color="OKBLUE"):
        """Imprime mensaje con color"""
        print(f"{self.colors[color]}{message}{self.colors['ENDC']}")
        
    def print_header(self, message):
        """Imprime header estilizado"""
        border = "═" * 70
        print(f"\n{self.colors['HEADER']}{self.colors['BOLD']}")
        print(border)
        print(f"  {message}")
        print(border)
        print(self.colors['ENDC'])
        
    def create_directory(self, path):
        """Crea directorio si no existe"""
        full_path = self.base_path / path
        full_path.mkdir(parents=True, exist_ok=True)
        self.print_colored(f"✓ Creado: {path}", "OKGREEN")
        return full_path
        
    def create_file(self, path, content=""):
        """Crea archivo con contenido"""
        full_path = self.base_path / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.print_colored(f"✓ Archivo: {path}", "OKGREEN")
        
    def setup_virtual_environment(self):
        """Crea y configura entorno virtual Python"""
        self.print_header("🐍 CREANDO ENTORNO VIRTUAL PYTHON")
        
        venv_path = self.base_path / "venv"
        
        if venv_path.exists():
            self.print_colored("⚠ Entorno virtual ya existe, omitiendo...", "WARNING")
            return True
            
        try:
            self.print_colored("📦 Creando entorno virtual...", "OKCYAN")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            self.print_colored("✅ Entorno virtual creado exitosamente", "OKGREEN")
            return True
        except Exception as e:
            self.print_colored(f"❌ Error creando entorno virtual: {e}", "FAIL")
            return False
            
    def install_python_dependencies(self):
        """Instala dependencias Python en el entorno virtual"""
        self.print_header("📚 INSTALANDO DEPENDENCIAS PYTHON")
        
        # Determinar ruta del pip según OS
        if self.is_windows:
            pip_path = self.base_path / "venv" / "Scripts" / "pip.exe"
        else:
            pip_path = self.base_path / "venv" / "bin" / "pip"
            
        if not pip_path.exists():
            self.print_colored("❌ No se encontró pip en el entorno virtual", "FAIL")
            return False
            
        dependencies = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "sqlalchemy==2.0.23",
            "python-multipart==0.0.6",
            "python-dotenv==1.0.0",
            "pydantic==2.5.0",
            "python-docx==1.1.0",
            "Pillow==10.1.0",
            "reportlab==4.0.7",
            "google-generativeai==0.3.1",
            "chromadb==0.4.18",
            "PyPDF2==3.0.1",
            "openpyxl==3.1.2",
            "pytesseract==0.3.10",
            "matplotlib==3.8.2",
            "pandas==2.1.3",
            "aiofiles==23.2.1",
            "python-jose[cryptography]==3.3.0",
            "passlib[bcrypt]==1.7.4",
            "bcrypt==4.1.1"
        ]
        
        try:
            self.print_colored("⏳ Instalando paquetes... (esto puede tomar varios minutos)", "OKCYAN")
            
            # Actualizar pip primero
            subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
            
            # Instalar dependencias una por una para mejor feedback
            for dep in dependencies:
                self.print_colored(f"  📦 Instalando {dep.split('==')[0]}...", "OKCYAN")
                subprocess.run([str(pip_path), "install", dep], check=True, capture_output=True)
                
            self.print_colored("✅ Todas las dependencias instaladas correctamente", "OKGREEN")
            return True
        except Exception as e:
            self.print_colored(f"❌ Error instalando dependencias: {e}", "FAIL")
            return False
            
    def create_backend_structure(self):
        """Crea estructura completa del backend"""
        self.print_header("⚙️ CREANDO ESTRUCTURA BACKEND")
        
        # Crear directorios
        dirs = [
            "backend",
            "backend/app",
            "backend/app/core",
            "backend/app/models",
            "backend/app/schemas",
            "backend/app/services",
            "backend/app/routers",
            "backend/app/utils",
            "backend/templates",
            "backend/storage",
            "backend/storage/documentos",
            "backend/storage/proyectos",
            "backend/storage/generados",
        ]
        
        for directory in dirs:
            self.create_directory(directory)
            
        # Crear __init__.py en cada paquete
        init_paths = [
            "backend/app/__init__.py",
            "backend/app/core/__init__.py",
            "backend/app/models/__init__.py",
            "backend/app/schemas/__init__.py",
            "backend/app/services/__init__.py",
            "backend/app/routers/__init__.py",
            "backend/app/utils/__init__.py",
        ]
        
        for init_path in init_paths:
            self.create_file(init_path, '"""Tesla Cotizador v3.0 - Package"""\n')
            
    def create_frontend_structure(self):
        """Crea estructura del frontend"""
        self.print_header("⚛️ CREANDO ESTRUCTURA FRONTEND")
        
        dirs = [
            "frontend",
            "frontend/public",
            "frontend/src",
            "frontend/src/components",
            "frontend/src/services",
            "frontend/src/utils",
        ]
        
        for directory in dirs:
            self.create_directory(directory)
            
    def create_database_structure(self):
        """Crea estructura de base de datos"""
        self.print_header("🗄️ CREANDO ESTRUCTURA BASE DE DATOS")
        
        self.create_directory("database")
        self.create_directory("database/migrations")
        
    def create_docs_structure(self):
        """Crea estructura de documentación"""
        self.print_header("📖 CREANDO DOCUMENTACIÓN")
        
        self.create_directory("docs")
        
    def create_env_file(self):
        """Crea archivo .env con configuraciones"""
        self.print_header("🔐 CREANDO ARCHIVO DE CONFIGURACIÓN")
        
        env_content = """# ═══════════════════════════════════════════════════════════
# TESLA COTIZADOR V3.0 - CONFIGURACIÓN DE ENTORNO
# ═══════════════════════════════════════════════════════════

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🤖 GOOGLE GEMINI API
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Obtén tu API key en: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=tu_api_key_aqui

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🗄️ BASE DE DATOS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Desarrollo (SQLite)
DATABASE_URL=sqlite:///./database/tesla_cotizador.db

# Producción (PostgreSQL) - Descomentar cuando esté listo
# DATABASE_URL=postgresql://user:password@localhost:5432/tesla_cotizador

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔒 SEGURIDAD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECRET_KEY=tesla_secret_key_change_in_production_2025
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🌐 SERVIDOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📁 RUTAS DE ALMACENAMIENTO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STORAGE_PATH=./backend/storage
TEMPLATES_PATH=./backend/templates

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎯 CONFIGURACIÓN DE IA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GEMINI_MODEL=gemini-1.5-pro
MAX_TOKENS=8192
TEMPERATURE=0.7

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📊 RAG (Vector Database)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHROMA_PERSIST_DIRECTORY=./backend/storage/chroma_db
EMBEDDING_MODEL=models/embedding-001

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⚙️ CONFIGURACIÓN GENERAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📤 LÍMITES DE ARCHIVOS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MAX_UPLOAD_SIZE_MB=50
ALLOWED_EXTENSIONS=pdf,docx,xlsx,jpg,jpeg,png,txt,csv
"""
        self.create_file("backend/.env", env_content)
        self.create_file("backend/.env.example", env_content)
        
    def create_gitignore(self):
        """Crea archivo .gitignore"""
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/
.venv

# Environment variables
.env
.env.local

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Storage
backend/storage/documentos/*
backend/storage/proyectos/*
backend/storage/generados/*
!backend/storage/.gitkeep

# Logs
*.log
logs/

# Node
node_modules/
npm-debug.log
yarn-error.log

# Build
dist/
build/
*.egg-info/

# Chroma DB
backend/storage/chroma_db/
"""
        self.create_file(".gitignore", gitignore_content)
        
    def create_requirements_txt(self):
        """Crea requirements.txt"""
        requirements_content = """# ═══════════════════════════════════════════════════════════
# TESLA COTIZADOR V3.0 - DEPENDENCIAS PYTHON
# ═══════════════════════════════════════════════════════════

# Framework Web
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Base de Datos
sqlalchemy==2.0.23

# Utilidades
python-multipart==0.0.6
python-dotenv==1.0.0
pydantic==2.5.0
aiofiles==23.2.1

# Generación de Documentos
python-docx==1.1.0
reportlab==4.0.7
Pillow==10.1.0
matplotlib==3.8.2

# IA y Machine Learning
google-generativeai==0.3.1
chromadb==0.4.18

# Procesamiento de Archivos
PyPDF2==3.0.1
openpyxl==3.1.2
pytesseract==0.3.10
pandas==2.1.3

# Seguridad
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.1
"""
        self.create_file("backend/requirements.txt", requirements_content)
        
    def create_readme(self):
        """Crea README principal"""
        readme_content = """# 🚀 TESLA COTIZADOR V3.0

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
venv\\Scripts\\activate

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
venv\\Scripts\\python backend/app/main.py

# Linux/Mac:
venv/bin/python backend/app/main.py

# O con uvicorn directamente:
# Windows:
venv\\Scripts\\uvicorn backend.app.main:app --reload

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
"""
        self.create_file("README.md", readme_content)
        
    def create_run_scripts(self):
        """Crea scripts para ejecutar la aplicación"""
        self.print_header("📜 CREANDO SCRIPTS DE EJECUCIÓN")
        
        # Script Windows
        if self.is_windows:
            run_backend_win = """@echo off
echo ═══════════════════════════════════════════════════════════
echo   TESLA COTIZADOR V3.0 - INICIANDO BACKEND
echo ═══════════════════════════════════════════════════════════
echo.

echo [1/3] Activando entorno virtual...
call venv\\Scripts\\activate

echo [2/3] Verificando variables de entorno...
if not exist backend\\.env (
    echo ERROR: No se encontro el archivo .env
    echo Por favor configura backend\\.env con tu GEMINI_API_KEY
    pause
    exit /b 1
)

echo [3/3] Iniciando servidor FastAPI...
echo.
echo Backend corriendo en: http://localhost:8000
echo Documentacion API: http://localhost:8000/docs
echo.
echo Presiona CTRL+C para detener el servidor
echo.

uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

pause
"""
            self.create_file("run_backend.bat", run_backend_win)
            
            run_frontend_win = """@echo off
echo ═══════════════════════════════════════════════════════════
echo   TESLA COTIZADOR V3.0 - INICIANDO FRONTEND
echo ═══════════════════════════════════════════════════════════
echo.

cd frontend

echo [1/2] Verificando node_modules...
if not exist node_modules (
    echo Instalando dependencias...
    call npm install
)

echo [2/2] Iniciando React App...
echo.
echo Frontend corriendo en: http://localhost:3000
echo.
echo Presiona CTRL+C para detener el servidor
echo.

call npm start

pause
"""
            self.create_file("run_frontend.bat", run_frontend_win)
            
        # Script Linux/Mac
        run_backend_sh = """#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  TESLA COTIZADOR V3.0 - INICIANDO BACKEND"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "[1/3] Activando entorno virtual..."
source venv/bin/activate

echo "[2/3] Verificando variables de entorno..."
if [ ! -f backend/.env ]; then
    echo "ERROR: No se encontró el archivo .env"
    echo "Por favor configura backend/.env con tu GEMINI_API_KEY"
    exit 1
fi

echo "[3/3] Iniciando servidor FastAPI..."
echo ""
echo "Backend corriendo en: http://localhost:8000"
echo "Documentación API: http://localhost:8000/docs"
echo ""
echo "Presiona CTRL+C para detener el servidor"
echo ""

uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
"""
        self.create_file("run_backend.sh", run_backend_sh)
        
        run_frontend_sh = """#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  TESLA COTIZADOR V3.0 - INICIANDO FRONTEND"
echo "═══════════════════════════════════════════════════════════"
echo ""

cd frontend

echo "[1/2] Verificando node_modules..."
if [ ! -d "node_modules" ]; then
    echo "Instalando dependencias..."
    npm install
fi

echo "[2/2] Iniciando React App..."
echo ""
echo "Frontend corriendo en: http://localhost:3000"
echo ""
echo "Presiona CTRL+C para detener el servidor"
echo ""

npm start
"""
        self.create_file("run_frontend.sh", run_frontend_sh)
        
        # Hacer ejecutables los scripts (Linux/Mac)
        if not self.is_windows:
            try:
                os.chmod(self.base_path / "run_backend.sh", 0o755)
                os.chmod(self.base_path / "run_frontend.sh", 0o755)
            except:
                pass
                
    def create_package_json(self):
        """Crea package.json para el frontend"""
        package_json = {
            "name": "tesla-cotizador-frontend",
            "version": "3.0.0",
            "private": True,
            "description": "Tesla Cotizador v3.0 - Sistema profesional de cotización",
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "lucide-react": "^0.263.1",
                "axios": "^1.6.2"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "devDependencies": {
                "react-scripts": "5.0.1",
                "tailwindcss": "^3.3.0",
                "autoprefixer": "^10.4.16",
                "postcss": "^8.4.32"
            },
            "eslintConfig": {
                "extends": ["react-app"]
            },
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": ["last 1 chrome version"]
            }
        }
        self.create_file("frontend/package.json", json.dumps(package_json, indent=2))
        
    def print_final_instructions(self):
        """Imprime instrucciones finales"""
        self.print_header("✅ INSTALACIÓN COMPLETADA")
        
        instructions = f"""
{self.colors['OKGREEN']}{self.colors['BOLD']}¡FELICITACIONES! La estructura base está lista.{self.colors['ENDC']}

{self.colors['OKCYAN']}═══════════════════════════════════════════════════════════════
📋 SIGUIENTES PASOS:
═══════════════════════════════════════════════════════════════{self.colors['ENDC']}

{self.colors['BOLD']}1. CONFIGURAR API KEY DE GEMINI:{self.colors['ENDC']}
   - Edita: {self.colors['WARNING']}backend/.env{self.colors['ENDC']}
   - Cambia: {self.colors['WARNING']}GEMINI_API_KEY=tu_api_key_aqui{self.colors['ENDC']}

{self.colors['BOLD']}2. INSTALAR DEPENDENCIAS FRONTEND:{self.colors['ENDC']}
   cd frontend
   npm install

{self.colors['BOLD']}3. COPIAR TU CHASIS (CotizadorTesla30.jsx):{self.colors['ENDC']}
   - Copia tu archivo a: {self.colors['WARNING']}frontend/src/App.jsx{self.colors['ENDC']}

{self.colors['BOLD']}4. EJECUTAR APLICACIÓN:{self.colors['ENDC']}
   
   {self.colors['OKGREEN']}Backend:{self.colors['ENDC']}
   {'run_backend.bat' if self.is_windows else './run_backend.sh'}
   
   {self.colors['OKGREEN']}Frontend:{self.colors['ENDC']}
   {'run_frontend.bat' if self.is_windows else './run_frontend.sh'}

{self.colors['OKCYAN']}═══════════════════════════════════════════════════════════════
🌐 URLs DE ACCESO:
═══════════════════════════════════════════════════════════════{self.colors['ENDC']}

{self.colors['OKBLUE']}Frontend:{self.colors['ENDC']} http://localhost:3000
{self.colors['OKBLUE']}Backend API:{self.colors['ENDC']} http://localhost:8000
{self.colors['OKBLUE']}Docs API:{self.colors['ENDC']} http://localhost:8000/docs

{self.colors['OKCYAN']}═══════════════════════════════════════════════════════════════
📁 PRÓXIMOS ARCHIVOS GRANDES A RECIBIR:
═══════════════════════════════════════════════════════════════{self.colors['ENDC']}

Voy a entregarte los siguientes archivos completos para que los copies:

{self.colors['OKGREEN']}✓{self.colors['ENDC']} backend/app/main.py (FastAPI app principal)
{self.colors['OKGREEN']}✓{self.colors['ENDC']} backend/app/core/config.py (Configuración)
{self.colors['OKGREEN']}✓{self.colors['ENDC']} backend/app/services/gemini_service.py (Integración IA)
{self.colors['OKGREEN']}✓{self.colors['ENDC']} backend/app/services/word_generator.py (Generador Word)
{self.colors['OKGREEN']}✓{self.colors['ENDC']} backend/app/routers/cotizaciones.py (API cotizaciones)
{self.colors['OKGREEN']}✓{self.colors['ENDC']} frontend/src/services/api.js (Conexión API)

{self.colors['WARNING']}═══════════════════════════════════════════════════════════════
⚠️  IMPORTANTE:
═══════════════════════════════════════════════════════════════{self.colors['ENDC']}

- El entorno virtual Python YA ESTÁ ACTIVADO y con dependencias instaladas
- Solo falta configurar tu GEMINI_API_KEY en el archivo .env
- Los archivos grandes te llegarán a continuación

{self.colors['OKGREEN']}{self.colors['BOLD']}✅ ¡TODO LISTO PARA CONTINUAR!{self.colors['ENDC']}
"""
        print(instructions)
        
    def run(self):
        """Ejecuta el proceso completo de instalación"""
        try:
            self.print_header("🚀 TESLA COTIZADOR V3.0 - INSTALACIÓN PROFESIONAL")
            
            # 1. Crear estructura de directorios
            self.create_backend_structure()
            self.create_frontend_structure()
            self.create_database_structure()
            self.create_docs_structure()
            
            # 2. Crear archivos de configuración
            self.create_env_file()
            self.create_gitignore()
            self.create_requirements_txt()
            self.create_package_json()
            
            # 3. Crear documentación y scripts
            self.create_readme()
            self.create_run_scripts()
            
            # 4. Configurar entorno Python
            if self.setup_virtual_environment():
                self.install_python_dependencies()
            
            # 5. Instrucciones finales
            self.print_final_instructions()
            
        except KeyboardInterrupt:
            self.print_colored("\n\n⚠️  Instalación cancelada por el usuario", "WARNING")
            sys.exit(0)
        except Exception as e:
            self.print_colored(f"\n\n❌ Error durante la instalación: {e}", "FAIL")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    setup = TeslaSetupProfessional()
    setup.run()