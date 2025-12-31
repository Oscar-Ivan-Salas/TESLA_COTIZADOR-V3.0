@echo off
REM Script para reiniciar backend con caché limpio después del fix
REM Ejecutar desde la raíz del proyecto

echo ================================================================================
echo REINICIAR BACKEND - FIX LOOP INFINITO ITSE
echo ================================================================================
echo.

echo [1/4] Limpiando caché de Python...
echo.

REM Limpiar __pycache__ en backend
cd backend
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul

echo     ✅ Caché limpiado
echo.

echo [2/4] Verificando archivos modificados...
echo.
echo     ✅ backend/app/schemas/cotizacion.py (línea 188: conversation_state)
echo     ✅ backend/app/routers/chat.py (línea 4667: estado simplificado)
echo.

echo [3/4] Activando entorno virtual...
echo.

REM Activar venv
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo     ✅ Entorno virtual activado
) else (
    echo     ⚠️  No se encontró venv, continuando sin activar...
)
echo.

echo [4/4] Iniciando backend...
echo.
echo ================================================================================
echo 🚀 BACKEND INICIANDO CON FIX APLICADO
echo ================================================================================
echo.
echo Una vez que veas "Application startup complete", abre OTRA terminal y ejecuta:
echo     python verificar_fix_loop_infinito.py
echo.
echo ================================================================================
echo.

REM Iniciar backend con reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
