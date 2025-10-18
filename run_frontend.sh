#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  TESLA COTIZADOR V3.0 - INICIANDO FRONTEND"
echo "═══════════════════════════════════════════════════════════"
echo ""

cd frontend

echo "[1/2] Verificando node_modules..."
if [ ! -d "node_modules" ]; then
    echo "Instalando dependencias..."
    npm install
fi

echo "[2/2] Iniciando React App..."
echo ""
echo "Frontend corriendo en: http://localhost:3000"
echo ""
echo "Presiona CTRL+C para detener el servidor"
echo ""

npm start
