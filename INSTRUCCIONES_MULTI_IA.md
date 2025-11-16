# 🤖 MULTI-IA SETUP - TESLA COTIZADOR V3.0

## 🎯 ¿Qué es esto?

Tu sistema ahora soporta **6 proveedores de IA diferentes** con fallback automático a PILIBrain (offline). Solo necesitas configurar **UNA API key** y el sistema funcionará.

---

## 🚀 SETUP RÁPIDO (5 minutos)

### 1️⃣ Copia el archivo de configuración

```bash
cd backend
cp .env.example .env
```

### 2️⃣ Elige tu IA preferida y agrega la API key en `.env`

**OPCIÓN RECOMENDADA - Google Gemini (GRATIS):**
```bash
# En .env agrega:
GEMINI_API_KEY=AIzaSy...tu_key_aqui
```
👉 Obtén tu key gratis en: https://makersuite.google.com/app/apikey

**O cualquiera de estas:**

| IA | Costo | Obtener Key | Variable en .env |
|---|---|---|---|
| 🟢 **Gemini** | Gratis | [makersuite.google.com](https://makersuite.google.com/app/apikey) | `GEMINI_API_KEY=` |
| 🟢 **Groq** | Gratis | [console.groq.com](https://console.groq.com/) | `GROQ_API_KEY=` |
| 🟢 **Together** | Gratis | [api.together.xyz](https://api.together.xyz/) | `TOGETHER_API_KEY=` |
| 🟢 **Cohere** | Gratis | [dashboard.cohere.com](https://dashboard.cohere.com/api-keys) | `COHERE_API_KEY=` |
| 🟡 **OpenAI** | De pago | [platform.openai.com](https://platform.openai.com/api-keys) | `OPENAI_API_KEY=` |
| 🟡 **Anthropic** | De pago | [console.anthropic.com](https://console.anthropic.com/) | `ANTHROPIC_API_KEY=` |

### 3️⃣ Instala las dependencias (solo la primera vez)

Si vas a usar **Gemini** (ya está instalado):
```bash
# No necesitas hacer nada, ya está listo
```

Si vas a usar **otras IAs**, descomenta en `requirements.txt` y luego:
```bash
pip install -r requirements.txt
```

### 4️⃣ ¡Listo! Arranca el servidor

```bash
uvicorn app.main:app --reload
```

---

## 🧪 PRUEBA FINAL - GENERAR 6 DOCUMENTOS

```bash
cd backend
python generar_6_documentos_demo.py
```

Esto generará en `documentos_generados_demo/`:
1. ✅ Cotización Simple.docx
2. ✅ Cotización Compleja.docx
3. ✅ Proyecto Simple.docx
4. ✅ Proyecto Complejo PMI.docx
5. ✅ Informe Técnico.docx
6. ✅ Informe Ejecutivo APA.docx

---

## 🔄 Sistema de Fallback Automático

```
Usuario hace request
       ↓
¿Tienes GEMINI_API_KEY?
   SÍ → Usa Gemini
   NO ↓

¿Tienes OPENAI_API_KEY?
   SÍ → Usa OpenAI
   NO ↓

¿Tienes GROQ_API_KEY?
   SÍ → Usa Groq
   NO ↓

... (prueba todas las configuradas)
       ↓
Si TODAS fallan o no hay ninguna:
   → USA PILIBrain (100% OFFLINE)
```

**✅ Siempre funcionará**, aunque no tengas ninguna API key.

---

## 📊 Verificar qué IAs están activas

```bash
# Endpoint del backend
GET /api/chat/pili/estado-ias
```

Respuesta:
```json
{
  "total_proveedores": 2,
  "proveedores_activos": [
    "Google Gemini 1.5 Pro",
    "Groq Llama 3 70B"
  ],
  "fallback_disponible": true,
  "configuracion": {
    "gemini": true,
    "openai": false,
    "anthropic": false,
    "groq": true,
    "together": false,
    "cohere": false
  }
}
```

---

## 💡 Recomendaciones

### Para DESARROLLO:
✅ **Usa Gemini** (gratis, bueno, rápido)

### Para PRODUCCIÓN:
✅ **Configura 2-3 IAs** para redundancia:
```bash
GEMINI_API_KEY=...        # Principal
GROQ_API_KEY=...          # Backup 1 (gratis)
ANTHROPIC_API_KEY=...     # Backup 2 (de pago pero confiable)
```

### Para DEMOS sin internet:
✅ **No configures nada** → PILIBrain funciona 100% offline

---

## 🐛 Troubleshooting

**Problema:** "No se pudo conectar a la IA"
**Solución:** Verifica tu API key en `.env`, debe ser válida

**Problema:** "Rate limit exceeded"
**Solución:** El sistema automáticamente usará la siguiente IA disponible

**Problema:** "Todas las IAs fallaron"
**Solución:** PILIBrain tomará el control automáticamente (offline)

---

## 📞 Soporte

Si tienes problemas:
1. Verifica que `.env` existe y tiene al menos una API key
2. Verifica que la API key es válida (copia/pega completa)
3. Revisa `logs/app.log` para ver qué IA se está usando
4. En el peor caso, funciona offline con PILIBrain

---

**🎯 TU SISTEMA ESTÁ LISTO PARA DEMO** 🚀
