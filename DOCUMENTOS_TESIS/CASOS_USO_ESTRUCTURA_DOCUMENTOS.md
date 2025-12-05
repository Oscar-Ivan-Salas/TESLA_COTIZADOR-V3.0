# 📑 CASOS DE USO Y ESTRUCTURA DE DOCUMENTOS

**Fecha**: 04 de Diciembre, 2025
**Sistema**: TESLA COTIZADOR V3.0

Este documento detalla **cuándo** se generan documentos (Casos de Uso) y **cómo** están compuestos internamente (Estructura).

---

## 1. 🎯 CASOS DE USO (Use Cases)

El sistema genera documentos en tres escenarios principales, cada uno con un propósito y nivel de complejidad diferente.

### A. Cotización Comercial (Sales Quote)
*   **Actor**: PILI Cotizadora.
*   **Disparador**: El usuario finaliza el flujo de cotización rápida (residencial/comercial).
*   **Objetivo**: Presentar una oferta económica clara y profesional para cerrar una venta.
*   **Formatos**: PDF (para enviar) y Word (para editar).
*   **Contenido Clave**:
    *   Datos del cliente.
    *   Tabla de items con precios unitarios y totales.
    *   Condiciones comerciales (vigencia, forma de pago).

### B. Informe Ejecutivo de Proyecto (Project Executive Report)
*   **Actor**: PILI Project Manager / PILI Analista Senior.
*   **Disparador**: El usuario solicita un reporte de estado de un proyecto en curso.
*   **Objetivo**: Informar a la gerencia o al cliente sobre el avance, finanzas y riesgos.
*   **Característica Única**: **Análisis Inteligente (IA)**. El sistema usa Gemini para analizar los datos del proyecto y redactar automáticamente:
    *   Resumen Ejecutivo.
    *   Conclusiones.
    *   Recomendaciones estratégicas.
*   **Contenido Clave**:
    *   Estado del proyecto (Semáforo).
    *   Métricas financieras (Total cotizado vs Aprobado).
    *   Listado de documentos asociados.

### C. Informe Técnico / Simple (Technical Report)
*   **Actor**: PILI Reportera.
*   **Disparador**: Necesidad de un reporte rápido o específico (ej: visita técnica).
*   **Objetivo**: Documentar hallazgos técnicos o situaciones puntuales.
*   **Contenido Clave**:
    *   Descripción del problema/hallazgo.
    *   Fotos (si aplica).
    *   Recomendaciones técnicas.

---

## 2. 🏗️ ESTRUCTURA DEL DOCUMENTO (Composition)

Todos los documentos siguen una estructura "Elite" estandarizada para mantener la identidad corporativa de Tesla Electricidad.

### 🧩 Anatomía de una Página

| Sección | Componente | Descripción |
| :--- | :--- | :--- |
| **HEADER** | **Logo Dinámico** | Logo de Tesla o personalizado del cliente (inyectado vía Base64). |
| | **Marca de Agua PILI** | Texto discreto: *"Generado por [Nombre Agente]"* (ej: PILI Cotizadora). |
| **BODY** | **Título** | Tipografía corporativa, color Rojo Tesla (`#8B0000`) o Dorado (`#DAA520`). |
| | **Datos Cliente** | Tabla sin bordes con información clave. |
| | **Tabla Principal** | **Estilo Elite**: Cabecera con fondo Dorado PILI (`#D4AF37`), texto blanco, alineación precisa. |
| | **Totales** | Sección destacada al final de la tabla (Subtotal, IGV, Total). |
| | **Contenido IA** | Párrafos de texto generados por Gemini (en informes). |
| **FOOTER** | **Firma Digital** | *"✨ Documento generado por IA - Tesla V3.0"*. |
| | **Legal** | Dirección, RUC y datos de contacto de la empresa en gris suave. |
| | **Paginación** | "Página X de Y". |

### 🎨 Identidad Visual (Estilos)

El sistema no usa estilos por defecto de Word/PDF. Define sus propios estilos:

*   **Colores**:
    *   🔴 **Rojo Tesla**: `#8B0000` (Títulos principales).
    *   🟡 **Dorado PILI**: `#D4AF37` (Cabeceras de tabla, destacados).
    *   🔵 **Azul Tech**: `#0066CC` (Enlaces, elementos digitales).
*   **Tipografía**: Helvetica-Bold para títulos, Arial/Helvetica para cuerpo.

---

## 3. 🤖 INTEGRACIÓN INTELIGENTE (The "Smart" Layer)

La generación no es estática. El componente `TemplateProcessor` y los generadores inyectan inteligencia:

1.  **Inyección de Tablas Reales**: El marcador `{{items_tabla}}` no pone texto, construye una tabla nativa de Word con filas dinámicas.
2.  **Decodificación de Imágenes**: El marcador `{{logo}}` recibe un string Base64, lo decodifica a imagen temporal y lo inserta con dimensiones exactas.
3.  **Contexto de Agente**: El documento "sabe" quién lo creó. Si lo hizo "PILI Analista", el tono y la firma del documento reflejan esa personalidad técnica.
