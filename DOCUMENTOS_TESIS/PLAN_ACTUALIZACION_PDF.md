# Plan de Actualización: Paridad Total Word-PDF

## Problema Detectado
El usuario identificó correctamente que `pdf_generator.py` (364 líneas) es una versión simplificada comparada con `word_generator.py` (943 líneas). Actualmente, los métodos de "Proyecto" e "Informe" son simples alias de "Cotización", lo que impide generar los 6 tipos de documentos prometidos con su diseño específico.

## Objetivo
Llevar `pdf_generator.py` a **Paridad Funcional Total** con `word_generator.py`, implementando la lógica específica para cada tipo de documento bajo el estándar "Twin Design" (Diseño Gemelo HTML).

## Cambios Propuestos en `pdf_generator.py`

### 1. Implementar Despachador Polimórfico
Añadir el método `generar_desde_json_pili` que actúe como cerebro central, igual que en el generador de Word, para decidir qué función específica llamar según el `tipo_documento`.

### 2. Implementar `_generar_proyecto_pili`
Crear un método dedicado para Proyectos que incluya:
*   **Header Específico:** "GESTIÓN DE PROYECTO" (Dorado).
*   **Tabla de Fases:** Replicar la tabla de fases/hitos del HTML.
*   **Información de Proyecto:** Cliente, Duración, Estado.
*   **Estilo:** Uso de colores Tesla Blue para headers de tablas y Dorado para totales/hitos clave.

### 3. Implementar `_generar_informe_pili`
Crear un método dedicado para Informes que incluya:
*   **Header Específico:** "INFORME TÉCNICO" o "EJECUTIVO".
*   **Secciones Dinámicas:** Resumen Ejecutivo, Conclusiones, Recomendaciones.
*   **Estilo:** Formato de texto justificado y limpio, con encabezados claros en Azul Tesla.

### 4. Refactorización de Estilos
Asegurar que todos los nuevos métodos utilicen las constantes de color `COLOR_TESLA_BLUE` (#1a3c6e) y `COLOR_DORADO` definidos previamente.

## Verificación
Una vez aplicado, `pdf_generator.py` debería crecer en tamaño y complejidad, reflejando la lógica necesaria para manejar los 6 casos de uso (Simple/Complejo para cada una de las 3 categorías).
