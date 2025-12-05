"""
Script de Auditoría Exhaustiva del Backend
Analiza estructura, responsabilidades y duplicaciones
"""

import os
from pathlib import Path
from collections import defaultdict
import json

print("=" * 80)
print("🔍 AUDITORÍA EXHAUSTIVA DE ARQUITECTURA DEL BACKEND")
print("=" * 80)
print()

backend_path = Path("e:/TESLA_COTIZADOR-V3.0/backend")

# Estructura para almacenar resultados
auditoria = {
    "total_archivos": 0,
    "total_lineas": 0,
    "duplicaciones": [],
    "estructura": {},
    "archivos_por_tipo": defaultdict(list),
    "archivos_grandes": [],
    "archivos_copy": []
}

def contar_lineas(filepath):
    """Cuenta líneas de código en un archivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0

def analizar_directorio(path, nivel=0):
    """Analiza recursivamente un directorio"""
    resultados = []
    
    try:
        for item in sorted(path.iterdir()):
            if item.name.startswith('.') or item.name == '__pycache__' or item.name == 'venv':
                continue
                
            if item.is_file():
                size = item.stat().st_size
                lineas = contar_lineas(item) if item.suffix == '.py' else 0
                
                info = {
                    "nombre": item.name,
                    "ruta": str(item.relative_to(backend_path)),
                    "tipo": "archivo",
                    "extension": item.suffix,
                    "tamaño_bytes": size,
                    "lineas": lineas,
                    "nivel": nivel
                }
                
                resultados.append(info)
                auditoria["total_archivos"] += 1
                auditoria["total_lineas"] += lineas
                auditoria["archivos_por_tipo"][item.suffix].append(info)
                
                # Detectar archivos copy
                if "copy" in item.name.lower() or item.name.endswith('.backup'):
                    auditoria["archivos_copy"].append(info)
                
                # Detectar archivos grandes
                if lineas > 500:
                    auditoria["archivos_grandes"].append(info)
                    
            elif item.is_dir():
                info = {
                    "nombre": item.name,
                    "ruta": str(item.relative_to(backend_path)),
                    "tipo": "directorio",
                    "nivel": nivel,
                    "contenido": analizar_directorio(item, nivel + 1)
                }
                resultados.append(info)
                
    except PermissionError:
        pass
        
    return resultados

print("📂 Analizando estructura del backend...")
auditoria["estructura"] = analizar_directorio(backend_path / "app")

print(f"✅ Análisis completado")
print(f"   📄 Total archivos: {auditoria['total_archivos']}")
print(f"   📝 Total líneas de código: {auditoria['total_lineas']:,}")
print(f"   🔄 Archivos duplicados (copy): {len(auditoria['archivos_copy'])}")
print(f"   📊 Archivos grandes (>500 líneas): {len(auditoria['archivos_grandes'])}")
print()

# Detectar duplicaciones por nombre base
print("🔍 Detectando duplicaciones...")
archivos_por_base = defaultdict(list)
for ext, archivos in auditoria["archivos_por_tipo"].items():
    for archivo in archivos:
        nombre_base = archivo["nombre"].replace(" copy", "").replace(" copy 2", "").replace(" copy 3", "").replace(" copy 4", "").replace(" copy 5", "").replace(" copy 6", "").replace(".backup", "")
        archivos_por_base[nombre_base].append(archivo)

duplicaciones_detectadas = {k: v for k, v in archivos_por_base.items() if len(v) > 1}
auditoria["duplicaciones"] = duplicaciones_detectadas

print(f"   ⚠️  Grupos de archivos duplicados: {len(duplicaciones_detectadas)}")
for nombre_base, archivos in list(duplicaciones_detectadas.items())[:5]:
    print(f"      - {nombre_base}: {len(archivos)} versiones")

print()

# Guardar resultados
with open("auditoria_backend_datos.json", "w", encoding="utf-8") as f:
    json.dump(auditoria, f, indent=2, ensure_ascii=False, default=str)

print("💾 Datos de auditoría guardados en: auditoria_backend_datos.json")
print()

# Generar resumen
print("=" * 80)
print("📊 RESUMEN DE AUDITORÍA")
print("=" * 80)
print()

print("📁 ARCHIVOS POR TIPO:")
for ext, archivos in sorted(auditoria["archivos_por_tipo"].items(), key=lambda x: len(x[1]), reverse=True):
    if ext:
        print(f"   {ext}: {len(archivos)} archivos")
print()

print("🔴 ARCHIVOS DUPLICADOS (TOP 10):")
for i, (nombre_base, archivos) in enumerate(list(duplicaciones_detectadas.items())[:10], 1):
    print(f"   {i}. {nombre_base}")
    for arch in archivos:
        print(f"      - {arch['ruta']} ({arch['lineas']} líneas)")
print()

print("📈 ARCHIVOS MÁS GRANDES (TOP 10):")
for i, archivo in enumerate(sorted(auditoria["archivos_grandes"], key=lambda x: x["lineas"], reverse=True)[:10], 1):
    print(f"   {i}. {archivo['nombre']}: {archivo['lineas']:,} líneas")
    print(f"      Ruta: {archivo['ruta']}")
print()

print("✅ Auditoría completada. Generando informe detallado...")
