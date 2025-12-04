#!/bin/bash

# Script de Verificación de Sincronización Git
# TESLA COTIZADOR V3.0

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  VERIFICACIÓN DE SINCRONIZACIÓN GIT - TESLA COTIZADOR V3.0 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar
verificar() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ CORRECTO${NC}"
        return 0
    else
        echo -e "${RED}✗ ERROR${NC}"
        return 1
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Verificando directorio actual..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pwd
if [[ $(pwd) == *"TESLA_COTIZADOR-V3.0"* ]]; then
    echo -e "${GREEN}✓ Estás en el directorio correcto${NC}"
else
    echo -e "${RED}✗ ADVERTENCIA: No estás en TESLA_COTIZADOR-V3.0${NC}"
    echo -e "${YELLOW}   Ejecuta: cd TESLA_COTIZADOR-V3.0${NC}"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. Verificando branch actual..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
CURRENT_BRANCH=$(git branch --show-current)
echo "Branch actual: $CURRENT_BRANCH"
if [[ "$CURRENT_BRANCH" == "claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa" ]]; then
    echo -e "${GREEN}✓ Estás en el branch correcto${NC}"
else
    echo -e "${RED}✗ ADVERTENCIA: Estás en el branch incorrecto${NC}"
    echo -e "${YELLOW}   Ejecuta: git checkout claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa${NC}"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. Verificando estado de Git..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
git status
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. Verificando últimos commits..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
git log --oneline -5
LAST_COMMIT=$(git log --oneline -1 | cut -d' ' -f1)
if [[ "$LAST_COMMIT" == "5ab7ff4" ]]; then
    echo -e "${GREEN}✓ Tienes el último commit${NC}"
else
    echo -e "${YELLOW}⚠ El último commit no coincide. Puede que necesites hacer pull.${NC}"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. Verificando archivos creados recientemente..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

archivos_verificar=(
    "DIAGNOSTICO_FINAL_Y_SOLUCION.md"
    "SINCRONIZACION_SERVICIOS_COMPLETADA.md"
    "backend/test_diagnostico_completo.py"
    "GUIA_VERIFICACION_GIT.md"
)

total_archivos=${#archivos_verificar[@]}
archivos_encontrados=0

for archivo in "${archivos_verificar[@]}"; do
    if [ -f "$archivo" ]; then
        size=$(ls -lh "$archivo" | awk '{print $5}')
        echo -e "${GREEN}✓${NC} $archivo (${size})"
        archivos_encontrados=$((archivos_encontrados + 1))
    else
        echo -e "${RED}✗${NC} $archivo ${RED}NO ENCONTRADO${NC}"
    fi
done

echo ""
echo -e "Archivos encontrados: ${archivos_encontrados}/${total_archivos}"

if [ $archivos_encontrados -eq $total_archivos ]; then
    echo -e "${GREEN}✓ Todos los archivos están presentes${NC}"
else
    echo -e "${RED}✗ Faltan algunos archivos. Ejecuta: git pull origin claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa${NC}"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. Archivos modificados en los últimos commits..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
git diff HEAD~5 HEAD --name-status
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. Comparación con el remoto..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Descargando información del remoto..."
git fetch origin >/dev/null 2>&1

LOCAL_COMMIT=$(git rev-parse HEAD)
REMOTE_COMMIT=$(git rev-parse origin/claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa 2>/dev/null)

echo "Commit local:  $LOCAL_COMMIT"
echo "Commit remoto: $REMOTE_COMMIT"

if [ "$LOCAL_COMMIT" == "$REMOTE_COMMIT" ]; then
    echo -e "${GREEN}✓ Local y remoto están sincronizados${NC}"
else
    echo -e "${YELLOW}⚠ Local y remoto NO están sincronizados${NC}"
    echo -e "${YELLOW}   Ejecuta: git pull origin claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa${NC}"
fi
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    RESUMEN FINAL                           ║"
echo "╚════════════════════════════════════════════════════════════╝"

if [ $archivos_encontrados -eq $total_archivos ] && [ "$LOCAL_COMMIT" == "$REMOTE_COMMIT" ]; then
    echo -e "${GREEN}✓✓✓ TODO ESTÁ CORRECTAMENTE SINCRONIZADO ✓✓✓${NC}"
    echo ""
    echo "Tus archivos están actualizados y sincronizados con el repositorio remoto."
else
    echo -e "${YELLOW}⚠⚠⚠ NECESITAS SINCRONIZAR ⚠⚠⚠${NC}"
    echo ""
    echo "Ejecuta estos comandos para sincronizar:"
    echo ""
    echo "  git fetch origin"
    echo "  git pull origin claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa"
    echo ""
fi

echo ""
echo "Para más ayuda, consulta: GUIA_VERIFICACION_GIT.md"
echo ""
