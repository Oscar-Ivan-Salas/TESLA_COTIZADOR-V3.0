# ============================================
# AUDITORIA FINAL COMPLETA
# TESLA COTIZADOR V3
# Verifica TODOS los archivos creados
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AUDITORIA FINAL COMPLETA             " -ForegroundColor Cyan
Write-Host "   Verificando archivos creados         " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$reportFile = "auditoria-final-$timestamp.txt"

# ============================================
# FUNCIÓN PARA REPORTAR
# ============================================

function Write-Report {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
    Add-Content -Path $reportFile -Value $Message
}

# Iniciar reporte
Write-Report "========================================" "Cyan"
Write-Report "AUDITORIA FINAL - TESLA COTIZADOR V3" "Cyan"
Write-Report "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

# ============================================
# LISTA COMPLETA DE ARCHIVOS ESPERADOS
# ============================================

$archivosEsperados = @{
    # RAÍZ
    ".gitignore" = "Control de versiones"
    "docker-compose.yml" = "Orquestación Docker"
    "README.md" = "Documentación"
    
    # BACKEND - Core
    "backend\app\__init__.py" = "Package backend"
    "backend\app\main.py" = "Aplicación FastAPI principal"
    "backend\app\core\__init__.py" = "Package core"
    "backend\app\core\config.py" = "Configuración"
    "backend\app\core\database.py" = "Conexión BD"
    
    # BACKEND - Models
    "backend\app\models\__init__.py" = "Package models"
    "backend\app\models\proyecto.py" = "Modelo Proyecto"
    "backend\app\models\cotizacion.py" = "Modelo Cotizacion"
    "backend\app\models\documento.py" = "Modelo Documento"
    "backend\app\models\item.py" = "Modelo Item"
    
    # BACKEND - Schemas
    "backend\app\schemas\__init__.py" = "Package schemas"
    "backend\app\schemas\proyecto.py" = "Schema Proyecto"
    "backend\app\schemas\cotizacion.py" = "Schema Cotizacion"
    "backend\app\schemas\documento.py" = "Schema Documento"
    
    # BACKEND - Services
    "backend\app\services\__init__.py" = "Package services"
    "backend\app\services\gemini_service.py" = "Servicio Gemini AI"
    "backend\app\services\word_generator.py" = "Generador Word"
    "backend\app\services\pdf_generator.py" = "Generador PDF"
    "backend\app\services\file_processor.py" = "Procesador archivos"
    "backend\app\services\rag_service.py" = "Servicio RAG/ChromaDB"
    
    # BACKEND - Routers
    "backend\app\routers\__init__.py" = "Package routers"
    "backend\app\routers\proyectos.py" = "Router Proyectos"
    "backend\app\routers\cotizaciones.py" = "Router Cotizaciones"
    "backend\app\routers\chat.py" = "Router Chat IA"
    "backend\app\routers\documentos.py" = "Router Documentos"
    
    # BACKEND - Utils
    "backend\app\utils\__init__.py" = "Package utils"
    "backend\app\utils\ocr.py" = "Utilidad OCR"
    "backend\app\utils\helpers.py" = "Funciones helper"
    
    # BACKEND - Config
    "backend\requirements.txt" = "Dependencias Python"
    "backend\.env.example" = "Template env backend"
    
    # FRONTEND
    "frontend\package.json" = "Dependencias Node"
    "frontend\public\index.html" = "HTML principal"
    "frontend\src\index.js" = "Entry point React"
    "frontend\src\index.css" = "Estilos globales"
    "frontend\src\App.jsx" = "Componente principal"
    "frontend\.env.example" = "Template env frontend"
    
    # DATABASE
    "database\init.sql" = "Script inicialización BD"
}

# ============================================
# VERIFICAR ARCHIVOS CREADOS
# ============================================

Write-Report "========================================" "Cyan"
Write-Report "1. VERIFICACION DE ARCHIVOS CREADOS" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

$existentes = 0
$faltantes = 0
$archivosFaltantes = @()

foreach ($archivo in $archivosEsperados.Keys | Sort-Object) {
    $descripcion = $archivosEsperados[$archivo]
    $rutaCompleta = Join-Path $PSScriptRoot $archivo
    
    if (Test-Path $rutaCompleta) {
        # Verificar que no esté vacío
        $lineas = (Get-Content $rutaCompleta -ErrorAction SilentlyContinue).Count
        
        if ($lineas -gt 0) {
            Write-Report ("[OK] {0} ({1} lineas)" -f $archivo, $lineas) "Green"
            $existentes++
        } else {
            Write-Report ("[VACIO] {0} - {1}" -f $archivo, $descripcion) "Yellow"
            $existentes++
        }
    } else {
        Write-Report ("[FALTA] {0} - {1}" -f $archivo, $descripcion) "Red"
        $faltantes++
        $archivosFaltantes += $archivo
    }
}

Write-Report ""
Write-Report "Resumen:" "Yellow"
Write-Report ("  [OK] Archivos existentes: {0}" -f $existentes) "Green"
Write-Report ("  [FALTA] Archivos faltantes: {0}" -f $faltantes) "Red"
Write-Report ""

# ============================================
# CONTAR LÍNEAS DE CÓDIGO
# ============================================

Write-Report "========================================" "Cyan"
Write-Report "2. CONTEO DE LINEAS DE CODIGO" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

function Count-Lines {
    param([string]$Path, [string]$Extension)
    
    $files = Get-ChildItem -Path $Path -Recurse -Filter "*.$Extension" -File -ErrorAction SilentlyContinue | Where-Object {
        $_.DirectoryName -notmatch 'node_modules|venv|\.git|__pycache__|build|dist'
    }
    
    $totalLines = 0
    $fileCount = 0
    
    foreach ($file in $files) {
        $lines = (Get-Content $file.FullName -ErrorAction SilentlyContinue).Count
        $totalLines += $lines
        $fileCount++
    }
    
    return @{
        Files = $fileCount
        Lines = $totalLines
    }
}

# Python
$pythonStats = Count-Lines -Path (Join-Path $PSScriptRoot "backend") -Extension "py"
Write-Report ("[PYTHON] {0} archivos - {1} lineas" -f $pythonStats.Files, $pythonStats.Lines) "Cyan"

# JavaScript/JSX
$jsStats = Count-Lines -Path (Join-Path $PSScriptRoot "frontend") -Extension "js"
$jsxStats = Count-Lines -Path (Join-Path $PSScriptRoot "frontend") -Extension "jsx"
$totalJS = $jsStats.Lines + $jsxStats.Lines
$totalJSFiles = $jsStats.Files + $jsxStats.Files
Write-Report ("[JAVASCRIPT/JSX] {0} archivos - {1} lineas" -f $totalJSFiles, $totalJS) "Cyan"

# CSS
$cssStats = Count-Lines -Path (Join-Path $PSScriptRoot "frontend") -Extension "css"
Write-Report ("[CSS] {0} archivos - {1} lineas" -f $cssStats.Files, $cssStats.Lines) "Cyan"

# SQL
$sqlStats = Count-Lines -Path (Join-Path $PSScriptRoot "database") -Extension "sql"
Write-Report ("[SQL] {0} archivos - {1} lineas" -f $sqlStats.Files, $sqlStats.Lines) "Cyan"

# YAML
$yamlFiles = Get-ChildItem -Path $PSScriptRoot -Filter "*.yml" -File -ErrorAction SilentlyContinue
$yamlLines = 0
foreach ($file in $yamlFiles) {
    $yamlLines += (Get-Content $file.FullName -ErrorAction SilentlyContinue).Count
}
Write-Report ("[YAML] {0} archivos - {1} lineas" -f $yamlFiles.Count, $yamlLines) "Cyan"

# Markdown
$mdFiles = Get-ChildItem -Path $PSScriptRoot -Filter "*.md" -File -Recurse -ErrorAction SilentlyContinue | Where-Object {
    $_.DirectoryName -notmatch 'node_modules|venv'
}
$mdLines = 0
foreach ($file in $mdFiles) {
    $mdLines += (Get-Content $file.FullName -ErrorAction SilentlyContinue).Count
}
Write-Report ("[MARKDOWN] {0} archivos - {1} lineas" -f $mdFiles.Count, $mdLines) "Cyan"

Write-Report ""
$totalLineas = $pythonStats.Lines + $totalJS + $cssStats.Lines + $sqlStats.Lines + $yamlLines + $mdLines
Write-Report ("[TOTAL] {0} lineas de codigo" -f $totalLineas) "Yellow"
Write-Report ""

# ============================================
# VERIFICAR ESTRUCTURA DE CARPETAS
# ============================================

Write-Report "========================================" "Cyan"
Write-Report "3. ESTRUCTURA DE CARPETAS" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

$carpetasEsperadas = @(
    "backend",
    "backend\app",
    "backend\app\core",
    "backend\app\models",
    "backend\app\schemas",
    "backend\app\services",
    "backend\app\routers",
    "backend\app\utils",
    "backend\storage",
    "backend\storage\documentos",
    "backend\storage\generados",
    "backend\storage\chroma_db",
    "frontend",
    "frontend\public",
    "frontend\src",
    "frontend\src\components",
    "frontend\src\services",
    "database",
    "database\migrations"
)

$carpetasOK = 0
$carpetasFaltan = 0

foreach ($carpeta in $carpetasEsperadas) {
    $rutaCompleta = Join-Path $PSScriptRoot $carpeta
    if (Test-Path $rutaCompleta -PathType Container) {
        Write-Report ("[OK] {0}" -f $carpeta) "Green"
        $carpetasOK++
    } else {
        Write-Report ("[FALTA] {0}" -f $carpeta) "Red"
        $carpetasFaltan++
    }
}

Write-Report ""
Write-Report ("Carpetas encontradas: {0} de {1}" -f $carpetasOK, $carpetasEsperadas.Count) "Yellow"
Write-Report ""

# ============================================
# VERIFICAR ENTORNO VIRTUAL
# ============================================

Write-Report "========================================" "Cyan"
Write-Report "4. ENTORNO VIRTUAL" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

$venvPath = Join-Path $PSScriptRoot "backend\venv"
if (Test-Path $venvPath) {
    Write-Report "[OK] Entorno virtual encontrado en backend\venv" "Green"
} else {
    Write-Report "[FALTA] No se encontró el entorno virtual en backend\venv" "Red"
}

# ============================================
# VERIFICAR NODE_MODULES
# ============================================

Write-Report "========================================" "Cyan"
Write-Report "5. DEPENDENCIAS DE NODE" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

$nodeModulesPath = Join-Path $PSScriptRoot "frontend\node_modules"
if (Test-Path $nodeModulesPath) {
    Write-Report "[OK] Dependencias de Node.js instaladas" "Green"
} else {
    Write-Report "[FALTA] Ejecutar: cd frontend; npm install" "Red"
}

Write-Report ""

# ============================================
# VERIFICAR ARCHIVOS DE CONFIGURACIÓN
# ============================================

Write-Report "========================================" "Cyan"
Write-Report "6. ARCHIVOS DE CONFIGURACION" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

# Verificar .env del backend
$backendEnv = Join-Path $PSScriptRoot "backend\.env"
if (Test-Path $backendEnv) {
    $envContent = Get-Content $backendEnv -Raw
    if ($envContent -match "GEMINI_API_KEY=") {
        Write-Report "[OK] Archivo .env del backend (con GEMINI_API_KEY)" "Green"
    } else {
        Write-Report "[ADVERTENCIA] .env del backend sin GEMINI_API_KEY" "Yellow"
    }
} else {
    Write-Report "[FALTA] Archivo .env del backend no encontrado" "Red"
}

# Verificar .env del frontend
$frontendEnv = Join-Path $PSScriptRoot "frontend\.env"
if (Test-Path $frontendEnv) {
    Write-Report "[OK] Archivo .env del frontend" "Green"
} else {
    Write-Report "[ADVERTENCIA] Archivo .env del frontend no encontrado" "Yellow"
}

Write-Report ""

# ============================================
# RESUMEN FINAL
# ============================================

Write-Report "========================================" "Cyan"
Write-Report "RESUMEN FINAL" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

$porcentajeCompletitud = [math]::Round(($existentes / $archivosEsperados.Count) * 100, 1)

# Mostrar resumen
Write-Report "ESTADISTICAS GENERALES:" "Yellow"
Write-Report ("- Archivos: {0}/{1} ({2}%)" -f $existentes, $archivosEsperados.Count, $porcentajeCompletitud) "White"
Write-Report ("- Carpetas: {0}/{1}" -f $carpetasOK, $carpetasEsperadas.Count) "White"
Write-Report ("- Lineas de codigo: {0}" -f $totalLineas) "White"
Write-Report ""

# Estado del proyecto
if ($porcentajeCompletitud -ge 90) {
    Write-Report "ESTADO: PROYECTO COMPLETO" "Green"
} elseif ($porcentajeCompletitud -ge 70) {
    Write-Report "ESTADO: PROYECTO CASI COMPLETO" "Yellow"
} else {
    Write-Report "ESTADO: PROYECTO INCOMPLETO" "Red"
}

# Mostrar archivos faltantes si los hay
if ($archivosFaltantes.Count -gt 0) {
    Write-Report ""
    Write-Report "ARCHIVOS FALTANTES:" "Yellow"
    foreach ($archivo in $archivosFaltantes) {
        Write-Report ("- {0}" -f $archivo) "Red"
    }
}

# Mostrar carpetas faltantes si las hay
if ($carpetasFaltan -gt 0) {
    Write-Report ""
    Write-Report "CARPETAS FALTANTES:" "Yellow"
    foreach ($carpeta in $carpetasEsperadas) {
        $rutaCompleta = Join-Path $PSScriptRoot $carpeta
        if (-not (Test-Path $rutaCompleta -PathType Container)) {
            Write-Report ("- {0}" -f $carpeta) "Red"
        }
    }
}

# Mostrar pasos siguientes
Write-Report ""
Write-Report "SIGUIENTES PASOS:" "Cyan"
if (-not (Test-Path $venvPath)) {
    Write-Report "1. Crear entorno virtual: python -m venv backend\venv" "White"
} else {
    Write-Report "1. [HECHO] Entorno virtual creado" "Green"
}

if (-not (Test-Path (Join-Path $PSScriptRoot "backend\requirements.txt"))) {
    Write-Report "2. Crear archivo requirements.txt con las dependencias" "White"
} else {
    Write-Report "2. [HECHO] Archivo requirements.txt encontrado" "Green"
}

if (-not (Test-Path $nodeModulesPath)) {
    Write-Report "3. Instalar dependencias de Node.js: cd frontend; npm install" "White"
} else {
    Write-Report "3. [HECHO] Dependencias de Node.js instaladas" "Green"
}

Write-Report "4. Configurar archivos .env con las credenciales necesarias" "White"
Write-Report "5. Iniciar el servidor de desarrollo" "White"

# Guardar reporte
Write-Report ""
Write-Report "========================================" "Cyan"
Write-Report ("Reporte guardado en: {0}" -f $reportFile) "Green"
Write-Report "========================================" "Cyan"

# Mostrar mensaje final
Write-Host ""
Write-Host "Auditoria completada. Revisa el archivo $reportFile para ver el informe detallado." -ForegroundColor Cyan
Write-Host ""