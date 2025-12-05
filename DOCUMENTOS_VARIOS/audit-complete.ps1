# ============================================
# AUDITORIA COMPLETA PROFESIONAL
# TESLA COTIZADOR V3
# NO ELIMINA NADA - SOLO ANALIZA
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AUDITORIA PROFESIONAL COMPLETA      " -ForegroundColor Cyan
Write-Host "   (Sin eliminar ni modificar nada)    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$reportFile = "auditoria-completa-$timestamp.txt"

# Función para escribir en reporte y consola
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
Write-Report "AUDITORIA COMPLETA - TESLA COTIZADOR V3" "Cyan"
Write-Report "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

# ============================================
# 1. ESTRUCTURA COMPLETA DEL PROYECTO
# ============================================

Write-Report "========================================" "Cyan"
Write-Report "1. ESTRUCTURA COMPLETA DEL PROYECTO" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

function Get-TreeStructure {
    param(
        [string]$Path = ".",
        [int]$Depth = 0,
        [int]$MaxDepth = 10,
        [string]$Prefix = "",
        [switch]$LastItem
    )
    
    if ($Depth -gt $MaxDepth) { return }
    
    # Obtener items excluyendo carpetas pesadas
    $items = Get-ChildItem -Path $Path -Force -ErrorAction SilentlyContinue | Where-Object {
        $_.Name -notmatch '^(node_modules|\.git|__pycache__|\.pytest_cache|\.next)$'
    } | Sort-Object { $_.PSIsContainer }, Name
    
    $totalItems = $items.Count
    $currentIndex = 0
    
    foreach ($item in $items) {
        $currentIndex++
        $isLast = ($currentIndex -eq $totalItems)
        
        # Símbolos del árbol
        if ($isLast) {
            $branch = "`-- "
            $extension = "    "
        } else {
            $branch = "|-- "
            $extension = "|   "
        }
        
        # Determinar icono según tipo
        $icon = if ($item.PSIsContainer) { 
            "[DIR]" 
        } elseif ($item.Extension -match '\.(py|js|jsx|ts|tsx)$') {
            "[CODE]"
        } elseif ($item.Extension -match '\.(json|yml|yaml|toml|ini|env)$') {
            "[CONF]"
        } elseif ($item.Extension -match '\.(md|txt|pdf|docx)$') {
            "[DOC]"
        } elseif ($item.Extension -match '\.(sql)$') {
            "[SQL]"
        } else {
            "[FILE]"
        }
        
        # Construir línea
        $line = "$Prefix$branch$icon $($item.Name)"
        
        # Agregar tamaño si es archivo
        if (-not $item.PSIsContainer) {
            $size = if ($item.Length -gt 1MB) {
                "{0:N2} MB" -f ($item.Length / 1MB)
            } elseif ($item.Length -gt 1KB) {
                "{0:N2} KB" -f ($item.Length / 1KB)
            } else {
                "$($item.Length) bytes"
            }
            $line += " ($size)"
        }
        
        Write-Report $line "Gray"
        
        # Recursión para carpetas
        if ($item.PSIsContainer) {
            $newPrefix = "$Prefix$extension"
            Get-TreeStructure -Path $item.FullName -Depth ($Depth + 1) -MaxDepth $MaxDepth -Prefix $newPrefix
        }
    }
}

Write-Report "TESLA-COTIZADOR-V3/" "Cyan"
Get-TreeStructure -MaxDepth 10

# ============================================
# 2. INVENTARIO DETALLADO DE ARCHIVOS
# ============================================

Write-Report ""
Write-Report "========================================" "Cyan"
Write-Report "2. INVENTARIO DETALLADO DE ARCHIVOS" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

# Obtener TODOS los archivos
$allFiles = Get-ChildItem -Path . -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
    $_.DirectoryName -notmatch 'node_modules|\.git|__pycache__|venv\\|\.venv'
}

# Agrupar por extensión
$filesByExtension = $allFiles | Group-Object Extension | Sort-Object Count -Descending

Write-Report "Total de archivos encontrados: $($allFiles.Count)" "Yellow"
Write-Report ""
Write-Report "Archivos por tipo:" "Yellow"

foreach ($group in $filesByExtension) {
    $ext = if ($group.Name) { $group.Name } else { "(sin extension)" }
    Write-Report "  $ext : $($group.Count) archivos" "Gray"
}

# ============================================
# 3. ANÁLISIS DE CARPETAS PRINCIPALES
# ============================================

Write-Report ""
Write-Report "========================================" "Cyan"
Write-Report "3. ANALISIS DE CARPETAS PRINCIPALES" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

$mainFolders = @("backend", "frontend", "database")

foreach ($folder in $mainFolders) {
    if (Test-Path $folder) {
        Write-Report "[$folder]" "Green"
        
        # Contar archivos
        $files = Get-ChildItem -Path $folder -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
            $_.DirectoryName -notmatch 'node_modules|venv|\.git|__pycache__'
        }
        
        Write-Report "  Total archivos: $($files.Count)" "Gray"
        
        # Agrupar por extensión
        $extensions = $files | Group-Object Extension | Sort-Object Count -Descending
        foreach ($ext in $extensions) {
            $extName = if ($ext.Name) { $ext.Name } else { "(sin ext)" }
            Write-Report "    $extName : $($ext.Count)" "Gray"
        }
        
        Write-Report ""
    } else {
        Write-Report "[$folder] - NO EXISTE" "Red"
        Write-Report ""
    }
}

# ============================================
# 4. ARCHIVOS CRÍTICOS - VERIFICACIÓN
# ============================================

Write-Report ""
Write-Report "========================================" "Cyan"
Write-Report "4. VERIFICACION DE ARCHIVOS CRITICOS" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

$criticalFiles = @{
    # Raíz
    "docker-compose.yml" = "Orquestacion Docker"
    ".gitignore" = "Control de versiones"
    ".env.example" = "Template variables entorno"
    "README.md" = "Documentacion principal"
    
    # Backend - Configuración
    "backend\requirements.txt" = "Dependencias Python"
    "backend\.env" = "Variables de entorno backend"
    "backend\.env.example" = "Template env backend"
    "backend\Dockerfile" = "Imagen Docker backend"
    
    # Backend - Aplicación
    "backend\app\__init__.py" = "Paquete Python app"
    "backend\app\main.py" = "Entry point FastAPI"
    "backend\app\core\__init__.py" = "Paquete core"
    "backend\app\core\config.py" = "Configuracion app"
    "backend\app\core\database.py" = "Conexion BD"
    
    # Backend - Modelos
    "backend\app\models\__init__.py" = "Paquete models"
    "backend\app\models\cotizacion.py" = "Modelo Cotizacion"
    "backend\app\models\proyecto.py" = "Modelo Proyecto"
    "backend\app\models\documento.py" = "Modelo Documento"
    
    # Backend - Schemas
    "backend\app\schemas\__init__.py" = "Paquete schemas"
    "backend\app\schemas\cotizacion.py" = "Schema Cotizacion"
    
    # Backend - Services
    "backend\app\services\__init__.py" = "Paquete services"
    "backend\app\services\gemini_service.py" = "Servicio Gemini AI"
    "backend\app\services\word_generator.py" = "Generador Word"
    "backend\app\services\pdf_generator.py" = "Generador PDF"
    
    # Backend - Routers
    "backend\app\routers\__init__.py" = "Paquete routers"
    "backend\app\routers\cotizaciones.py" = "Endpoints cotizaciones"
    "backend\app\routers\proyectos.py" = "Endpoints proyectos"
    "backend\app\routers\chat.py" = "Endpoints chat IA"
    
    # Backend - Utils
    "backend\app\utils\__init__.py" = "Paquete utils"
    "backend\app\utils\ocr.py" = "Utilidad OCR"
    "backend\app\utils\helpers.py" = "Funciones helper"
    
    # Frontend - Configuración
    "frontend\package.json" = "Dependencias Node"
    "frontend\.env.local" = "Variables entorno frontend"
    "frontend\.env.example" = "Template env frontend"
    "frontend\Dockerfile" = "Imagen Docker frontend"
    "frontend\tailwind.config.js" = "Config Tailwind"
    "frontend\postcss.config.js" = "Config PostCSS"
    
    # Frontend - Aplicación
    "frontend\public\index.html" = "HTML principal"
    "frontend\src\index.js" = "Entry point React"
    "frontend\src\index.css" = "Estilos globales"
    "frontend\src\App.jsx" = "Componente principal"
    
    # Frontend - Componentes
    "frontend\src\components\ChatIA.jsx" = "Componente Chat IA"
    "frontend\src\components\UploadZone.jsx" = "Componente Upload"
    "frontend\src\components\CotizacionEditor.jsx" = "Editor cotizacion"
    "frontend\src\components\VistaPrevia.jsx" = "Vista previa"
    "frontend\src\components\Alerta.jsx" = "Componente alerta"
    
    # Frontend - Services
    "frontend\src\services\api.js" = "Cliente API"
    
    # Database
    "database\init.sql" = "Script inicializacion BD"
    "database\migrations\README.md" = "Guia migraciones"
}

$existingFiles = @()
$missingFiles = @()

foreach ($file in $criticalFiles.Keys) {
    if (Test-Path $file) {
        Write-Report "[OK] $file" "Green"
        $existingFiles += $file
    } else {
        Write-Report "[FALTA] $file - $($criticalFiles[$file])" "Red"
        $missingFiles += $file
    }
}

Write-Report ""
Write-Report "Resumen:" "Yellow"
Write-Report "  Archivos existentes: $($existingFiles.Count)" "Green"
Write-Report "  Archivos faltantes: $($missingFiles.Count)" "Red"

# ============================================
# 5. DETECCIÓN DE DUPLICADOS
# ============================================

Write-Report ""
Write-Report "========================================" "Cyan"
Write-Report "5. DETECCION DE DUPLICADOS" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

# Entornos virtuales
Write-Report "[ENTORNOS VIRTUALES]" "Yellow"
$venvs = Get-ChildItem -Path . -Recurse -Directory -ErrorAction SilentlyContinue | Where-Object {
    $_.Name -match '^(venv|env|\.venv|virtualenv)$'
}

if ($venvs.Count -eq 0) {
    Write-Report "  No se encontraron entornos virtuales" "Gray"
} else {
    foreach ($venv in $venvs) {
        $path = $venv.FullName.Replace($PWD.Path, ".")
        if ($path -eq ".\backend\venv") {
            Write-Report "  [OK] $path (ubicacion correcta)" "Green"
        } else {
            Write-Report "  [DUPLICADO] $path (debe estar solo en backend\venv)" "Yellow"
        }
    }
}

# node_modules
Write-Report ""
Write-Report "[NODE_MODULES]" "Yellow"
$nodeModules = Get-ChildItem -Path . -Recurse -Directory -Filter "node_modules" -ErrorAction SilentlyContinue

if ($nodeModules.Count -eq 0) {
    Write-Report "  No se encontraron carpetas node_modules" "Gray"
} else {
    foreach ($nm in $nodeModules) {
        $path = $nm.FullName.Replace($PWD.Path, ".")
        if ($path -eq ".\frontend\node_modules") {
            Write-Report "  [OK] $path (ubicacion correcta)" "Green"
        } else {
            Write-Report "  [DUPLICADO] $path (debe estar solo en frontend\node_modules)" "Yellow"
        }
    }
}

# Archivos .env
Write-Report ""
Write-Report "[ARCHIVOS .ENV]" "Yellow"
$envFiles = Get-ChildItem -Path . -Recurse -Filter ".env*" -File -ErrorAction SilentlyContinue | Where-Object {
    $_.DirectoryName -notmatch 'node_modules|venv|\.git'
}

if ($envFiles.Count -eq 0) {
    Write-Report "  No se encontraron archivos .env" "Gray"
} else {
    foreach ($env in $envFiles) {
        $path = $env.FullName.Replace($PWD.Path, ".")
        Write-Report "  $path" "Gray"
    }
}

# ============================================
# 6. ARCHIVOS TEMPORALES Y CACHE
# ============================================

Write-Report ""
Write-Report "========================================" "Cyan"
Write-Report "6. ARCHIVOS TEMPORALES Y CACHE" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

# __pycache__
$pycache = Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue
Write-Report "[__pycache__] $($pycache.Count) carpetas encontradas" "Yellow"

# .pyc
$pyc = Get-ChildItem -Path . -Recurse -Include "*.pyc", "*.pyo" -File -ErrorAction SilentlyContinue | Where-Object {
    $_.DirectoryName -notmatch 'venv'
}
Write-Report "[.pyc/.pyo] $($pyc.Count) archivos encontrados" "Yellow"

# Temporales
$temp = Get-ChildItem -Path . -Recurse -Include "*.tmp", "*.log", "*.bak" -File -ErrorAction SilentlyContinue
Write-Report "[Temporales] $($temp.Count) archivos encontrados (.tmp, .log, .bak)" "Yellow"

# ============================================
# 7. ANÁLISIS DE TAMAÑOS
# ============================================

Write-Report ""
Write-Report "========================================" "Cyan"
Write-Report "7. ANALISIS DE TAMANOS" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

function Get-FolderSizeFormatted {
    param([string]$Path)
    
    if (-not (Test-Path $Path)) { return "N/A" }
    
    $size = (Get-ChildItem -Path $Path -Recurse -File -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum).Sum
    
    if ($null -eq $size) { return "0 bytes" }
    
    if ($size -gt 1GB) {
        return "{0:N2} GB" -f ($size / 1GB)
    } elseif ($size -gt 1MB) {
        return "{0:N2} MB" -f ($size / 1MB)
    } elseif ($size -gt 1KB) {
        return "{0:N2} KB" -f ($size / 1KB)
    } else {
        return "$size bytes"
    }
}

$folders = @{
    "backend" = "Backend FastAPI"
    "frontend" = "Frontend React"
    "database" = "Scripts BD"
    "backend\venv" = "Entorno virtual Python"
    "frontend\node_modules" = "Dependencias Node"
}

foreach ($folder in $folders.Keys) {
    if (Test-Path $folder) {
        $size = Get-FolderSizeFormatted -Path $folder
        Write-Report "[$folder] $size" "Cyan"
    }
}

# ============================================
# 8. VALIDACIÓN DE SINTAXIS
# ============================================

Write-Report ""
Write-Report "========================================" "Cyan"
Write-Report "8. VALIDACION DE SINTAXIS" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

# Python files
Write-Report "[ARCHIVOS PYTHON]" "Yellow"
$pyFiles = Get-ChildItem -Path "backend\app" -Recurse -Filter "*.py" -File -ErrorAction SilentlyContinue

$validPy = 0
$invalidPy = 0

foreach ($pyFile in $pyFiles) {
    try {
        python -m py_compile $pyFile.FullName 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $validPy++
        } else {
            $invalidPy++
            Write-Report "  [ERROR] $($pyFile.Name)" "Red"
        }
    } catch {
        $invalidPy++
        Write-Report "  [ERROR] $($pyFile.Name)" "Red"
    }
}

Write-Report "  Archivos validos: $validPy" "Green"
if ($invalidPy -gt 0) {
    Write-Report "  Archivos con errores: $invalidPy" "Red"
}

# ============================================
# 9. RESUMEN Y RECOMENDACIONES
# ============================================

Write-Report ""
Write-Report "========================================" "Cyan"
Write-Report "9. RESUMEN Y RECOMENDACIONES" "Cyan"
Write-Report "========================================" "Cyan"
Write-Report ""

Write-Report "RESUMEN GENERAL:" "Yellow"
Write-Report "  Total archivos analizados: $($allFiles.Count)" "Gray"
Write-Report "  Archivos criticos existentes: $($existingFiles.Count)" "Green"
Write-Report "  Archivos criticos faltantes: $($missingFiles.Count)" "Red"
Write-Report ""

Write-Report "ESTADO DEL PROYECTO:" "Yellow"
$completionPercentage = [math]::Round(($existingFiles.Count / $criticalFiles.Count) * 100, 1)
Write-Report "  Completitud estimada: $completionPercentage%" $(if ($completionPercentage -ge 80) { "Green" } elseif ($completionPercentage -ge 50) { "Yellow" } else { "Red" })
Write-Report ""

if ($missingFiles.Count -gt 0) {
    Write-Report "ARCHIVOS FALTANTES PRIORITARIOS:" "Yellow"
    foreach ($missing in $missingFiles) {
        Write-Report "  - $missing" "Gray"
    }
    Write-Report ""
}

Write-Report "ACCIONES RECOMENDADAS:" "Yellow"

$actions = @()

if ($venvs.Count -gt 1) {
    $actions += "Mover entorno virtual duplicado a backend\venv"
}

if ($pycache.Count -gt 0 -or $pyc.Count -gt 0) {
    $actions += "Limpiar archivos cache de Python ($($pycache.Count + $pyc.Count) elementos)"
}

if ($missingFiles.Count -gt 0) {
    $actions += "Crear $($missingFiles.Count) archivos faltantes"
}

if (-not (Test-Path "backend\.env")) {
    $actions += "Configurar backend\.env con GEMINI_API_KEY"
}

if ($actions.Count -eq 0) {
    Write-Report "  [OK] Proyecto en buen estado!" "Green"
} else {
    for ($i = 0; $i -lt $actions.Count; $i++) {
        Write-Report "  $($i + 1). $($actions[$i])" "Cyan"
    }
}

# ============================================
# FINALIZAR REPORTE
# ============================================

Write-Report ""
Write-Report "========================================" "Cyan"
Write-Report "AUDITORIA COMPLETADA" "Cyan"
Write-Report "Reporte guardado en: $reportFile" "Green"
Write-Report "========================================" "Cyan"

Write-Host ""
Write-Host "Reporte completo guardado en: $reportFile" -ForegroundColor Green
Write-Host "Abre ese archivo para ver el analisis detallado" -ForegroundColor Yellow