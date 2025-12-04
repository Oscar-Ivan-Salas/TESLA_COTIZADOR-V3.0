@echo off
REM Script de Verificación de Sincronización Git - Windows
REM TESLA COTIZADOR V3.0

echo ================================================================
echo   VERIFICACION DE SINCRONIZACION GIT - TESLA COTIZADOR V3.0
echo ================================================================
echo.

echo ================================================================
echo 1. Verificando directorio actual...
echo ================================================================
cd
echo.

echo ================================================================
echo 2. Verificando branch actual...
echo ================================================================
git branch --show-current
echo.

echo ================================================================
echo 3. Verificando estado de Git...
echo ================================================================
git status
echo.

echo ================================================================
echo 4. Verificando ultimos commits...
echo ================================================================
git log --oneline -5
echo.

echo ================================================================
echo 5. Verificando archivos creados recientemente...
echo ================================================================

echo Verificando DIAGNOSTICO_FINAL_Y_SOLUCION.md...
if exist "DIAGNOSTICO_FINAL_Y_SOLUCION.md" (
    echo [OK] DIAGNOSTICO_FINAL_Y_SOLUCION.md existe
    dir "DIAGNOSTICO_FINAL_Y_SOLUCION.md" | findstr /C:"DIAGNOSTICO_FINAL_Y_SOLUCION.md"
) else (
    echo [ERROR] DIAGNOSTICO_FINAL_Y_SOLUCION.md NO ENCONTRADO
)
echo.

echo Verificando SINCRONIZACION_SERVICIOS_COMPLETADA.md...
if exist "SINCRONIZACION_SERVICIOS_COMPLETADA.md" (
    echo [OK] SINCRONIZACION_SERVICIOS_COMPLETADA.md existe
    dir "SINCRONIZACION_SERVICIOS_COMPLETADA.md" | findstr /C:"SINCRONIZACION_SERVICIOS_COMPLETADA.md"
) else (
    echo [ERROR] SINCRONIZACION_SERVICIOS_COMPLETADA.md NO ENCONTRADO
)
echo.

echo Verificando backend\test_diagnostico_completo.py...
if exist "backend\test_diagnostico_completo.py" (
    echo [OK] backend\test_diagnostico_completo.py existe
    dir "backend\test_diagnostico_completo.py" | findstr /C:"test_diagnostico_completo.py"
) else (
    echo [ERROR] backend\test_diagnostico_completo.py NO ENCONTRADO
)
echo.

echo Verificando GUIA_VERIFICACION_GIT.md...
if exist "GUIA_VERIFICACION_GIT.md" (
    echo [OK] GUIA_VERIFICACION_GIT.md existe
) else (
    echo [ERROR] GUIA_VERIFICACION_GIT.md NO ENCONTRADO
)
echo.

echo ================================================================
echo 6. Archivos modificados en los ultimos commits...
echo ================================================================
git diff HEAD~5 HEAD --name-status
echo.

echo ================================================================
echo 7. Comparacion con el remoto...
echo ================================================================
echo Descargando informacion del remoto...
git fetch origin

echo.
echo Commit local:
git rev-parse HEAD

echo.
echo Commit remoto:
git rev-parse origin/claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa

echo.
echo ================================================================
echo                       RESUMEN FINAL
echo ================================================================
echo.
echo Si ves "NO ENCONTRADO" en algun archivo, ejecuta:
echo   git pull origin claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa
echo.
echo Para mas ayuda, consulta: GUIA_VERIFICACION_GIT.md
echo.
pause
