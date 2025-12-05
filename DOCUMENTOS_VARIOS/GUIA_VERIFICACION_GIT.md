# 🔍 Guía de Verificación Git - TESLA COTIZADOR V3.0

## ⚠️ ¿No ves los archivos después de hacer pull?

Sigue estos pasos **en orden** para diagnosticar el problema:

---

## Paso 1: Verifica en qué branch estás

```bash
git status
git branch
```

**Deberías ver:**
```
On branch claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa
```

**Si estás en otro branch (main, master, etc.):**
```bash
# Cambia al branch correcto
git checkout claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa
```

---

## Paso 2: Verifica que estás en el directorio correcto

```bash
# Ver directorio actual
pwd

# Debe mostrar algo como:
# C:\Users\TuUsuario\TESLA_COTIZADOR-V3.0
# o
# /home/usuario/TESLA_COTIZADOR-V3.0
```

**Si no estás en el directorio correcto:**
```bash
cd TESLA_COTIZADOR-V3.0
```

---

## Paso 3: Descarga los últimos cambios

```bash
# Opción 1: Pull del branch específico (RECOMENDADO)
git pull origin claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa

# Opción 2: Fetch y merge
git fetch origin
git merge origin/claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa
```

---

## Paso 4: Verifica que los archivos existen

```bash
# Listar archivos en la raíz del proyecto
ls -lh *.md

# O en Windows
dir *.md

# Deberías ver archivos como:
# - DIAGNOSTICO_FINAL_Y_SOLUCION.md
# - SINCRONIZACION_SERVICIOS_COMPLETADA.md
# - CLAUDE.md
# - README.md
# etc.
```

**Verificar archivo específico:**
```bash
# En Linux/Mac
ls -lh DIAGNOSTICO_FINAL_Y_SOLUCION.md

# En Windows
dir DIAGNOSTICO_FINAL_Y_SOLUCION.md

# Debe mostrar: -rw------- 1 usuario grupo 13K Dec  3 20:18 DIAGNOSTICO_FINAL_Y_SOLUCION.md
```

---

## Paso 5: Ver últimos commits

```bash
# Ver últimos 10 commits
git log --oneline -10

# Deberías ver commits como:
# 5ab7ff4 fix: Corregir formato de .gitignore para test_diagnostico
# a6c776e chore: Ignorar archivos de prueba de diagnóstico en storage
# f54fa56 docs: Documentación completa de sincronización de servicios
# 13b73f3 feat: Sincronizar 10 servicios entre frontend y backend
# f7f0fdd feat: Sistema de diagnóstico completo + solución al problema de generación
```

---

## Paso 6: Ver qué archivos se modificaron recientemente

```bash
# Ver archivos modificados en los últimos 5 commits
git diff HEAD~5 HEAD --name-status

# Deberías ver:
# M    .gitignore
# A    DIAGNOSTICO_FINAL_Y_SOLUCION.md
# A    SINCRONIZACION_SERVICIOS_COMPLETADA.md
# A    backend/test_diagnostico_completo.py
# M    frontend/src/App.jsx
```

**Leyenda:**
- `M` = Modificado
- `A` = Agregado (nuevo archivo)
- `D` = Eliminado

---

## Paso 7: Forzar actualización (si nada más funciona)

```bash
# ⚠️ CUIDADO: Esto descartará cambios locales NO commiteados
git fetch origin
git reset --hard origin/claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa
```

**SOLO usa esto si:**
- No tienes cambios locales importantes
- Estás seguro de que quieres sobrescribir todo

---

## 🔍 Verificación Visual de Archivos Específicos

### Archivos que DEBERÍAN existir en la raíz del proyecto:

```bash
# Verificar todos a la vez
ls -lh DIAGNOSTICO_FINAL_Y_SOLUCION.md \
       SINCRONIZACION_SERVICIOS_COMPLETADA.md \
       ANALISIS_PROFUNDO_PILI.md \
       MAPA_ARQUITECTURA_EXISTENTE.md \
       CLAUDE.md

# En Windows (PowerShell)
Get-ChildItem -Name DIAGNOSTICO_FINAL_Y_SOLUCION.md,SINCRONIZACION_SERVICIOS_COMPLETADA.md,ANALISIS_PROFUNDO_PILI.md,MAPA_ARQUITECTURA_EXISTENTE.md,CLAUDE.md
```

### Archivos en backend:

```bash
# Linux/Mac
ls -lh backend/test_diagnostico_completo.py

# Windows
dir backend\test_diagnostico_completo.py
```

---

## 🛠️ Solución de Problemas Comunes

### Problema 1: "No veo los archivos en mi explorador de archivos"

**Solución:**
```bash
# Actualiza el explorador de archivos (F5)
# O abre el directorio de nuevo desde la terminal

# Linux/Mac
open .

# Windows
explorer .
```

### Problema 2: "Git dice que ya está actualizado pero no veo los archivos"

**Solución:**
```bash
# Verifica el hash del último commit
git rev-parse HEAD

# Debe mostrar: 5ab7ff44cf15333b18b7eb1dd9d19d52b1cd423e

# Compara con el remoto
git rev-parse origin/claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa

# Deben ser iguales
```

### Problema 3: "Estoy en otro branch y no sé cómo cambiar"

**Solución:**
```bash
# Ver todos los branches disponibles
git branch -a

# Cambiar al branch correcto
git checkout claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa

# Si el branch no existe localmente
git checkout -b claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa origin/claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa
```

### Problema 4: "Tengo cambios locales que no quiero perder"

**Solución:**
```bash
# Guardar cambios temporalmente
git stash save "Mis cambios locales"

# Hacer pull
git pull origin claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa

# Recuperar tus cambios
git stash pop
```

---

## 📋 Checklist Final

Marca cada item cuando lo verifiques:

- [ ] Estoy en el branch correcto: `claude/project-update-analysis-013z6LHTDTiBVUzCKu3gMBDa`
- [ ] Estoy en el directorio correcto: `TESLA_COTIZADOR-V3.0`
- [ ] Hice `git pull` exitosamente
- [ ] El último commit es: `5ab7ff4 fix: Corregir formato de .gitignore`
- [ ] Veo el archivo `DIAGNOSTICO_FINAL_Y_SOLUCION.md` en la raíz
- [ ] Veo el archivo `SINCRONIZACION_SERVICIOS_COMPLETADA.md` en la raíz
- [ ] Veo el archivo `backend/test_diagnostico_completo.py`
- [ ] Los archivos tienen contenido (no están vacíos)

---

## 🎯 Comando Completo de Verificación Rápida

Copia y pega esto en tu terminal:

```bash
echo "=== VERIFICACIÓN GIT RÁPIDA ==="
echo ""
echo "Branch actual:"
git branch | grep '*'
echo ""
echo "Último commit:"
git log --oneline -1
echo ""
echo "Archivos recientes creados:"
git diff HEAD~5 HEAD --name-status | grep '^A'
echo ""
echo "¿Existen los archivos?"
ls -lh DIAGNOSTICO_FINAL_Y_SOLUCION.md SINCRONIZACION_SERVICIOS_COMPLETADA.md backend/test_diagnostico_completo.py 2>&1 | grep -v "No such file"
echo ""
echo "=== FIN VERIFICACIÓN ==="
```

---

## 📞 Contacto

Si después de seguir todos estos pasos aún no ves los archivos, proporciona:

1. Output de `git status`
2. Output de `git log --oneline -5`
3. Output de `ls -lh *.md` (o `dir *.md` en Windows)
4. Captura de pantalla de tu explorador de archivos

---

**Última actualización:** 2025-12-04
**Versión:** 1.0
**Autor:** Claude Code Assistant
