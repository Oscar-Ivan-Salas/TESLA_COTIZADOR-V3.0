# ❓ PREGUNTAS CRÍTICAS - ARQUITECTURA PILI

**Fecha**: 30 de Diciembre 2025
**Estado**: ⏸️ **DETENIDO** - Esperando validación del usuario
**Razón**: No crear más código sin estar 100% seguros de la arquitectura

---

## 🎯 CONTEXTO

He creado una **estructura propuesta** en `backend/app/services/pili_blackbox/` como **ANÁLISIS**, pero **NO implementaré nada más** hasta validar con el usuario.

**Archivos creados** (solo como propuesta):
```
backend/app/services/pili_blackbox/
├── router.py (130 líneas - propuesta)
└── services/
    └── itse/
        ├── chat_pili_itse.py (355 líneas - propuesta)
        ├── config.yaml (copiado)
        └── knowledge.py (copiado)
```

**Sistema antiguo**: 100% INTACTO (chat.py sin tocar)

---

## ❓ PREGUNTAS CRÍTICAS QUE NECESITO QUE RESPONDAS

### 1️⃣ Sobre los 10 servicios

**Pregunta**: ¿Los 10 servicios tienen flujos conversacionales similares?

**Ejemplo ITSE**:
```
Paso 1: Seleccionar categoría (Salud, Comercio, etc.)
Paso 2: Seleccionar tipo específico (Tienda, Hospital, etc.)
Paso 3: Ingresar área (m²)
Paso 4: Ingresar pisos
Paso 5: Cotización con cálculo de riesgo
```

**Pregunta específica**:
- ¿Electricidad, Pozo Tierra, Contraincendios, etc. tienen flujos similares (pregunta 1, pregunta 2, cotización)?
- ¿O cada servicio tiene un flujo COMPLETAMENTE diferente?

**¿Por qué es importante?**:
- Si son similares → Puedo crear lógica compartida (menos duplicación)
- Si son diferentes → Cada servicio debe ser 100% independiente

---

### 2️⃣ Sobre los 6 tipos de documentos

**Contexto**: Tenemos 6 tipos de documentos:
1. Cotización Simple
2. Cotización Compleja
3. Proyecto Simple
4. Proyecto Complejo PMI
5. Informe Técnico
6. Informe Ejecutivo APA

**Pregunta**: ¿Cualquier servicio puede generar cualquier tipo de documento?

**Ejemplo**:
- ¿ITSE puede generar "Cotización Simple" Y "Proyecto Complejo PMI"?
- ¿Electricidad puede generar los 6 tipos de documentos?
- ¿O hay restricciones? (ej: ITSE solo genera Cotización Simple/Compleja)

**Matriz posible**:
```
           | Cot.Simple | Cot.Compleja | Proy.Simple | Proy.PMI | Inf.Técnico | Inf.APA |
-----------+------------+--------------+-------------+----------+-------------+---------|
ITSE       |     ✅     |      ✅      |      ?      |    ?     |      ?      |    ?    |
Electricid |     ?      |      ?       |      ?      |    ?     |      ?      |    ?    |
Pozo Tier  |     ?      |      ?       |      ?      |    ?     |      ?      |    ?    |
...        |     ?      |      ?       |      ?      |    ?     |      ?      |    ?    |
```

**¿Puedes llenar esta matriz?** (o explicar la relación)

---

### 3️⃣ Sobre tu ChatPiliITSE (el que SÍ funciona)

**Pregunta**: ¿Dónde está ubicado tu ChatPiliITSE que ya funciona?

**Búsqueda realizada**:
```bash
find . -name "*ChatPili*" -o -name "*chat_pili*"
# No encontré carpeta "ChatPiliITSE"
```

**¿Está en**:
- Una carpeta dentro de `backend/app/services/`?
- Un repositorio separado?
- Un archivo específico?

**¿Por qué necesito verlo?**:
- Para entender EXACTAMENTE cómo resolviste el problema
- Para replicar tu solución a los otros 9 servicios
- Para asegurarme de que mi propuesta se alinea con lo que YA funciona

---

### 4️⃣ Sobre la estrategia de integración

**Pregunta**: ¿Qué prefieres?

**OPCIÓN A: 10 carpetas separadas (SIN código compartido)**
```
pili_blackbox/
├── itse/           (auto-contenida, 100% independiente)
├── electricidad/   (auto-contenida, 100% independiente)
├── pozo_tierra/    (auto-contenida, 100% independiente)
... (7 más)
```
- ✅ Ventaja: Cada servicio aislado, cambios NO afectan a otros
- ❌ Desventaja: Código duplicado (conversación, cálculos, validaciones)

**OPCIÓN B: Lógica compartida en `core/`**
```
pili_blackbox/
├── core/           (conversación, cálculos, validaciones compartidas)
└── services/
    ├── itse/       (solo lógica específica ITSE)
    ├── electricidad/ (solo lógica específica Electricidad)
    ... (8 más)
```
- ✅ Ventaja: Menos duplicación, cambios globales en 1 solo lugar
- ❌ Desventaja: Si `core/` se rompe, afecta a todos los servicios

**¿Cuál prefieres?** (o una mezcla de ambas)

---

### 5️⃣ Sobre los 6 generadores de documentos

**Contexto**: Ya migramos 6 generadores a `backend/app/services/professional/generators/`:
```
professional/generators/
├── cotizaciones/
│   ├── simple.py (16.7 KB)
│   └── compleja.py (16.2 KB)
├── proyectos/
│   ├── simple.py (15.0 KB)
│   └── complejo_pmi.py (16.5 KB)
└── informes/
    ├── tecnico.py (8.0 KB)
    └── ejecutivo_apa.py (10.5 KB)
```

**Pregunta**: ¿Los servicios PILI deben llamar a estos generadores?

**Flujo propuesto**:
```
Usuario → PILI (itse) → Datos estructurados → Generator (simple.py) → Documento .docx
```

**¿O tienes otra forma de integración?**

---

## 🛑 COMPROMISO

**NO escribiré MÁS CÓDIGO** hasta que respondas estas 5 preguntas.

**Una vez que respondas**:
1. Validaremos la arquitectura juntos
2. Ajustaremos lo necesario
3. Solo entonces continuaremos con FASE 2

---

## 📝 RESUMEN DE LO HECHO HASTA AHORA

### ✅ Documentos de análisis creados:
1. `ANALISIS_CRITICO_ARQUITECTURA_PILI.md` (700 líneas)
   - Análisis del problema
   - Propuesta de solución caja negra
   - Plan de 4 fases
   - Comparación antes/después

2. `VERIFICACION_CAMBIOS_SEGUROS.md` (275 líneas)
   - Verificación de que NO se modificó código antiguo
   - Solo documentación y propuestas

3. `PREGUNTAS_CRITICAS_ARQUITECTURA.md` (este archivo)
   - Preguntas clave antes de continuar

### ✅ Estructura propuesta (NO implementada):
- `backend/app/services/pili_blackbox/` (solo como referencia)
- Test de validación `test_pili_blackbox_itse.py` (sin ejecutar)

### ✅ Sistema antiguo:
- **100% INTACTO** (sin modificaciones)
- `chat.py` sigue con 4,635 líneas
- Todo funcionante como antes

---

**Esperando tus respuestas para continuar con seguridad.**

---

**Documento creado**: 30 de Diciembre 2025
**Arquitecto**: Claude Code (Sonnet 4.5)
**Estado**: ⏸️ DETENIDO - Esperando validación
