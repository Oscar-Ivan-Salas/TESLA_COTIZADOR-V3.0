# 🤖 INSTRUCCIONES: PILI ULTRA INTELIGENTE

## 📋 Descripción

**PILI Ultra Inteligente** es la versión avanzada de PILI que utiliza:
- **LangChain**: Framework para agentes inteligentes
- **LiteLLM**: Router multi-IA con fallback automático
- **3 Agentes Especializados**: Cotizadora, Proyectos, Informes

---

## 🎯 ¿Qué cambió vs PILI anterior?

| Aspecto | PILI Anterior | PILI Ultra Inteligente |
|---------|---------------|------------------------|
| **Arquitectura** | Monolítica | 3 agentes especializados |
| **Framework** | Código custom | LangChain (estándar industria) |
| **Razonamiento** | Regex + if/else | ReAct (Reasoning + Acting) |
| **IAs soportadas** | Solo Gemini | 6+ IAs con fallback automático |
| **Herramientas** | N/A | 19 herramientas especializadas |
| **Producción** | Cambiar código | Solo cambiar .env |

---

## 🏗️ Arquitectura

```
                    ┌─────────────────────────────┐
                    │   USUARIO (Frontend)        │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │  ORQUESTADOR PILI           │
                    │  (Detecta tipo documento)   │
                    └──────────────┬──────────────┘
                                   │
                   ┌───────────────┼───────────────┐
                   │               │               │
                   ▼               ▼               ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │PILICotizadora│  │PILIProyectos │  │PILIInformes  │
        │              │  │              │  │              │
        │ 6 Tools      │  │ 6 Tools      │  │ 7 Tools      │
        │              │  │              │  │              │
        │Cotiz Simple  │  │Proy Simple   │  │Inf Técnico   │
        │Cotiz Compleja│  │Proy PMI      │  │Inf Ejecutivo │
        └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
               │                  │                  │
               └──────────────────┼──────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │     PILI MULTI-IA           │
                    │   (LiteLLM Router)          │
                    └──────────────┬──────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
    ┌──────────┐            ┌──────────┐            ┌──────────┐
    │ Gemini   │            │  Groq    │            │Together  │
    │ (Primary)│            │(Fallback)│            │(Fallback)│
    └──────────┘            └──────────┘            └──────────┘
```

---

## 📦 Instalación

### 1. Dependencias ya instaladas

Las dependencias ya están en `requirements.txt` y fueron instaladas:

```bash
# LangChain
langchain==0.1.0
langchain-community==0.0.13
langchain-core==0.1.10

# LiteLLM (Multi-IA Router)
litellm==1.17.0

# Integración Gemini
langchain-google-genai==1.0.1

# Vector Store
faiss-cpu==1.8.0
```

### 2. Configurar API Keys

**Opción A: Solo Gemini (Mínimo requerido)**
```bash
# En backend/.env
GEMINI_API_KEY=tu_api_key_aqui
PRIMARY_MODEL=gemini/gemini-1.5-pro
```

**Opción B: Multi-IA con Fallback (Recomendado)**
```bash
# En backend/.env

# Modelo primario
PRIMARY_MODEL=gemini/gemini-1.5-pro

# Fallbacks (se intentan en orden si primario falla)
FALLBACK_MODELS=groq/llama-3.1-70b-versatile,together_ai/meta-llama/Llama-3-70b-chat-hf

# API Keys (solo configura las que vayas a usar)
GEMINI_API_KEY=tu_gemini_key        # GRATIS - https://makersuite.google.com/app/apikey
GROQ_API_KEY=tu_groq_key            # GRATIS - https://console.groq.com/
TOGETHER_API_KEY=tu_together_key    # GRATIS - https://api.together.xyz/
```

**Opción C: Producción (Pagar por mejor calidad)**
```bash
PRIMARY_MODEL=gpt-4-turbo
FALLBACK_MODELS=claude-3-opus,gemini/gemini-1.5-pro

OPENAI_API_KEY=sk-...               # PAGO
ANTHROPIC_API_KEY=sk-ant-...        # PAGO
GEMINI_API_KEY=...                  # GRATIS (fallback)
```

---

## 🚀 Uso

### Desde Python

```python
from app.services.pili_cotizadora_langchain import PILICotizadoraLangChain
from app.services.pili_proyectos_langchain import PILIProyectosLangChain
from app.services.pili_informes_langchain import PILIInformesLangChain
import os

# 1. COTIZACIONES
cotizadora = PILICotizadoraLangChain(gemini_api_key=os.getenv("GEMINI_API_KEY"))

resultado = cotizadora.procesar(
    mensaje="Necesito cotización para instalación eléctrica en oficina de 100m2 con 15 puntos de luz"
)

print(resultado["respuesta"])
if resultado["puede_generar"]:
    datos = resultado["datos_cotizacion"]
    # Usar datos para generar Word/PDF

# 2. PROYECTOS
proyectos = PILIProyectosLangChain(gemini_api_key=os.getenv("GEMINI_API_KEY"))

resultado = proyectos.procesar(
    mensaje="Crear proyecto PMI para automatización industrial, presupuesto S/ 80,000, 4 meses"
)

if resultado["puede_generar"]:
    datos = resultado["datos_proyecto"]
    # Generar Gantt, calcular ROI, analizar riesgos automáticamente

# 3. INFORMES
informes = PILIInformesLangChain(gemini_api_key=os.getenv("GEMINI_API_KEY"))

resultado = informes.procesar(
    mensaje="Generar informe ejecutivo APA sobre modernización eléctrica"
)

if resultado["puede_generar"]:
    datos = resultado["datos_informe"]
    # Incluye bibliografía APA, análisis técnico, conclusiones
```

### Desde API REST

```bash
# Cotización
curl -X POST http://localhost:8000/api/chat/mensaje \
  -H "Content-Type: application/json" \
  -d '{
    "mensaje": "Cotización para instalación eléctrica 100m2",
    "tipo_flujo": "cotizacion-compleja"
  }'

# Proyecto
curl -X POST http://localhost:8000/api/chat/mensaje \
  -H "Content-Type: application/json" \
  -d '{
    "mensaje": "Proyecto PMI automatización industrial S/ 80,000",
    "tipo_flujo": "proyecto-complejo"
  }'

# Informe
curl -X POST http://localhost:8000/api/chat/mensaje \
  -H "Content-Type: application/json" \
  -d '{
    "mensaje": "Informe técnico instalación eléctrica",
    "tipo_flujo": "informe-ejecutivo"
  }'
```

---

## 🔧 Herramientas Disponibles

### PILICotizadora (6 tools)

| Tool | Descripción | Input | Output |
|------|-------------|-------|--------|
| `calcular_carga_electrica` | Cálculo CNE Peru | área + tipo | Carga VA + conductor AWG |
| `calcular_igv` | IGV 18% Peru | monto | IGV calculado |
| `generar_items_instalacion_electrica` | Items instalación | área + puntos | Lista items con precios |
| `generar_items_itse` | Items ITSE | tipo local + área | Lista items ITSE |
| `validar_completitud` | Validar datos | datos cotización | completo: bool + faltantes |
| `formatear_cotizacion_json` | JSON final | datos completos | JSON estructurado |

### PILIProyectos (6 tools)

| Tool | Descripción | Input | Output |
|------|-------------|-------|--------|
| `generar_cronograma_gantt` | Gantt automático | fases + duraciones | Gantt con fechas |
| `calcular_roi` | ROI + payback | inversión + beneficio | ROI% + años payback |
| `analizar_riesgos` | Matriz riesgos | descripción + presupuesto | Riesgos + mitigación |
| `calcular_presupuesto` | Presupuesto estimado | tipo + duración | Presupuesto + desglose |
| `generar_kpis` | KPIs PMI | tipo + datos | KPIs con metas |
| `formatear_proyecto_json` | JSON final | datos completos | JSON estructurado |

### PILIInformes (7 tools)

| Tool | Descripción | Input | Output |
|------|-------------|-------|--------|
| `generar_resumen_ejecutivo` | Resumen 200-300 palabras | tema + objetivos | Resumen estructurado |
| `generar_analisis_tecnico` | Análisis técnico | tipo + datos | Análisis con subsecciones |
| `generar_conclusiones_recomendaciones` | Conclusiones + recoms | hallazgos + objetivos | Listas numeradas |
| `generar_bibliografia_apa` | Bibliografía APA 7ma | tipo fuentes | Referencias APA |
| `estructurar_informe_tecnico` | Estructura técnica | datos informe | Estructura completa |
| `estructurar_informe_ejecutivo_apa` | Estructura APA | datos informe | Estructura APA completa |
| `formatear_informe_json` | JSON final | datos completos | JSON estructurado |

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
cd backend
pytest tests/test_pili_langchain.py -v

# Solo tests rápidos (sin E2E)
pytest tests/test_pili_langchain.py -v -m "not slow"

# Test específico
pytest tests/test_pili_langchain.py::TestPILICotizadora::test_calcular_carga_electrica -v

# Con coverage
pytest tests/test_pili_langchain.py --cov=app.services --cov-report=html
```

**Tests incluidos**:
- ✅ 3 tests PILIMultiIA (router)
- ✅ 6 tests PILICotizadora
- ✅ 5 tests PILIProyectos
- ✅ 6 tests PILIInformes
- ✅ 3 tests E2E (integración completa)
- **Total: 23 tests**

---

## 🔄 Migración desde PILI anterior

### ¿Qué pasa con archivos anteriores?

Los archivos anteriores NO se borran, coexisten:

```
backend/app/services/
├── pili_cotizadora.py              # ANTERIOR (sigue funcionando)
├── pili_cotizadora_langchain.py    # NUEVO (LangChain)
│
├── pili_proyectos.py               # ANTERIOR
├── pili_proyectos_langchain.py     # NUEVO
│
├── pili_informes.py                # ANTERIOR
├── pili_informes_langchain.py      # NUEVO
│
├── pili_multi_ia.py                # NUEVO (router multi-IA)
└── pili_orchestrator.py            # INTEGRACIÓN (usa nuevos + anteriores)
```

### Migración gradual

**Paso 1: Configurar API keys**
```bash
# En .env agregar:
GEMINI_API_KEY=tu_key
PRIMARY_MODEL=gemini/gemini-1.5-pro
```

**Paso 2: Testear agentes nuevos**
```bash
pytest tests/test_pili_langchain.py -v
```

**Paso 3: Actualizar endpoints API**
```python
# En backend/app/routers/chat.py

# Importar nuevos agentes
from app.services.pili_cotizadora_langchain import PILICotizadoraLangChain
from app.services.pili_proyectos_langchain import PILIProyectosLangChain
from app.services.pili_informes_langchain import PILIInformesLangChain

# Usar según tipo de flujo
if tipo_flujo == "cotizacion-compleja":
    agente = PILICotizadoraLangChain(gemini_api_key=GEMINI_API_KEY)
    resultado = agente.procesar(mensaje)
```

**Paso 4: Probar en frontend**
- Frontend no necesita cambios
- API mantiene mismo formato de respuesta

**Paso 5: Monitorear y comparar**
- Comparar respuestas PILI anterior vs PILI LangChain
- Ajustar prompts según necesidad
- Validar que JSON generado sea compatible

---

## ⚙️ Configuración Avanzada

### Personalizar Temperatura

```python
# En código
cotizadora = PILICotizadoraLangChain(gemini_api_key=key)
cotizadora.llm.temperature = 0.5  # Más creativo
cotizadora.llm.max_tokens = 8000  # Respuestas más largas
```

### Cambiar Modelo LLM

```python
# Cambiar de Gemini a GPT-4
from langchain_openai import ChatOpenAI

cotizadora.llm = ChatOpenAI(
    model="gpt-4-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3
)
```

### Agregar Nuevas Herramientas

```python
# En pili_cotizadora_langchain.py

def _crear_herramientas(self):
    tools = [
        # ... herramientas existentes ...

        Tool(
            name="calcular_descuento_volumen",
            func=self._calcular_descuento,
            description="""
            Calcula descuento por volumen.
            Input: {"cantidad": int, "precio_unitario": float}
            Output: {"descuento_%": float, "precio_final": float}
            """
        )
    ]
    return tools

def _calcular_descuento(self, input_str: str) -> str:
    data = json.loads(input_str)
    cantidad = int(data.get("cantidad", 1))
    precio = float(data.get("precio_unitario", 0))

    # Lógica de descuento
    if cantidad >= 100:
        descuento = 0.15
    elif cantidad >= 50:
        descuento = 0.10
    elif cantidad >= 20:
        descuento = 0.05
    else:
        descuento = 0.0

    precio_final = precio * (1 - descuento)

    return json.dumps({
        "descuento_porcentaje": descuento * 100,
        "precio_final": precio_final
    })
```

---

## 📊 Comparación de Rendimiento

### Velocidad (respuesta típica)

| IA Provider | Velocidad | Calidad | Costo | Límite Gratis |
|-------------|-----------|---------|-------|---------------|
| **Gemini 1.5 Pro** | ~2-3 seg | ⭐⭐⭐⭐⭐ | GRATIS | 60 req/min |
| **Groq Llama 3.1** | <1 seg | ⭐⭐⭐⭐ | GRATIS | 30 req/min |
| **Together AI** | ~2 seg | ⭐⭐⭐⭐ | GRATIS | 60 req/min |
| **GPT-4 Turbo** | ~3-5 seg | ⭐⭐⭐⭐⭐ | $0.01/1K tokens | No gratis |
| **Claude 3 Opus** | ~3-4 seg | ⭐⭐⭐⭐⭐ | $0.015/1K tokens | No gratis |

### Recomendaciones

**DESARROLLO:**
```bash
PRIMARY_MODEL=gemini/gemini-1.5-pro
FALLBACK_MODELS=groq/llama-3.1-70b-versatile
```
- ✅ 100% GRATIS
- ✅ Excelente calidad
- ✅ Fallback ultra-rápido (Groq)

**PRODUCCIÓN:**
```bash
PRIMARY_MODEL=gpt-4-turbo
FALLBACK_MODELS=claude-3-opus,gemini/gemini-1.5-pro
```
- ✅ Máxima calidad (GPT-4)
- ✅ Fallback profesional (Claude)
- ✅ Fallback gratis (Gemini)

---

## 🐛 Troubleshooting

### Error: "API key not configured"

**Solución:**
```bash
# Verificar .env
cat backend/.env | grep GEMINI_API_KEY

# Debe mostrar: GEMINI_API_KEY=tu_key_real

# Si está vacío, agregar:
echo "GEMINI_API_KEY=tu_key_aqui" >> backend/.env
```

### Error: "All models failed"

**Causa:** Ninguna IA respondió (problemas de red o API keys incorrectas)

**Solución:**
```bash
# 1. Verificar conexión a internet
ping google.com

# 2. Verificar API keys
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Gemini:', os.getenv('GEMINI_API_KEY')[:10] if os.getenv('GEMINI_API_KEY') else 'NO CONFIGURADA')
print('Groq:', os.getenv('GROQ_API_KEY')[:10] if os.getenv('GROQ_API_KEY') else 'NO CONFIGURADA')
"

# 3. Probar manualmente
python -c "
from app.services.pili_multi_ia import PILIMultiIA
multi = PILIMultiIA()
print(multi.chat('Hola'))
"
```

### Error: "Tool execution failed"

**Causa:** Error en alguna herramienta (función Tool)

**Solución:**
```python
# Ver logs detallados
import logging
logging.basicConfig(level=logging.DEBUG)

# Ejecutar agente
from app.services.pili_cotizadora_langchain import PILICotizadoraLangChain
cotizadora = PILICotizadoraLangChain(gemini_api_key="tu_key")
resultado = cotizadora.procesar("test")

# Revisar logs en backend/logs/
tail -f backend/logs/app.log
```

---

## 📚 Referencias

- **LangChain Docs**: https://python.langchain.com/docs/
- **LiteLLM Docs**: https://docs.litellm.ai/
- **Gemini API**: https://ai.google.dev/docs
- **Groq API**: https://console.groq.com/docs
- **Together AI**: https://docs.together.ai/

---

## 📞 Soporte

**Preguntas frecuentes:**

1. **¿Puedo usar solo Gemini sin otros proveedores?**
   - Sí, solo configura `GEMINI_API_KEY` y deja `FALLBACK_MODELS` vacío.

2. **¿Cuánto cuesta en producción?**
   - Con Gemini: **GRATIS** (hasta 60 req/min)
   - Con GPT-4: ~$0.03 por cotización
   - Con Claude: ~$0.045 por cotización

3. **¿Qué pasa si se excede el límite gratuito?**
   - LiteLLM automáticamente intenta el siguiente modelo de fallback.

4. **¿Es necesario LangChain?**
   - Sí, es el framework que permite los agentes con herramientas y razonamiento ReAct.

5. **¿Funcionan los tests sin API keys?**
   - No, los tests requieren al menos `GEMINI_API_KEY` configurada.

---

**Versión**: 3.0.0 - PILI Ultra Inteligente
**Fecha**: Diciembre 2025
**Autor**: TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.
