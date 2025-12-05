# Estrategia de Marca y Adaptabilidad Documental

Este documento responde a las necesidades críticas de personalización (Logo/Colores) y manejo de contenido variable (Paginación Automática) en el sistema TESLA COTIZADOR V3.0.

## 1. Estrategia de Marca Dinámica (Logo y Colores)

El sistema no debe estar "quemado" (hardcoded) con un solo color. La arquitectura permite inyectar la identidad visual en tiempo de ejecución.

### A. Ubicación del Logo
Recomendamos una estructura de **Encabezado Flexible**:
*   **Opción A (Estándar):** Logo de la Empresa a la Izquierda | Datos del Documento a la Derecha.
*   **Opción B (Co-Branding):** Logo Empresa (Izq) | Logo Cliente (Der) - Ideal para proyectos grandes.
*   **Implementación Técnica:**
    El generador recibe la ruta del logo en el JSON:
    ```json
    "branding": {
        "logo_path": "assets/logos/tesla_v3.png",
        "logo_position": "left",
        "logo_width_mm": 40
    }
    ```

### B. Paleta de Colores (Tesla Red vs Blue)
El usuario puede elegir el "Tema" del documento antes de generar.
*   **Tema Corporativo (Azul Tesla):** Seriedad, Ingeniería, Contratos.
*   **Tema Urgente/Oferta (Rojo Tesla):** Cotizaciones rápidas, descuentos, alertas.
*   **Implementación Técnica:**
    Definimos un diccionario de temas en Python:
    ```python
    THEMES = {
        "tesla_blue": {"primary": RGBColor(26, 60, 110), "accent": RGBColor(49, 130, 206)},
        "tesla_red":  {"primary": RGBColor(229, 62, 62),  "accent": RGBColor(252, 129, 129)}
    }
    ```
    El generador usa `THEMES[user_choice]` para pintar bordes y textos.

---

## 2. Adaptabilidad y Auto-Ajuste (El "Flow" del Documento)

Esta es la ventaja crítica sobre los PDFs estáticos.

### A. Crecimiento Vertical (Paginación)
*   **Problema:** Una cotización puede tener 5 ítems (1 página) o 500 ítems (20 páginas).
*   **Solución Nativa:** `python-docx` maneja el "flujo" de texto automáticamente.
    *   Si una tabla crece, Word crea una nueva página automáticamente.
    *   Los encabezados de tabla se repiten automáticamente en la nueva página (`table.rows[0].table_header = True`).
    *   El pie de página (Página X de Y) se actualiza solo.

### B. Imágenes y Gráficos Variables
*   **Escenario:** Un informe técnico puede incluir 1 foto o 50 fotos de evidencia.
*   **Lógica de Ajuste:**
    *   El script calcula el espacio restante en la página.
    *   Si la imagen no cabe, inserta un salto de página (`document.add_page_break()`) antes de la imagen para evitar que quede cortada.
    *   Las imágenes se redimensionan proporcionalmente para no romper los márgenes (`width=Inches(6)`).

---

## 3. Opinión Crítica del Especialista

**Veredicto:** Su enfoque es **CORRECTO y NECESARIO**.

1.  **Profesionalismo:** Un documento que se "rompe" o corta imágenes se ve amateur. La generación nativa en Word evita esto.
2.  **Flexibilidad de Marca:** Permitir cambiar entre Azul/Rojo o cambiar el logo sin tocar código es vital para que el software sea vendible a otras empresas (SaaS) o adaptable a diferentes unidades de negocio de Tesla.
3.  **Escalabilidad:** Un proyecto "muy amplio" (como menciona) con cientos de hojas es inmanejable si se trata de "dibujar" pixel por pixel. Al usar el motor de renderizado de Word, delegamos la complejidad de la paginación al software más experto del mundo en eso (Microsoft Word).

**Conclusión:** La arquitectura propuesta soporta nativamente tanto la personalización estética como la escalabilidad de contenido masivo.
