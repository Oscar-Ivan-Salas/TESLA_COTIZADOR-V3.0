# Índice Maestro: Documentación Técnica para Tesis
## Sistema TESLA COTIZADOR V3.0 - Módulo de Generación Documental

Este índice organiza todos los artefactos generados durante el análisis y diseño del sistema, estructurados lógicamente para su incorporación directa en la tesis.

---

### 📂 CAPÍTULO 1: ARQUITECTURA DEL SISTEMA
*Fundamentación técnica y diseño de alto nivel.*

1.  **[Visión Global del Sistema](./VISION_GLOBAL_SISTEMA.md)**
    *   *Radiografía:* Análisis de carpetas, los 10 servicios nucleares y los 6 tipos de documentos.
2.  **[Arquitectura "Cerebro vs Manos"](./ARQUITECTURA_CEREBRO_MANOS.md)**
    *   *Concepto:* Desacople total entre la lógica de negocio (PILI) y la generación de archivos (Python).
2.  **[Flujo de Generación Híbrido](./FLUJO_GENERACION_DOCUMENTOS.md)**
    *   *Proceso:* Diagrama del flujo de datos desde el Frontend -> JSON -> Backend -> Archivo Final.
3.  **[Crítica Arquitectónica](./CRITICA_ARQUITECTURA_SISTEMA.md)**
    *   *Validación:* Análisis de robustez y escalabilidad del diseño actual.
4.  **[Matriz de Correspondencia (HTML vs Python)](./MATRIZ_CORRESPONDENCIA.md)**
    *   *Vinculación:* Tabla que conecta cada prototipo visual con su función lógica específica.

---

### 📂 CAPÍTULO 2: INTELIGENCIA ARTIFICIAL (AGENTE PILI)
*Capacidades lógicas y servicios especializados.*

4.  **[Capacidades Offline de PILI](./CAPACIDADES_PILI_OFFLINE.md)**
    *   *Detalle:* Documentación de los 10 servicios y la lógica de los 3 agentes (Cotizador, PM, Reportero).
5.  **[Casos de Uso y Estructura Documental](./CASOS_USO_ESTRUCTURA_DOCUMENTOS.md)**
    *   *Definición:* Desglose de los tipos de documentos (Simples vs Complejos).

---

### 📂 CAPÍTULO 3: DISEÑO VISUAL Y EXPERIENCIA DE USUARIO
*Validación estética y prototipos de alta fidelidad.*

6.  **[Plan de Visualización](./PLAN_VISUALIZACION_DOCUMENTAL.md)**
    *   *Estrategia:* Definición de estilos "Premium & Serio".
7.  **Prototipos Visuales (Evidencia):**
    *   [Cotización Industrial](./COTIZACION_COMPLEJA_PROTOTYPE.html)
    *   [Proyecto Gantt](./PROYECTO_COMPLEJO_PROTOTYPE.html)
    *   [Informe Ejecutivo](./INFORME_EJECUTIVO_PROTOTYPE.html)
8.  **[Reporte de Verificación Visual](./REPORTE_VERIFICACION_VISUAL.md)**
    *   *Conclusión:* Validación de la estética mediante grabación de pantalla.

---

### 📂 CAPÍTULO 4: FACTIBILIDAD TÉCNICA Y VENTAJA COMPETITIVA
*Justificación de la tecnología elegida.*

9.  **[Ventaja Competitiva (Generación Nativa)](./VENTAJA_COMPETITIVA_DOCS.md)**
    *   *El Plus:* Por qué generar Word editable es superior a PDF estático.
10. **[Mapeo Técnico (CSS a Word)](./MAPEO_ESTILOS_WORD.md)**
    *   *Implementación:* Guía técnica de cómo traducir estilos web a objetos Python.
11. **[Estrategia de Marca y Adaptabilidad](./ESTRATEGIA_MARCA_Y_ADAPTABILIDAD.md)**
    *   *Escalabilidad:* Solución para logos dinámicos, temas de color y paginación automática.

### 📂 CAPÍTULO 5: VALIDACIÓN Y CONCLUSIONES FINALES
*Cierre técnico y defensa de la tesis.*

12. **[Conclusión Técnica Crítica](./CONCLUSION_TECNICA_CRITICA.md)**
    *   *Defensa:* Análisis "no complaciente" y validación del potencial gráfico con Python.
13. **[Validación Arquitectura Dual](./VALIDACION_ARQUITECTURA_DUAL.md)**
    *   *Escalabilidad:* Confirmación del modelo "Cerebro Híbrido + Manos Únicas".

---

### 📂 ANEXOS TÉCNICOS
14. **[Reporte de Cobertura de Generadores](./REPORTE_COBERTURA_GENERADORES.md)**
15. **[Estrategia de Plantillas Profesionales](./ESTRATEGIA_PLANTILLAS_PROFESIONALES.md)**
16. **[Anexo: Código Fuente del Sistema](./ANEXO_CODIGO_FUENTE.md)**
    *   *Evidencia:* Scripts Python originales (`word_generator.py`, `pili_orchestrator.py`, etc.).
17. **[Auditoría de Capacidad de Generadores](./AUDITORIA_CAPACIDAD_GENERADORES.md)**
    *   *Verificación:* Análisis detallado de cómo Python replica los 6 prototipos HTML.
18. **[Recomendación de Estrategia PDF](./RECOMENDACION_ESTRATEGIA_PDF.md)**
    *   *Veredicto:* Por qué la generación nativa es superior a la conversión Word-PDF para este caso.
19. **[Plan de Limpieza y Consolidación](./PLAN_LIMPIEZA_CONSOLIDACION.md)**
    *   *Estrategia:* Pasos finales para organizar la entrega de tesis y limpiar el entorno.
