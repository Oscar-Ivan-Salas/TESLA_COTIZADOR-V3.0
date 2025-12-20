# 🔧 INSTRUCCIONES PARA ACTUALIZAR TU PC LOCAL

**Fecha:** 20 de Diciembre 2025
**Problema resuelto:** Documentos Word/PDF se generaban vacíos sin datos del cliente

---

## ✅ PROBLEMA ENCONTRADO Y CORREGIDO

### El Error:
- `word_generator.py` esperaba `cliente` como **STRING**
- El frontend envía `cliente` como **OBJETO** `{nombre, ruc, email, ...}`
- Por eso los documentos mostraban: `Cliente: [Cliente por definir]`
- Los datos del formulario NO se insertaban en el documento

### La Solución:
- ✅ Corregido `word_generator.py` líneas 596-641
- ✅ Ahora detecta si cliente es string u objeto
- ✅ Extrae: nombre, RUC, dirección, teléfono, email
- ✅ Muestra TODOS los datos del cliente en el Word/PDF

---

## 📥 CÓMO ACTUALIZAR TU PC LOCAL

### OPCIÓN 1: Pull desde GitHub (Recomendado)

```bash
# 1. Ir a tu carpeta del proyecto en tu PC
cd C:\Users\TuUsuario\TESLA_COTIZADOR-V3.0
# o en Linux/Mac:
cd ~/TESLA_COTIZADOR-V3.0

# 2. Ver en qué branch estás
git branch

# 3. Traer los cambios del repositorio
git pull origin claude/claude-md-miqrk3a6qr7npunb-01QYdNbWfxau46szuGTVYEeo

# Si estás en otro branch, primero cambia:
git checkout claude/claude-md-miqrk3a6qr7npunb-01QYdNbWfxau46szuGTVYEeo
git pull
```

### OPCIÓN 2: Descargar archivo específico

Si solo quieres el archivo corregido:

1. Ve a GitHub → tu repositorio
2. Navega a: `backend/app/services/word_generator.py`
3. Click en "Raw" → Copiar todo el contenido
4. En tu PC, pega el contenido en el archivo local

---

## 🚀 DESPUÉS DE ACTUALIZAR

### 1. Reiniciar Backend

```bash
# Detener el backend actual (Ctrl+C)

# Ir a la carpeta backend
cd backend

# Iniciar de nuevo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Espera a ver este mensaje:
# "Application startup complete"
```

### 2. Limpiar Caché del Navegador

**En Chrome/Edge/Brave:**
- Presiona **Ctrl + Shift + R** (Windows)
- O **Cmd + Shift + R** (Mac)

**O método más fuerte:**
- F12 → Click derecho en botón Recargar
- "Vaciar caché y volver a cargar de forma forzada"

### 3. Probar Generación

1. Ve a http://localhost:3000
2. Crea una nueva cotización
3. Llena los datos del cliente:
   - Nombre: Rogelio Infantas Contreras
   - RUC: 20601140740
   - Dirección: Jr. Jorge Chavez 736
   - Teléfono: 906315961
   - Email: rogelio.infantas@gmail.com
4. Agrega items con precios
5. Click en **Descargar Word**

---

## ✅ RESULTADO ESPERADO

**ANTES (mal):**
```
Cliente: [Cliente por definir]
Proyecto:
Fecha: 19/12/2025

Subtotal: S/ 0.00
IGV (18%): S/ 0.00
TOTAL: S/ 0.00
```

**AHORA (correcto):**
```
Cliente: Rogelio Infantas Contreras
RUC: 20601140740
Dirección: Jr. Jorge Chavez 736
Teléfono: 906315961
Email: rogelio.infantas@gmail.com
Proyecto: Instalación Eléctrica
Número: COTIZACION-20251220123456
Fecha: 20/12/2025

DETALLE DE ITEMS:
-----------------------------------------
DESCRIPCIÓN    CANT.  UND.  P.UNIT.  TOTAL
Tablero         1     und   S/ 450   S/ 450
Cableado       50     m     S/ 2.50  S/ 125
Tomacorrientes 10     und   S/ 15    S/ 150
-----------------------------------------

Subtotal: S/ 725.00
IGV (18%): S/ 130.50
TOTAL: S/ 855.50
```

---

## 🔍 VERIFICAR QUE FUNCIONÓ

**Logs del Backend:**

Cuando presiones "Descargar Word", deberías ver en la terminal del backend:

```
📄 Generando documento Word profesional con datos: COTIZACION-XXXXX
👤 Cliente: Rogelio Infantas Contreras
✅ Documento procesado: COTIZACION-XXXXX - Rogelio Infantas Contreras
✅ PILI documento generado: cotizacion-simple_Rogelio_Infantas_Contreras_XXXXX.docx
```

**Nombre del archivo descargado:**

Antes: `e1eb1ee2-1125-4c69-b92b-3fb5a207ee21.docx` ❌
Ahora: `COTIZACION_Rogelio_Infantas_Contreras_2025-12-20.docx` ✅

---

## 🆘 SI AÚN NO FUNCIONA

1. **Verifica que tienes el archivo correcto:**
   ```bash
   cd backend/app/services
   grep -n "isinstance(cliente, dict)" word_generator.py
   ```

   Deberías ver: `609:        if isinstance(cliente, dict):`

2. **Verifica que el backend se reinició:**
   - Debe aparecer: `Application startup complete`
   - Si no, detén (Ctrl+C) y vuelve a iniciar

3. **Muéstrame los logs:**
   - Copia TODOS los logs del backend cuando presiones "Descargar Word"
   - Envíamelos para analizar qué está pasando

---

## 📊 COMMITS APLICADOS

```
a356156 - fix(backend): Manejar cliente como objeto en word_generator
1448bef - fix(backend): Usar word_generator profesional
428a239 - fix(frontend): Nombres descriptivos para documentos
```

---

## 🎯 RESUMEN EJECUTIVO

**Cambio principal:** `backend/app/services/word_generator.py` líneas 596-641

**Antes:**
```python
("Cliente:", datos.get("cliente", "[Cliente por definir]")),
```

**Ahora:**
```python
cliente = datos.get("cliente", "[Cliente por definir]")
if isinstance(cliente, dict):
    nombre_cliente = cliente.get("nombre", "[Cliente]")
    ruc_cliente = cliente.get("ruc", "")
    direccion_cliente = cliente.get("direccion", "")
    # ... extrae todos los campos
```

**Resultado:** Los documentos Word/PDF ahora muestran todos los datos del cliente correctamente.

---

**Tesla Electricidad y Automatización S.A.C.**
Sistema Tesla Cotizador V4.0
