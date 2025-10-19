# ============================================================
# TESLA COTIZADOR V3.0 - SCRIPT DE INICIALIZACIÓN
# ============================================================
# Este script verifica e instala todas las dependencias necesarias
# y arranca el backend correctamente
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 TESLA COTIZADOR V3.0 - INICIALIZACIÓN DEL BACKEND" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# 1. VERIFICAR UBICACIÓN
# ============================================================

$EXPECTED_PATH = "E:\TESLA_COTIZADOR-V3.0"

if ($PWD.Path -ne $EXPECTED_PATH) {
    Write-Host "⚠️  WARNING: No estás en la raíz del proyecto" -ForegroundColor Yellow
    Write-Host "   Ubicación actual: $($PWD.Path)" -ForegroundColor Yellow
    Write-Host "   Ubicación esperada: $EXPECTED_PATH" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📁 Cambiando a directorio correcto..." -ForegroundColor Cyan
    Set-Location $EXPECTED_PATH
}

Write-Host "✅ Ubicación correcta: $EXPECTED_PATH" -ForegroundColor Green
Write-Host ""

# ============================================================
# 2. VERIFICAR ENTORNO VIRTUAL
# ============================================================

Write-Host "🔍 Verificando entorno virtual..." -ForegroundColor Cyan

$VENV_PATH = ".\venv"
$VENV_PYTHON = ".\venv\Scripts\python.exe"
$VENV_ACTIVATE = ".\venv\Scripts\Activate.ps1"

if (-Not (Test-Path $VENV_PATH)) {
    Write-Host "❌ ERROR: Entorno virtual no existe en $VENV_PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ERROR: No se pudo crear el entorno virtual" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Entorno virtual creado" -ForegroundColor Green
}

Write-Host "✅ Entorno virtual existe" -ForegroundColor Green
Write-Host ""

# ============================================================
# 3. ACTIVAR ENTORNO VIRTUAL
# ============================================================

Write-Host "🔌 Activando entorno virtual..." -ForegroundColor Cyan

& $VENV_ACTIVATE

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: No se pudo activar el entorno virtual" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
Write-Host ""

# ============================================================
# 4. VERIFICAR E INSTALAR DEPENDENCIAS CRÍTICAS
# ============================================================

Write-Host "📦 Verificando dependencias críticas..." -ForegroundColor Cyan
Write-Host ""

$CRITICAL_PACKAGES = @(
    "fastapi",
    "uvicorn",
    "pydantic",
    "pydantic-settings",
    "sqlalchemy",
    "python-dotenv",
    "python-docx",
    "reportlab",
    "chromadb",
    "python-magic-bin",
    "requests"
)

$PACKAGES_TO_INSTALL = @()

foreach ($package in $CRITICAL_PACKAGES) {
    Write-Host "   Verificando $package..." -NoNewline
    
    $result = & $VENV_PYTHON -m pip show $package 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
    } else {
        Write-Host " ❌ FALTA" -ForegroundColor Red
        $PACKAGES_TO_INSTALL += $package
    }
}

Write-Host ""

# ============================================================
# 5. INSTALAR DEPENDENCIAS FALTANTES
# ============================================================

if ($PACKAGES_TO_INSTALL.Count -gt 0) {
    Write-Host "📥 Instalando dependencias faltantes..." -ForegroundColor Yellow
    Write-Host ""
    
    foreach ($package in $PACKAGES_TO_INSTALL) {
        Write-Host "   Instalando $package..." -ForegroundColor Cyan
        & $VENV_PYTHON -m pip install $package --quiet
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ $package instalado" -ForegroundColor Green
        } else {
            Write-Host "   ❌ Error instalando $package" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "✅ Todas las dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "✅ Todas las dependencias ya están instaladas" -ForegroundColor Green
}

Write-Host ""

# ============================================================
# 6. VERIFICAR ARCHIVOS CRÍTICOS
# ============================================================

Write-Host "📄 Verificando archivos críticos..." -ForegroundColor Cyan

$CRITICAL_FILES = @{
    "backend\app\main.py" = "Main de FastAPI"
    "backend\app\core\config.py" = "Configuración"
    "backend\app\core\database.py" = "Base de datos"
    "backend\.env" = "Variables de entorno"
}

$ALL_FILES_OK = $true

foreach ($file in $CRITICAL_FILES.Keys) {
    Write-Host "   $($CRITICAL_FILES[$file])..." -NoNewline
    
    if (Test-Path $file) {
        Write-Host " ✅" -ForegroundColor Green
    } else {
        Write-Host " ❌ FALTA" -ForegroundColor Red
        $ALL_FILES_OK = $false
    }
}

Write-Host ""

if (-Not $ALL_FILES_OK) {
    Write-Host "⚠️  WARNING: Algunos archivos críticos faltan" -ForegroundColor Yellow
    Write-Host "   El sistema puede no funcionar correctamente" -ForegroundColor Yellow
    Write-Host ""
}

# ============================================================
# 7. VERIFICAR ESTRUCTURA DE ROUTERS
# ============================================================

Write-Host "🔌 Verificando routers..." -ForegroundColor Cyan

$ROUTERS = @(
    "cotizaciones",
    "proyectos",
    "documentos",
    "chat"
)

$ALL_ROUTERS_OK = $true

foreach ($router in $ROUTERS) {
    Write-Host "   Router $router..." -NoNewline
    
    $router_file = "backend\app\routers\$router.py"
    
    if (Test-Path $router_file) {
        Write-Host " ✅" -ForegroundColor Green
    } else {
        Write-Host " ❌ FALTA" -ForegroundColor Red
        $ALL_ROUTERS_OK = $false
    }
}

Write-Host ""

# ============================================================
# 8. TEST DE IMPORTS
# ============================================================

Write-Host "🧪 Probando imports de Python..." -ForegroundColor Cyan

$IMPORT_TESTS = @(
    @{cmd="from pydantic_settings import BaseSettings"; desc="pydantic_settings"},
    @{cmd="from fastapi import FastAPI"; desc="FastAPI"},
    @{cmd="from sqlalchemy import create_engine"; desc="SQLAlchemy"},
    @{cmd="import chromadb"; desc="ChromaDB"}
)

$ALL_IMPORTS_OK = $true

foreach ($test in $IMPORT_TESTS) {
    Write-Host "   $($test.desc)..." -NoNewline
    
    $result = & $VENV_PYTHON -c $test.cmd 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $ALL_IMPORTS_OK = $false
    }
}

Write-Host ""

if (-Not $ALL_IMPORTS_OK) {
    Write-Host "❌ ERROR: Algunos imports fallan" -ForegroundColor Red
    Write-Host "   Ejecuta: pip install -r backend\requirements.txt" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# ============================================================
# 9. VERIFICAR PUERTO 8000
# ============================================================

Write-Host "🔌 Verificando puerto 8000..." -ForegroundColor Cyan

$port_in_use = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

if ($port_in_use) {
    Write-Host "⚠️  Puerto 8000 ya está en uso" -ForegroundColor Yellow
    Write-Host "   PID: $($port_in_use.OwningProcess)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Opciones:" -ForegroundColor Cyan
    Write-Host "   1. Detener el proceso: Stop-Process -Id $($port_in_use.OwningProcess)" -ForegroundColor Yellow
    Write-Host "   2. O el backend ya está corriendo ✅" -ForegroundColor Green
    Write-Host ""
    
    $continue = Read-Host "¿Continuar de todas formas? (s/n)"
    
    if ($continue -ne "s") {
        exit 0
    }
} else {
    Write-Host "✅ Puerto 8000 disponible" -ForegroundColor Green
}

Write-Host ""

# ============================================================
# 10. INICIAR BACKEND
# ============================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 INICIANDO BACKEND" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Ubicación: backend/" -ForegroundColor Cyan
Write-Host "🔌 Puerto: 8000" -ForegroundColor Cyan
Write-Host "📚 Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location backend

& $VENV_PYTHON -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000