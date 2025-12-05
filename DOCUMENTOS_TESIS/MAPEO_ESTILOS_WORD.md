# Mapeo Técnico: De HTML/CSS a Word Nativo (.docx)

Este documento demuestra técnicamente cómo los diseños "Premium" visualizados en HTML se traducen a documentos Word nativos y editables usando Python (`python-docx`).

**Veredicto de Factibilidad:** ✅ **TOTALMENTE POSIBLE**
**Ventaja Competitiva:** A diferencia de otros sistemas que solo "imprimen" HTML a PDF (estático), nosotros generamos archivos `.docx` reales donde el usuario puede editar textos, cambiar cifras y ajustar formatos.

---

## 1. Estrategia de "Diseño Gemelo" (Twin Design)

No convertimos el HTML. Reconstruimos el documento en Word usando las mismas reglas de estilo.

| Elemento Visual | En HTML/CSS (Prototipo) | En Python (`python-docx`) |
| :--- | :--- | :--- |
| **Colores** | `color: #1a3c6e;` (Tesla Blue) | `run.font.color.rgb = RGBColor(26, 60, 110)` |
| **Tablas** | `<table>...</table>` | `table = document.add_table(...)` |
| **Grillas** | `display: grid;` | Tablas invisibles (bordes ocultos) para layout |
| **Alertas** | `.status-danger { color: red; }` | `run.font.color.rgb = RGBColor(255, 0, 0)` |
| **Fuentes** | `font-family: 'Roboto';` | `style.font.name = 'Roboto'` |

---

## 2. Mapeo Detallado por Agente

### 🤖 Agente 1: Cotizador (Tablas Financieras)

**Reto:** Tablas con bordes específicos y alineación decimal.

*   **HTML:**
    ```html
    <td class="text-right">S/ 1,121.00</td>
    ```
*   **Python (`word_generator.py`):**
    ```python
    cell = table.cell(row, 4)
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("S/ 1,121.00")
    run.font.bold = True  # Para totales
    ```

### 🤖 Agente 2: Project Manager (Gantt y Cronogramas)

**Reto:** Barras de progreso visuales (Gantt).
*Solución:* En Word, usamos celdas de tabla con sombreado de fondo (Shading) para simular las barras.

*   **HTML:**
    ```html
    <div class="gantt-bar bar-blue"></div>
    ```
*   **Python (`word_generator.py`):**
    ```python
    # Simulación de Gantt en Word
    cell = gantt_table.cell(task_row, week_col)
    shading_elm = parse_xml(r'<w:shd {} w:fill="1A3C6E"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shading_elm)
    ```

### 🤖 Agente 3: Reportero (Layout Ejecutivo)

**Reto:** Encabezados con fondo de color y texto blanco (Cover Header).

*   **HTML:**
    ```css
    .cover-header { background-color: #1a3c6e; color: white; }
    ```
*   **Python (`word_generator.py`):**
    ```python
    # Crear tabla de 1 celda que ocupe todo el ancho
    header_table = document.add_table(rows=1, cols=1)
    cell = header_table.cell(0, 0)
    # Aplicar fondo azul
    shading_elm = parse_xml(r'<w:shd {} w:fill="1A3C6E"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shading_elm)
    # Texto blanco
    run = cell.paragraphs[0].add_run("INFORME EJECUTIVO")
    run.font.color.rgb = RGBColor(255, 255, 255)
    ```

---

## 3. ¿Por qué Python es Superior?

1.  **Editabilidad Real:** El usuario recibe un `.docx` donde puede corregir un error ortográfico o cambiar un precio manualmente si lo necesita. Los convertidores HTML->PDF no permiten esto.
2.  **Calidad Vectorial:** Las tablas y fuentes son nativas, no "imágenes" pixeladas. Se imprimen con nitidez perfecta.
3.  **Peso del Archivo:** Un `.docx` generado así pesa KBs (muy ligero), mientras que los PDFs generados desde imágenes pesan MBs.

## 4. Conclusión

**SÍ, ES POSIBLE.**
Todo lo que diseñamos en los prototipos HTML (colores serios, layouts, tablas complejas) se puede replicar programáticamente en `word_generator.py`. Es un trabajo de "traducción" de CSS a objetos Python, pero el resultado es un documento profesional de clase mundial.
