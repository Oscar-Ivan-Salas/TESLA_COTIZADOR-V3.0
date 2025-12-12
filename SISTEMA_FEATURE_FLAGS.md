# 🎚️ SISTEMA DE FEATURE FLAGS - Tesla Cotizador V3.0

> **Guía completa para activar/desactivar funcionalidades**
> **Fecha**: 2025-12-12
> **Versión**: 3.0.0

---

## 📋 TABLA DE CONTENIDOS

- [¿Qué son los Feature Flags?](#qué-son-los-feature-flags)
- [Funcionalidades Disponibles](#funcionalidades-disponibles)
- [Métodos de Activación](#métodos-de-activación)
- [Panel de Administrador Web](#panel-de-administrador-web)
- [Configuración .env](#configuración-env)
- [Servicios ON/OFF](#servicios-onoff)
- [Guía de Uso](#guía-de-uso)
- [Troubleshooting](#troubleshooting)

---

## 🎯 ¿QUÉ SON LOS FEATURE FLAGS?

Los **Feature Flags** (banderas de características) son **interruptores ON/OFF** que permiten:

✅ **Habilitar/deshabilitar funcionalidades sin tocar código**
✅ **Probar features de forma independiente**
✅ **Rollback instantáneo si algo falla**
✅ **Desarrollo incremental sin romper producción**
✅ **Control total del sistema desde un panel**

---

## 🚀 FUNCIONALIDADES DISPONIBLES

### 1. **Sistema de Tokens** 🎯

**Variable**: `FEATURE_TOKEN_MANAGER`

**Qué hace**:
- Limita el consumo de tokens por usuario según plan
- Plan Free: 1,000 tokens/mes
- Plan Pro: 10,000 tokens/mes
- Plan Enterprise: 100,000 tokens/mes

**Estado inicial**: OFF (ilimitado en desarrollo)

**Cuándo activar**: Cuando estés listo para limitar uso y monetizar

---

### 2. **Multi-IA Orchestrator** 🤖

**Variable**: `FEATURE_MULTI_IA`

**Qué hace**:
- Orquesta múltiples IAs (Gemini, Claude, GPT-4, Groq)
- Selecciona IA apropiada según plan del usuario
- Free: solo Gemini (gratis)
- Pro: Gemini + Claude + GPT-4
- Enterprise: todas las IAs con routing inteligente

**Estado inicial**: OFF (solo Gemini)

**Cuándo activar**: Cuando tengas API keys de otras IAs configuradas

---

### 3. **Sistema Multi-Agente** 👥

**Variable**: `FEATURE_MULTI_AGENT`

**Qué hace**:
- 3 agentes colaborando (Planner, Generator, Reviewer)
- Mayor calidad de documentos
- Revisión automática de errores
- Especialización por agente

**Estado inicial**: OFF

**Cuándo activar**: Cuando implementes LangGraph

---

### 4. **Autenticación de Usuarios** 🔐

**Variable**: `FEATURE_AUTH_USUARIOS`

**Qué hace**:
- Login/registro de usuarios
- Autenticación con JWT
- Sesiones seguras
- Recuperación de contraseña

**Estado inicial**: OFF

**Cuándo activar**: Cuando implementes auth completo

---

### 5. **Rate Limiting** ⏱️

**Variable**: `FEATURE_RATE_LIMIT`

**Qué hace**:
- Límite de requests por minuto
- Protección contra abuso
- Prevención de ataques

**Estado inicial**: OFF

**Cuándo activar**: En producción

---

### 6. **Analytics Dashboard** 📊

**Variable**: `FEATURE_ANALYTICS`

**Qué hace**:
- Dashboard de analytics avanzado
- Gráficos y métricas
- Exportación de reportes

**Estado inicial**: OFF

**Cuándo activar**: Cuando implementes analytics

---

## 🎛️ MÉTODOS DE ACTIVACIÓN

### **MÉTODO 1: Panel de Administrador Web** (RECOMENDADO)

#### 1. Acceder al panel

```
http://localhost:3000/admin
```

o en producción:

```
https://tesla-cotizador.com/admin
```

#### 2. Login

```
Usuario: Admin
Contraseña: Admin1234
```

#### 3. Dashboard

Verás el panel de administración con:

```
┌────────────────────────────────────────────────────────┐
│  TESLA COTIZADOR V3.0 - Panel Administrativo          │
│  👤 Admin                                    [Logout]  │
├────────────────────────────────────────────────────────┤
│                                                         │
│  📊 RESUMEN GENERAL                                     │
│  ┌─────────┬─────────┬─────────┬─────────┐            │
│  │ Usuarios│ Docs    │ Ingresos│ Tokens  │            │
│  │   30    │  157    │ $1,107  │ 45.2K   │            │
│  └─────────┴─────────┴─────────┴─────────┘            │
│                                                         │
│  🎚️ FUNCIONALIDADES AVANZADAS                          │
│  ┌────────────────────────────────────────┐            │
│  │ Sistema de Tokens           [🔴 OFF]   │← Click aquí│
│  │ Multi-IA Orchestrator       [🔴 OFF]   │            │
│  │ Sistema Multi-Agente        [🔴 OFF]   │            │
│  │ Autenticación Usuarios      [🔴 OFF]   │            │
│  └────────────────────────────────────────┘            │
│                                                         │
│  ⚙️ SERVICIOS DISPONIBLES (ON/OFF)                     │
│  ┌────────────────────────────────────────┐            │
│  │ ⚡ Eléctrico Residencial    [🟢 ON]    │            │
│  │ 🏢 Eléctrico Comercial      [🟢 ON]    │            │
│  │ 🏭 Eléctrico Industrial     [🟢 ON]    │            │
│  └────────────────────────────────────────┘            │
└────────────────────────────────────────────────────────┘
```

#### 4. Click en el switch

- 🔴 OFF → Click → 🟢 ON
- 🟢 ON → Click → 🔴 OFF

**⚠️ IMPORTANTE**: Los cambios via panel son **temporales** (solo memoria).

Para hacerlos **permanentes**, edita `.env` (Método 2).

---

### **MÉTODO 2: Archivo .env** (PERMANENTE)

#### 1. Abrir archivo

```bash
cd backend
nano .env
```

#### 2. Editar feature flags

```env
# ═══════════════════════════════════════════════════════════════
# 🎚️ FEATURE FLAGS (ON/OFF)
# ═══════════════════════════════════════════════════════════════

# Sistema de tokens (límites por plan)
FEATURE_TOKEN_MANAGER=False  # ← Cambiar a True

# Multi-IA Orchestrator (Gemini + Claude + GPT-4)
FEATURE_MULTI_IA=False  # ← Cambiar a True

# Sistema Multi-Agente (3 agentes colaborando)
FEATURE_MULTI_AGENT=False

# Autenticación de usuarios
FEATURE_AUTH_USUARIOS=False

# Rate limiting (límite de requests/minuto)
FEATURE_RATE_LIMIT=False

# Dashboard de analytics
FEATURE_ANALYTICS=False
```

#### 3. Guardar y reiniciar backend

```bash
# Ctrl+O para guardar
# Ctrl+X para salir

# Reiniciar backend
# Si usas Docker:
docker-compose restart backend

# Si usas Python directo:
uvicorn app.main:app --reload
```

---

## ⚙️ SERVICIOS ON/OFF

### ¿Qué son?

Los **servicios** son los 10 tipos de documentos que Tesla Cotizador puede generar.

### Lista de servicios:

1. ⚡ **Eléctrico Residencial**
2. 🏢 **Eléctrico Comercial**
3. 🏭 **Eléctrico Industrial**
4. 🔥 **Contraincendios**
5. 🏠 **Domótica**
6. 📋 **ITSE**
7. 🔌 **Pozo a Tierra**
8. 📹 **Redes y CCTV**
9. 📐 **Expedientes Técnicos**
10. 💧 **Saneamiento**

### ¿Cómo funcionan?

- **ON** → Servicio aparece en la web para usuarios
- **OFF** → Servicio NO aparece (invisible para usuarios)

### Casos de uso:

✅ **Mantenimiento temporal** de un servicio
✅ **Pruebas** antes de lanzar nuevo servicio
✅ **Desactivar** servicios no rentables
✅ **Control total** del catálogo de servicios

### Configuración:

**Via Panel Admin**:
- Login → Sección "Servicios Disponibles" → Click en switch

**Via código** (`backend/app/core/features.py`):
```python
SERVICIOS_CONFIG = {
    "electrico-residencial": {
        "habilitado": True,  # ← Cambiar a False
        # ...
    }
}
```

---

## 📘 GUÍA DE USO

### Escenario 1: Activar Sistema de Tokens

**Objetivo**: Limitar uso de IA para control de costos

**Pasos**:

1. **Verificar** que tienes usuarios creados en BD
2. **Abrir** `.env`
3. **Cambiar** `FEATURE_TOKEN_MANAGER=True`
4. **Guardar** y **reiniciar** backend
5. **Verificar** en logs:

```bash
tail -f backend/app/logs/app.log

# Deberías ver:
✅ TokenManager activado
🔓 TokenManager ON - Verificando tokens antes de operación
```

6. **Probar** haciendo una solicitud
7. **Verificar** que se consumen tokens:

```bash
# Endpoint de prueba
curl http://localhost:8000/api/admin/estadisticas/tokens \
  -u Admin:Admin1234

# Respuesta:
{
  "tokens_usados": 150,
  "tokens_disponibles": 850,
  ...
}
```

---

### Escenario 2: Deshabilitar un Servicio

**Objetivo**: Mantenimiento temporal de servicio Domótica

**Pasos**:

1. **Login** en panel admin: http://localhost:3000/admin
2. **Buscar** servicio "Domótica"
3. **Click** en switch: 🟢 ON → 🔴 OFF
4. **Verificar** en frontend usuario:
   - Botón de Domótica **desaparece**
   - Solo aparecen 9 servicios

5. **Cuando termines mantenimiento**:
   - Click en switch: 🔴 OFF → 🟢 ON
   - Botón reaparece para usuarios

---

### Escenario 3: Activar Multi-IA

**Objetivo**: Usar Claude para usuarios Pro

**Prerequisitos**:
- API Key de Anthropic configurada en `.env`:
  ```env
  ANTHROPIC_API_KEY=sk-ant-...
  ```

**Pasos**:

1. **Configurar** API key
2. **Cambiar** `.env`:
   ```env
   FEATURE_MULTI_IA=True
   ```
3. **Reiniciar** backend
4. **Verificar** logs:
   ```
   ✅ Claude disponible
   🤖 Multi-IA Orchestrator activado
   ```
5. **Probar** con usuario Pro:
   - Login como usuario Pro
   - Hacer solicitud
   - Verificar en logs:
     ```
     🤖 IA seleccionada: claude | Plan: pro
     ```

---

## 🔧 TROUBLESHOOTING

### Problema 1: Feature activada pero no funciona

**Síntomas**:
- Cambié `.env` a True
- Pero sigue en modo OFF

**Solución**:
```bash
# 1. Verificar que guardaste .env
cat backend/.env | grep FEATURE_TOKEN_MANAGER

# 2. Reiniciar backend
docker-compose restart backend

# 3. Verificar logs
docker-compose logs backend | grep "Feature"
```

---

### Problema 2: Panel admin no carga

**Síntomas**:
- http://localhost:3000/admin → error 404

**Solución**:
```bash
# 1. Verificar que el componente existe
ls frontend/src/components/AdminDashboard.jsx

# 2. Importar en App.jsx si no está
# Editar frontend/src/App.jsx:
import AdminDashboard from './components/AdminDashboard';

# 3. Agregar ruta (si usas React Router)
<Route path="/admin" element={<AdminDashboard />} />
```

---

### Problema 3: Credenciales admin no funcionan

**Síntomas**:
- Admin/Admin1234 → "Credenciales incorrectas"

**Solución**:
```bash
# Verificar backend
curl http://localhost:8000/api/admin/dashboard \
  -u Admin:Admin1234

# Si retorna 401:
# 1. Verificar que el router admin está cargado
docker-compose logs backend | grep "Router Admin"

# Debería aparecer:
✅ Router Admin cargado
```

---

## 📊 MONITOREO

### Ver estado de features

```bash
# Via API
curl http://localhost:8000/api/admin/dashboard -u Admin:Admin1234

# Respuesta incluye:
{
  "features": {
    "token_manager": false,
    "multi_ia": false,
    "multi_agent": false,
    ...
  }
}
```

### Ver consumo de tokens

```bash
curl http://localhost:8000/api/admin/estadisticas/tokens -u Admin:Admin1234
```

### Ver usuarios activos

```bash
curl http://localhost:8000/api/admin/usuarios -u Admin:Admin1234
```

---

## 🎓 MEJORES PRÁCTICAS

### 1. Desarrollo Incremental

```
Fase 1: Todo OFF → Documentos funcionando perfectos
Fase 2: Token Manager ON → Probar límites
Fase 3: Multi-IA ON → Probar Claude/GPT-4
Fase 4: Multi-Agente ON → Probar calidad mejorada
Fase 5: Producción → Todo ON
```

### 2. Testing Aislado

- Activa **UNA feature a la vez**
- Prueba exhaustivamente
- Si falla → OFF inmediatamente
- Fix el problema
- Vuelve a ON

### 3. Rollback Rápido

Si algo falla en producción:

```bash
# Opción A: Via panel admin (instantáneo)
1. Login → Click switch OFF

# Opción B: Via .env (permanente)
1. Editar .env → False
2. Restart backend
```

---

## 🚀 ROADMAP DE ACTIVACIÓN

### Semana 1-2: Documentos Perfectos
- ✅ TODO OFF
- ✅ Enfoque 100% en calidad de documentos
- ✅ Logos funcionando
- ✅ Colores correctos

### Semana 3: Tokens
- ✅ `FEATURE_TOKEN_MANAGER=True`
- ✅ Probar con 30 usuarios
- ✅ Verificar límites
- ✅ Dashboard de consumo

### Semana 4: Multi-IA
- ✅ Configurar Claude API
- ✅ `FEATURE_MULTI_IA=True`
- ✅ Probar calidad comparativa
- ✅ Ajustar routing

### Semana 5-6: Multi-Agente
- ✅ Implementar LangGraph
- ✅ `FEATURE_MULTI_AGENT=True`
- ✅ Probar 3 agentes
- ✅ Medir mejora de calidad

### Semana 7: Producción
- ✅ Todo ON
- ✅ Monitoreo activo
- ✅ Usuarios reales

---

## 📞 SOPORTE

**Dudas o problemas**:
- Email: ingenieria.teslaelectricidad@gmail.com
- Revisar logs: `backend/app/logs/app.log`
- Documentación: Este archivo

---

**Fin de documentación**

**Versión**: 1.0.0
**Última actualización**: 2025-12-12
