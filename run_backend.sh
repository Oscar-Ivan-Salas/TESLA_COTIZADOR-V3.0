#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  TESLA COTIZADOR V3.0 - INICIANDO BACKEND"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "[1/3] Activando entorno virtual..."
source venv/bin/activate

echo "[2/3] Verificando variables de entorno..."
if [ ! -f backend/.env ]; then
    echo "ERROR: No se encontró el archivo .env"
    echo "Por favor configura backend/.env con tu GEMINI_API_KEY"
    exit 1
fi

echo "[3/3] Iniciando servidor FastAPI..."
echo ""
echo "Backend corriendo en: http://localhost:8000"
echo "Documentación API: http://localhost:8000/docs"
echo ""
echo "Presiona CTRL+C para detener el servidor"
echo ""

uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
