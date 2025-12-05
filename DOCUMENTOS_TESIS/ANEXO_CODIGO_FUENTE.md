# Anexo: Código Fuente del Sistema de Generación

Este anexo contiene los scripts de Python originales que implementan la arquitectura "Cerebro vs Manos". Estos archivos son la evidencia técnica de la implementación.

## 📂 Estructura del Código

Los archivos se encuentran en la carpeta adjunta `./CODIGO_FUENTE/`.

### 1. El Cerebro (Lógica y Orquestación)

*   **[pili_orchestrator.py](./CODIGO_FUENTE/pili_orchestrator.py)**
    *   *Descripción:* El coordinador central. Decide si usar el modo "Offline" o el modo "IA" (Gemini). Gestiona el flujo de datos y llama a los generadores.
    *   *Patrón:* Facade / Strategy.

*   **[pili_brain.py](./CODIGO_FUENTE/pili_brain.py)**
    *   *Descripción:* La lógica cognitiva "Offline". Contiene las reglas de negocio, heurísticas y expresiones regulares para entender las solicitudes sin internet.

### 2. Las Manos (Generación de Documentos)

*   **[word_generator.py](./CODIGO_FUENTE/word_generator.py)**
    *   *Descripción:* El motor de construcción de `.docx`. Utiliza `python-docx` para crear tablas, estilos y paginación dinámica. Implementa la lógica de "Twin Design" (replicar el CSS en objetos Python).
    *   *Clave:* Es agnóstico a la IA. Solo recibe JSON.

*   **[pdf_generator.py](./CODIGO_FUENTE/pdf_generator.py)**
    *   *Descripción:* El motor de generación de `.pdf` seguros usando `ReportLab`. Diseñado para documentos finales inalterables (contratos, facturas).

---

## Nota para la Tesis
Estos scripts demuestran la implementación de:
1.  **Desacoplamiento:** La lógica de negocio está separada de la presentación.
2.  **Polimorfismo:** El mismo orquestador puede llamar a diferentes generadores (Word/PDF).
3.  **Inyección de Dependencia:** Los generadores reciben los datos y configuraciones, no los buscan.
