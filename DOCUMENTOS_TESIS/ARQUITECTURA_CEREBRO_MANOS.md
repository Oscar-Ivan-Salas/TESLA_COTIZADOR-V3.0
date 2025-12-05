# 🧠 ARQUITECTURA "CEREBRO Y MANOS" (BRAIN & HANDS)

**Fecha**: 04 de Diciembre, 2025
**Concepto**: Modelo de Ejecución de PILI
**Propósito**: Base para Tesis/Informe Técnico del Proyecto

Este documento formaliza la arquitectura conceptual de PILI, separando claramente la **Inteligencia (Cerebro)** de la **Ejecución (Manos)**. Esta distinción es clave para entender cómo el sistema logra generar documentos complejos en segundos.

---

## 1. 🧠 EL CEREBRO (The Brain)
**Componente**: `PILIBrain` (`backend/app/services/pili_brain.py`)

El "Cerebro" es el estratega. No toca los archivos, solo piensa, decide y estructura. Es responsable del **QUÉ** y el **POR QUÉ**.

### Funciones Cognitivas:
1.  **Comprensión del Lenguaje (NLU)**:
    *   Analiza el mensaje del usuario (ej: "Cotízame una casa de 200m2").
    *   Detecta la intención y extrae entidades (Área=200, Tipo=Residencial).
2.  **Toma de Decisiones (Lógica de Negocio)**:
    *   Selecciona el servicio correcto de los 10 disponibles (ej: `electrico-residencial`).
    *   Determina la complejidad (Simple vs Compleja).
3.  **Ingeniería Inversa (Cálculos)**:
    *   Aplica ratios de ingeniería (ej: 1 punto de luz cada 10m²).
    *   Calcula costos, márgenes e impuestos (IGV).
4.  **Orquestación**:
    *   Prepara el "paquete de datos" (JSON) perfecto para que las "Manos" trabajen.

---

## 2. 👐 LAS MANOS (The Hands)
**Componentes**: Generadores (`word_generator.py`, `pdf_generator.py`)

Las "Manos" son los ejecutores expertos. No cuestionan la lógica, solo construyen con precisión milimétrica. Son responsables del **CÓMO**.

### Mano Derecha: `python-docx` (Word)
Es el artesano de documentos editables.
*   **Tecnología**: Librería `python-docx` (Manipulación XML de Office).
*   **Habilidades**:
    *   Inyección de tablas dinámicas con estilos corporativos.
    *   Manejo de plantillas `.docx` pre-diseñadas.
    *   Control de márgenes, fuentes y colores (Branding Tesla).
    *   Inserción de imágenes (Logos) desde Base64.

### Mano Izquierda: `reportlab` (PDF)
Es el impresor de documentos seguros.
*   **Tecnología**: Librería `reportlab` (Generación PDF de bajo nivel).
*   **Habilidades**:
    *   Dibujo vectorial de elementos gráficos.
    *   Posicionamiento exacto (coordenadas X,Y) de cada letra.
    *   Generación de documentos inmutables (No editables).
    *   Optimización de peso de archivo para envío rápido.

---

## 3. ⚡ EL FLUJO DE TRABAJO (Workflow)

El proceso completo dura milisegundos y sigue este orden estricto:

1.  **Estímulo**: Usuario pide "Cotización para fábrica".
2.  **Procesamiento (Cerebro)**:
    *   `PILIBrain` detecta "Industrial".
    *   Calcula: Tableros trifásicos, cableado grueso.
    *   Salida: JSON estructurado con items y precios.
3.  **Orden Motora**: El Router envía el JSON al Generador.
4.  **Ejecución (Manos)**:
    *   `WordGenerator` recibe el JSON.
    *   Abre la plantilla "Industrial".
    *   "Escribe" los datos en las tablas.
    *   "Pinta" los encabezados de color Dorado.
5.  **Resultado**: Archivo `.docx` listo para descargar.

---

## 4. 🚀 VALOR PARA LA TESIS

Esta arquitectura demuestra un principio avanzado de diseño de software: **Separación de Responsabilidades (SoC)**.

*   Si cambiamos los precios (Lógica), solo tocamos el **Cerebro**.
*   Si cambiamos el logo o la fuente (Estética), solo tocamos las **Manos**.

Esto permite que PILI sea escalable, mantenible y extremadamente rápida, cumpliendo la promesa de "hacer en segundos lo que toma horas manualmente".
