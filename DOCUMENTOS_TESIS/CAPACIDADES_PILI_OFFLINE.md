# 🧠 CAPACIDADES DE PILI (OFFLINE & HÍBRIDO)

**Fecha**: 04 de Diciembre, 2025
**Versión**: PILI v3.0

Este documento detalla exhaustivamente las capacidades del cerebro de PILI, diseñado para operar con lógica propia (Offline) y potenciarse con IA cuando está disponible.

---

## 1. 📄 LOS 6 TIPOS DE DOCUMENTOS (Agentes Especializados)

PILI no es un solo bot; es un sistema multi-agente. Cada tipo de documento es manejado por una "personalidad" distinta con reglas de negocio específicas.

### A. COTIZACIONES (Sales)

| Tipo | Agente Responsable | Enfoque | Lógica Offline |
| :--- | :--- | :--- | :--- |
| **1. Cotización Simple** | **PILI Cotizadora** | Velocidad (5-15 min). Para clientes residenciales/comerciales. | Detecta área (m²) y puntos. Calcula materiales básicos (cables, tomacorrientes) usando ratios estándar (ej: 1 luz/10m²). |
| **2. Cotización Compleja** | **PILI Analista** | Profundidad técnica. Para industria y licitaciones. | Requiere planos/PDFs. Analiza cargas, factor de demanda y selecciona equipos de protección industrial. |

### B. PROYECTOS (Management)

| Tipo | Agente Responsable | Enfoque | Lógica Offline |
| :--- | :--- | :--- | :--- |
| **3. Proyecto Simple** | **PILI Coordinadora** | Organización. Cronogramas básicos y listas de tareas. | Estructura fases estándar: Diseño → Materiales → Ejecución. Asigna cuadrillas básicas. |
| **4. Proyecto Complejo** | **PILI Project Manager** | Metodología PMI. Gestión de riesgos y stakeholders. | Crea WBS (Desglose de Trabajo), Matriz de Riesgos y Cronogramas con ruta crítica. |

### C. INFORMES (Reporting)

| Tipo | Agente Responsable | Enfoque | Lógica Offline |
| :--- | :--- | :--- | :--- |
| **5. Informe Simple** | **PILI Reportera** | Técnico/Campo. Reportes de visita o incidentes. | Estructura: Hallazgo → Evidencia → Recomendación. Usa plantillas de inspección predefinidas. |
| **6. Informe Ejecutivo** | **PILI Analista Senior** | Estratégico/APA. Para gerencia y toma de decisiones. | Analiza KPIs financieros (ROI, VAN). Redacta en tercera persona con formato académico/corporativo. |

---

## 2. ⚡ LOS 10 SERVICIOS ESPECIALIZADOS

PILI tiene "conocimiento enciclopédico" local de estos 10 verticales, incluyendo normativas peruanas y precios base.

| # | Servicio (ID Interno) | Nombre Comercial | Normativa Clave (Perú) | Unidad Base |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `electrico-residencial` | **Instalaciones Residenciales** | CNE Suministro 2011 | m² |
| 2 | `electrico-comercial` | **Instalaciones Comerciales** | CNE + RNE EM.010 | m² |
| 3 | `electrico-industrial` | **Instalaciones Industriales** | CNE Utilización | HP / kW |
| 4 | `contraincendios` | **Sistemas Contra Incendios** | NFPA 13, 72, 20 | m² / Puntos |
| 5 | `domotica` | **Domótica y Automatización** | KNX / Zigbee | Dispositivos |
| 6 | `expedientes` | **Expedientes Técnicos** | RNE / Municipal | Proyecto |
| 7 | `saneamiento` | **Agua y Desagüe** | RNE IS.010 | Puntos |
| 8 | `itse` | **Certificaciones ITSE** | D.S. 002-2018-PCM | Local |
| 9 | `pozo-tierra` | **Puesta a Tierra** | CNE Sec. 060 | Ohmios |
| 10 | `redes-cctv` | **Redes y Videovigilancia** | ANSI/TIA-568 | Puntos |

---

## 3. 🧠 LÓGICA DE DETECCIÓN "OFFLINE"

Cuando no hay IA externa, `PILIBrain` (`pili_brain.py`) usa esta lógica determinista:

### Detección de Complejidad
El sistema clasifica automáticamente una solicitud como **COMPLEJA** si:
1.  **Keywords**: Contiene palabras como "industrial", "planta", "fábrica", "440V", "media tensión", "subestación".
2.  **Magnitud**: Área > 300 m² o Potencia > 50 kW.
3.  **Archivos**: El usuario sube planos CAD/DWG (implica ingeniería).

*Si no cumple ninguna, se asume **SIMPLE**.*

### Cálculo de Precios (Motor de Inferencia)
PILI no inventa precios; usa una base de datos interna de costos unitarios (Materiales + Mano de Obra) ajustada al mercado peruano 2025.
*   *Ejemplo*: Si detecta "Casa de 100m²", calcula automáticamente:
    *   10 Puntos de luz (Ratio 1/10m²).
    *   6 Tomacorrientes (Ratio 1/15m²).
    *   1 Tablero General.
    *   **Total**: Suma de unitarios + Margen + IGV.

---

## 4. 🔮 VISIÓN FUTURA (PRODUCCIÓN)

En la etapa de producción con API Keys activas:
1.  **Hybrid Intelligence**: `PILIBrain` hará los cálculos matemáticos (que las LLMs suelen fallar) y la IA (Gemini/GPT) hará la redacción persuasiva y el análisis de contexto.
2.  **OCR Cognitivo**: La IA leerá los planos y pasará los datos estructurados a `PILIBrain` para cotizar.
