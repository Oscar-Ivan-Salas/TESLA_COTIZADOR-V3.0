# 🚀 INSTRUCCIONES DE INSTALACIÓN - PILI v3.0

## ⚠️ PROBLEMA ACTUAL:
- ❌ Error: "no such table: cotizaciones"
- ❌ Error: CORS bloqueando peticiones
- ❌ Base de datos no existe

---

## ✅ SOLUCIÓN PASO A PASO:

### PASO 1: Descargar todos los cambios de GitHub

```powershell
# Abrir PowerShell en E:\TESLA_COTIZADOR-V3.0

# Descargar todos los branches
git fetch --all

# Ver qué branches hay disponibles
git branch -a

# Cambiar al branch con todos los arreglos
git checkout claude/analyze-prompts-01Bao3FK5gRS9TW5z3QekTFx

# Descargar los últimos cambios
git pull origin claude/analyze-prompts-01Bao3FK5gRS9TW5z3QekTFx
```

**Deberías ver archivos actualizándose:**
```
backend/app/main.py
backend/app/routers/chat.py
backend/crear_tablas.py (NUEVO)
frontend/src/App.jsx
frontend/src/components/PiliAvatar.jsx
```

---

### PASO 2: Crear la base de datos manualmente (SI EL SCRIPT NO EXISTE)

Si después de git pull NO tienes el archivo `backend/crear_tablas.py`, crea la base de datos manualmente:

**Opción A - Usar Python puro:**

```powershell
cd E:\TESLA_COTIZADOR-V3.0
python -c "
import sqlite3
from pathlib import Path

# Crear carpeta database
Path('database').mkdir(exist_ok=True)

# Crear base de datos
db = Path('database/tesla_cotizador.db')
conn = sqlite3.connect(str(db))
cursor = conn.cursor()

# Crear tabla cotizaciones
cursor.execute('''
CREATE TABLE IF NOT EXISTS cotizaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero VARCHAR(50) UNIQUE NOT NULL,
    cliente VARCHAR(200) NOT NULL,
    proyecto VARCHAR(200) NOT NULL,
    descripcion TEXT,
    subtotal DECIMAL(10, 2) DEFAULT 0.00,
    igv DECIMAL(10, 2) DEFAULT 0.00,
    total DECIMAL(10, 2) DEFAULT 0.00,
    observaciones TEXT,
    vigencia VARCHAR(100) DEFAULT '30 días',
    estado VARCHAR(50) DEFAULT 'borrador',
    items TEXT,
    metadata_adicional TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    proyecto_id INTEGER
)
''')

# Crear tabla proyectos
cursor.execute('''
CREATE TABLE IF NOT EXISTS proyectos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    cliente VARCHAR(200),
    descripcion TEXT,
    estado VARCHAR(50) DEFAULT 'planificacion',
    presupuesto_estimado DECIMAL(12, 2),
    duracion_meses INTEGER,
    tipo VARCHAR(100),
    metadata_adicional TEXT,
    fecha_inicio DATETIME,
    fecha_fin DATETIME,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Crear tabla documentos
cursor.execute('''
CREATE TABLE IF NOT EXISTS documentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_archivo VARCHAR(255) NOT NULL,
    tipo VARCHAR(50),
    ruta VARCHAR(500),
    tamanio INTEGER,
    contenido_extraido TEXT,
    metadata TEXT,
    fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP,
    proyecto_id INTEGER
)
''')

# Crear tabla items
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    cantidad DECIMAL(10, 2) DEFAULT 0,
    unidad VARCHAR(20) DEFAULT 'und',
    precio_unitario DECIMAL(10, 2) DEFAULT 0.00,
    total DECIMAL(10, 2) DEFAULT 0.00,
    categoria VARCHAR(100),
    metadata TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    cotizacion_id INTEGER,
    proyecto_id INTEGER
)
''')

conn.commit()
conn.close()

print('✅ Base de datos creada: E:/TESLA_COTIZADOR-V3.0/database/tesla_cotizador.db')
print('✅ Tablas creadas: cotizaciones, proyectos, documentos, items')
"
```

**Opción B - Si el script SÍ existe:**

```powershell
cd E:\TESLA_COTIZADOR-V3.0\backend
python crear_tablas.py
```

---

### PASO 3: Verificar que la base de datos existe

```powershell
# Debería mostrar el archivo
dir E:\TESLA_COTIZADOR-V3.0\database\tesla_cotizador.db
```

---

### PASO 4: Reiniciar el backend

**IMPORTANTE: Debes DETENER el backend actual primero**

1. Ve a la ventana de PowerShell donde corre el backend
2. Presiona `Ctrl + C` para detenerlo
3. Ejecuta:

```powershell
cd E:\TESLA_COTIZADOR-V3.0\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Deberías ver:**
```
INFO: 🗄️  Verificando base de datos...
INFO: ✅ Base de datos inicializada correctamente
INFO: 🚀 INICIANDO TESLA COTIZADOR API V3.0
INFO: 🔗 Registrando routers avanzados...
INFO: ✅ ROUTERS ACTIVOS (PILI completa)
INFO: Uvicorn running on http://0.0.0.0:8000
```

---

### PASO 5: Recargar el frontend

En el navegador donde tienes `http://localhost:3000`:

1. Presiona `Ctrl + Shift + R` (recarga forzada)
2. Abre la consola del navegador (F12)
3. Verifica que NO haya errores CORS

---

## 🧪 PRUEBA:

1. Selecciona "Cotización Simple"
2. Escribe: "Necesito instalación eléctrica para casa 120 m²"
3. Espera la respuesta de PILI
4. Haz clic en "Descargar Word"

**Resultado esperado:**
- ✅ Sin error "no such table"
- ✅ Sin error CORS
- ✅ Documento Word descargado

---

## 📂 ESTRUCTURA CORRECTA:

```
E:\TESLA_COTIZADOR-V3.0\
├── database\
│   └── tesla_cotizador.db          ← Debe existir (40KB aprox)
├── backend\
│   ├── crear_tablas.py             ← Script de creación
│   └── app\
│       ├── main.py                 ← CORS configurado
│       └── routers\
│           └── chat.py             ← PILIBrain integrado
└── frontend\
    └── src\
        ├── App.jsx                 ← Bug entidad arreglado
        └── components\
            └── PiliAvatar.jsx      ← Warning arreglado
```

---

## ❌ SI ALGO FALLA:

**Error: "git checkout" no funciona**
→ Ejecuta primero: `git fetch --all`

**Error: "python crear_tablas.py" no existe**
→ Usa la Opción A del PASO 2

**Error: CORS persiste**
→ Asegúrate de haber REINICIADO el backend (Ctrl+C y volver a iniciar)

**Error: "no such table" persiste**
→ Verifica que existe: `E:\TESLA_COTIZADOR-V3.0\database\tesla_cotizador.db`

---

## 📞 REPORTA:

Dime QUÉ PASO te da error y QUÉ MENSAJE exacto aparece.
