# 📥 GUÍA COMPLETA: Descargar Repositorio a PC Local

**Fecha**: 29 de Diciembre 2025
**Branch de trabajo**: `claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8`
**Último commit**: `46298b7`
**Propósito**: Sincronizar PC local con repositorio remoto

---

## 🎯 OBJETIVO

Asegurar que tu **PC local** tenga **exactamente los mismos archivos** que el **repositorio remoto**.

---

## 📋 ESCENARIO 1: Si AÚN NO TIENES el repositorio en tu PC

### PASO 1: Clonar el Repositorio

```bash
# 1. Abrir terminal/CMD en la ubicación donde quieres el proyecto
# Ejemplo: C:\Users\TuNombre\Proyectos\
cd C:\Users\TuNombre\Proyectos

# 2. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>

# Ejemplo (reemplaza con tu URL real):
# git clone https://github.com/Oscar-Ivan-Salas/TESLA_COTIZADOR-V3.0.git

# 3. Entrar a la carpeta del proyecto
cd TESLA_COTIZADOR-V3.0
```

---

### PASO 2: Cambiar al Branch de Trabajo

```bash
# Ver todas las ramas disponibles
git branch -a

# Cambiar al branch donde está todo el trabajo
git checkout claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8

# Verificar que estás en el branch correcto
git branch
# Debe mostrar: * claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8
```

---

### PASO 3: Verificar que Tienes Todo

```bash
# Ver el último commit
git log --oneline -1
# Debe mostrar: 46298b7 docs: Documentación completa de PILI inteligente en entorno propio

# Ver estado del repositorio
git status
# Debe mostrar: On branch claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8
#               Your branch is up to date with 'origin/...'
#               nothing to commit, working tree clean
```

**✅ Si todo coincide → Tu PC está sincronizado con el repositorio**

---

## 📋 ESCENARIO 2: Si YA TIENES el repositorio en tu PC (ACTUALIZAR)

### PASO 1: Ir a la Carpeta del Proyecto

```bash
# Windows
cd C:\Users\TuNombre\Proyectos\TESLA_COTIZADOR-V3.0

# Linux/Mac
cd ~/Proyectos/TESLA_COTIZADOR-V3.0
```

---

### PASO 2: Verificar Branch Actual

```bash
# Ver en qué branch estás
git branch
# Si NO estás en claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8:

# Cambiar al branch correcto
git checkout claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8
```

---

### PASO 3: Descargar Últimos Cambios

```bash
# Traer información del repositorio remoto
git fetch origin

# Actualizar tu branch local con los cambios remotos
git pull origin claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8

# Debería mostrar:
# From <repositorio>
#  * branch            claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8 -> FETCH_HEAD
# Already up to date. (si ya estabas actualizado)
# O mostrar los archivos nuevos/modificados que descargó
```

---

### PASO 4: Verificar Sincronización

```bash
# 1. Ver último commit
git log --oneline -1
# Debe mostrar: 46298b7 docs: Documentación completa de PILI inteligente en entorno propio

# 2. Ver estado
git status
# Debe mostrar: On branch claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8
#               Your branch is up to date with 'origin/...'
#               nothing to commit, working tree clean

# 3. Ver últimos 7 commits
git log --oneline -7
# Debe mostrar:
# 46298b7 docs: Documentación completa de PILI inteligente en entorno propio
# 3ef0a43 docs: Análisis exhaustivo - Comparación ACTUAL vs NUEVO
# 0539381 docs: Agregar resumen ejecutivo de estado actual y próximos pasos
# 1114fa5 docs: Enumeración completa de 6 documentos y 10 servicios
# e36e5de docs: Análisis exhaustivo - Comparación ACTUAL vs NUEVO
# 2a6e8c2 docs: Verificación exhaustiva - Sistema antiguo 100% INTACTO
# f0ec092 docs: Agregar resumen ejecutivo de estado actual y próximos pasos
```

**✅ Si todo coincide → Tu PC está sincronizado con el repositorio**

---

## 📂 VERIFICAR QUE TIENES TODOS LOS ARCHIVOS

### Documentación (Archivos .md)

```bash
# Listar archivos de documentación
ls -lh *.md

# Deberías tener (entre otros):
# ✅ PILI_INTELIGENTE_ENTORNO_PROPIO.md (NUEVO)
# ✅ VERIFICACION_CAMBIOS_SEGUROS.md (NUEVO)
# ✅ FLUJO_COMPLETO_GENERACION_DOCUMENTOS.md
# ✅ RESUMEN_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md
# ✅ ENUMERACION_DOCUMENTOS_Y_SERVICIOS.md
# ✅ COMPARACION_SISTEMA_ACTUAL_VS_NUEVO.md
# ✅ VERIFICACION_SISTEMA_ANTIGUO_INTACTO.md
# ✅ PLAN_MIGRACION_SISTEMAS.md
# ✅ TESTING_GENERADORES_PROFESIONALES.md
# ✅ PROGRESO_MIGRACION_GENERADORES.md
# ✅ ARQUITECTURA_EMPRESARIAL_SENIOR.md
# ✅ CLAUDE.md
# ✅ README.md
```

---

### Backend (Código Python)

```bash
# Verificar estructura del backend
ls -lh backend/app/services/

# Deberías tener:
# ✅ generators/ (SISTEMA ANTIGUO - INTACTO)
# ✅ professional/ (SISTEMA NUEVO - MIGRADO)
# ✅ pili/ (SISTEMA DE ESPECIALISTAS)
# ✅ pili_brain.py
# ✅ pili_integrator.py
# ✅ pili_local_specialists.py
# ✅ gemini_service.py
# ✅ word_generator.py
# ✅ pdf_generator.py
# ✅ rag_service.py
```

---

### Sistema NUEVO (Professional)

```bash
# Verificar generadores profesionales
ls -lh backend/app/services/professional/generators/

# Deberías tener:
# ✅ cotizaciones/ (simple.py, compleja.py)
# ✅ proyectos/ (simple.py, complejo_pmi.py)
# ✅ informes/ (tecnico.py, ejecutivo_apa.py)
# ✅ base/ (base_generator.py)
# ✅ document_generator_pro.py
# ✅ pdf_converter.py
# ✅ __init__.py
```

---

### Tests

```bash
# Verificar tests
ls -lh backend/tests/

# Deberías tener:
# ✅ conftest.py (fixtures)
# ✅ test_professional_generators.py (24 tests)
# ✅ test_comparison_systems.py (10 tests)
# ✅ __init__.py
# ✅ README.md
```

---

### Requirements (Dependencias)

```bash
# Verificar requirements
ls -lh backend/requirements*.txt

# Deberías tener:
# ✅ requirements.txt (DESARROLLO - 79 líneas)
# ✅ requirements_enterprise.txt (PRODUCCIÓN - 261 líneas)
```

---

### Plantillas HTML

```bash
# Verificar plantillas HTML
ls -lh backend/app/templates/documentos/

# Deberías tener 6 plantillas:
# ✅ PLANTILLA_HTML_COTIZACION_SIMPLE.html
# ✅ PLANTILLA_HTML_COTIZACION_COMPLEJA.html
# ✅ PLANTILLA_HTML_PROYECTO_SIMPLE.html
# ✅ PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html
# ✅ PLANTILLA_HTML_INFORME_TECNICO.html
# ✅ PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html
```

---

### PILI (Especialistas)

```bash
# Verificar configuración PILI
ls -lh backend/app/services/pili/config/

# Deberías tener 10 archivos YAML:
# ✅ electricidad.yaml
# ✅ itse.yaml
# ✅ pozo-tierra.yaml
# ✅ contraincendios.yaml
# ✅ domotica.yaml
# ✅ cctv.yaml
# ✅ redes.yaml
# ✅ automatizacion-industrial.yaml
# ✅ expedientes.yaml
# ✅ saneamiento.yaml
```

---

## ✅ VERIFICACIÓN FINAL: TODO SINCRONIZADO

### Checklist de Verificación

Ejecuta estos comandos y verifica que coincidan:

```bash
# 1. Branch correcto
git branch
# ✅ Debe mostrar: * claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8

# 2. Último commit
git log --oneline -1
# ✅ Debe mostrar: 46298b7 docs: Documentación completa de PILI inteligente en entorno propio

# 3. Estado limpio
git status
# ✅ Debe mostrar: nothing to commit, working tree clean

# 4. Total de commits en el branch
git log --oneline | wc -l
# ✅ Debe mostrar un número (ejemplo: 47)

# 5. Archivos no rastreados (debe estar vacío o solo archivos locales)
git status --short
# ✅ Debe estar vacío O mostrar solo archivos que NO deban estar en git (.env, storage/, etc.)
```

---

## 🚀 SIGUIENTE PASO: Instalar Entorno Virtual

Una vez verificado que tienes todo sincronizado, sigue estos pasos:

### PASO 1: Ir a Backend

```bash
cd backend
```

---

### PASO 2: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual

# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

---

### PASO 3: Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Tiempo estimado: 5-10 minutos
```

---

### PASO 4: Configurar .env

```bash
# Copiar archivo de ejemplo
copy .env.example .env  # Windows
# O
cp .env.example .env    # Linux/Mac

# Editar .env con tu editor favorito
notepad .env  # Windows
# O
nano .env     # Linux/Mac

# Agregar tu API key de Gemini:
# GEMINI_API_KEY=tu_api_key_aqui
```

---

### PASO 5: Verificar Instalación

```bash
# Test rápido de importación
python -c "import fastapi; import google.generativeai; print('✅ Todo OK')"

# Si muestra: ✅ Todo OK
# → Instalación correcta
```

---

## 📊 ARCHIVOS IMPORTANTES EN TU PC

Después de sincronizar, deberías tener:

### 📄 Documentación (11 archivos principales)

```
✅ PILI_INTELIGENTE_ENTORNO_PROPIO.md (550 líneas)
✅ VERIFICACION_CAMBIOS_SEGUROS.md (414 líneas)
✅ FLUJO_COMPLETO_GENERACION_DOCUMENTOS.md (665 líneas)
✅ RESUMEN_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md (645 líneas)
✅ ENUMERACION_DOCUMENTOS_Y_SERVICIOS.md (599 líneas)
✅ COMPARACION_SISTEMA_ACTUAL_VS_NUEVO.md (487 líneas)
✅ VERIFICACION_SISTEMA_ANTIGUO_INTACTO.md (266 líneas)
✅ PLAN_MIGRACION_SISTEMAS.md (800 líneas)
✅ TESTING_GENERADORES_PROFESIONALES.md (550 líneas)
✅ ARQUITECTURA_EMPRESARIAL_SENIOR.md (1000+ líneas)
✅ CLAUDE.md (50 KB - Guía completa del proyecto)
```

---

### 🐍 Código Backend (14 archivos principales del sistema nuevo)

```
✅ backend/app/services/professional/generators/__init__.py
✅ backend/app/services/professional/generators/cotizaciones/simple.py (16.7 KB)
✅ backend/app/services/professional/generators/cotizaciones/compleja.py (16.2 KB)
✅ backend/app/services/professional/generators/proyectos/simple.py (15.0 KB)
✅ backend/app/services/professional/generators/proyectos/complejo_pmi.py (16.5 KB)
✅ backend/app/services/professional/generators/informes/tecnico.py (8.0 KB)
✅ backend/app/services/professional/generators/informes/ejecutivo_apa.py (10.5 KB)
✅ backend/app/services/professional/generators/pdf_converter.py (3.4 KB)
✅ backend/app/services/professional/ml/ml_engine.py (21 KB)
✅ backend/app/services/pili_brain.py (63 KB)
✅ backend/app/services/pili/specialist.py (16 KB)
✅ 10 archivos YAML de configuración PILI (85 KB)
✅ 10 archivos Python de conocimiento PILI (8.5 KB)
```

---

### 🧪 Tests (3 archivos)

```
✅ backend/tests/conftest.py (8 fixtures)
✅ backend/tests/test_professional_generators.py (24 tests)
✅ backend/tests/test_comparison_systems.py (10 tests)
```

---

### 📦 Configuración (2 archivos)

```
✅ backend/requirements.txt (79 paquetes)
✅ backend/requirements_enterprise.txt (261 paquetes)
```

---

## ⚠️ ARCHIVOS QUE **NO** DEBEN ESTAR EN GIT

Si ejecutas `git status` y ves estos archivos, **NO los agregues a git**:

```bash
❌ .env (contiene API keys - NUNCA commitear)
❌ backend/venv/ (entorno virtual - NUNCA commitear)
❌ backend/__pycache__/ (archivos compilados Python)
❌ storage/generados/ (documentos generados)
❌ database/tesla_cotizador.db (base de datos local)
❌ backend/logs/ (archivos de log)
```

**Estos archivos están en `.gitignore`** y no deben subirse al repositorio.

---

## 🎯 COMANDOS RÁPIDOS DE VERIFICACIÓN

### Verificación en 1 Comando

```bash
# Ejecutar todo junto
git status && git log --oneline -3 && echo "✅ Verificación completa"

# Debería mostrar:
# On branch claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8
# Your branch is up to date with 'origin/...'
# nothing to commit, working tree clean
# 46298b7 docs: Documentación completa de PILI inteligente en entorno propio
# 3ef0a43 docs: Análisis exhaustivo - Comparación ACTUAL vs NUEVO
# 0539381 docs: Agregar resumen ejecutivo de estado actual y próximos pasos
# ✅ Verificación completa
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Problema 1: "fatal: not a git repository"

**Causa**: No estás en la carpeta del proyecto

**Solución**:
```bash
cd C:\Users\TuNombre\Proyectos\TESLA_COTIZADOR-V3.0
```

---

### Problema 2: "Your branch is behind 'origin/...'"

**Causa**: El repositorio remoto tiene cambios que tu PC no tiene

**Solución**:
```bash
git pull origin claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8
```

---

### Problema 3: "Merge conflict"

**Causa**: Tienes cambios locales que chocan con cambios remotos

**Solución**:
```bash
# Opción 1: Guardar tus cambios en stash
git stash
git pull origin claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8
git stash pop

# Opción 2: Descartar cambios locales (CUIDADO: pierdes cambios)
git reset --hard origin/claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8
```

---

### Problema 4: "fatal: remote origin already exists"

**Causa**: Ya tienes el remote configurado (normal)

**Solución**: No hacer nada, esto es correcto.

---

## ✅ CONFIRMACIÓN FINAL

Después de seguir esta guía, deberías tener:

1. ✅ Repositorio clonado/actualizado en tu PC
2. ✅ Branch correcto: `claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8`
3. ✅ Último commit: `46298b7`
4. ✅ Todos los archivos sincronizados
5. ✅ Entorno virtual creado e instalado (opcional)
6. ✅ `.env` configurado con tu API key (opcional)

**Estado**: ✅ **PC y REPOSITORIO 100% SINCRONIZADOS** 🚀

---

**Documento creado**: 29 de Diciembre 2025
**Actualizado por**: Claude Code (Sonnet 4.5)
**Branch**: `claude/claude-md-mifgupwu28q5qjdd-01DXJ3Tf3TXpPfvV7gqqkWf8`
**Último commit**: `46298b7`
