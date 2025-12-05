# Visión Global del Sistema: TESLA COTIZADOR V3.0

Este documento proporciona una radiografía completa del producto, analizando su estructura de carpetas, sus 10 servicios nucleares y la arquitectura de sus 6 tipos de documentos.

## 1. Estructura del Proyecto (Radiografía)

El sistema sigue una arquitectura moderna de microservicios monolíticos (Modular Monolith) basada en FastAPI (Backend) y React (Frontend).

### 📂 Raíz (`e:\TESLA_COTIZADOR-V3.0`)
*   **`backend/`**: El núcleo lógico. Contiene toda la inteligencia (PILI) y los generadores.
*   **`frontend/`**: La interfaz de usuario (React + Vite).
*   **`database/`**: Almacenamiento persistente (SQLite/PostgreSQL).
*   **`storage/`**: Repositorio temporal de archivos generados.
*   **`DOCUMENTOS_TESIS/`**: **(Nuevo)** Carpeta consolidada con toda la documentación técnica y prototipos.

### 📂 Backend (`backend/app/services/`) - El Motor
Aquí residen los scripts que dan vida a la "Arquitectura Cerebro vs Manos":
1.  `pili_orchestrator.py`: El director de orquesta (Decide si usar IA o Lógica).
2.  `pili_brain.py`: El cerebro lógico offline.
3.  `word_generator.py`: Las manos que escriben DOCX.
4.  `pdf_generator.py`: Las manos que escriben PDF.
5.  `gemini_service.py`: Conexión con la IA avanzada.
6.  `file_processor.py`: Lector de planos y archivos técnicos.

---

## 2. Los 10 Servicios Nucleares de PILI
El sistema no es solo un "chat". Es una suite de 10 herramientas especializadas:

| # | Servicio | Descripción Técnica | Script Responsable |
| :--- | :--- | :--- | :--- |
| 1 | **Análisis de Planos** | OCR y extracción de metrados desde PDF/CAD. | `file_processor.py` |
| 2 | **Cotización Residencial** | Cálculo rápido de puntos de luz/tomacorrientes. | `pili_brain.py` (Modo Simple) |
| 3 | **Cotización Industrial** | Análisis complejo de cargas y tableros trifásicos. | `gemini_service.py` |
| 4 | **Gestión de Proyectos** | Creación de cronogramas y asignación de recursos. | `pili_orchestrator.py` |
| 5 | **Generación de Informes** | Redacción técnica de avances y conclusiones. | `word_generator.py` |
| 6 | **Auditoría de Costos** | Verificación de precios unitarios vs mercado. | `rag_service.py` |
| 7 | **Conversión de Formatos** | Transformación de datos a Word/PDF/Excel. | `pdf_generator.py` |
| 8 | **Chat Técnico** | Asistente consultivo sobre normativa CNE. | `gemini_service.py` |
| 9 | **Gestión de Plantillas** | Inyección de datos en formatos corporativos. | `template_processor.py` |
| 10 | **Orquestación Multi-Agente** | Coordinación entre el Cotizador, PM y Reportero. | `pili_orchestrator.py` |

---

## 3. Los 6 Documentos Maestros
El sistema genera 6 entregables distintos, cada uno con su propia lógica de negocio y presentación visual.

### 🤖 Agente 1: Cotizador
1.  **Cotización Simple:** Formato ágil para clientes residenciales. (1-2 páginas).
2.  **Cotización Compleja:** Formato detallado para industria. Incluye desglose de IGV, fases y condiciones técnicas. (5-10 páginas).

### 🤖 Agente 2: Project Manager
3.  **Plan de Proyecto Simple:** Lista de tareas y recursos básicos.
4.  **Plan Maestro (Gantt):** Cronograma detallado, matriz de riesgos y curva S.

### 🤖 Agente 3: Reportero
5.  **Informe Técnico:** Reporte de campo, hallazgos y fotos.
6.  **Informe Ejecutivo:** Dashboard gerencial con KPIs financieros y estado del portafolio.

---

## 4. Conclusión del Análisis
El sistema **TESLA COTIZADOR V3.0** es una plataforma madura. No es un prototipo.
Tiene una estructura de código profesional, separación de responsabilidades clara y una cobertura de servicios que abarca todo el ciclo de vida de un proyecto de ingeniería eléctrica, desde la cotización hasta el informe final.
