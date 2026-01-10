# Script para limpiar caché de npm y reiniciar sin caché

Write-Host "🧹 Limpiando caché de npm..." -ForegroundColor Yellow

# 1. Matar todos los procesos de Node.js
Write-Host "1. Matando procesos de Node.js..." -ForegroundColor Cyan
taskkill /F /IM node.exe 2>$null
Start-Sleep -Seconds 2

# 2. Eliminar carpeta node_modules/.cache
Write-Host "2. Eliminando caché de node_modules..." -ForegroundColor Cyan
if (Test-Path "frontend\node_modules\.cache") {
    Remove-Item -Recurse -Force "frontend\node_modules\.cache"
    Write-Host "   ✅ Caché de node_modules eliminado" -ForegroundColor Green
}

# 3. Eliminar build cache
Write-Host "3. Eliminando build cache..." -ForegroundColor Cyan
if (Test-Path "frontend\build") {
    Remove-Item -Recurse -Force "frontend\build"
    Write-Host "   ✅ Build eliminado" -ForegroundColor Green
}

# 4. Limpiar caché de npm
Write-Host "4. Limpiando caché de npm..." -ForegroundColor Cyan
Set-Location frontend
npm cache clean --force
Write-Host "   ✅ Caché de npm limpiado" -ForegroundColor Green

# 5. Reiniciar npm
Write-Host "5. Reiniciando npm start..." -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  AHORA ABRE EL NAVEGADOR EN MODO INCÓGNITO" -ForegroundColor Magenta
Write-Host "  http://localhost:3000" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""

npm start
