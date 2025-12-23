# TESLA COTIZADOR V3.0

Sistema profesional de cotizaciones y gestión de proyectos con generación automática de documentos (Word/PDF) usando IA.

---

## 📋 ACTUALIZACIONES RECIENTES

### Sesión: 06 de Diciembre 2025

#### ✅ **Limpieza Profesional de Código**
- **30 archivos duplicados** movidos a `backup/`
- Eliminados archivos `*copy*`, `*.pyc`, `__pycache__`
- Carpeta `backup/` agregada al repositorio con documentación
- Proyecto limpio: **57 archivos Python funcionales**
- **20,854 líneas** de código duplicado removidas

#### ✅ **Base de Datos Actualizada**
- BD recreada con esquema correcto (`cliente_id`, `proyecto_id`)
- **50 clientes demo** cargados desde `crear_datos_demo.py`
- 6 tablas: `clientes`, `cotizaciones`, `items`, `proyectos`, `documentos`, `informes`
- Tamaño: **124KB** (`database/tesla_cotizador.db`)
- Fix: RUCs de búsqueda corregidos (20100001000 vs 20101000000)

#### ✅ **Generación de Documentos - Paridad Total**
- **6 tipos de documentos** funcionando:
  1. Cotización Simple
  2. Cotización Compleja
  3. Proyecto Simple
  4. Proyecto Complejo (PMI)
  5. Informe Técnico
  6. Informe Ejecutivo
- **30 documentos de prueba** generados usando datos reales de BD
- Generadores: `word_generator.py` (943 líneas), `pdf_generator.py` (490 líneas)

#### ✅ **Fusión de Ramas**
- Integrados cambios de PC (documentación tesis, PDF Twin Design)
- Mantenida carpeta `backup/` de mi trabajo
- Tema de colores: **Twin Design Azul** (#1a3c6e) en PDF
- Documentación completa de tesis agregada

#### ✅ **Documentación de Tesis**
- **27 documentos markdown** en `DOCUMENTOS_TESIS/`
- **6 prototipos HTML** profesionales
- **4 archivos de código fuente** respaldados
- Estrategia Twin Design documentada
- Análisis de arquitectura completo

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Backend (FastAPI + Python)
```
backend/
├── app/
│   ├── main.py                    # Punto de entrada FastAPI
│   ├── core/                      # Configuración y BD
│   ├── models/                    # 7 modelos SQLAlchemy
│   ├── routers/                   # 10 endpoints API
│   ├── services/                  # 12 servicios
│   │   ├── word_generator.py     # Generador Word (943 líneas)
│   │   ├── pdf_generator.py      # Generador PDF (490 líneas)
│   │   ├── pili_brain.py         # Cerebro IA
│   │   └── pili_orchestrator.py  # Orquestador
│   ├── schemas/                   # 5 validaciones Pydantic
│   └── templates/
│       └── documentos/
│           └── plantillas_modelo.py  # Plantillas 6 tipos docs
└── crear_datos_demo.py            # Script carga 50 clientes
```

### Frontend (React)
```
frontend/
└── src/
    ├── App.jsx                    # Componente principal
    ├── components/                # 7 componentes React
    │   ├── PiliAvatar.jsx
    │   ├── ChatIA.jsx
    │   ├── ClienteSelector.jsx
    │   └── CotizacionEditor.jsx
    └── services/
        └── api.js                 # Cliente API
```

### Base de Datos
```
database/
└── tesla_cotizador.db             # SQLite 124KB
    ├── clientes (50 registros)
    ├── cotizaciones (2)
    ├── proyectos (2)
    ├── items (0)
    ├── documentos (0)
    └── informes (0)
```

---

## 📄 TIPOS DE DOCUMENTOS SOPORTADOS

| Tipo | Formato | Generador | Estado |
|------|---------|-----------|--------|
| **Cotización Simple** | Word/PDF | `word_generator.py` / `pdf_generator.py` | ✅ Funcionando |
| **Cotización Compleja** | Word/PDF | `word_generator.py` / `pdf_generator.py` | ✅ Funcionando |
| **Proyecto Simple** | Word/PDF | `word_generator.py` / `pdf_generator.py` | ✅ Funcionando |
| **Proyecto Complejo** | Word/PDF | `word_generator.py` / `pdf_generator.py` | ✅ Funcionando |
| **Informe Técnico** | Word/PDF | `word_generator.py` / `pdf_generator.py` | ✅ Funcionando |
| **Informe Ejecutivo** | Word/PDF | `word_generator.py` / `pdf_generator.py` | ✅ Funcionando |

### Características:
- **Diseño Twin Design**: PDFs idénticos a prototipos HTML
- **Paleta de colores**: Azul corporativo (#1a3c6e) + Dorado (#DAA520)
- **Editable (Word)**: Formato nativo `.docx` para colaboración
- **Seguro (PDF)**: Formato inmutable para contratos legales
- **Polimórfico**: Mismo código adapta complejidad según datos

---

## 🚀 INSTALACIÓN

### Requisitos
- Python 3.11+
- Node.js 18+
- SQLite 3

### Backend
```bash
cd backend
pip install fastapi uvicorn sqlalchemy pydantic python-docx reportlab
python -m uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Base de Datos
```bash
# Crear BD con 50 clientes demo
python backend/crear_datos_demo.py
```

---

## 🧪 PRUEBAS REALIZADAS

### Script de Prueba
```bash
# Generar 30 documentos (6 tipos × 5 clientes)
python generar_documentos_prueba.py
```

**Resultado:**
- ✅ 30 documentos generados exitosamente
- ✅ Guardados en `storage/generados/`
- ✅ Usa datos reales de BD (50 clientes)
- ✅ Todos los tipos funcionando

---

## 📁 ESTRUCTURA DEL PROYECTO

```
TESLA_COTIZADOR-V3.0/
├── backend/                       # FastAPI backend
│   ├── app/                       # Aplicación principal
│   ├── crear_datos_demo.py        # Script BD demo
│   └── documentos_generados_demo/ # 6 ejemplos .docx
├── frontend/                      # React frontend
│   └── src/
├── database/                      # Base de datos
│   └── tesla_cotizador.db         # SQLite 124KB
├── storage/                       # Archivos generados
│   └── generados/                 # 31 documentos .docx
├── backup/                        # 30 archivos duplicados
│   ├── backend/                   # 24 archivos backend
│   ├── frontend/                  # 6 archivos frontend
│   └── README.md
├── DOCUMENTOS_TESIS/              # Documentación tesis (27 docs)
│   ├── *.md                       # Análisis técnico
│   ├── *.html                     # 6 prototipos
│   └── CODIGO_FUENTE/             # 4 archivos Python
├── DOCUMENTOS_VARIOS/             # Archivo histórico
├── ARCHIVOS_PYTHON/               # 16 scripts de prueba
├── generar_documentos_prueba.py   # Script generación docs
└── README.md                      # Este archivo
```

---

## 🎨 DISEÑO Y ESTILOS

### Twin Design
Estrategia de diseño donde PDF replica exactamente los prototipos HTML:
- **Colores corporativos**: `#1a3c6e` (Azul Tesla) + `#DAA520` (Dorado)
- **Tipografía**: Helvetica / Helvetica-Bold
- **Tablas**: Headers azules + filas alternadas (zebra striping)
- **Márgenes**: Consistentes entre HTML y documentos generados

### Flujo de Generación
```
Usuario → HTML (Vista Previa) → JSON → Plantillas Python → Documento (.docx/.pdf)
```

---

## 📊 ESTADÍSTICAS

| Métrica | Valor |
|---------|-------|
| **Archivos Python** | 91 activos |
| **Líneas de código** | ~50,000 |
| **Modelos de datos** | 7 |
| **Endpoints API** | 10 |
| **Servicios backend** | 12 |
| **Componentes React** | 7 |
| **Clientes demo** | 50 |
| **Documentos generados** | 31 |
| **Tipos de documentos** | 6 |
| **Prototipos HTML** | 6 |
| **Documentos tesis** | 27 |

---

## 🔧 SERVICIOS BACKEND

| Servicio | Archivo | Función |
|----------|---------|---------|
| **PILI Brain** | `pili_brain.py` | Cerebro IA - Lógica de negocio |
| **PILI Orchestrator** | `pili_orchestrator.py` | Orquestador de agentes |
| **Word Generator** | `word_generator.py` | Generación documentos Word |
| **PDF Generator** | `pdf_generator.py` | Generación documentos PDF |
| **Gemini Service** | `gemini_service.py` | Integración Google Gemini |
| **Template Processor** | `template_processor.py` | Procesamiento plantillas |
| **RAG Service** | `rag_service.py` | Retrieval Augmented Generation |
| **Multi IA Service** | `multi_ia_service.py` | Integración múltiples IAs |
| **Report Generator** | `report_generator.py` | Generador de reportes |
| **File Processor** | `file_processor.py` | Procesamiento archivos |
| **PILI Integrator** | `pili_integrator.py` | Integrador PILI |

---

## 📚 DOCUMENTACIÓN ADICIONAL

### Tesis
Ver `DOCUMENTOS_TESIS/INDICE_TESIS_DOCUMENTACION.md` para:
- Arquitectura del sistema
- Análisis de IA (PILI)
- Diseño visual y UX
- Ventaja competitiva
- Conclusiones técnicas

### Histórico
Ver `DOCUMENTOS_VARIOS/` para análisis preliminares y borradores.

---

## 🔒 BACKUP

Carpeta `backup/` contiene:
- 30 archivos duplicados movidos durante limpieza
- 24 archivos backend (configs, databases, schemas)
- 6 archivos frontend (App.jsx copies)
- Documentación en `backup/README.md`

**Nota:** No eliminar sin revisar. Puede contener código útil de versiones anteriores.

---

## 📝 COMMITS IMPORTANTES

| Commit | Descripción |
|--------|-------------|
| `e3103c8` | feat: Agregar carpeta backup/ al repositorio |
| `8e15a13` | fix(pdf): Actualizar tema de colores de azul a rojo/dorado Tesla |
| `5fd8601` | merge: Integrar cambios de PC (BD actualizada, PDF Twin Design) |
| `a5575d8` | fix(db): Corregir RUCs de búsqueda en crear_datos_demo.py |
| `dbc42af` | chore: Limpieza profesional de archivos duplicados |
| `d5435f8` | feat: Script generación 30 documentos prueba desde BD |

---

## ⚙️ CONFIGURACIÓN

### Variables de Entorno
Crear `.env` basado en `.env.example`:
```bash
# Base de datos
DATABASE_URL=sqlite:///./database/tesla_cotizador.db

# API Keys
GEMINI_API_KEY=tu_api_key_aqui

# Configuración
ENVIRONMENT=development
DEBUG=True
```

---

## 🎯 PRÓXIMOS PASOS

1. **Vista Previa Frontend**: Integrar prototipos HTML con componente React
2. **Plantillas .docx**: Crear archivos base editables
3. **Testing**: Pruebas unitarias e integración
4. **Deploy**: Configurar producción

---

## 👨‍💻 DESARROLLO

**Proyecto:** TESLA COTIZADOR V3.0
**Empresa:** TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.
**Ubicación:** Huancayo, Junín - Perú
**Actualización:** 06 de Diciembre 2025

---

## 📄 LICENCIA

Todos los derechos reservados © 2025 TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.
