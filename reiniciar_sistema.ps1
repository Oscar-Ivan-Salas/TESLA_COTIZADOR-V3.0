# Script PowerShell para Reinicio Completo del Sistema
# Limpia cache y reinicia backend y frontend

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "REINICIO COMPLETO - TESLA COTIZADOR V3.0" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Limpiar cache de Python
Write-Host "1. Limpiando cache de Python..." -ForegroundColor Yellow
python backend/scripts/limpiar_cache.py

Write-Host ""
Write-Host "2. Cache limpiado exitosamente!" -ForegroundColor Green
Write-Host ""

# 2. Instrucciones para reiniciar
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SIGUIENTE PASO: REINICIAR SERVIDORES" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "BACKEND:" -ForegroundColor Yellow
Write-Host "  1. Presiona Ctrl+C en la terminal del backend" -ForegroundColor White
Write-Host "  2. Ejecuta:" -ForegroundColor White
Write-Host "     cd backend" -ForegroundColor Gray
Write-Host "     python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "FRONTEND:" -ForegroundColor Yellow
Write-Host "  1. Presiona Ctrl+C en la terminal del frontend" -ForegroundColor White
Write-Host "  2. Ejecuta:" -ForegroundColor White
Write-Host "     cd frontend" -ForegroundColor Gray
Write-Host "     npm start" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "VERIFICACION POST-REINICIO:" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Verifica que el backend muestre:" -ForegroundColor White
Write-Host "   'Router Clientes cargado'" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Prueba crear un cliente desde el frontend" -ForegroundColor White
Write-Host ""
Write-Host "3. Si aun falla, ejecuta:" -ForegroundColor White
Write-Host "   curl http://localhost:8000/" -ForegroundColor Gray
Write-Host "   Busca: 'routers_cargados'" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
