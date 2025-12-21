# 💻 INSTRUCCIONES: Actualizar PC Local con PILI Ultra Inteligente

## 📋 Descripción

Esta guía te ayudará a actualizar tu instalación local de **Tesla Cotizador V3.0** para incluir **PILI Ultra Inteligente** con LangChain.

---

## ⚠️ IMPORTANTE: Lee Antes de Empezar

1. **Esta rama es solo para PILI inteligente** - NO incluye fixes de generación de documentos
2. **Otra rama tiene los fixes de Word/PDF** - Serán integradas después
3. **Trabaja en un branch separado** - NO modifiques `main` directamente
4. **Haz backup** - Guarda tu `.env` actual antes de actualizar

---

## 🔄 Proceso de Actualización

### PASO 1: Verificar Estado Actual

```bash
# 1. Ver en qué branch estás
git branch

# 2. Ver estado de cambios
git status

# 3. Ver últimos commits
git log --oneline -5

# 4. Verificar si tienes cambios sin commitear
git diff
```

**Si tienes cambios sin commitear**:
```bash
# Guardar cambios temporalmente
git stash save "Cambios locales antes de actualizar PILI"

# O commitear si quieres conservarlos
git add .
git commit -m "wip: Cambios antes de actualizar PILI"
```

---

### PASO 2: Obtener Cambios del Repositorio

```bash
# 1. Asegurarte de estar en el directorio del proyecto
cd /path/to/TESLA_COTIZADOR-V3.0

# 2. Hacer fetch del branch de PILI
git fetch origin claude/claude-md-miqrk3a6qr7npunb-01QYdNbWfxau46szuGTVYEeo

# 3. Ver qué cambios hay
git log HEAD..origin/claude/claude-md-miqrk3a6qr7npunb-01QYdNbWfxau46szuGTVYEeo --oneline

# 4. Hacer pull (integrar cambios)
git pull origin claude/claude-md-miqrk3a6qr7npunb-01QYdNbWfxau46szuGTVYEeo
```

---

### PASO 3: Instalar Nuevas Dependencias

```bash
# 1. Activar entorno virtual
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# 2. Actualizar pip
python -m pip install --upgrade pip

# 3. Instalar nuevas dependencias de PILI LangChain
cd backend
pip install -r requirements.txt

# Si hay conflictos con packaging:
pip install --ignore-installed packaging -r requirements.txt
```

**Nuevas dependencias instaladas**:
- `langchain==0.1.0`
- `langchain-community==0.0.13`
- `langchain-core==0.1.10`
- `litellm==1.17.0`
- `langchain-google-genai==1.0.1`
- `faiss-cpu==1.8.0`

---

### PASO 4: Configurar API Keys (CRÍTICO)

#### Opción A: Solo Gemini (Mínimo)

```bash
# 1. Copiar .env.example si no tienes .env
cp backend/.env.example backend/.env

# 2. Editar backend/.env
nano backend/.env  # o usar tu editor favorito

# 3. Agregar MÍNIMO estas líneas:
GEMINI_API_KEY=tu_gemini_api_key_aqui
PRIMARY_MODEL=gemini/gemini-1.5-pro
FALLBACK_MODELS=
```

**¿Cómo obtener Gemini API Key GRATIS?**
1. Ir a: https://makersuite.google.com/app/apikey
2. Hacer clic en "Create API Key"
3. Copiar la key
4. Pegarla en `GEMINI_API_KEY=`

#### Opción B: Multi-IA con Fallback (Recomendado)

```bash
# En backend/.env agregar:

# Gemini (primario) - GRATIS
GEMINI_API_KEY=tu_gemini_key

# Groq (fallback 1) - GRATIS - https://console.groq.com/
GROQ_API_KEY=tu_groq_key

# Together AI (fallback 2) - GRATIS - https://api.together.xyz/
TOGETHER_API_KEY=tu_together_key

# Configuración router
PRIMARY_MODEL=gemini/gemini-1.5-pro
FALLBACK_MODELS=groq/llama-3.1-70b-versatile,together_ai/meta-llama/Llama-3-70b-chat-hf
```

#### Opción C: Producción (Solo si vas a pagar)

```bash
# Para producción con IAs de pago:
PRIMARY_MODEL=gpt-4-turbo
FALLBACK_MODELS=claude-3-opus,gemini/gemini-1.5-pro

# API Keys (PAGO)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Gemini gratis como último fallback
GEMINI_API_KEY=tu_gemini_key_gratis
```

---

### PASO 5: Verificar Archivos Nuevos

Los siguientes archivos fueron creados/modificados:

```bash
# Verificar que existan:
ls -lh backend/app/services/pili_*langchain.py
ls -lh backend/app/services/pili_multi_ia.py
ls -lh backend/tests/test_pili_langchain.py
ls -lh PLAN_PILI_LANGCHAIN_ULTRA_INTELIGENTE.md
ls -lh INSTRUCCIONES_PILI_LANGCHAIN.md
```

**Debe mostrar**:
```
✅ backend/app/services/pili_cotizadora_langchain.py      (437 líneas)
✅ backend/app/services/pili_proyectos_langchain.py       (365 líneas)
✅ backend/app/services/pili_informes_langchain.py        (565 líneas)
✅ backend/app/services/pili_multi_ia.py                  (237 líneas)
✅ backend/tests/test_pili_langchain.py                   (589 líneas)
✅ PLAN_PILI_LANGCHAIN_ULTRA_INTELIGENTE.md              (635 líneas)
✅ INSTRUCCIONES_PILI_LANGCHAIN.md                        (documentación completa)
```

---

### PASO 6: Ejecutar Tests

```bash
# 1. Ir a backend
cd backend

# 2. Verificar que .env tiene GEMINI_API_KEY
cat .env | grep GEMINI_API_KEY

# 3. Ejecutar tests
pytest tests/test_pili_langchain.py -v

# 4. Si todo pasa correctamente, deberías ver:
# ✅ test_inicializacion PASSED
# ✅ test_calcular_carga_electrica PASSED
# ... (23 tests en total)
```

**¿Qué hacer si fallan tests?**

```bash
# Ver logs detallados
pytest tests/test_pili_langchain.py -v -s

# Ver solo errores
pytest tests/test_pili_langchain.py --tb=short

# Ejecutar solo tests rápidos (sin E2E)
pytest tests/test_pili_langchain.py -v -m "not slow"
```

---

### PASO 7: Probar Backend

```bash
# 1. Levantar backend
cd backend
uvicorn app.main:app --reload

# 2. En otra terminal, probar PILI Multi-IA
python -c "
from app.services.pili_multi_ia import PILIMultiIA
import os
from dotenv import load_dotenv

load_dotenv()

multi = PILIMultiIA()
resultado = multi.chat('Hola PILI, ¿estás funcionando?')

print(f'✅ Modelo usado: {resultado[\"modelo_usado\"]}')
print(f'✅ Respuesta: {resultado[\"respuesta\"][:100]}...')
"

# 3. Probar PILICotizadora
python -c "
from app.services.pili_cotizadora_langchain import PILICotizadoraLangChain
import os
from dotenv import load_dotenv

load_dotenv()

cotizadora = PILICotizadoraLangChain(os.getenv('GEMINI_API_KEY'))
resultado = cotizadora.procesar('Cotización para instalación eléctrica 50m2')

print(f'✅ Respuesta: {resultado[\"respuesta\"][:150]}...')
"
```

---

### PASO 8: Probar Frontend (Opcional)

```bash
# 1. En otra terminal
cd frontend
npm start

# 2. Abrir navegador en http://localhost:3000

# 3. Probar chat PILI:
# - Ir a "Cotización Compleja"
# - Escribir: "Necesito cotización para oficina 100m2"
# - Verificar que PILI responda inteligentemente
```

---

## 🔍 Verificación Completa

### Checklist de Verificación

- [ ] ✅ Git fetch y pull completados sin conflictos
- [ ] ✅ Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] ✅ `.env` configurado con al menos `GEMINI_API_KEY`
- [ ] ✅ Archivos nuevos existen (pili_*_langchain.py)
- [ ] ✅ Tests pasan (`pytest tests/test_pili_langchain.py -v`)
- [ ] ✅ Backend inicia sin errores (`uvicorn app.main:app --reload`)
- [ ] ✅ Test manual de PILI Multi-IA funciona
- [ ] ✅ Test manual de PILICotizadora funciona
- [ ] ✅ Frontend se conecta correctamente (opcional)

### Comandos de Verificación Rápida

```bash
# Script de verificación completa
cat > verificar_instalacion.sh << 'EOF'
#!/bin/bash

echo "🔍 VERIFICANDO INSTALACIÓN DE PILI ULTRA INTELIGENTE"
echo "=================================================="

# 1. Verificar archivos
echo ""
echo "1. Verificando archivos nuevos..."
FILES=(
    "backend/app/services/pili_cotizadora_langchain.py"
    "backend/app/services/pili_proyectos_langchain.py"
    "backend/app/services/pili_informes_langchain.py"
    "backend/app/services/pili_multi_ia.py"
    "backend/tests/test_pili_langchain.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ FALTA: $file"
    fi
done

# 2. Verificar dependencias
echo ""
echo "2. Verificando dependencias Python..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

python -c "
import sys
try:
    import langchain
    print('  ✅ langchain instalado')
except:
    print('  ❌ langchain NO instalado')
    sys.exit(1)

try:
    import litellm
    print('  ✅ litellm instalado')
except:
    print('  ❌ litellm NO instalado')
    sys.exit(1)

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print('  ✅ langchain-google-genai instalado')
except:
    print('  ❌ langchain-google-genai NO instalado')
    sys.exit(1)
"

# 3. Verificar .env
echo ""
echo "3. Verificando configuración (.env)..."
if [ -f "backend/.env" ]; then
    echo "  ✅ backend/.env existe"

    if grep -q "GEMINI_API_KEY=.\+" backend/.env; then
        echo "  ✅ GEMINI_API_KEY configurada"
    else
        echo "  ⚠️  GEMINI_API_KEY vacía o no configurada"
    fi
else
    echo "  ❌ backend/.env NO EXISTE"
fi

# 4. Resumen
echo ""
echo "=================================================="
echo "✅ Verificación completada"
echo ""
echo "Siguiente paso:"
echo "  cd backend && pytest tests/test_pili_langchain.py -v"
EOF

chmod +x verificar_instalacion.sh
./verificar_instalacion.sh
```

---

## 🐛 Troubleshooting Común

### Error 1: "No module named 'langchain'"

**Causa:** Dependencias no instaladas

**Solución:**
```bash
cd backend
pip install -r requirements.txt

# Si persiste:
pip install langchain langchain-community langchain-core litellm langchain-google-genai faiss-cpu
```

### Error 2: "GEMINI_API_KEY not configured"

**Causa:** `.env` no configurado o API key vacía

**Solución:**
```bash
# Verificar
cat backend/.env | grep GEMINI

# Debe mostrar: GEMINI_API_KEY=AIza...
# Si está vacío, editar:
nano backend/.env

# Agregar:
GEMINI_API_KEY=tu_key_real_aqui
```

### Error 3: "Cannot uninstall packaging"

**Causa:** Conflicto con packaging del sistema

**Solución:**
```bash
pip install --ignore-installed packaging
pip install -r requirements.txt
```

### Error 4: Tests fallan con "API key invalid"

**Causa:** API key incorrecta o expirada

**Solución:**
```bash
# 1. Obtener nueva key en https://makersuite.google.com/app/apikey
# 2. Actualizar .env
# 3. Probar manualmente:
python -c "
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('GEMINI_API_KEY')
print(f'Key: {key[:10]}...')

genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-1.5-pro')
response = model.generate_content('Hola')
print(f'✅ Funciona: {response.text[:50]}')
"
```

### Error 5: Backend no inicia

**Causa:** Puerto 8000 ocupado o error en código

**Solución:**
```bash
# Ver si puerto está ocupado
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Matar proceso si existe
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows

# Iniciar en otro puerto
uvicorn app.main:app --reload --port 8001
```

---

## 📊 Comparación Antes vs Después

| Aspecto | ANTES (PILI Anterior) | DESPUÉS (PILI LangChain) |
|---------|----------------------|---------------------------|
| **Dependencias** | ~15 | ~21 (+6 de LangChain) |
| **Archivos Python** | 3 archivos PILI | 7 archivos (3 nuevos + 3 anteriores + multi-IA) |
| **Tests** | 0 | 23 tests exhaustivos |
| **IAs soportadas** | 1 (Gemini) | 6+ (con fallback) |
| **Herramientas** | N/A | 19 herramientas especializadas |
| **Documentación** | README | README + PLAN + INSTRUCCIONES (3 docs) |

---

## 🎯 ¿Qué Sigue?

Después de actualizar correctamente:

1. **Probar exhaustivamente** los 3 agentes nuevos
2. **Integrar** con routers existentes en `backend/app/routers/chat.py`
3. **Merge** con branch de generación de documentos (Word/PDF fixes)
4. **Deploy** a producción

---

## 📞 Ayuda

**Si tienes problemas**:

1. **Ver logs**:
   ```bash
   tail -f backend/logs/app.log
   ```

2. **Ejecutar en modo debug**:
   ```bash
   DEBUG=True uvicorn app.main:app --reload --log-level debug
   ```

3. **Revisar documentación**:
   - `PLAN_PILI_LANGCHAIN_ULTRA_INTELIGENTE.md` - Arquitectura completa
   - `INSTRUCCIONES_PILI_LANGCHAIN.md` - Uso detallado
   - `backend/tests/test_pili_langchain.py` - Ejemplos de uso

4. **Contactar**:
   - Email: ingenieria.teslaelectricidad@gmail.com
   - Revisar issues en GitHub

---

**Versión**: 3.0.0 - PILI Ultra Inteligente
**Última actualización**: Diciembre 2025
**Autor**: TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.
