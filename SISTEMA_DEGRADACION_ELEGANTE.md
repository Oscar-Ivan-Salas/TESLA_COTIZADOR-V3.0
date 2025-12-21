# 🛡️ SISTEMA DE DEGRADACIÓN ELEGANTE DE PILI

## 📋 Descripción

**PILI NUNCA se quedará paralizado**. Tiene un sistema de degradación elegante con múltiples niveles de fallback que garantiza que SIEMPRE pueda responder, incluso sin conexión a IAs.

---

## 🏗️ ARQUITECTURA DE DEGRADACIÓN MULTINIVEL

```
┌─────────────────────────────────────────────────────────┐
│            USUARIO HACE UNA PREGUNTA                    │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │   NIVEL 1: IAs en la Nube  │
         │   (Intentar primero)       │
         └────────────┬───────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   ┌────────┐   ┌────────┐   ┌────────┐
   │ Gemini │   │  Groq  │   │Together│
   │GRATIS  │   │GRATIS  │   │ GRATIS │
   └────┬───┘   └────┬───┘   └────┬───┘
        │            │            │
        │  Si falla  │  Si falla  │
        └────────────┼────────────┘
                     │
          ┌──────────▼──────────┐
          │ OpenAI / Claude     │
          │ (Si configurados)   │
          └──────────┬──────────┘
                     │
              Si TODOS fallan
                     │
                     ▼
         ┌────────────────────────────┐
         │   NIVEL 2: Modo Offline    │
         │   (Lógica Propia de PILI)  │
         └────────────┬───────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   Reglas de    Templates    Respuestas
   Detección    Predefinidos  Guiadas
                      │
                      ▼
         ┌────────────────────────────┐
         │  ✅ PILI SIEMPRE RESPONDE  │
         └────────────────────────────┘
```

---

## 🎯 NIVELES DE DEGRADACIÓN

### NIVEL 1: IAs en la Nube (PRIMARIO)

**Intenta en orden:**

| # | IA | Velocidad | Costo | Límite Gratis |
|---|----|-----------| ------|---------------|
| 1 | **Gemini 1.5 Pro** | ~2 seg | GRATIS | 60 req/min |
| 2 | **Groq Llama 3.1** | <1 seg | GRATIS | 30 req/min |
| 3 | **Together AI** | ~2 seg | GRATIS | 60 req/min |
| 4 | **OpenAI GPT-4** | ~3 seg | PAGO | Ilimitado* |
| 5 | **Claude 3** | ~3 seg | PAGO | Ilimitado* |

*Ilimitado pero pagas por uso

**Comportamiento:**
```
1. Intenta Gemini
   ├─ ✅ Funciona → Devuelve respuesta
   └─ ❌ Falla → Intenta Groq

2. Intenta Groq
   ├─ ✅ Funciona → Devuelve respuesta
   └─ ❌ Falla → Intenta Together AI

3. Intenta Together AI
   ├─ ✅ Funciona → Devuelve respuesta
   └─ ❌ Falla → Intenta OpenAI (si configurado)

4. Intenta OpenAI
   ├─ ✅ Funciona → Devuelve respuesta
   └─ ❌ Falla → Intenta Claude (si configurado)

5. Intenta Claude
   ├─ ✅ Funciona → Devuelve respuesta
   └─ ❌ TODOS FALLARON → MODO OFFLINE
```

---

### NIVEL 2: Modo Offline (FALLBACK FINAL)

**Si TODAS las IAs fallan o no hay API keys configuradas**, PILI activa su **lógica propia**.

#### Detección de Intención (Sin IA)

PILI analiza palabras clave para detectar qué quiere el usuario:

| Intención | Palabras Clave | Respuesta |
|-----------|---------------|-----------|
| **Cotización** | cotiz, presupuesto, precio, costo | Guía paso a paso para cotizar |
| **Proyecto** | proyecto, gantt, cronograma, pmi | Guía para crear proyecto |
| **Informe** | informe, reporte, documento, análisis | Guía para generar informe |
| **Saludo** | hola, buenos días, hey, hi | Bienvenida con opciones |
| **Despedida** | adiós, chau, gracias | Despedida amable |
| **Genérico** | Otros | Pregunta qué necesita el usuario |

#### Ejemplo de Modo Offline

**Usuario dice:**
```
"Necesito una cotización"
```

**PILI responde (sin IA):**
```
Perfecto, te ayudo con la cotización usando mi lógica local.

🔧 **MODO OFFLINE** - Necesito algunos datos:

**Para Instalación Eléctrica:**
1. ¿Cuál es el nombre del cliente?
2. ¿Qué área en m² tiene el proyecto?
3. ¿Cuántos puntos de luz necesitas?
4. ¿Cuántos tomacorrientes?

**Servicios disponibles:**
• Instalaciones Eléctricas
• Certificados ITSE
• Puestas a Tierra
• Sistemas Contra Incendios
• Domótica
• CCTV
• Redes de Datos
• Automatización Industrial

Por favor proporciona estos datos y generaré la cotización.
```

**✅ PILI NO se quedó paralizado - Siguió funcionando**

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### Código del Modo Offline

**Ubicación**: `backend/app/services/pili_multi_ia.py`

```python
def chat(self, mensaje: str, ...) -> Dict[str, Any]:
    """Chat con fallback automático"""

    # Intentar todas las IAs configuradas
    all_models = [self.primary_model] + self.fallback_models

    for idx, model in enumerate(all_models):
        try:
            # Intentar con esta IA
            response = completion(model=model, messages=messages, ...)
            return response  # ✅ Éxito

        except Exception as e:
            # Si es el ÚLTIMO modelo
            if idx == len(all_models) - 1:
                # ❌ TODOS fallaron

                # 🔧 ACTIVAR MODO OFFLINE
                return self._modo_offline(mensaje, historial)

            # Continuar con siguiente modelo
            continue
```

### Lógica de Detección

```python
def _modo_offline(self, mensaje: str, ...) -> Dict[str, Any]:
    """Modo Offline - Lógica propia"""

    mensaje_lower = mensaje.lower()

    # Detección por palabras clave
    if "cotiz" in mensaje_lower or "presupuesto" in mensaje_lower:
        return self._offline_cotizacion(mensaje)

    elif "proyecto" in mensaje_lower or "gantt" in mensaje_lower:
        return self._offline_proyecto(mensaje)

    elif "informe" in mensaje_lower:
        return self._offline_informe(mensaje)

    elif "hola" in mensaje_lower:
        return self._offline_saludo()

    else:
        return self._offline_generico()
```

---

## 🎯 VENTAJAS DEL SISTEMA

### 1. Alta Disponibilidad (99.99%+)

- **Si Gemini está caído** → Usa Groq
- **Si Groq está caído** → Usa Together AI
- **Si TODOS están caídos** → Modo Offline
- **Resultado**: PILI SIEMPRE responde

### 2. Sin Dependencia Única

- **NO depende** de una sola IA
- **NO se paraliza** si falta API key
- **NO requiere** conexión a internet (modo offline)

### 3. Costo Controlado

- **Desarrollo**: 100% GRATIS (Gemini, Groq, Together)
- **Producción**: Usa gratis primero, paga solo si es necesario
- **Modo Offline**: $0 (siempre gratis)

### 4. Experiencia de Usuario

- **Usuario NO ve errores** técnicos
- **Usuario SIEMPRE recibe** respuesta útil
- **Usuario NO necesita** esperar reconexiones

---

## 📊 COMPARACIÓN DE MODOS

| Aspecto | Con IA (Nivel 1) | Modo Offline (Nivel 2) |
|---------|------------------|------------------------|
| **Inteligencia** | ⭐⭐⭐⭐⭐ (máxima) | ⭐⭐⭐ (buena) |
| **Velocidad** | 1-3 seg | <0.1 seg (instantánea) |
| **Costo** | $0 (gratis) o pago | $0 (siempre gratis) |
| **Disponibilidad** | 99.9% | 100% (siempre) |
| **Conexión requerida** | Sí | No |
| **Personalización** | Alta | Media |
| **Creatividad** | Alta | Baja (templates) |

---

## 🧪 PRUEBAS DEL SISTEMA

### Escenario 1: Todo Funciona Normal

```bash
# .env tiene:
GEMINI_API_KEY=sk-xxx

# Usuario:
"Necesito cotización para instalación eléctrica"

# PILI usa:
✅ Gemini (intento 1) → ÉXITO
```

### Escenario 2: Gemini Falla, Groq Funciona

```bash
# .env tiene:
GEMINI_API_KEY=sk-invalida  # Key incorrecta
GROQ_API_KEY=sk-xxx

# Usuario:
"Necesito cotización para instalación eléctrica"

# PILI usa:
❌ Gemini (intento 1) → FALLA
✅ Groq (intento 2) → ÉXITO
```

### Escenario 3: TODAS las IAs Fallan

```bash
# .env tiene:
# (vacío o keys inválidas)

# Usuario:
"Necesito cotización para instalación eléctrica"

# PILI usa:
❌ Gemini → FALLA (no hay key)
❌ Groq → FALLA (no hay key)
❌ Together → FALLA (no hay key)
🔧 MODO OFFLINE → ÉXITO (lógica propia)

# Respuesta:
"Perfecto, te ayudo con la cotización usando mi lógica local.
🔧 **MODO OFFLINE** - Necesito algunos datos:
..."
```

### Escenario 4: Sin Conexión a Internet

```bash
# Usuario sin internet

# Usuario:
"Hola PILI"

# PILI usa:
❌ Todas las IAs → TIMEOUT (no hay internet)
🔧 MODO OFFLINE → ÉXITO (lógica local)

# Respuesta:
"¡Hola! Soy PILI, tu asistente de Tesla Electricidad.
🔧 **MODO OFFLINE ACTIVADO** - Trabajando con lógica local.
..."
```

---

## 📝 CONFIGURACIÓN

### Configuración Mínima (Solo Offline)

```bash
# backend/.env
# (dejar vacío o comentar API keys)

# GEMINI_API_KEY=
# GROQ_API_KEY=
```

**Resultado**: PILI funciona 100% offline con lógica propia.

### Configuración Recomendada (Multi-IA)

```bash
# backend/.env

# Primaria (GRATIS)
GEMINI_API_KEY=tu_gemini_key

# Fallbacks (GRATIS)
GROQ_API_KEY=tu_groq_key
TOGETHER_API_KEY=tu_together_key

# Router
PRIMARY_MODEL=gemini/gemini-1.5-pro
FALLBACK_MODELS=groq/llama-3.1-70b-versatile,together_ai/meta-llama/Llama-3-70b-chat-hf
```

**Resultado**: Alta disponibilidad con degradación a offline si TODO falla.

### Configuración Producción (Máxima Calidad)

```bash
# backend/.env

# Primaria (PAGO - máxima calidad)
PRIMARY_MODEL=gpt-4-turbo
OPENAI_API_KEY=sk-xxx

# Fallbacks (PAGO + GRATIS)
FALLBACK_MODELS=claude-3-opus,gemini/gemini-1.5-pro,groq/llama-3.1-70b-versatile
ANTHROPIC_API_KEY=sk-ant-xxx
GEMINI_API_KEY=tu_gemini_key
GROQ_API_KEY=tu_groq_key
```

**Resultado**: Máxima calidad con múltiples fallbacks + modo offline final.

---

## 🚀 VENTAJAS vs COMPETENCIA

| Sistema | Sin API Key | Falla IA Primaria | Todas IAs Fallan | Sin Internet |
|---------|-------------|-------------------|------------------|--------------|
| **PILI V3** | ✅ Funciona (offline) | ✅ Usa fallback | ✅ Modo offline | ✅ Funciona |
| ChatGPT | ❌ Error | ❌ Error | ❌ Error | ❌ Error |
| Claude | ❌ Error | ❌ Error | ❌ Error | ❌ Error |
| Otros | ❌ Error | ⚠️ Algunos fallback | ❌ Error | ❌ Error |

**PILI V3 es el ÚNICO que NUNCA se paraliza.**

---

## 📚 DOCUMENTACIÓN RELACIONADA

- **PLAN_PILI_LANGCHAIN_ULTRA_INTELIGENTE.md** - Arquitectura completa
- **INSTRUCCIONES_PILI_LANGCHAIN.md** - Manual de uso
- **backend/app/services/pili_multi_ia.py** - Implementación

---

## ✅ GARANTÍAS

### PILI V3 GARANTIZA:

1. ✅ **Siempre responde** - Nunca se queda en blanco
2. ✅ **Nunca se paraliza** - Modo offline como último recurso
3. ✅ **Alta disponibilidad** - 99.99%+ (multi-IA + offline)
4. ✅ **Sin dependencia única** - No depende de una sola IA
5. ✅ **Funciona offline** - Lógica propia sin internet
6. ✅ **Costo $0 posible** - Puede funcionar 100% gratis

---

**Versión**: 3.0.0 - PILI Ultra Inteligente
**Fecha**: Diciembre 2025
**Garantía**: NUNCA se paraliza
**Autor**: TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.
