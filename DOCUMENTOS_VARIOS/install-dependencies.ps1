# ============================================================
# TESLA COTIZADOR V3.0 - INSTALACIÓN DE DEPENDENCIAS
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "📦 INSTALANDO DEPENDENCIAS - TESLA COTIZADOR V3.0" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Ir a raíz
Set-Location E:\TESLA_COTIZADOR-V3.0

# Activar venv
Write-Host "🔌 Activando entorno virtual..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Actualizar pip
Write-Host "📦 Actualizando pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet

# Instalar pydantic-settings (CRÍTICO)
Write-Host "📦 Instalando pydantic-settings..." -ForegroundColor Cyan
pip install pydantic-settings --quiet

# Instalar chromadb
Write-Host "📦 Instalando chromadb..." -ForegroundColor Cyan
pip install chromadb --quiet

# Instalar python-magic-bin
Write-Host "📦 Instalando python-magic-bin..." -ForegroundColor Cyan
pip install python-magic-bin --quiet

# Instalar requests
Write-Host "📦 Instalando requests..." -ForegroundColor Cyan
pip install requests --quiet

# Verificar instalaciones
Write-Host ""
Write-Host "✅ Verificando instalaciones..." -ForegroundColor Green
Write-Host ""

pip show pydantic-settings | Select-String "Version"
pip show chromadb | Select-String "Version"
pip show python-magic-bin | Select-String "Version"

Write-Host ""
Write-Host "✅ INSTALACIÓN COMPLETA" -ForegroundColor Green
Write-Host ""