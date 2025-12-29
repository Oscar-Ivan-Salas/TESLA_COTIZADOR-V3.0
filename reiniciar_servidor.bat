@echo off
echo ========================================
echo REINICIO COMPLETO DEL SERVIDOR
echo ========================================
echo.

echo [1/4] Deteniendo servidor actual...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
timeout /t 2 /nobreak >nul

echo [2/4] Limpiando cache de Python...
cd backend
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
cd ..

echo [3/4] Esperando 3 segundos...
timeout /t 3 /nobreak >nul

echo [4/4] Iniciando servidor con codigo limpio...
cd backend
start "Tesla Backend Server" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo ========================================
echo SERVIDOR REINICIADO
echo ========================================
echo.
echo Espera 5 segundos y luego verifica:
echo   http://localhost:8000/
echo.
echo Deberia mostrar: "routers_avanzados": true
echo.
pause
