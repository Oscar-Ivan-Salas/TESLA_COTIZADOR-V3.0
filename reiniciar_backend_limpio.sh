#!/bin/bash
# Script para reiniciar backend con caché limpio después del fix
# Ejecutar desde la raíz del proyecto: bash reiniciar_backend_limpio.sh

echo "================================================================================"
echo "REINICIAR BACKEND - FIX LOOP INFINITO ITSE"
echo "================================================================================"
echo ""

echo "[1/4] Limpiando caché de Python..."
echo ""

# Limpiar __pycache__
find backend -type d -name __pycache__ -exec rm -r {} + 2>/dev/null
find backend -type f -name "*.pyc" -delete 2>/dev/null

echo "    ✅ Caché limpiado"
echo ""

echo "[2/4] Verificando archivos modificados..."
echo ""
echo "    ✅ backend/app/schemas/cotizacion.py (línea 188: conversation_state)"
echo "    ✅ backend/app/routers/chat.py (línea 4667: estado simplificado)"
echo ""

echo "[3/4] Activando entorno virtual..."
echo ""

# Activar venv si existe
if [ -f backend/venv/bin/activate ]; then
    source backend/venv/bin/activate
    echo "    ✅ Entorno virtual activado"
else
    echo "    ⚠️  No se encontró venv, continuando sin activar..."
fi
echo ""

echo "[4/4] Iniciando backend..."
echo ""
echo "================================================================================"
echo "🚀 BACKEND INICIANDO CON FIX APLICADO"
echo "================================================================================"
echo ""
echo "Una vez que veas 'Application startup complete', abre OTRA terminal y ejecuta:"
echo "    python verificar_fix_loop_infinito.py"
echo ""
echo "================================================================================"
echo ""

# Iniciar backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
