# ✅ IMPLEMENTACIÓN COMPLETA: Single Source of Truth (SSOT) - Datos de Empresa
**Fecha**: 2025-12-04
**Estado**: ✅ **COMPLETADO** (Backend + Frontend)

---

## 🎯 PROBLEMA RESUELTO

### Antes (Problema):
- ❌ Datos de empresa duplicados en 3 lugares diferentes
- ❌ Dirección INCORRECTA en word_generator.py (Lima en lugar de Huancayo)
- ❌ Cambiar datos requería editar múltiples archivos
- ❌ Alto riesgo de inconsistencias

### Después (Solución):
- ✅ **UN SOLO LUGAR** para datos de empresa (`config.py`)
- ✅ Dirección CORRECTA de Huancayo centralizada
- ✅ Cambios se propagan automáticamente
- ✅ Arquitectura DRY (Don't Repeat Yourself)

---

## 📊 ARQUITECTURA SSOT IMPLEMENTADA

```
┌─────────────────────────────────────────────────────────┐
│         config.py (SSOT - Single Source of Truth)       │
│                                                          │
│  EMPRESA_NOMBRE:    "TESLA ELECTRICIDAD..."            │
│  EMPRESA_RUC:       "20601138787"                       │
│  EMPRESA_DIRECCION: "Jr. Los Narcisos Mz H lote 4..."  │
│  EMPRESA_TELEFONO:  "906315961"                         │
│  EMPRESA_EMAIL:     "ingenieria.teslaelectricidad..."   │
│  EMPRESA_CIUDAD:    "Huancayo, Junín - Perú"           │
│                                                          │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ Fuente centralizada
                 │
         ┌───────┴────────┐
         │                │
         ▼                ▼
┌─────────────────┐  ┌─────────────────┐
│ word_generator  │  │  API Endpoint   │
│     .py         │  │ /empresa-info   │
│                 │  │                 │
│ get_empresa_    │  │ get_empresa_    │
│ info()          │  │ info()          │
│                 │  │                 │
│ Genera Word     │  │ Expone JSON     │
│ con datos       │  │ al frontend     │
│ correctos       │  │                 │
└─────────────────┘  └────────┬────────┘
                              │
                              │
                              ▼
                     ┌─────────────────┐
                     │   App.jsx       │
                     │  (Frontend)     │
                     │                 │
                     │  useEffect()    │
                     │  fetch API      │
                     │  actualiza      │
                     │  estado         │
                     └─────────────────┘
```

---

## 🔧 CAMBIOS IMPLEMENTADOS

### 1. **config.py** - Fuente Central de Verdad

**Ubicación**: `backend/app/core/config.py`

**Agregado (líneas 73-95)**:
```python
# =======================================
# INFORMACIÓN DE LA EMPRESA (SSOT - Single Source of Truth)
# =======================================
EMPRESA_NOMBRE: str = "TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C."
EMPRESA_RUC: str = "20601138787"
EMPRESA_DIRECCION: str = "Jr. Los Narcisos Mz H lote 4 Urb. Los jardines de San Carlos"
EMPRESA_TELEFONO: str = "906315961"
EMPRESA_EMAIL: str = "ingenieria.teslaelectricidad@gmail.com"
EMPRESA_CIUDAD: str = "Huancayo, Junín - Perú"
EMPRESA_WEB: str = Field(default="", env="EMPRESA_WEB")  # Opcional desde .env

@property
def EMPRESA_INFO(self) -> dict:
    """Retorna información completa de la empresa"""
    return {
        "nombre": self.EMPRESA_NOMBRE,
        "ruc": self.EMPRESA_RUC,
        "direccion": self.EMPRESA_DIRECCION,
        "telefono": self.EMPRESA_TELEFONO,
        "email": self.EMPRESA_EMAIL,
        "ciudad": self.EMPRESA_CIUDAD,
        "web": self.EMPRESA_WEB
    }
```

**Funciones Helper Agregadas (líneas 300-314)**:
```python
def get_empresa_info() -> dict:
    """Obtiene información completa de la empresa (SSOT)"""
    return settings.EMPRESA_INFO

def get_empresa_nombre() -> str:
    """Obtiene nombre de la empresa"""
    return settings.EMPRESA_NOMBRE

def get_empresa_direccion_completa() -> str:
    """Obtiene dirección completa con ciudad"""
    return f"{settings.EMPRESA_DIRECCION}, {settings.EMPRESA_CIUDAD}"
```

---

### 2. **word_generator.py** - Uso de Config

**Ubicación**: `backend/app/services/word_generator.py`

**Antes (líneas 61-67)** ❌:
```python
# Configuración de documentos
self.empresa_info = {
    "nombre": "TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.",
    "ruc": "20601138787",
    "direccion": "Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL",  # ❌ LIMA
    "telefono": "906315961",
    "email": "ingenieria.teslaelectricidad@gmail.com"
}
```

**Después (líneas 60-66)** ✅:
```python
# Configuración de documentos (SSOT - Single Source of Truth)
from app.core.config import get_empresa_info
self.empresa_info = get_empresa_info()

logger.info("✅ WordGenerator + PILI inicializado")
logger.info(f"📍 Empresa: {self.empresa_info['nombre']}")
logger.info(f"📍 Ciudad: {self.empresa_info['ciudad']}")
```

**Beneficio**:
- ✅ Ahora usa dirección correcta de Huancayo automáticamente
- ✅ Si cambias datos en config.py, Word se actualiza automáticamente

---

### 3. **system.py** - Nuevo Endpoint API

**Ubicación**: `backend/app/routers/system.py`

**Agregado (líneas 74-105)**:
```python
@router.get("/empresa-info",
            summary="Obtiene información de la empresa (SSOT)",
            status_code=status.HTTP_200_OK)
async def get_empresa_information():
    """
    Retorna información corporativa de Tesla Electricidad.

    Esta es la **Single Source of Truth (SSOT)** para datos de la empresa.
    Todos los documentos (Word, PDF) y el frontend obtienen datos desde aquí.

    **Returns:**
    - nombre: Nombre legal de la empresa
    - ruc: RUC de la empresa
    - direccion: Dirección física
    - telefono: Teléfono de contacto
    - email: Email de contacto
    - ciudad: Ciudad y región
    - web: Sitio web (opcional)
    """
    try:
        info = get_empresa_info()
        logger.info("Información de empresa solicitada")
        return {
            "exito": True,
            "datos": info
        }
    except Exception as e:
        logger.error(f"Error al obtener información de empresa: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener información de la empresa"
        )
```

**Endpoint**:
```
GET http://localhost:8000/api/system/empresa-info
```

**Respuesta**:
```json
{
  "exito": true,
  "datos": {
    "nombre": "TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.",
    "ruc": "20601138787",
    "direccion": "Jr. Los Narcisos Mz H lote 4 Urb. Los jardines de San Carlos",
    "telefono": "906315961",
    "email": "ingenieria.teslaelectricidad@gmail.com",
    "ciudad": "Huancayo, Junín - Perú",
    "web": ""
  }
}
```

---

## ✅ PASO 5: App.jsx - Frontend SSOT Implementado

### IMPLEMENTADO - Código Actualizado

**Ubicación**: `frontend/src/App.jsx`

**Antes (líneas 66-73)** ❌:
```javascript
const [datosEmpresa] = useState({
  nombre: 'TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.',
  ruc: '20601138787',
  direccion: 'Jr. Los Narcisos Mz H lote 4 Urb. Los jardines de San Calos',  // Typos
  telefono: '906315961',
  email: 'ingenieria.teslaelectricidad@gmail.com',
  ciudad: 'Huanacayo, Junin - Perú'  // Typos
});
```

**Después (líneas 68-76, 134-169)** ✅:
```javascript
// Los datos de empresa se cargan desde la API para mantener sincronización
const [datosEmpresa, setDatosEmpresa] = useState({
  nombre: '',
  ruc: '',
  direccion: '',
  telefono: '',
  email: '',
  ciudad: '',
  web: ''
});

// ... más abajo en el código (líneas 134-169) ...

// Cargar información de empresa desde API al montar el componente
useEffect(() => {
  const cargarEmpresaInfo = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/system/empresa-info');
      const data = await response.json();

      if (data.exito) {
        setDatosEmpresa(data.datos);
        console.log('✅ Información de empresa cargada desde API:', data.datos);
      } else {
        console.warn('⚠️ API no retornó datos exitosos');
        usarDatosPorDefecto();
      }
    } catch (error) {
      console.error('❌ Error al cargar información de empresa:', error);
      // Fallback a datos por defecto si API falla
      usarDatosPorDefecto();
    }
  };

  const usarDatosPorDefecto = () => {
    // Fallback con datos correctos de Huancayo
    setDatosEmpresa({
      nombre: 'TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.',
      ruc: '20601138787',
      direccion: 'Jr. Los Narcisos Mz H lote 4 Urb. Los jardines de San Carlos',
      telefono: '906315961',
      email: 'ingenieria.teslaelectricidad@gmail.com',
      ciudad: 'Huancayo, Junín - Perú',
      web: ''
    });
  };

  cargarEmpresaInfo();
}, []); // [] significa que se ejecuta solo al montar el componente
```

**Nota**: useEffect ya estaba importado en App.jsx:
```javascript
import React, { useState, useRef, useEffect } from 'react';
```

**Beneficios de esta implementación**:
- ✅ Datos corregidos automáticamente (sin typos en "Calos" o "Huanacayo")
- ✅ Fallback robusto si la API no está disponible
- ✅ Logging completo para debugging
- ✅ Sincronización automática con backend

---

## 🧪 CÓMO PROBAR

### 1. **Probar Backend (word_generator)**

```bash
# Terminal 1: Levantar backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Ejecutar test
cd backend
python test_generacion_word.py
```

**Verificar en logs**:
```
✅ WordGenerator + PILI inicializado
📍 Empresa: TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.
📍 Ciudad: Huancayo, Junín - Perú
```

**Abrir documento Word generado** y verificar que tiene:
- ✅ Dirección correcta de Huancayo (no Lima)
- ✅ Todos los datos actualizados

---

### 2. **Probar Endpoint API**

```bash
# Con curl
curl http://localhost:8000/api/system/empresa-info

# O en navegador
http://localhost:8000/api/system/empresa-info
```

**Esperado**:
```json
{
  "exito": true,
  "datos": {
    "nombre": "TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.",
    "direccion": "Jr. Los Narcisos Mz H lote 4 Urb. Los jardines de San Carlos",
    "ciudad": "Huancayo, Junín - Perú",
    ...
  }
}
```

---

### 3. **Probar Frontend (cuando implementes App.jsx)**

```bash
# Terminal 1: Backend corriendo
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm start
```

**Abrir consola del navegador (F12)** y buscar:
```
✅ Información de empresa cargada desde API: {nombre: "TESLA...", ...}
```

**Verificar en la interfaz** que los datos de empresa se muestran correctamente.

---

## 📝 BENEFICIOS DE ESTA IMPLEMENTACIÓN

### 1. **Mantenibilidad**
- ✅ Cambiar dirección: Solo editar 1 archivo (config.py)
- ✅ Agregar teléfono fijo: Solo agregar en config.py
- ✅ Actualizar email: Solo cambiar en config.py

### 2. **Consistencia**
- ✅ Frontend, backend y documentos Word usan MISMOS datos
- ✅ Imposible tener inconsistencias
- ✅ Datos siempre sincronizados

### 3. **Escalabilidad**
- ✅ Fácil agregar nuevos campos (ej: sitio web, teléfono fijo)
- ✅ Fácil crear nuevos documentos (PDF, Excel) usando mismos datos
- ✅ Fácil agregar nuevos consumidores (mobile app, etc.)

### 4. **Profesionalismo**
- ✅ Arquitectura limpia siguiendo best practices
- ✅ Código DRY (Don't Repeat Yourself)
- ✅ Single Source of Truth (SSOT)
- ✅ API RESTful bien documentada

---

## 🎯 RESUMEN DE COMMITS

### Commit 1: `515c30c`
```
feat: Centralizar información de empresa en config.py (SSOT)

- Agregar sección EMPRESA_INFO en config.py
- Datos correctos de Huancayo centralizados
- Funciones helper: get_empresa_info(), get_empresa_nombre(), get_empresa_direccion_completa()
```

### Commit 2: `8fda144`
```
feat: Actualizar word_generator y crear endpoint /empresa-info (SSOT)

- word_generator.py usa get_empresa_info() de config
- Eliminar datos hardcodeados incorrectos (Lima)
- Crear endpoint GET /api/system/empresa-info
- Documentación Swagger completa
```

---

## ✅ CHECKLIST DE VERIFICACIÓN

### Backend (COMPLETADO)

- [x] Datos centralizados en config.py
- [x] word_generator.py usa config
- [x] Endpoint /empresa-info creado
- [x] Pruebas de generación Word pasadas
- [x] Logs muestran ciudad correcta (Huancayo)
- [x] Commits realizados y pusheados

### Frontend (COMPLETADO)

- [x] App.jsx actualizado con useEffect
- [x] Import de useEffect (ya estaba presente)
- [x] Código con fallback robusto implementado
- [x] Logging agregado para debugging
- [x] Datos corregidos (sin typos)
- [ ] Probado en desarrollo (npm start) - PENDIENTE PRUEBA DEL USUARIO
- [ ] Consola muestra carga exitosa - PENDIENTE PRUEBA DEL USUARIO
- [ ] Interfaz muestra datos correctos - PENDIENTE PRUEBA DEL USUARIO

---

## 🚀 PRÓXIMOS PASOS

### Inmediato
1. ✅ **App.jsx actualizado** con useEffect y fetch de API
2. **PROBAR** que frontend carga datos correctamente:
   ```bash
   # Terminal 1: Levantar backend
   cd backend
   uvicorn app.main:app --reload

   # Terminal 2: Levantar frontend
   cd frontend
   npm start
   ```
3. **Verificar** en consola del navegador (F12):
   - Debe mostrar: `✅ Información de empresa cargada desde API: {nombre: "TESLA...", ...}`
   - Los datos deben tener la dirección correcta de Huancayo (sin typos)

### Futuro
1. **Agregar campo sitio web** si tienen uno
2. **Agregar teléfono fijo** de oficina si tienen
3. **Considerar multi-sucursal** si abren otras oficinas

---

## 📞 DATOS ACTUALES EN EL SISTEMA

```
Nombre:    TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.
RUC:       20601138787
Dirección: Jr. Los Narcisos Mz H lote 4 Urb. Los jardines de San Carlos
Teléfono:  906315961
Email:     ingenieria.teslaelectricidad@gmail.com
Ciudad:    Huancayo, Junín - Perú
Web:       (vacío - agregar si tienen)
```

**¿Todos son correctos?** ✅

---

## 💡 TIPS

### Cambiar Datos de Empresa
```python
# backend/app/core/config.py (líneas 76-82)
EMPRESA_NOMBRE: str = "NUEVO NOMBRE"
EMPRESA_DIRECCION: str = "NUEVA DIRECCIÓN"
# etc...
```

**Reiniciar backend** y listo! Todos los componentes usan nuevos datos automáticamente.

### Agregar Nuevo Campo
```python
# 1. En config.py
EMPRESA_TELEFONO_FIJO: str = "064-123456"

# 2. Agregar a EMPRESA_INFO property
@property
def EMPRESA_INFO(self) -> dict:
    return {
        # ... campos existentes ...
        "telefono_fijo": self.EMPRESA_TELEFONO_FIJO
    }
```

### Variables de Entorno (Opcional)
Si quieres cambiar datos sin editar código:

```bash
# backend/.env
EMPRESA_WEB=https://teslaelectricidad.com
EMPRESA_TELEFONO_FIJO=064-123456
```

```python
# config.py
EMPRESA_WEB: str = Field(default="", env="EMPRESA_WEB")
EMPRESA_TELEFONO_FIJO: str = Field(default="", env="EMPRESA_TELEFONO_FIJO")
```

---

**FIN DEL DOCUMENTO**

**Estado**: ✅ **IMPLEMENTACIÓN COMPLETA** (Backend + Frontend)
**Fecha**: 2025-12-04
**Implementado por**: Claude (Asistente IA)

**Archivos modificados**:
- ✅ `backend/app/core/config.py` - SSOT centralizado
- ✅ `backend/app/services/word_generator.py` - Usa config
- ✅ `backend/app/routers/system.py` - API endpoint
- ✅ `frontend/src/App.jsx` - Fetch desde API

**Commits**:
- `515c30c` - feat: Centralizar información de empresa en config.py (SSOT)
- `8fda144` - feat: Actualizar word_generator y crear endpoint /empresa-info (SSOT)
- Pendiente commit para App.jsx

**Siguiente paso**: Probar en desarrollo (backend + frontend) y verificar logs en consola del navegador.
