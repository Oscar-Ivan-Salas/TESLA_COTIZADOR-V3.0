# SCRIPT DE VERIFICACIÓN PILI
# Ejecuta este script en PowerShell para verificar que todo está correcto

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "🔍 VERIFICACIÓN AVATAR PILI" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Yellow

$errores = 0

# 1. Verificar archivo PiliAvatar.jsx
Write-Host "1. Verificando PiliAvatar.jsx..." -NoNewline
if (Test-Path "frontend/src/components/PiliAvatar.jsx") {
    Write-Host " ✓ EXISTE" -ForegroundColor Green
} else {
    Write-Host " ✗ NO EXISTE" -ForegroundColor Red
    $errores++
}

# 2. Verificar último commit
Write-Host "2. Verificando último commit..." -NoNewline
$ultimoCommit = git log --oneline -1
if ($ultimoCommit -match "1e2485c") {
    Write-Host " ✓ CORRECTO" -ForegroundColor Green
    Write-Host "   $ultimoCommit" -ForegroundColor Gray
} else {
    Write-Host " ✗ DESACTUALIZADO" -ForegroundColor Red
    Write-Host "   Commit actual: $ultimoCommit" -ForegroundColor Gray
    Write-Host "   Esperado: 1e2485c fix: Integrar Avatar PILI en App.jsx principal" -ForegroundColor Yellow
    $errores++
}

# 3. Verificar import en App.jsx
Write-Host "3. Verificando import en App.jsx..." -NoNewline
$appContent = Get-Content "frontend/src/App.jsx" -Raw
if ($appContent -match "import PiliAvatar from './components/PiliAvatar'") {
    Write-Host " ✓ CORRECTO" -ForegroundColor Green
} else {
    Write-Host " ✗ FALTA IMPORT" -ForegroundColor Red
    $errores++
}

# 4. Verificar uso de PiliAvatar en App.jsx
Write-Host "4. Verificando uso de PiliAvatar..." -NoNewline
if ($appContent -match "PiliAvatar size=") {
    Write-Host " ✓ CORRECTO" -ForegroundColor Green
} else {
    Write-Host " ✗ NO SE USA" -ForegroundColor Red
    $errores++
}

# 5. Verificar texto "👑 PILI"
Write-Host "5. Verificando texto '👑 PILI'..." -NoNewline
if ($appContent -match "👑 PILI") {
    Write-Host " ✓ CORRECTO" -ForegroundColor Green
} else {
    Write-Host " ✗ NO ENCONTRADO" -ForegroundColor Red
    $errores++
}

# 6. Verificar node_modules
Write-Host "6. Verificando node_modules..." -NoNewline
if (Test-Path "frontend/node_modules") {
    Write-Host " ✓ INSTALADAS" -ForegroundColor Green
} else {
    Write-Host " ⚠ NO INSTALADAS" -ForegroundColor Yellow
    Write-Host "   Ejecuta: cd frontend && npm install" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Yellow

if ($errores -eq 0) {
    Write-Host "✅ TODO CORRECTO - PILI DEBERÍA FUNCIONAR" -ForegroundColor Green
    Write-Host "`nPara probar:" -ForegroundColor Cyan
    Write-Host "1. cd frontend" -ForegroundColor White
    Write-Host "2. npm run dev" -ForegroundColor White
    Write-Host "3. Abre: http://localhost:5173`n" -ForegroundColor White
} else {
    Write-Host "❌ ENCONTRADOS $errores ERRORES" -ForegroundColor Red
    Write-Host "`nPara corregir:" -ForegroundColor Cyan
    Write-Host "git pull origin claude/analyze-prompts-01Bao3FK5gRS9TW5z3QekTFx`n" -ForegroundColor White
}

Write-Host "========================================`n" -ForegroundColor Yellow
