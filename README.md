# 🚀 TESLA COTIZADOR V3.0 - Sistema Profesional de Generación de Documentos

> **Estado**: ✅ **SISTEMA OPERATIVO** - Frontend conectado con Backend Profesional v4.0  
> **Última actualización**: 25 de Noviembre, 2025  
> **Versión**: 3.0.0 (Backend Profesional v4.0 integrado)

---

## 📋 Tabla de Contenidos

1. [Descripción General](#-descripción-general)
2. [Estado Actual del Sistema](#-estado-actual-del-sistema)
3. [Características Principales](#-características-principales)
4. [Inicio Rápido](#-inicio-rápido)
5. [Arquitectura](#-arquitectura)
6. [Documentación Detallada](#-documentación-detallada)
7. [Solución de Problemas](#-solución-de-problemas)

---

## 🎯 Descripción General

TESLA COTIZADOR v3.0 es un **sistema inteligente de generación de documentos** que combina:

- 🤖 **IA Local (PILIBrain)**: Generación automática de cotizaciones sin internet
- 📊 **6 Tipos de Documentos**: Cotizaciones, Proyectos e Informes (simples y complejos)
- 🧠 **ML Local**: Clasificación automática de servicios con spaCy + sklearn
- 🔍 **RAG Local**: Búsqueda semántica con ChromaDB
- 📈 **Gráficas Profesionales**: Gantt, KPIs, matrices con Plotly
- 📄 **Multi-formato**: Procesa PDF, Word, Excel, imágenes con OCR

---

## ✅ Estado Actual del Sistema

### Correcciones Aplicadas (25/Nov/2025)

| Componente | Estado | Descripción |
|------------|--------|-------------|
| **Frontend** | ✅ OPERATIVO | Conectado con backend profesional |
| **Backend Profesional** | ✅ ACTIVO | PILIBrain funcionando |
| **Integración** | ✅ CONECTADO | Endpoint `/api/chat/chat-contextualizado` activo |
| **Generación Items** | ✅ AUTOMÁTICA | ML Engine detecta y genera items |
| **Vista Previa** | ✅ PROFESIONAL | HTML generado por backend |
| **RAG Engine** | ✅ DISPONIBLE | ChromaDB listo para indexar documentos |

### Última Auditoría

Se realizó una auditoría completa el 25/Nov/2025 que identificó y corrigió:
- ✅ Desconexión entre frontend y backend profesional
- ✅ Endpoint de chat actualizado a versión profesional
- ✅ Formato de historial ajustado para PILIBrain
- ✅ Sistema v4.0 completamente integrado

📄 **Ver**: [`implementation_plan.md`](./implementation_plan.md) para detalles de la auditoría

---

## 🌟 Características Principales

### 1. Generación Automática con IA

```
Usuario: "Cotización para casa de 150m2"
   ↓
PILIBrain analiza y detecta: "eléctrico-residencial"
   ↓
Genera automáticamente:
  ✅ 15x Punto de luz LED 18W
  ✅ 12x Tomacorriente doble
  ✅ 8x Interruptor simple
  ✅ 1x Tablero eléctrico
  ✅ 150m Cable THW 2.5mm²
```

### 2. 6 Tipos de Documentos

| Tipo | Simple | Complejo |
|------|--------|----------|
| **Cotización** | Lista items + precios | + Cronograma + Garantías |
| **Proyecto** | 5 fases básicas | 6 fases PMI + Gantt + KPIs |
| **Informe** | 5 secciones técnicas | Formato APA + ROI/TIR + Gráficas |

### 3. 10 Servicios Soportados

- ⚡ Eléctrico (residencial, comercial, industrial)
- 🔥 Contraincendios
- 🏠 Domótica
- 📋 Expedientes técnicos
- 🚰 Saneamiento
- 🏢 ITSE
- 🔌 Pozo a tierra
- 📹 CCTV
- 🌐 Redes
- ⚙️ Automatización industrial

### 4. Procesamiento de Archivos

Sube archivos de referencia y el sistema los procesa automáticamente:
- 📄 **PDF**: Extrae texto y tablas
- 📝 **Word**: Lee párrafos y tablas
- 📊 **Excel**: Procesa todas las hojas
- 📷 **Imágenes**: OCR con Tesseract
- 🔍 **RAG**: Indexa en ChromaDB para búsqueda semántica

---

## 🚀 Inicio Rápido

### Requisitos Previos

- **Python**: 3.11+
- **Node.js**: 16+
- **RAM**: 8GB mínimo (16GB recomendado)
- **Disco**: 2GB libres

### Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/Oscar-Ivan-Salas/TESLA_COTIZADOR-V3.0.git
cd TESLA_COTIZADOR-V3.0

# 2. Instalar dependencias del backend
cd backend
pip install -r requirements_professional.txt
python -m spacy download es_core_news_sm

# 3. Instalar dependencias del frontend
cd ../frontend
npm install

# 4. Configurar variables de entorno
cp backend/.env.example backend/.env
# Editar backend/.env según necesidades
```

### Ejecutar el Sistema

#### Opción 1: Scripts de inicio (Windows)

```bash
# Terminal 1: Backend
.\run_backend.bat

# Terminal 2: Frontend
cd frontend
npm start
```

#### Opción 2: Manual

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm start
```

### Acceder a la Aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

---

## 🏗️ Arquitectura

### Diagrama de Componentes

```
┌─────────────────────────────────────────┐
│  FRONTEND (React + TailwindCSS)         │
│  - Chat con PILI                        │
│  - Vista previa editable                │
│  - Gestión de archivos                  │
└─────────────────────────────────────────┘
              ↓ HTTP/REST
┌─────────────────────────────────────────┐
│  BACKEND PROFESIONAL (FastAPI)          │
│  ┌─────────────────────────────────┐   │
│  │ PILIBrain (IA Local)            │   │
│  │ - Generación automática         │   │
│  │ - Detección de servicios        │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ RAG Engine (ChromaDB)           │   │
│  │ - Búsqueda semántica            │   │
│  │ - Indexación de documentos      │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ ML Engine (spaCy + sklearn)     │   │
│  │ - Clasificación de servicios    │   │
│  │ - Extracción de entidades       │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ Chart Engine (Plotly)           │   │
│  │ - Gantt, KPIs, Matrices         │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ Word/PDF Generator              │   │
│  │ - Documentos profesionales      │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  STORAGE                                │
│  - PostgreSQL (datos)                   │
│  - ChromaDB (vectores)                  │
│  - Filesystem (archivos)                │
└─────────────────────────────────────────┘
```

### Flujo de Generación de Cotización

```mermaid
graph LR
    A[Usuario escribe mensaje] --> B[PILIBrain]
    B --> C[ML Engine: Detecta servicio]
    C --> D[Genera items automáticamente]
    D --> E[HTML Preview]
    E --> F[Usuario edita]
    F --> G[Genera Word/PDF]
```

---

## 📚 Documentación Detallada

### Documentos Principales

| Documento | Descripción | Ubicación |
|-----------|-------------|-----------|
| **README_PROFESSIONAL.md** | Documentación técnica completa del sistema v4.0 | [`README_PROFESSIONAL.md`](./README_PROFESSIONAL.md) |
| **implementation_plan.md** | Auditoría y correcciones aplicadas | [`implementation_plan.md`](./implementation_plan.md) |
| **walkthrough.md** | Guía de cambios y verificación | [`walkthrough.md`](./walkthrough.md) |

### Endpoints Principales

#### Chat con PILI (Profesional)
```http
POST /api/chat/chat-contextualizado
Content-Type: application/json

{
  "tipo_flujo": "cotizacion-simple",
  "mensaje": "Cotización para casa de 150m2",
  "historial": [],
  "contexto_adicional": "",
  "generar_html": true
}
```

#### Generar Documento Word
```http
POST /api/cotizaciones/{id}/generar-word
```

#### Subir Archivos
```http
POST /api/documentos/upload
Content-Type: multipart/form-data
```

---

## 🔧 Solución de Problemas

### Problema: Chat no genera items automáticamente

**Solución**: Verificar que el endpoint profesional esté activo

```bash
# Verificar endpoint
curl -X POST http://localhost:8000/api/chat/chat-contextualizado \
  -H "Content-Type: application/json" \
  -d '{"tipo_flujo":"cotizacion-simple","mensaje":"test","historial":[],"generar_html":true}'

# Debe responder con JSON que incluye "cotizacion_generada"
```

### Problema: Error de conexión con backend

**Solución**: Verificar que el backend está corriendo

```bash
# Verificar estado
curl http://localhost:8000/

# Debe responder:
# {"message":"Tesla Cotizador API v3.0","status":"online",...}
```

### Problema: Vista previa no aparece

**Solución**: Verificar en consola del navegador (F12)

1. Abrir DevTools
2. Ver tab "Console"
3. Buscar errores relacionados con `html_preview`
4. Verificar que `data.html_preview` existe en la respuesta

### Problema: Modelos ML no cargan

**Solución**: Descargar modelo spaCy

```bash
python -m spacy download es_core_news_sm
```

---

## 🧪 Pruebas

### Prueba Rápida del Sistema

```bash
# 1. Abrir http://localhost:3000
# 2. Seleccionar "Cotización Simple"
# 3. Escribir: "Cotización para casa de 150m2"
# 4. Verificar que:
#    ✅ PILI responde
#    ✅ Se generan items automáticamente
#    ✅ Vista previa HTML aparece
#    ✅ Items tienen descripciones reales
```

### Verificar Logs del Backend

```bash
# Deberías ver en la terminal del backend:
🤖 PILI chat contextualizado para cotizacion-simple
✅ PILIBrain generó 5 items para cotización
📊 Servicio detectado: electrico-residencial
```

---

## 📊 Rendimiento

| Operación | Tiempo Promedio |
|-----------|----------------|
| Clasificación ML | < 100ms |
| Búsqueda RAG | < 500ms |
| Generar gráficas | 1-3s |
| Documento completo | 5-10s |
| OCR de imagen | 2-5s |

---

## 🔐 Seguridad

- ✅ CORS configurado para localhost
- ✅ Validación de archivos subidos
- ✅ Límite de tamaño de archivos (10MB)
- ✅ Sanitización de inputs
- ⚠️ **Producción**: Configurar HTTPS y autenticación

---

## 🚀 Despliegue en Producción

### Docker

```bash
# Construir y levantar
docker-compose -f docker-compose.production.yml up -d

# Ver logs
docker-compose -f docker-compose.production.yml logs -f
```

### Variables de Entorno Importantes

```env
# Backend
DATABASE_URL=postgresql://user:pass@localhost/tesla
GEMINI_API_KEY=your_key_here  # Opcional
STORAGE_PATH=./storage

# Frontend
REACT_APP_API_URL=https://api.tudominio.com
```

---

## 📝 Changelog

### v3.0.0 (25/Nov/2025) - Integración Backend Profesional

**Añadido**:
- ✅ Integración completa con PILIBrain
- ✅ Generación automática de items con ML
- ✅ RAG Engine con ChromaDB
- ✅ Chart Engine con Plotly
- ✅ Procesamiento multi-formato de archivos

**Corregido**:
- ✅ Conexión frontend-backend profesional
- ✅ Formato de historial para PILIBrain
- ✅ Endpoint de chat actualizado

**Mejorado**:
- ✅ Vista previa HTML profesional
- ✅ Detección automática de servicios
- ✅ Documentación completa

---

## 👥 Equipo

- **Desarrollador Principal**: Oscar Ivan Salas
- **Empresa**: Tesla Electricidad y Automatización S.A.C.
- **Email**: ingenieria.teslaelectricidad@gmail.com
- **Teléfono**: 906315961

---

## 📄 Licencia

Copyright © 2024 Tesla Electricidad y Automatización S.A.C.  
Todos los derechos reservados.

---

## 🙏 Agradecimientos

- **FastAPI**: Framework backend
- **React**: Framework frontend
- **ChromaDB**: Vector database
- **spaCy**: NLP en español
- **Plotly**: Gráficas profesionales
- **Tesseract**: OCR

---

## 📞 Soporte

¿Necesitas ayuda? Contacta:
- 📧 Email: ingenieria.teslaelectricidad@gmail.com
- 📱 WhatsApp: +51 906315961
- 📍 Ubicación: Huancayo, Junín - Perú

---

**¡Sistema listo para generar documentos profesionales!** 🎉
