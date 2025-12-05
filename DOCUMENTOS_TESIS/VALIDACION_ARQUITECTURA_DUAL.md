# Validación de Arquitectura Dual: "Cerebro Híbrido + Manos Únicas"

Este documento confirma que la arquitectura actual de TESLA COTIZADOR V3.0 soporta nativamente dos modos de operación para el "Cerebro" (PILI), manteniendo un único juego de "Manos" (Generadores Python) para la producción de documentos.

## 1. El Concepto: Manos Agnósticas
Los scripts de generación (`word_generator.py`, `pdf_generator.py`) son **agnósticos** a la fuente de la inteligencia.
*   No saben si los datos vienen de un `if/else` simple o de `GPT-5`.
*   Solo les importa recibir un JSON bien formado.

Esto garantiza que **los 6 prototipos de documentos funcionarán siempre**, sin importar qué tan inteligente se vuelva PILI en el futuro.

## 2. Los Dos Modos de Operación (Confirmados en Código)

### Modo A: Lógica / Offline (Pre-Producción)
*   **Fuente:** `pili_brain.py` (Lógica interna, Regex, Heurística).
*   **Uso:** Pruebas unitarias, demos rápidas, entornos sin internet.
*   **Comportamiento:**
    *   Detecta palabras clave ("residencial", "300m2").
    *   Genera un JSON estándar con valores estimados o por defecto.
    *   **Salida:** Documento Word perfecto (estructura correcta, datos simulados).

### Modo B: IA Avanzada / Producción (High-Level)
*   **Fuente:** `pili_orchestrator.py` conectando a `Gemini Pro` / `Anthropic Claude`.
*   **Uso:** Producción real, análisis de planos complejos, razonamiento profundo.
*   **Comportamiento:**
    *   La IA "piensa" y estructura la solución óptima.
    *   Genera el MISMO formato JSON estándar que el Modo A.
    *   **Salida:** Documento Word perfecto (estructura correcta, datos reales e inteligentes).

## 3. Flujo de Datos Unificado

```mermaid
graph TD
    A[Usuario] --> B{Router}
    B -->|Modo Offline| C[PILI Lógica (Regex/Python)]
    B -->|Modo Producción| D[PILI IA (Gemini/Claude)]
    
    C -->|JSON Estándar| E[Orquestador]
    D -->|JSON Estándar| E
    
    E --> F[Word Generator (Manos)]
    E --> G[PDF Generator (Manos)]
    
    F --> H[Documento Final (.docx)]
    G --> I[Documento Final (.pdf)]
```

## 4. Conclusión para Tesis
La arquitectura implementa un patrón de **"Inyección de Dependencia Cognitiva"**.
El sistema de generación de documentos (Manos) es una infraestructura estable que acepta "cartuchos de inteligencia" (Cerebros) intercambiables. Esto asegura que la inversión en el desarrollo de plantillas y scripts de generación (los 6 modelos) está protegida y es reutilizable al 100% cuando se escale a modelos de IA superiores.
