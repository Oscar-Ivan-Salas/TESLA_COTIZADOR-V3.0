# 📦 GUÍA MAESTRA DE INSTALACIÓN
## Sistema Tesla Cotizador v3.0 - Actualización Completa

---

## 📋 ÍNDICE

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Archivos Actualizados](#archivos-actualizados)
3. [Orden de Instalación](#orden-instalacion)
4. [Instrucciones Detalladas](#instrucciones-detalladas)
5. [Checklist de Verificación](#checklist-verificacion)
6. [Configuración Requerida](#configuracion-requerida)
7. [Testing y Validación](#testing-validacion)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 RESUMEN EJECUTIVO {#resumen-ejecutivo}

### ¿Qué se actualizó?

Se han creado y actualizado **9 archivos** que transforman el sistema Tesla Cotizador v3.0 en una plataforma completa con:

✅ **Generación de documentos profesionales** (Word y PDF)
✅ **Análisis inteligente con IA** (Gemini)
✅ **Plantillas personalizables** por el usuario
✅ **Informes ejecutivos automáticos** con métricas y KPIs
✅ **Procesamiento de plantillas** con marcadores dinámicos
✅ **Análisis de riesgos** y recomendaciones
✅ **Gestión completa de documentos**

### Beneficios Principales

```
🚀 Velocidad: Genera cotizaciones en 30 segundos
🤖 Inteligencia: IA analiza y sugiere mejoras
📊 Profesionalismo: Documentos con calidad ejecutiva
🎨 Personalización: Plantillas propias del usuario
📈 Métricas: KPIs y análisis automáticos
🔒 Seguridad: PDFs no editables para clientes
```

---

## 📁 ARCHIVOS ACTUALIZADOS {#archivos-actualizados}

### Resumen de Archivos

| # | Archivo | Tipo | Líneas | Ubicación |
|---|---------|------|--------|-----------|
| 1 | `template_processor.py` | ⭐ NUEVO | 550 | `backend/app/services/` |
| 2 | `__init__.py` | ✏️ Actualizado | 17 | `backend/app/services/` |
| 3 | `proyectos.py` | ✏️ Actualizado | 487 | `backend/app/routers/` |
| 4 | `word_generator.py` | ✏️ Actualizado | 720 | `backend/app/services/` |
| 5 | `pdf_generator.py` | ✏️ Actualizado | 680 | `backend/app/services/` |
| 6 | `documentos.py` | ✏️ Actualizado | 620 | `backend/app/routers/` |
| 7 | `report_generator.py` | ⭐ NUEVO | 750 | `backend/app/services/` |
| 8 | `proyectos_mejorado.py` | ✏️ Mejorado | 640 | `backend/app/routers/` |
| 9 | `chat_mejorado.py` | ✏️ Mejorado | 680 | `backend/app/routers/` |

**Total: 5,144 líneas de código**

---

## 🔢 ORDEN DE INSTALACIÓN {#orden-instalacion}

### ⚠️ IMPORTANTE: Sigue este orden exacto

```
PASO 1: Servicios Base
├─ 1.1 → template_processor.py (NUEVO)
├─ 1.2 → report_generator.py (NUEVO)
└─ 1.3 → __init__.py (ACTUALIZAR)

PASO 2: Generadores de Documentos
├─ 2.1 → word_generator.py (ACTUALIZAR)
└─ 2.2 → pdf_generator.py (ACTUALIZAR)

PASO 3: Routers/Endpoints
├─ 3.1 → proyectos_mejorado.py → proyectos.py (REEMPLAZAR)
├─ 3.2 → documentos.py (ACTUALIZAR)
└─ 3.3 → chat_mejorado.py → chat.py (REEMPLAZAR)
```

### Por qué este orden

1. **Servicios primero**: Los routers dependen de los servicios
2. **Generadores después**: Los routers usan los generadores
3. **Routers al final**: Así no hay errores de import

---

## 📝 INSTRUCCIONES DETALLADAS {#instrucciones-detalladas}

### PASO 1: Preparación del Entorno

#### 1.1. Hacer Backup

```bash
# Crear backup de archivos que se van a reemplazar
cd TESLA_COTIZADOR-V3.0/

# Crear carpeta de backup
mkdir -p backup_$(date +%Y%m%d_%H%M%S)
cd backup_$(date +%Y%m%d_%H%M%S)

# Copiar archivos originales
cp ../backend/app/services/__init__.py ./services_init_backup.py
cp ../backend/app/services/word_generator.py ./word_generator_backup.py
cp ../backend/app/services/pdf_generator.py ./pdf_generator_backup.py
cp ../backend/app/routers/proyectos.py ./proyectos_backup.py
cp ../backend/app/routers/documentos.py ./documentos_backup.py
cp ../backend/app/routers/chat.py ./chat_backup.py

cd ..
```

#### 1.2. Verificar Estructura de Directorios

```bash
# Crear directorios necesarios si no existen
mkdir -p backend/app/services
mkdir -p backend/app/routers
mkdir -p backend/templates
mkdir -p backend/storage/generated
mkdir -p backend/storage/uploads
```

---

### PASO 2: Instalación de Archivos NUEVOS

#### 2.1. Instalar `template_processor.py`

```bash
# Copiar archivo
cp template_processor.py backend/app/services/template_processor.py

# Verificar
ls -lh backend/app/services/template_processor.py
```

**Verificación:**
```bash
# Debe mostrar ~550 líneas
wc -l backend/app/services/template_processor.py
```

#### 2.2. Instalar `report_generator.py`

```bash
# Copiar archivo
cp report_generator.py backend/app/services/report_generator.py

# Verificar
ls -lh backend/app/services/report_generator.py
```

**Verificación:**
```bash
# Debe mostrar ~750 líneas
wc -l backend/app/services/report_generator.py
```

---

### PASO 3: Actualización de Archivos EXISTENTES

#### 3.1. Actualizar `__init__.py`

```bash
# Reemplazar archivo
cp __init__.py backend/app/services/__init__.py

# Verificar
cat backend/app/services/__init__.py
```

**Debe contener:**
```python
from .template_processor import template_processor
from .report_generator import report_generator
from .word_generator import word_generator
from .pdf_generator import pdf_generator
# ... otros imports
```

#### 3.2. Actualizar `word_generator.py`

```bash
# Reemplazar archivo
cp word_generator.py backend/app/services/word_generator.py

# Verificar que tenga la función nueva
grep -n "generar_informe_proyecto" backend/app/services/word_generator.py
```

**Debe mostrar:** Línea donde está `def generar_informe_proyecto(`

#### 3.3. Actualizar `pdf_generator.py`

```bash
# Reemplazar archivo
cp pdf_generator.py backend/app/services/pdf_generator.py

# Verificar que tenga la función nueva
grep -n "generar_informe_proyecto" backend/app/services/pdf_generator.py
```

#### 3.4. Actualizar `documentos.py`

```bash
# Reemplazar archivo
cp documentos.py backend/app/routers/documentos.py

# Verificar endpoints nuevos
grep -n "generar-informe-analisis" backend/app/routers/documentos.py
```

**Debe mostrar:**
- `generar-informe-analisis-word`
- `generar-informe-analisis-pdf`

#### 3.5. Actualizar `proyectos.py`

```bash
# ⚠️ IMPORTANTE: El archivo se llama proyectos_mejorado.py
# pero se instala como proyectos.py

# Reemplazar archivo
cp proyectos_mejorado.py backend/app/routers/proyectos.py

# Verificar integración con IA
grep -n "incluir_analisis_ia" backend/app/routers/proyectos.py
```

**Debe mostrar:** Parámetro `incluir_analisis_ia` en endpoints

#### 3.6. Actualizar `chat.py`

```bash
# ⚠️ IMPORTANTE: El archivo se llama chat_mejorado.py
# pero se instala como chat.py

# Reemplazar archivo
cp chat_mejorado.py backend/app/routers/chat.py

# Verificar endpoints de plantillas
grep -n "plantilla" backend/app/routers/chat.py
```

**Debe mostrar:** Varios endpoints con "plantilla"

---

### PASO 4: Verificación de Imports

#### 4.1. Verificar que no hay errores de sintaxis

```bash
cd backend/

# Verificar sintaxis de Python
python3 -m py_compile app/services/template_processor.py
python3 -m py_compile app/services/report_generator.py
python3 -m py_compile app/services/word_generator.py
python3 -m py_compile app/services/pdf_generator.py
python3 -m py_compile app/routers/proyectos.py
python3 -m py_compile app/routers/documentos.py
python3 -m py_compile app/routers/chat.py

cd ..
```

**Si no hay errores:** ✅ Todo bien
**Si hay errores:** ⚠️ Revisar el archivo indicado

#### 4.2. Probar imports en Python

```bash
cd backend/

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Probar imports
python3 << EOF
from app.services.template_processor import template_processor
from app.services.report_generator import report_generator
from app.services.word_generator import word_generator
from app.services.pdf_generator import pdf_generator
print("✅ Todos los imports funcionan correctamente")
EOF

cd ..
```

---

### PASO 5: Configuración

#### 5.1. Verificar `config.py`

```bash
# Abrir archivo de configuración
nano backend/app/core/config.py
# O usar tu editor preferido
```

**Verificar que existan estas variables:**

```python
class Settings(BaseSettings):
    # ... otras configuraciones ...
    
    # Directorios
    TEMPLATES_DIR: str = "backend/templates"
    GENERATED_DIR: str = "backend/storage/generated"
    UPLOAD_DIR: str = "backend/storage/uploads"
    
    # ... resto de configuración ...
```

**Si NO existen, agregar:**

```python
    # Directorios para documentos
    TEMPLATES_DIR: str = os.getenv("TEMPLATES_DIR", "backend/templates")
    GENERATED_DIR: str = os.getenv("GENERATED_DIR", "backend/storage/generated")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "backend/storage/uploads")
```

#### 5.2. Crear directorios de almacenamiento

```bash
cd backend/

# Crear directorios
mkdir -p templates
mkdir -p storage/generated
mkdir -p storage/uploads

# Verificar
ls -la templates/
ls -la storage/

cd ..
```

#### 5.3. Verificar permisos

```bash
# Linux/Mac
chmod -R 755 backend/templates
chmod -R 755 backend/storage

# Windows (PowerShell como Administrador)
# Los permisos suelen estar bien por defecto
```

---

### PASO 6: Instalar Dependencias

#### 6.1. Verificar `requirements.txt`

```bash
# Ver dependencias actuales
cat backend/requirements.txt
```

**Debe incluir:**

```
python-docx>=0.8.11
reportlab>=3.6.12
Pillow>=9.5.0
python-magic>=0.4.27
```

**Si faltan, agregar al final:**

```bash
echo "python-docx>=0.8.11" >> backend/requirements.txt
echo "reportlab>=3.6.12" >> backend/requirements.txt
echo "Pillow>=9.5.0" >> backend/requirements.txt
echo "python-magic>=0.4.27" >> backend/requirements.txt
```

#### 6.2. Instalar dependencias

```bash
cd backend/

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar
pip install -r requirements.txt

# Verificar instalación
pip list | grep -E "python-docx|reportlab|Pillow|python-magic"

cd ..
```

---

### PASO 7: Iniciar el Sistema

#### 7.1. Iniciar Backend

```bash
cd backend/

# Activar entorno virtual (si no está activo)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Iniciar servidor
python app/main.py

# O con uvicorn:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Debes ver:**

```
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 7.2. Verificar Endpoints

**Abrir navegador:**

```
http://localhost:8000/docs
```

**Verificar que aparezcan los nuevos endpoints:**

```
✅ POST /api/proyectos/{proyecto_id}/generar-informe-word
✅ POST /api/proyectos/{proyecto_id}/generar-informe-pdf
✅ GET  /api/proyectos/{proyecto_id}/analisis-ia
✅ POST /api/documentos/{documento_id}/generar-informe-analisis-word
✅ POST /api/documentos/{documento_id}/generar-informe-analisis-pdf
✅ POST /api/chat/subir-plantilla
✅ GET  /api/chat/listar-plantillas
✅ POST /api/chat/usar-plantilla/{cotizacion_id}
```

---

## ✅ CHECKLIST DE VERIFICACIÓN {#checklist-verificacion}

### Antes de Empezar

- [ ] Backup de archivos originales creado
- [ ] Estructura de directorios verificada
- [ ] Entorno virtual activado
- [ ] Base de datos funcionando

### Instalación de Archivos

- [ ] `template_processor.py` copiado a `services/`
- [ ] `report_generator.py` copiado a `services/`
- [ ] `__init__.py` actualizado en `services/`
- [ ] `word_generator.py` actualizado en `services/`
- [ ] `pdf_generator.py` actualizado en `services/`
- [ ] `proyectos.py` actualizado en `routers/`
- [ ] `documentos.py` actualizado en `routers/`
- [ ] `chat.py` actualizado en `routers/`

### Verificación de Código

- [ ] No hay errores de sintaxis
- [ ] Imports funcionan correctamente
- [ ] Todas las funciones están presentes

### Configuración

- [ ] `config.py` tiene variables de directorios
- [ ] Directorios creados: `templates/`, `storage/generated/`, `storage/uploads/`
- [ ] Permisos correctos en directorios
- [ ] Dependencias instaladas

### Testing Básico

- [ ] Backend inicia sin errores
- [ ] Endpoints nuevos visibles en `/docs`
- [ ] Se puede crear cotización
- [ ] Se puede generar Word
- [ ] Se puede generar PDF

---

## ⚙️ CONFIGURACIÓN REQUERIDA {#configuracion-requerida}

### Variables de Entorno (.env)

```bash
# backend/.env

# ═══════════════════════════════════════════
# API KEYS
# ═══════════════════════════════════════════
GEMINI_API_KEY=tu_api_key_aqui

# ═══════════════════════════════════════════
# DIRECTORIOS
# ═══════════════════════════════════════════
TEMPLATES_DIR=backend/templates
GENERATED_DIR=backend/storage/generated
UPLOAD_DIR=backend/storage/uploads

# ═══════════════════════════════════════════
# BASE DE DATOS
# ═══════════════════════════════════════════
DATABASE_URL=sqlite:///./database/tesla_cotizador.db

# ═══════════════════════════════════════════
# CONFIGURACIÓN GENERAL
# ═══════════════════════════════════════════
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=.pdf,.docx,.xlsx,.png,.jpg,.jpeg
```

### Estructura de Directorios Final

```
TESLA_COTIZADOR-V3.0/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── __init__.py ✅ ACTUALIZADO
│   │   │   ├── template_processor.py ⭐ NUEVO
│   │   │   ├── report_generator.py ⭐ NUEVO
│   │   │   ├── word_generator.py ✅ ACTUALIZADO
│   │   │   ├── pdf_generator.py ✅ ACTUALIZADO
│   │   │   ├── gemini_service.py
│   │   │   ├── rag_service.py
│   │   │   └── file_processor.py
│   │   ├── routers/
│   │   │   ├── proyectos.py ✅ ACTUALIZADO
│   │   │   ├── documentos.py ✅ ACTUALIZADO
│   │   │   ├── chat.py ✅ ACTUALIZADO
│   │   │   ├── cotizaciones.py
│   │   │   └── informes.py
│   │   └── main.py
│   ├── templates/ ⭐ NUEVO (vacío inicialmente)
│   ├── storage/
│   │   ├── generated/ ⭐ NUEVO
│   │   └── uploads/
│   ├── .env
│   └── requirements.txt
├── frontend/
├── database/
└── venv/
```

---

## 🧪 TESTING Y VALIDACIÓN {#testing-validacion}

### Test 1: Generar Informe de Proyecto con IA

```bash
# Usando curl

curl -X POST "http://localhost:8000/api/proyectos/1/generar-informe-word" \
  -H "Content-Type: application/json" \
  -d '{
    "incluir_cotizaciones": true,
    "incluir_documentos": true,
    "incluir_estadisticas": true,
    "incluir_analisis_ia": true
  }' \
  --output informe_proyecto.docx
```

**Resultado esperado:**
- ✅ Archivo `informe_proyecto.docx` descargado
- ✅ Documento incluye análisis de IA
- ✅ Métricas y KPIs presentes
- ✅ Conclusiones generadas

### Test 2: Subir Plantilla

```bash
# Usando curl

curl -X POST "http://localhost:8000/api/chat/subir-plantilla" \
  -F "archivo=@mi_plantilla.docx" \
  -F "nombre_plantilla=Mi Plantilla Premium" \
  -F "descripcion=Plantilla para proyectos grandes"
```

**Resultado esperado:**
```json
{
  "success": true,
  "nombre_plantilla": "Mi Plantilla Premium",
  "marcadores_encontrados": ["{{cliente}}", "{{proyecto}}", ...],
  "total_marcadores": 8
}
```

### Test 3: Listar Plantillas

```bash
curl -X GET "http://localhost:8000/api/chat/listar-plantillas"
```

**Resultado esperado:**
```json
{
  "total": 1,
  "plantillas": [
    {
      "nombre": "mi_plantilla_premium",
      "total_marcadores": 8,
      ...
    }
  ]
}
```

### Test 4: Usar Plantilla

```bash
curl -X POST "http://localhost:8000/api/chat/usar-plantilla/1" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_plantilla": "mi_plantilla_premium_20251018.docx"
  }' \
  --output cotizacion_personalizada.docx
```

**Resultado esperado:**
- ✅ Archivo generado con plantilla del usuario
- ✅ Marcadores reemplazados
- ✅ Formato preservado

### Test 5: Análisis IA de Proyecto

```bash
curl -X GET "http://localhost:8000/api/proyectos/1/analisis-ia"
```

**Resultado esperado:**
```json
{
  "success": true,
  "analisis": {
    "resumen_ejecutivo": {
      "estado_general": "EN BUEN CURSO",
      "salud_financiera": "EXCELENTE",
      ...
    },
    "metricas": {...},
    "conclusiones": "...",
    "recomendaciones": [...],
    "riesgos": [...]
  }
}
```

---

## 🔧 TROUBLESHOOTING {#troubleshooting}

### Problema 1: Error de Import

**Error:**
```
ImportError: cannot import name 'template_processor' from 'app.services'
```

**Solución:**
```bash
# Verificar que __init__.py tenga el import
grep "template_processor" backend/app/services/__init__.py

# Si no está, agregar:
echo "from .template_processor import template_processor" >> backend/app/services/__init__.py

# Reiniciar servidor
```

### Problema 2: Directorio no existe

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'backend/templates'
```

**Solución:**
```bash
# Crear directorios
mkdir -p backend/templates
mkdir -p backend/storage/generated
mkdir -p backend/storage/uploads

# Verificar en config.py
```

### Problema 3: python-docx no instalado

**Error:**
```
ModuleNotFoundError: No module named 'docx'
```

**Solución:**
```bash
pip install python-docx
```

### Problema 4: Endpoint no aparece

**Error:**
Los nuevos endpoints no aparecen en `/docs`

**Solución:**
```bash
# Verificar que el router esté registrado en main.py
grep "proyectos" backend/app/main.py

# Debe tener:
# app.include_router(proyectos_router, prefix="/api/proyectos", tags=["Proyectos"])

# Reiniciar servidor completamente
```

### Problema 5: Error al generar documento

**Error:**
```
Exception: Error al generar informe
```

**Solución:**
```bash
# Verificar logs
tail -f backend/logs/app.log

# Verificar permisos de escritura
chmod -R 755 backend/storage/generated

# Verificar que el directorio existe
ls -la backend/storage/generated
```

---

## 🎓 PRÓXIMOS PASOS

### Una vez instalado:

1. **Probar cada endpoint** usando Postman o `/docs`
2. **Crear plantillas de ejemplo** para diferentes tipos de proyectos
3. **Configurar Gemini API** para análisis completo
4. **Entrenar al equipo** en el uso del sistema
5. **Crear documentación** de procesos internos

### Recomendaciones:

- ✅ Hacer backup semanal de la base de datos
- ✅ Mantener plantillas versionadas
- ✅ Revisar logs regularmente
- ✅ Actualizar dependencias mensualmente
- ✅ Documentar casos de uso

---

## 📞 SOPORTE

### Si encuentras problemas:

1. Revisar este documento
2. Revisar sección de Troubleshooting
3. Consultar logs: `backend/logs/app.log`
4. Verificar que todas las dependencias estén instaladas

### Logs útiles:

```bash
# Ver logs en tiempo real
tail -f backend/logs/app.log

# Ver últimas 100 líneas
tail -n 100 backend/logs/app.log

# Buscar errores
grep "ERROR" backend/logs/app.log
```

---

## ✅ INSTALACIÓN COMPLETADA

Si llegaste hasta aquí y pasaste todos los tests:

**🎉 ¡FELICITACIONES! 🎉**

Tu sistema Tesla Cotizador v3.0 está completamente actualizado con:

✅ Generación avanzada de documentos
✅ Análisis inteligente con IA
✅ Plantillas personalizables
✅ Informes ejecutivos automáticos
✅ Gestión completa de documentos

**El sistema está listo para producción.**

---

**Versión del documento:** 1.0
**Fecha:** 18 de Octubre, 2025
**Autor:** Sistema de Actualización Tesla Cotizador