# Plan de Visualización y Verificación Documental

Este plan detalla la estrategia para visualizar y validar los documentos generados por el sistema TESLA COTIZADOR V3.0 sin necesidad de examinar el código subyacente. Utilizaremos **Artefactos Visuales (HTML/CSS)** que simulan con alta fidelidad el resultado final (PDF/Word).

## 1. Estrategia de Simulación: "Los 3 Agentes"

Simularemos la ejecución de 3 agentes especializados, cada uno responsable de una categoría de documentos.

### 🤖 Agente 1: El Cotizador (Quotes)
*   **Responsabilidad:** Generar cotizaciones rápidas y precisas.
*   **Estilo Visual:** Limpio, comercial, enfocado en precios y totales claros.
*   **Tipos:**
    *   *Cotización Simple:* Residencial/Comercial pequeña.
    *   *Cotización Compleja:* Industrial/Licitaciones con desglose técnico.

### 🤖 Agente 2: El Project Manager (Projects)
*   **Responsabilidad:** Planificación y ejecución de obras.
*   **Estilo Visual:** Estructurado, técnico, con cronogramas y fases.
*   **Tipos:**
    *   *Proyecto Simple:* Cronograma básico y lista de materiales.
    *   *Proyecto Complejo:* Gantt detallado, hitos, gestión de riesgos.

### 🤖 Agente 3: El Reportero (Reports)
*   **Responsabilidad:** Auditoría, informes técnicos y ejecutivos.
*   **Estilo Visual:** Formal, denso en datos, gráficos y conclusiones.
*   **Tipos:**
    *   *Informe Técnico:* Resultados de pruebas, mediciones.
    *   *Informe Ejecutivo:* Resumen para gerencia, KPIs.

---

## 2. Estándares de Diseño "Premium & Serio"

Para cumplir con el requerimiento de "colores serios" y "diseño profesional", aplicaremos:

*   **Paleta de Colores:**
    *   *Principal:* Azul Tesla Profundo (`#1a3c6e`) - Confianza y Tecnología.
    *   *Secundario:* Gris Pizarra (`#4a5568`) - Seriedad y Texto.
    *   *Acento:* Rojo Tesla (`#e53e3e`) - Solo para alertas o puntos críticos (usado con moderación).
    *   *Fondo:* Blanco Puro y Gris Humo (`#f7fafc`) - Limpieza visual.
*   **Tipografía:** Fuentes Sans-serif modernas (Inter/Roboto) para legibilidad en pantalla e impresión.
*   **Layout:**
    *   Encabezados consistentes con Logo y Datos de Contacto.
    *   Tablas con "Zebra Striping" sutil para lectura de datos.
    *   Pies de página con numeración y disclaimer legal.

---

## 3. Los 20 Prompts de Prueba (Casos de Uso)

Diseñaremos 20 escenarios para estresar el sistema y verificar la adaptabilidad de los agentes.

### Grupo A: Cotizaciones (Agente Cotizador)
1.  **Residencial Básico:** "Cotizar instalación de 10 puntos de luz y 5 tomas en un depa de 80m2."
2.  **Comercial Medio:** "Necesito recablear una oficina de 200m2 con pozo a tierra."
3.  **Industrial Simple:** "Instalación de tablero trifásico para taller de soldadura."
4.  **Urgencia:** "Cotización urgente para reparación de corto circuito en tienda."
5.  **Licitación (Complejo):** "Cotización para sistema eléctrico de colegio con 20 aulas, incluye planos."
6.  **Mantenimiento:** "Servicio anual de mantenimiento de tableros para edificio."
7.  **Domótica:** "Casa inteligente: luces, persianas y cámaras."

### Grupo B: Proyectos (Agente PM)
8.  **Remodelación:** "Cronograma para cambiar todo el cableado de una casa habitada."
9.  **Obra Nueva:** "Proyecto eléctrico para construcción de casa de playa desde cero."
10. **Industrial (Complejo):** "Plan de obra para electrificación de planta procesadora."
11. **Subestación:** "Instalación de transformador y celda de media tensión."
12. **Certificación:** "Adecuación de instalaciones para inspección INDECI."
13. **Energía Solar:** "Proyecto de paneles solares para consumo residencial."
14. **CCTV:** "Sistema de seguridad con 16 cámaras y centro de monitoreo."

### Grupo C: Informes (Agente Reportero)
15. **Auditoría Simple:** "Informe de revisión de tablero eléctrico principal."
16. **Medición Pozo:** "Certificado de medición de resistencia de pozo a tierra."
17. **Termografía:** "Informe de puntos calientes en tableros industriales."
18. **Incidente:** "Reporte técnico sobre causa de apagón en servidor."
19. **Ejecutivo (Complejo):** "Resumen mensual de consumos y eficiencia energética."
20. **Final de Obra:** "Dossier de calidad y entrega de proyecto finalizado."

---

## 4. Metodología de Entrega

Para cada uno de los 3 Agentes, entregaremos:
1.  **El Artefacto Visual:** Un archivo HTML autocontenido (con CSS incrustado) que representa el documento final.
2.  **La Validación:** Confirmación de que la estructura visual coincide con la lógica de negocio (sin mostrar código).
