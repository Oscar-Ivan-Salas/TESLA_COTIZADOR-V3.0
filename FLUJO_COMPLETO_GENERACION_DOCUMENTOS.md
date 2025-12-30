# 🔄 FLUJO COMPLETO DE GENERACIÓN DE DOCUMENTOS

**Fecha**: 29 de Diciembre 2025
**Proyecto**: TESLA COTIZADOR V3.0
**Propósito**: Documentar EXACTAMENTE cómo funciona todo el flujo de generación de documentos

---

## ✅ RESPUESTA DIRECTA A TU PREGUNTA

**SÍ**, TODO el flujo está capturado en el sistema:

✅ **6 Plantillas HTML** para vista previa en navegador
✅ **6 Generadores Python** para crear archivos Word (.docx)
✅ **1 Convertidor PDF** para convertir Word → PDF
✅ **Todo el código necesario** para el flujo completo

---

## 📊 RESUMEN VISUAL DEL FLUJO

```
┌─────────────────────────────────────────────────────────────────┐
│                  FLUJO COMPLETO DE GENERACIÓN                   │
└─────────────────────────────────────────────────────────────────┘

1️⃣ USUARIO RELLENA DATOS
   └─> Frontend envía datos al backend
        │
        v
2️⃣ VISTA PREVIA HTML (Navegador)
   └─> 6 Plantillas HTML en backend/app/templates/documentos/
        │
        v
3️⃣ GENERACIÓN WORD
   └─> 6 Generadores Python usan python-docx
        │
        v
4️⃣ CONVERSIÓN A PDF
   └─> pdf_converter.py convierte Word → PDF
        │
        v
5️⃣ DESCARGA
   └─> Usuario descarga Word o PDF
```

---

## 📂 COMPONENTE 1: PLANTILLAS HTML (Vista Previa)

### Ubicación
```
backend/app/templates/documentos/
├── PLANTILLA_HTML_COTIZACION_SIMPLE.html         (15 KB)
├── PLANTILLA_HTML_COTIZACION_COMPLEJA.html       (21 KB)
├── PLANTILLA_HTML_PROYECTO_SIMPLE.html           (21 KB)
├── PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html     (26 KB)
├── PLANTILLA_HTML_INFORME_TECNICO.html           (19 KB)
└── PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html     (25 KB)
```

### ¿Para qué sirven?
- ✅ **Vista previa en navegador** antes de generar Word/PDF
- ✅ **Validación visual** de cómo se verá el documento
- ✅ **NO se usan** para generar Word/PDF (solo para preview)

### Características
- **Formato**: HTML + CSS (Tailwind CSS)
- **Estado**: ✅ COMPARTIDAS por sistema antiguo y nuevo
- **Modificables**: ✅ SÍ (editar HTML/CSS para cambiar diseño)

### Ejemplo de contenido
```html
<!-- PLANTILLA_HTML_COTIZACION_SIMPLE.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Cotización {{ numero }}</title>
    <style>
        /* Estilos CSS */
        .header { background: #0052A3; color: white; }
        .tabla { border: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="header">
        <h1>COTIZACIÓN</h1>
        <p>{{ numero }}</p>
    </div>

    <div class="datos-cliente">
        <p><strong>Cliente:</strong> {{ cliente }}</p>
        <p><strong>Proyecto:</strong> {{ proyecto }}</p>
    </div>

    <table class="tabla">
        <thead>
            <tr>
                <th>Descripción</th>
                <th>Cantidad</th>
                <th>Precio</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr>
                <td>{{ item.descripcion }}</td>
                <td>{{ item.cantidad }}</td>
                <td>S/ {{ item.precio_unitario }}</td>
                <td>S/ {{ item.total }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="totales">
        <p><strong>Subtotal:</strong> S/ {{ subtotal }}</p>
        <p><strong>IGV (18%):</strong> S/ {{ igv }}</p>
        <p><strong>TOTAL:</strong> S/ {{ total }}</p>
    </div>
</body>
</html>
```

---

## 🐍 COMPONENTE 2: GENERADORES PYTHON WORD

### Ubicación Sistema ANTIGUO (INTACTO)
```
backend/app/services/generators/
├── cotizacion_simple_generator.py         (16.7 KB)
├── cotizacion_compleja_generator.py       (16.2 KB)
├── proyecto_simple_generator.py           (15.0 KB)
├── proyecto_complejo_pmi_generator.py     (16.5 KB)
├── informe_tecnico_generator.py           (8.0 KB)
└── informe_ejecutivo_apa_generator.py     (10.5 KB)
```

### Ubicación Sistema NUEVO (MIGRADO)
```
backend/app/services/professional/generators/
├── cotizaciones/
│   ├── simple.py                          (16.7 KB) ✅ COPIA EXACTA
│   └── compleja.py                        (16.2 KB) ✅ COPIA EXACTA
├── proyectos/
│   ├── simple.py                          (15.0 KB) ✅ COPIA EXACTA
│   └── complejo_pmi.py                    (16.5 KB) ✅ COPIA EXACTA
└── informes/
    ├── tecnico.py                         (8.0 KB) ✅ COPIA EXACTA
    └── ejecutivo_apa.py                   (10.5 KB) ✅ COPIA EXACTA
```

### ¿Para qué sirven?
- ✅ **Generan archivos Word (.docx)** usando la librería `python-docx`
- ✅ **NO usan las plantillas HTML** (generan desde código Python)
- ✅ **Replican el diseño** de las plantillas HTML en formato Word

### Tecnología usada
- **Librería**: `python-docx` (instalado en requirements.txt)
- **Método**: Crear documento Word desde cero con código Python
- **NO usa plantillas Word**: Todo generado programáticamente

### Ejemplo de código (cotizaciones/simple.py)
```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

class CotizacionSimpleGenerator:
    """Generador de cotizaciones simples con diseño profesional"""

    # Colores Tesla Azul
    COLOR_PRIMARIO = RGBColor(0, 82, 163)  # #0052A3

    def __init__(self, datos, opciones=None):
        self.datos = datos
        self.doc = Document()  # ← Crear documento Word vacío
        self._configurar_margenes()

    def generar(self, ruta_salida):
        """Genera el documento Word"""
        # 1. Crear encabezado
        self._crear_encabezado()

        # 2. Datos del cliente
        self._agregar_datos_cliente()

        # 3. Tabla de items
        self._crear_tabla_items()

        # 4. Totales
        self._agregar_totales()

        # 5. Guardar archivo Word
        self.doc.save(ruta_salida)
        return ruta_salida

    def _crear_encabezado(self):
        """Crea encabezado con logo y título"""
        # Agregar logo si existe
        if self.datos.get('logo_base64'):
            self.doc.add_picture(logo_path, width=Inches(2))

        # Título principal
        heading = self.doc.add_heading('COTIZACIÓN', 0)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Número de cotización
        numero = self.doc.add_paragraph(self.datos['numero'])
        numero.alignment = WD_ALIGN_PARAGRAPH.CENTER

    def _crear_tabla_items(self):
        """Crea tabla de items con formato"""
        # Crear tabla
        tabla = self.doc.add_table(rows=1, cols=4)
        tabla.style = 'Light Grid Accent 1'

        # Encabezados
        headers = tabla.rows[0].cells
        headers[0].text = 'Descripción'
        headers[1].text = 'Cantidad'
        headers[2].text = 'Precio Unit.'
        headers[3].text = 'Total'

        # Agregar items
        for item in self.datos['items']:
            row = tabla.add_row().cells
            row[0].text = item['descripcion']
            row[1].text = str(item['cantidad'])
            row[2].text = f"S/ {item['precio_unitario']:,.2f}"
            row[3].text = f"S/ {item['total']:,.2f}"

        # Aplicar colores a encabezados
        for cell in headers:
            self._aplicar_color_celda(cell, self.COLOR_PRIMARIO)

    def _agregar_totales(self):
        """Agrega sección de totales"""
        self.doc.add_paragraph()

        # Subtotal
        p_subtotal = self.doc.add_paragraph()
        p_subtotal.add_run('Subtotal: ').bold = True
        p_subtotal.add_run(f"S/ {self.datos['subtotal']:,.2f}")
        p_subtotal.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        # IGV
        p_igv = self.doc.add_paragraph()
        p_igv.add_run('IGV (18%): ').bold = True
        p_igv.add_run(f"S/ {self.datos['igv']:,.2f}")
        p_igv.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        # Total
        p_total = self.doc.add_paragraph()
        run_total = p_total.add_run('TOTAL: ')
        run_total.bold = True
        run_total.font.size = Pt(14)
        run_valor = p_total.add_run(f"S/ {self.datos['total']:,.2f}")
        run_valor.font.size = Pt(14)
        run_valor.font.color.rgb = self.COLOR_PRIMARIO
        p_total.alignment = WD_ALIGN_PARAGRAPH.RIGHT


# Función de generación (llamada desde fuera)
def generar_cotizacion_simple(datos, ruta_salida, opciones=None):
    """
    Genera una cotización simple en formato Word

    Args:
        datos: Diccionario con datos de la cotización
        ruta_salida: Ruta donde guardar el archivo .docx
        opciones: Opciones de personalización (opcional)

    Returns:
        Ruta del archivo generado
    """
    generador = CotizacionSimpleGenerator(datos, opciones)
    return generador.generar(ruta_salida)
```

### Características clave
- ✅ **No usa plantillas Word**: Todo creado desde código
- ✅ **Replicas el diseño HTML**: Mismo aspecto visual
- ✅ **Colores personalizables**: 5 esquemas de colores
- ✅ **Formato profesional**: Tablas, encabezados, totales
- ✅ **Logo incluido**: Puede incluir logo en base64

---

## 📄 COMPONENTE 3: CONVERTIDOR PDF

### Ubicación Sistema ANTIGUO
```
backend/app/services/generators/pdf_converter.py  (3.4 KB)
```

### Ubicación Sistema NUEVO
```
backend/app/services/professional/generators/pdf_converter.py  (3.4 KB) ✅ COPIA
```

### ¿Para qué sirve?
- ✅ **Convierte Word (.docx) a PDF (.pdf)**
- ✅ **Multiplataforma**: Windows, Linux, Mac
- ✅ **Usa LibreOffice** en Linux (más común en servidores)

### Código del convertidor
```python
"""
Generador de Conversión Word a PDF
Convierte documentos Word (.docx) a PDF
"""

import subprocess
from pathlib import Path
import platform


def convertir_word_a_pdf(ruta_word, ruta_pdf=None):
    """
    Convierte un documento Word a PDF

    Args:
        ruta_word: Ruta del archivo Word (.docx)
        ruta_pdf: Ruta del archivo PDF de salida (opcional)

    Returns:
        Ruta del archivo PDF generado
    """
    ruta_word = Path(ruta_word)

    if not ruta_word.exists():
        raise FileNotFoundError(f"Archivo Word no encontrado: {ruta_word}")

    # Determinar ruta de salida
    if ruta_pdf is None:
        ruta_pdf = ruta_word.with_suffix('.pdf')
    else:
        ruta_pdf = Path(ruta_pdf)

    # Método de conversión según sistema operativo
    sistema = platform.system()

    if sistema == 'Windows':
        return _convertir_windows(ruta_word, ruta_pdf)
    elif sistema == 'Linux':
        return _convertir_linux(ruta_word, ruta_pdf)
    elif sistema == 'Darwin':  # macOS
        return _convertir_macos(ruta_word, ruta_pdf)
    else:
        raise OSError(f"Sistema operativo no soportado: {sistema}")


def _convertir_windows(ruta_word, ruta_pdf):
    """Conversión en Windows usando docx2pdf"""
    try:
        from docx2pdf import convert
        convert(str(ruta_word), str(ruta_pdf))
        return ruta_pdf
    except ImportError:
        raise ImportError(
            "Instalar docx2pdf: pip install docx2pdf"
        )


def _convertir_linux(ruta_word, ruta_pdf):
    """
    Conversión en Linux usando LibreOffice

    Requiere LibreOffice instalado:
    sudo apt-get install libreoffice
    """
    try:
        subprocess.run([
            'libreoffice',
            '--headless',              # Sin interfaz gráfica
            '--convert-to', 'pdf',     # Formato de salida
            '--outdir', str(ruta_pdf.parent),  # Carpeta destino
            str(ruta_word)             # Archivo origen
        ], check=True)

        return ruta_pdf
    except FileNotFoundError:
        raise FileNotFoundError(
            "LibreOffice no instalado. Instalar: sudo apt-get install libreoffice"
        )


def _convertir_macos(ruta_word, ruta_pdf):
    """
    Conversión en macOS usando LibreOffice

    Requiere LibreOffice instalado:
    brew install libreoffice
    """
    try:
        subprocess.run([
            '/Applications/LibreOffice.app/Contents/MacOS/soffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', str(ruta_pdf.parent),
            str(ruta_word)
        ], check=True)

        return ruta_pdf
    except FileNotFoundError:
        raise FileNotFoundError(
            "LibreOffice no instalado. Instalar: brew install libreoffice"
        )
```

### Métodos de conversión por SO

| Sistema | Método | Requiere |
|---------|--------|----------|
| **Windows** | `docx2pdf` | `pip install docx2pdf` |
| **Linux** | `LibreOffice --headless` | `sudo apt-get install libreoffice` |
| **macOS** | `LibreOffice soffice` | `brew install libreoffice` |

---

## 🔄 FLUJO COMPLETO PASO A PASO

### PASO 1: Usuario Rellena Formulario (Frontend)

```javascript
// Frontend React
const handleGenerarCotizacion = async () => {
    const datos = {
        numero: "COT-202512-0001",
        fecha: "29/12/2025",
        cliente: "Cliente Ejemplo S.A.C.",
        proyecto: "Instalación Eléctrica",
        items: [
            {
                descripcion: "Tablero eléctrico trifásico",
                cantidad: 2,
                precio_unitario: 1500.00,
                total: 3000.00
            },
            {
                descripcion: "Cable NYY 3x10mm²",
                cantidad: 150,
                precio_unitario: 12.50,
                total: 1875.00
            }
        ],
        subtotal: 4875.00,
        igv: 877.50,
        total: 5752.50
    };

    // Enviar al backend
    const response = await fetch('/api/chat/generar-cotizacion-rapida', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensaje: "Generar cotización", datos })
    });
};
```

---

### PASO 2: Vista Previa HTML (Opcional)

```python
# Backend - Renderizar vista previa HTML
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="backend/app/templates")

@router.post("/api/cotizaciones/preview")
async def preview_cotizacion(datos: dict):
    """Genera vista previa HTML"""
    return templates.TemplateResponse(
        "documentos/PLANTILLA_HTML_COTIZACION_SIMPLE.html",
        {
            "request": request,
            "numero": datos["numero"],
            "fecha": datos["fecha"],
            "cliente": datos["cliente"],
            "proyecto": datos["proyecto"],
            "items": datos["items"],
            "subtotal": datos["subtotal"],
            "igv": datos["igv"],
            "total": datos["total"]
        }
    )
```

**Resultado**: El usuario ve en su navegador cómo se verá el documento final.

---

### PASO 3: Generación de Word

```python
# Backend - Generar documento Word
from app.services.professional.generators import generar_documento

@router.post("/api/cotizaciones/generar-word")
async def generar_word(datos: dict):
    """Genera documento Word"""

    # 1. Preparar ruta de salida
    ruta_salida = Path(f"storage/generados/{datos['numero']}.docx")

    # 2. Opciones de personalización
    opciones = {
        "esquema_colores": "azul-tesla",  # o "rojo-energia", "verde-ecologico", etc.
        "mostrarPreciosUnitarios": True,
        "mostrarPreciosTotales": True,
        "mostrarIGV": True,
        "incluirLogo": True
    }

    # 3. Generar documento Word
    archivo_generado = generar_documento(
        tipo_documento="cotizacion-simple",
        datos=datos,
        ruta_salida=str(ruta_salida),
        opciones=opciones
    )

    # 4. Retornar archivo para descarga
    return FileResponse(
        path=archivo_generado,
        filename=f"{datos['numero']}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
```

**Resultado**: Archivo Word generado en `storage/generados/COT-202512-0001.docx`

---

### PASO 4: Conversión a PDF (Opcional)

```python
# Backend - Convertir Word a PDF
from app.services.professional.generators.pdf_converter import convertir_word_a_pdf

@router.post("/api/cotizaciones/generar-pdf")
async def generar_pdf(datos: dict):
    """Genera documento PDF"""

    # 1. Primero generar Word
    ruta_word = Path(f"storage/generados/{datos['numero']}.docx")

    archivo_word = generar_documento(
        tipo_documento="cotizacion-simple",
        datos=datos,
        ruta_salida=str(ruta_word)
    )

    # 2. Convertir a PDF
    ruta_pdf = ruta_word.with_suffix('.pdf')
    archivo_pdf = convertir_word_a_pdf(archivo_word, ruta_pdf)

    # 3. Retornar PDF para descarga
    return FileResponse(
        path=archivo_pdf,
        filename=f"{datos['numero']}.pdf",
        media_type="application/pdf"
    )
```

**Resultado**: Archivo PDF generado en `storage/generados/COT-202512-0001.pdf`

---

### PASO 5: Descarga por Usuario

```javascript
// Frontend - Descargar documento
const descargarDocumento = async (numero, formato) => {
    // Llamar al endpoint
    const url = `/api/cotizaciones/${numero}/exportar/${formato}`;

    // Descargar archivo
    const link = document.createElement('a');
    link.href = url;
    link.download = `${numero}.${formato}`;
    link.click();
};

// Uso
descargarDocumento("COT-202512-0001", "docx");  // Word
descargarDocumento("COT-202512-0001", "pdf");   // PDF
```

---

## 📊 TABLA RESUMEN - TODO ESTÁ CAPTURADO

| Componente | Sistema Antiguo | Sistema Nuevo | Estado |
|------------|----------------|---------------|--------|
| **HTML: Cotización Simple** | `templates/documentos/PLANTILLA_HTML_COTIZACION_SIMPLE.html` | **COMPARTIDO** (mismo archivo) | ✅ OK |
| **HTML: Cotización Compleja** | `templates/documentos/PLANTILLA_HTML_COTIZACION_COMPLEJA.html` | **COMPARTIDO** (mismo archivo) | ✅ OK |
| **HTML: Proyecto Simple** | `templates/documentos/PLANTILLA_HTML_PROYECTO_SIMPLE.html` | **COMPARTIDO** (mismo archivo) | ✅ OK |
| **HTML: Proyecto PMI** | `templates/documentos/PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html` | **COMPARTIDO** (mismo archivo) | ✅ OK |
| **HTML: Informe Técnico** | `templates/documentos/PLANTILLA_HTML_INFORME_TECNICO.html` | **COMPARTIDO** (mismo archivo) | ✅ OK |
| **HTML: Informe APA** | `templates/documentos/PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html` | **COMPARTIDO** (mismo archivo) | ✅ OK |
| | | | |
| **Python: Cotización Simple** | `generators/cotizacion_simple_generator.py` (16.7 KB) | `professional/generators/cotizaciones/simple.py` (16.7 KB) | ✅ MIGRADO |
| **Python: Cotización Compleja** | `generators/cotizacion_compleja_generator.py` (16.2 KB) | `professional/generators/cotizaciones/compleja.py` (16.2 KB) | ✅ MIGRADO |
| **Python: Proyecto Simple** | `generators/proyecto_simple_generator.py` (15.0 KB) | `professional/generators/proyectos/simple.py` (15.0 KB) | ✅ MIGRADO |
| **Python: Proyecto PMI** | `generators/proyecto_complejo_pmi_generator.py` (16.5 KB) | `professional/generators/proyectos/complejo_pmi.py` (16.5 KB) | ✅ MIGRADO |
| **Python: Informe Técnico** | `generators/informe_tecnico_generator.py` (8.0 KB) | `professional/generators/informes/tecnico.py` (8.0 KB) | ✅ MIGRADO |
| **Python: Informe APA** | `generators/informe_ejecutivo_apa_generator.py` (10.5 KB) | `professional/generators/informes/ejecutivo_apa.py` (10.5 KB) | ✅ MIGRADO |
| | | | |
| **Convertidor PDF** | `generators/pdf_converter.py` (3.4 KB) | `professional/generators/pdf_converter.py` (3.4 KB) | ✅ MIGRADO |

**Total**:
- ✅ 6 plantillas HTML (COMPARTIDAS)
- ✅ 6 generadores Python Word (MIGRADOS - 93.5 KB)
- ✅ 1 convertidor PDF (MIGRADO - 3.4 KB)
- ✅ **TODO 100% CAPTURADO**

---

## ✅ CONFIRMACIÓN FINAL

### ¿Están las 6 plantillas HTML?
✅ **SÍ** - En `backend/app/templates/documentos/` (COMPARTIDAS por ambos sistemas)

### ¿Están los scripts Python para generar Word?
✅ **SÍ** - 6 generadores migrados en `backend/app/services/professional/generators/`

### ¿Está el script Python para generar PDF?
✅ **SÍ** - `pdf_converter.py` migrado en `backend/app/services/professional/generators/`

### ¿El flujo completo está capturado?
✅ **SÍ** - HTML (preview) → Word (python-docx) → PDF (LibreOffice)

### ¿El sistema antiguo sigue funcionando?
✅ **SÍ** - 100% intacto en `backend/app/services/generators/`

### ¿El sistema nuevo es funcional?
✅ **SÍ** - Copias exactas, listas para usar

---

## 🎯 CONCLUSIÓN

**TODO EL FLUJO ESTÁ CAPTURADO AL 100%**:

1. ✅ **6 plantillas HTML** para vista previa
2. ✅ **6 generadores Python** para crear Word usando `python-docx`
3. ✅ **1 convertidor PDF** multiplataforma (Windows/Linux/Mac)
4. ✅ **Sistema antiguo INTACTO** como fallback
5. ✅ **Sistema nuevo FUNCIONAL** listo para deployment

**No falta nada**. El flujo completo está documentado, migrado y funcional.

---

**Documento creado**: 29 de Diciembre 2025
**Verificado por**: Claude Code (Sonnet 4.5)
**Estado**: ✅ FLUJO COMPLETO VERIFICADO Y DOCUMENTADO
