# Matriz de Correspondencia: Prototipos Visuales vs. Lógica Python

Este documento certifica la vinculación técnica entre los **6 Prototipos Visuales (HTML)** y el **Motor de Generación (Python)**.

## La Estrategia de Eficiencia
En lugar de tener 6 scripts de Python separados (difíciles de mantener), utilizamos un **Único Motor Polimórfico** (`word_generator.py`) que adapta su comportamiento según los datos recibidos.

---

## Tabla de Mapeo

| # | Prototipo Visual (Lo que ve el Usuario) | Archivo HTML (Diseño) | Función Python Responsable (Lógica) |
| :--- | :--- | :--- | :--- |
| **1** | **Cotización Simple** | `COTIZACION_SIMPLE_PROTOTYPE.html` | `_generar_cotizacion_pili(..., modo="simple")` |
| **2** | **Cotización Industrial** | `COTIZACION_COMPLEJA_PROTOTYPE.html` | `_generar_cotizacion_pili(..., modo="complejo")` |
| **3** | **Proyecto Básico** | `PROYECTO_SIMPLE_PROTOTYPE.html` | `_generar_proyecto_pili(..., tipo="estandar")` |
| **4** | **Proyecto Gantt (Master)** | `PROYECTO_COMPLEJO_PROTOTYPE.html` | `_generar_proyecto_pili(..., tipo="master")` |
| **5** | **Informe Técnico** | `INFORME_SIMPLE_PROTOTYPE.html` | `_generar_informe_pili(..., estilo="tecnico")` |
| **6** | **Informe Ejecutivo** | `INFORME_EJECUTIVO_PROTOTYPE.html` | `_generar_informe_pili(..., estilo="ejecutivo")` |

---

## ¿Cómo funciona la conexión?

1.  **Frontend (React):** Muestra el HTML (`COTIZACION_SIMPLE_PROTOTYPE.html`) para que el usuario edite visualmente.
2.  **Envío de Datos:** Al guardar, envía un JSON con una etiqueta: `{"tipo_documento": "cotizacion_simple", ...}`.
3.  **Backend (Python):**
    *   El archivo `pili_orchestrator.py` recibe la etiqueta.
    *   Llama a `word_generator.py`.
    *   El generador activa las reglas específicas (ej. "Si es simple, no poner desglose de IGV", "Si es complejo, insertar tabla de fases").

## Conclusión
Existe una **correspondencia 1 a 1** entre el diseño y la lógica, pero implementada de manera inteligente en un solo archivo robusto (`word_generator.py`) para facilitar el mantenimiento futuro.
