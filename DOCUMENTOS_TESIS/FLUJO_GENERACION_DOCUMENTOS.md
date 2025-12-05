# 🔄 FLUJO DE GENERACIÓN DE DOCUMENTOS (PIPELINE)

**Fecha**: 04 de Diciembre, 2025
**Estado**: Implementado y Verificado

Este documento describe el flujo técnico exacto desde que el usuario ve la vista previa hasta que descarga el archivo final.

---

## 1. 🖥️ VISTA PREVIA (Frontend)
**Tecnología**: React + HTML/CSS Dinámico
1.  El usuario interactúa con PILI y refina los datos.
2.  El sistema genera un **HTML Editable** en tiempo real.
3.  El usuario ve exactamente cómo quedará la tabla de items, precios y totales.
4.  **Acción**: Usuario presiona "Generar Documento".

## 2. 📦 EMPAQUETADO DE DATOS (Frontend -> Backend)
**Formato**: JSON Estructurado
El frontend no envía el archivo Word; envía los **datos puros** y la estructura visual.
*   **Payload JSON**:
    ```json
    {
      "cliente": "Juan Pérez",
      "items": [...],
      "html_preview": "<div>...</div>",
      "configuracion": { "igv": true, "moneda": "PEN" }
    }
    ```
*   **Destino**: `POST /api/cotizaciones/` (Guardar) o `/api/generar-directo` (Rápido).

## 3. 💾 ALMACENAMIENTO (Backend Storage)
**Estrategia**: Persistencia Híbrida

### A. Base de Datos Relacional (SQL)
*   **Función**: Registro Oficial.
*   **Acción**: Se guarda la cotización en `PostgreSQL/SQLite` para historial, contabilidad y seguimiento.
*   **ID**: Se genera un código único (ej: `COT-202512-001`).

### B. Base de Datos Vectorial (RAG)
*   **Función**: Conocimiento a Largo Plazo.
*   **Acción**: *Documentos subidos* y *Proyectos finalizados* se indexan en la Vector DB (vía `rag_service`) para que PILI pueda "recordarlos" en el futuro.
    *   *Nota*: La generación instantánea de cotizaciones usa principalmente la SQL para velocidad, mientras que la Vector DB se alimenta en segundo plano.

## 4. 👐 EJECUCIÓN PARALELA (The Hands)
Aquí ocurre la magia de la "Generación en Milisegundos". A diferencia de un flujo serial (Word -> PDF), el sistema usa **Generación Paralela** para máxima calidad en ambos formatos.

### Camino A: Generación Word (`python-docx`)
*   **Fuente**: JSON de datos.
*   **Proceso**: Inyecta datos en una plantilla `.docx` optimizada.
*   **Resultado**: Documento 100% editable, perfecto para que el cliente haga ajustes finales.

### Camino B: Generación PDF (`reportlab`)
*   **Fuente**: JSON de datos (El mismo origen, garantizando consistencia).
*   **Proceso**: Dibuja vectorialmente el documento. No es una "impresión" del Word, es un **dibujo digital original**.
*   **Ventaja**: Calidad tipográfica superior y menor peso de archivo que una conversión Word->PDF.

---

## 5. 📤 ENTREGA (Download)
1.  El backend devuelve el `FileResponse` (stream de bytes).
2.  El navegador del usuario descarga el archivo con el nombre correcto (ej: `COT-JuanPerez.pdf`).
3.  **Tiempo Total**: < 2 segundos.

---

## 📝 RESUMEN PARA TESIS

El sistema utiliza un patrón de **"Single Source of Truth" (SSOT)**. El JSON es la verdad absoluta. De esa única fuente, las "Manos" de Python construyen simultáneamente el Word y el PDF, asegurando que ambos sean idénticos en contenido pero optimizados para su formato específico.
