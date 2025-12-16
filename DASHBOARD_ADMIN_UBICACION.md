# 📊 DASHBOARD DE ADMINISTRACIÓN - UBICACIÓN Y USO

**Fecha:** 15 de Diciembre 2025
**Estado:** ✅ EXISTE COMPLETO - Pero NO está visible en la app principal

---

## 📂 UBICACIÓN DE LOS ARCHIVOS

### ✅ Backend - Router Admin
**Archivo:** `backend/app/routers/admin.py` (285 líneas)
**Estado:** ✅ Registrado en main.py
**Endpoints:** `/api/admin/*`

### ✅ Frontend - Componente AdminDashboard
**Archivo:** `frontend/src/components/AdminDashboard.jsx` (478 líneas completas)
**Estado:** ⚠️ Existe pero NO está importado en App.jsx

---

## 🔍 FUNCIONALIDADES DEL DASHBOARD

### 📊 Métricas que muestra:

1. **Usuarios:**
   - Total de usuarios
   - Distribución por plan (Free, Pro, Enterprise)
   - Porcentajes

2. **Documentos:**
   - Total de cotizaciones
   - Documentos creados hoy
   - Cambio en las últimas 24h

3. **Proyectos:**
   - Total de proyectos
   - Proyectos activos

4. **Tokens:**
   - Tokens consumidos
   - Tokens disponibles
   - Estadísticas globales

5. **Ingresos:**
   - Ingresos mensuales estimados
   - Ingresos anuales proyectados

### 🎛️ Controles de administración:

1. **Toggle de Servicios:**
   - Habilitar/deshabilitar cada servicio:
     - ⚡ Instalaciones Eléctricas
     - 📋 Certificados ITSE
     - 🔌 Puestas a Tierra
     - 🔥 Sistemas Contra Incendios
     - 🏠 Domótica
     - 📹 CCTV
     - 🌐 Redes de Datos
     - ⚙️ Automatización

2. **Feature Flags:**
   - Activar/desactivar funcionalidades
   - Control en tiempo real

3. **Actividad Reciente:**
   - Últimas cotizaciones creadas
   - Timeline de actividad

---

## 🔐 AUTENTICACIÓN

**Usuario:** `Admin`
**Contraseña:** `Admin1234`

**Tipo:** HTTP Basic Authentication

---

## ❌ PROBLEMA: No está visible en la app

### El dashboard existe pero:

```javascript
// frontend/src/App.jsx - Línea 1-50

import React, { useState, useEffect } from 'react';
import { Zap, FileText, Folder, Users, ... } from 'lucide-react';

// ❌ NO HAY:
// import AdminDashboard from './components/AdminDashboard';

function App() {
  const [pantallaActual, setPantallaActual] = useState('inicio');

  // ❌ NO HAY opción de pantalla 'admin'
  // Las opciones son: 'inicio', 'cotizacion-simple', 'proyecto-simple', etc.
}
```

---

## ✅ SOLUCIÓN: AGREGAR DASHBOARD AL APP

### Opción A: Agregar como pantalla principal

```javascript
// frontend/src/App.jsx

import AdminDashboard from './components/AdminDashboard';

function App() {
  const [pantallaActual, setPantallaActual] = useState('inicio');

  // Agregar botón en dashboard principal
  const Dashboard = () => (
    <div>
      {/* Botones existentes */}

      {/* NUEVO: Botón Admin */}
      <div
        onClick={() => setPantallaActual('admin')}
        className="bg-purple-500 hover:bg-purple-600..."
      >
        <Settings className="w-12 h-12" />
        <h3>Panel Admin</h3>
        <p>Métricas y configuración</p>
      </div>
    </div>
  );

  // En el renderizado principal
  return (
    <div>
      {pantallaActual === 'inicio' && <Dashboard />}
      {pantallaActual === 'admin' && <AdminDashboard />}
      {/* ... otras pantallas ... */}
    </div>
  );
}
```

### Opción B: Botón secreto (Ctrl + Shift + A)

```javascript
// frontend/src/App.jsx

useEffect(() => {
  const handleKeyPress = (e) => {
    // Ctrl + Shift + A = Abrir Admin
    if (e.ctrlKey && e.shiftKey && e.key === 'A') {
      setPantallaActual('admin');
    }
  };

  window.addEventListener('keydown', handleKeyPress);
  return () => window.removeEventListener('keydown', handleKeyPress);
}, []);
```

### Opción C: Ruta directa `/admin`

```javascript
// Acceder directamente:
// http://localhost:3000/#admin

useEffect(() => {
  const hash = window.location.hash;
  if (hash === '#admin') {
    setPantallaActual('admin');
  }
}, []);
```

---

## 🚀 ACCESO RÁPIDO (SIN MODIFICAR CÓDIGO)

**OPCIÓN TEMPORAL - PRUEBA DIRECTA:**

### Crear archivo de prueba:

**Crear:** `frontend/src/TestAdmin.jsx`

```javascript
import React from 'react';
import AdminDashboard from './components/AdminDashboard';

function TestAdmin() {
  return (
    <div>
      <AdminDashboard />
    </div>
  );
}

export default TestAdmin;
```

**Modificar temporalmente:** `frontend/src/index.js`

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
// import App from './App';
import TestAdmin from './TestAdmin';  // ← Cambio temporal

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <TestAdmin />
  </React.StrictMode>
);
```

Luego abrir: `http://localhost:3000`

---

## 📊 ENDPOINTS BACKEND DISPONIBLES

Todos requieren autenticación: `Admin:Admin1234`

### 1. Dashboard principal
```http
GET /api/admin/dashboard
Authorization: Basic QWRtaW46QWRtaW4xMjM0
```

**Response:**
```json
{
  "exito": true,
  "metricas": {
    "usuarios": {
      "total": 30,
      "free": 25,
      "pro": 4,
      "enterprise": 1
    },
    "documentos": {
      "total": 150,
      "hoy": 12
    },
    "proyectos": {
      "total": 45,
      "activos": 45
    },
    "tokens": {
      "total_consumido": 125000,
      "total_disponible": 875000
    },
    "ingresos": {
      "mensual": 419.95,
      "anual_estimado": 5039.40
    }
  },
  "servicios": { ... },
  "features": { ... }
}
```

### 2. Listar usuarios
```http
GET /api/admin/usuarios?limit=50&offset=0
Authorization: Basic QWRtaW46QWRtaW4xMjM0
```

### 3. Toggle servicio
```http
POST /api/admin/toggle-servicio/ELECTRICO
Authorization: Basic QWRtaW46QWRtaW4xMjM0
```

### 4. Toggle feature
```http
POST /api/admin/toggle-feature/MULTI_IA
Authorization: Basic QWRtaW46QWRtaW4xMjM0
```

### 5. Actividad reciente
```http
GET /api/admin/actividad-reciente?limit=10
Authorization: Basic QWRtaW46QWRtaW4xMjM0
```

---

## 🎨 DISEÑO DEL DASHBOARD

El AdminDashboard.jsx tiene:

### Layout de 3 columnas:

```
┌─────────────────────────────────────────────────────────┐
│  🔐 Login Admin (si no autenticado)                     │
│  Usuario: Admin                                         │
│  Contraseña: ****                                       │
│  [Ingresar]                                             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  📊 PANEL DE ADMINISTRACIÓN - TESLA COTIZADOR V3.0      │
├───────────────┬───────────────┬─────────────────────────┤
│ 👥 USUARIOS   │ 📄 DOCUMENTOS │ 💰 INGRESOS             │
│ Total: 30     │ Total: 150    │ Mensual: S/ 419.95      │
│ Free: 25      │ Hoy: 12       │ Anual: S/ 5,039.40      │
│ Pro: 4        │ ↑ +34%        │                         │
│ Enterprise: 1 │               │                         │
├───────────────┴───────────────┴─────────────────────────┤
│  🎛️ SERVICIOS DISPONIBLES                              │
│  ⚡ Instalaciones Eléctricas    [ON ✅]                 │
│  📋 Certificados ITSE           [OFF ❌]                │
│  🔌 Puestas a Tierra            [ON ✅]                 │
│  🔥 Sistemas Contra Incendios   [ON ✅]                 │
│  🏠 Domótica                    [ON ✅]                 │
│  📹 CCTV                        [OFF ❌]                │
│  🌐 Redes de Datos              [ON ✅]                 │
│  ⚙️ Automatización              [ON ✅]                 │
├─────────────────────────────────────────────────────────┤
│  🚩 FEATURE FLAGS                                       │
│  Multi-IA Support     [ON ✅]                           │
│  RAG Advanced         [OFF ❌]                          │
│  OCR Processing       [ON ✅]                           │
├─────────────────────────────────────────────────────────┤
│  📊 TOKENS                                              │
│  Consumidos: 125,000                                    │
│  Disponibles: 875,000                                   │
│  [████████░░] 12.5%                                     │
├─────────────────────────────────────────────────────────┤
│  ⏰ ACTIVIDAD RECIENTE                                  │
│  • Cotización COT-202512-0045 creada (hace 5 min)      │
│  • Cotización COT-202512-0044 creada (hace 12 min)     │
│  • Cotización COT-202512-0043 creada (hace 25 min)     │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ RESUMEN

**Dashboard de Administración:**

| Aspecto | Estado |
|---------|--------|
| **Backend router** | ✅ Existe y funciona (`admin.py`) |
| **Frontend componente** | ✅ Existe completo (`AdminDashboard.jsx`) |
| **Registro en main.py** | ✅ Registrado correctamente |
| **Visible en App.jsx** | ❌ NO está importado ni usado |
| **Funcionalidad** | ✅ 100% funcional (si se accede) |

---

## 🎯 PRÓXIMO PASO

**¿Qué quieres hacer?**

**Opción A:** Agregar botón Admin al dashboard principal
- Modifico `App.jsx`
- Agrego botón visible
- Agrego pantalla 'admin'

**Opción B:** Acceso con tecla secreta (Ctrl+Shift+A)
- Menos visible
- Solo administradores

**Opción C:** Probar ahora de forma temporal
- Modifico `index.js` temporalmente
- Ves el dashboard inmediatamente
- Luego lo integro bien

**¿Cuál prefieres?** O dime cómo quieres acceder al dashboard.

---

**Guardado en:**
- Backend: `backend/app/routers/admin.py` ✅
- Frontend: `frontend/src/components/AdminDashboard.jsx` ✅
- Credenciales: Admin / Admin1234 ✅
