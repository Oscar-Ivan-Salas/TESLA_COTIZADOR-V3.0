
Write-Host "🛑 DETENIENDO SERVIDORES (Node.js y Python)..." -ForegroundColor Yellow
taskkill /F /IM node.exe /T 2>$null
taskkill /F /IM python.exe /T 2>$null
taskkill /F /IM uvicorn.exe /T 2>$null

Write-Host "🧹 LIMPIANDO CACHÉ DE PYTHON (__pycache__)..." -ForegroundColor Cyan
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Recurse -Directory -Filter ".pytest_cache" | Remove-Item -Recurse -Force

Write-Host "🧹 LIMPIANDO ARCHIVOS TEMPORALES..." -ForegroundColor Cyan
Remove-Item -Path "verify_output.txt" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "verify_output_clean.txt" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "*.log" -Force -ErrorAction SilentlyContinue

Write-Host "🧹 LIMPIANDO CACHÉ DE FRONTEND (Vite & Node)..." -ForegroundColor Cyan
if (Test-Path "frontend\node_modules\.vite") {
    Remove-Item -Path "frontend\node_modules\.vite" -Recurse -Force
}
if (Test-Path "frontend\dist") {
    Remove-Item -Path "frontend\dist" -Recurse -Force
}

Write-Host "✨ LIMPIEZA COMPLETADA." -ForegroundColor Green
Write-Host "🚀 INICIAR SISTEMA:" -ForegroundColor Yellow
Write-Host "   1. Abre una terminal y corre: cd backend; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
Write-Host "   2. Abre otra terminal y corre: cd frontend; npm start"
