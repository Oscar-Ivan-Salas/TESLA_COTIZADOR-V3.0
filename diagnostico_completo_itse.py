#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico EXHAUSTIVO para PILI ITSE
Captura TODOS los detalles del sistema y genera reporte completo

Ejecutar: python diagnostico_completo_itse.py
"""

import sys
import os
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Color output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

# Inicializar reporte
reporte = {
    "fecha": datetime.now().isoformat(),
    "sistema": {},
    "git": {},
    "archivos": {},
    "codigo": {},
    "caja_negra": {},
    "backend": {},
    "errores": []
}

print_header("🔍 DIAGNÓSTICO EXHAUSTIVO - PILI ITSE")
print_info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print_info(f"Directorio: {os.getcwd()}")

# ============================================================================
# 1. INFORMACIÓN DEL SISTEMA
# ============================================================================
print_header("1️⃣ INFORMACIÓN DEL SISTEMA")

try:
    # Python version
    python_version = sys.version
    print_info(f"Python: {python_version}")
    reporte["sistema"]["python_version"] = python_version

    # OS
    import platform
    os_info = f"{platform.system()} {platform.release()}"
    print_info(f"OS: {os_info}")
    reporte["sistema"]["os"] = os_info

    # Directorio actual
    cwd = os.getcwd()
    reporte["sistema"]["directorio_actual"] = cwd

    # Verificar que estamos en el proyecto
    if "TESLA_COTIZADOR" not in cwd:
        print_error(f"NO estás en el directorio del proyecto")
        print_warning(f"Directorio actual: {cwd}")
        print_warning(f"Debes estar en: .../TESLA_COTIZADOR-V3.0")
        reporte["errores"].append("Directorio incorrecto")
    else:
        print_success("Directorio correcto")

except Exception as e:
    print_error(f"Error obteniendo info del sistema: {e}")
    reporte["errores"].append(f"Sistema: {e}")

# ============================================================================
# 2. INFORMACIÓN GIT
# ============================================================================
print_header("2️⃣ INFORMACIÓN GIT")

try:
    # Branch actual
    branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
    print_info(f"Branch: {branch}")
    reporte["git"]["branch"] = branch

    # Últimos 5 commits
    commits = subprocess.check_output(["git", "log", "--oneline", "-5"], text=True).strip()
    print_info("Últimos 5 commits:")
    for line in commits.split("\n"):
        print(f"   {line}")
    reporte["git"]["commits"] = commits.split("\n")

    # Verificar commit del FIX
    if "061aa71" in commits:
        print_success("FIX CRÍTICO (061aa71) PRESENTE en el código")
        reporte["git"]["fix_presente"] = True
    else:
        print_error("FIX CRÍTICO (061aa71) NO ENCONTRADO")
        print_warning("Necesitas hacer: git pull origin <branch>")
        reporte["git"]["fix_presente"] = False
        reporte["errores"].append("Fix crítico no presente")

    # Estado de git
    status = subprocess.check_output(["git", "status", "--short"], text=True).strip()
    if status:
        print_warning(f"Archivos modificados:\n{status}")
        reporte["git"]["archivos_modificados"] = status.split("\n")
    else:
        print_success("Working tree clean")
        reporte["git"]["archivos_modificados"] = []

except Exception as e:
    print_error(f"Error con git: {e}")
    reporte["errores"].append(f"Git: {e}")

# ============================================================================
# 3. VERIFICAR ARCHIVOS CLAVE
# ============================================================================
print_header("3️⃣ VERIFICAR ARCHIVOS CLAVE")

archivos_clave = [
    "Pili_ChatBot/pili_itse_chatbot.py",
    "backend/app/routers/chat.py",
    "frontend/src/components/PiliITSEChat.jsx",
    "diagnostico_chatbot.py",
    "test_claude_api_demo.py"
]

for archivo in archivos_clave:
    path = Path(archivo)
    if path.exists():
        size = path.stat().st_size
        print_success(f"{archivo} ({size} bytes)")
        reporte["archivos"][archivo] = {"existe": True, "size": size}
    else:
        print_error(f"{archivo} NO EXISTE")
        reporte["archivos"][archivo] = {"existe": False}
        reporte["errores"].append(f"Archivo faltante: {archivo}")

# ============================================================================
# 4. VERIFICAR CÓDIGO CRÍTICO
# ============================================================================
print_header("4️⃣ VERIFICAR CÓDIGO CRÍTICO")

# Verificar línea del FIX en endpoint /pili-itse
try:
    resultado_grep = subprocess.check_output(
        ["grep", "-n", "\"datos_generados\".*resultado.get", "backend/app/routers/chat.py"],
        text=True
    ).strip()

    # Buscar la línea del endpoint /pili-itse (última ocurrencia)
    lineas = resultado_grep.split("\n")
    linea_fix = lineas[-1] if lineas else ""

    numero_linea = linea_fix.split(":")[0]
    contenido_linea = ":".join(linea_fix.split(":")[1:])

    print_info(f"Verificando línea {numero_linea} (FIX crítico en endpoint /pili-itse):")
    print(f"   {contenido_linea.strip()}")

    if "resultado.get('datos_generados')" in linea_fix or 'resultado.get("datos_generados")' in linea_fix:
        print_success("FIX APLICADO CORRECTAMENTE")
        reporte["codigo"]["linea_fix"] = {
            "numero": numero_linea,
            "contenido": contenido_linea.strip()
        }
        reporte["codigo"]["fix_aplicado"] = True
    elif "resultado.get('cotizacion')" in linea_fix or 'resultado.get("cotizacion")' in linea_fix:
        print_error("FIX NO APLICADO - Todavía usa 'cotizacion'")
        print_warning("Debe decir: resultado.get('datos_generados')")
        reporte["codigo"]["linea_fix"] = {
            "numero": numero_linea,
            "contenido": contenido_linea.strip()
        }
        reporte["codigo"]["fix_aplicado"] = False
        reporte["errores"].append(f"Fix no aplicado en línea {numero_linea}")
    else:
        print_warning(f"Mapeo de datos_generados encontrado pero formato inesperado")
        reporte["codigo"]["linea_fix"] = {
            "numero": numero_linea,
            "contenido": contenido_linea.strip()
        }
        reporte["codigo"]["fix_aplicado"] = False

except Exception as e:
    print_error(f"Error verificando chat.py: {e}")
    reporte["errores"].append(f"Verificación chat.py: {e}")

# Verificar que pili_itse_bot está instanciado
try:
    resultado = subprocess.check_output(
        ["grep", "-n", "pili_itse_bot = PILIITSEChatBot()", "backend/app/routers/chat.py"],
        text=True
    ).strip()
    print_success(f"Instancia pili_itse_bot encontrada: {resultado.split(':')[0]}")
    reporte["codigo"]["instancia_bot"] = resultado
except Exception as e:
    print_error(f"Instancia pili_itse_bot NO encontrada")
    reporte["errores"].append("Instancia bot no encontrada")

# ============================================================================
# 5. PROBAR CAJA NEGRA AISLADA
# ============================================================================
print_header("5️⃣ PROBAR CAJA NEGRA AISLADA")

try:
    sys.path.insert(0, os.getcwd())
    from Pili_ChatBot.pili_itse_chatbot import PILIITSEChatBot

    print_success("Import de PILIITSEChatBot exitoso")

    bot = PILIITSEChatBot()
    print_success("Instancia creada exitosamente")

    # Test 1: Estado inicial
    resultado = bot.procesar("", None)
    etapa = resultado['estado']['etapa']
    print_info(f"Test 1 (inicial): etapa={etapa}")

    if etapa == "categoria":
        print_success("Estado inicial correcto")
    else:
        print_error(f"Estado inicial incorrecto: {etapa}")
        reporte["errores"].append(f"Estado inicial: {etapa}")

    # Test 2: Procesar SALUD
    resultado = bot.procesar("SALUD", {
        'etapa': 'categoria',
        'categoria': None,
        'tipo': None,
        'area': None,
        'pisos': None,
        'riesgo': None
    })

    etapa = resultado['estado']['etapa']
    categoria = resultado['estado']['categoria']

    print_info(f"Test 2 (SALUD): etapa={etapa}, categoria={categoria}")

    if etapa == "tipo" and categoria == "SALUD":
        print_success("Caja negra procesa correctamente: categoria → tipo")
        reporte["caja_negra"]["test_salud"] = {"etapa": etapa, "categoria": categoria, "exitoso": True}
    else:
        print_error(f"Caja negra NO procesa correctamente")
        print_error(f"Esperado: etapa=tipo, categoria=SALUD")
        print_error(f"Recibido: etapa={etapa}, categoria={categoria}")
        reporte["caja_negra"]["test_salud"] = {"etapa": etapa, "categoria": categoria, "exitoso": False}
        reporte["errores"].append(f"Caja negra: etapa={etapa}, categoria={categoria}")

    # Test 3: Flujo completo
    print_info("Test 3: Flujo completo...")
    estado = {}

    pasos = [
        ("", "categoria"),
        ("COMERCIO", "tipo"),
        ("Tienda", "area"),
        ("150", "pisos"),
        ("2", "cotizacion")
    ]

    todos_ok = True
    for i, (mensaje, etapa_esperada) in enumerate(pasos, 1):
        resultado = bot.procesar(mensaje, estado)
        estado = resultado['estado']
        etapa_actual = estado['etapa']

        if etapa_actual == etapa_esperada:
            print_success(f"   Paso {i}: {mensaje or 'inicio'} → {etapa_actual} ✅")
        else:
            print_error(f"   Paso {i}: {mensaje or 'inicio'} → {etapa_actual} (esperado: {etapa_esperada}) ❌")
            todos_ok = False

    if todos_ok:
        print_success("Flujo completo exitoso")

        # Verificar datos_generados
        datos_gen = resultado.get('datos_generados')
        if datos_gen:
            items = datos_gen.get('items', [])
            print_success(f"datos_generados presente: {len(items)} items")
            print_info(f"   Subtotal: {datos_gen.get('subtotal')}")
            print_info(f"   IGV: {datos_gen.get('igv')}")
            print_info(f"   Total: {datos_gen.get('total')}")
            reporte["caja_negra"]["datos_generados"] = {
                "items_count": len(items),
                "subtotal": datos_gen.get('subtotal'),
                "igv": datos_gen.get('igv'),
                "total": datos_gen.get('total')
            }
        else:
            print_error("datos_generados NO presente")
            reporte["errores"].append("datos_generados no presente en caja negra")
    else:
        print_error("Flujo completo FALLÓ")
        reporte["errores"].append("Flujo completo falló")

except Exception as e:
    print_error(f"Error probando caja negra: {e}")
    import traceback
    traceback.print_exc()
    reporte["errores"].append(f"Caja negra: {e}")

# ============================================================================
# 6. VERIFICAR BACKEND
# ============================================================================
print_header("6️⃣ VERIFICAR BACKEND")

try:
    # Verificar si backend está corriendo
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8000))
    sock.close()

    if result == 0:
        print_success("Backend está CORRIENDO en puerto 8000")
        reporte["backend"]["corriendo"] = True

        # Hacer request de prueba
        try:
            import requests

            print_info("Haciendo request de prueba al endpoint /pili-itse...")

            response = requests.post(
                'http://localhost:8000/api/chat/pili-itse',
                json={
                    'mensaje': 'SALUD',
                    'conversation_state': {
                        'etapa': 'categoria',
                        'categoria': None,
                        'tipo': None,
                        'area': None,
                        'pisos': None,
                        'riesgo': None
                    }
                },
                timeout=10
            )

            print_success(f"Status: {response.status_code}")

            data = response.json()

            print_info("Respuesta del backend:")
            print(f"   success: {data.get('success')}")
            print(f"   respuesta: {data.get('respuesta', '')[:60]}...")

            estado = data.get('conversation_state', {})
            print(f"   Estado devuelto:")
            print(f"      etapa: {estado.get('etapa')}")
            print(f"      categoria: {estado.get('categoria')}")

            datos_gen = data.get('datos_generados')
            if datos_gen:
                print_success(f"   datos_generados PRESENTE")
                if isinstance(datos_gen, dict) and 'items' in datos_gen:
                    print_success(f"      items: {len(datos_gen['items'])} items")
                    reporte["backend"]["datos_generados_presente"] = True
                else:
                    print_warning(f"      datos_generados sin estructura 'items'")
                    print_warning(f"      Contenido: {datos_gen}")
                    reporte["backend"]["datos_generados_presente"] = False
            else:
                print_error(f"   datos_generados AUSENTE o NULL")
                reporte["backend"]["datos_generados_presente"] = False
                reporte["errores"].append("Backend no devuelve datos_generados")

            # Verificar si el estado avanzó
            if estado.get('etapa') == 'tipo' and estado.get('categoria') == 'SALUD':
                print_success("Backend procesa correctamente: categoria → tipo ✅")
                reporte["backend"]["procesa_correctamente"] = True
            else:
                print_error(f"Backend NO procesa correctamente")
                print_error(f"Esperado: etapa=tipo, categoria=SALUD")
                print_error(f"Recibido: etapa={estado.get('etapa')}, categoria={estado.get('categoria')}")
                reporte["backend"]["procesa_correctamente"] = False
                reporte["errores"].append(f"Backend estado incorrecto: {estado}")

            reporte["backend"]["response"] = {
                "status_code": response.status_code,
                "conversation_state": estado,
                "datos_generados": datos_gen
            }

        except requests.exceptions.RequestException as e:
            print_error(f"Error haciendo request: {e}")
            reporte["errores"].append(f"Request backend: {e}")
        except Exception as e:
            print_error(f"Error procesando respuesta: {e}")
            reporte["errores"].append(f"Procesamiento respuesta: {e}")

    else:
        print_error("Backend NO está corriendo")
        print_warning("Debes iniciar: cd backend && uvicorn app.main:app --reload")
        reporte["backend"]["corriendo"] = False
        reporte["errores"].append("Backend no está corriendo")

except Exception as e:
    print_error(f"Error verificando backend: {e}")
    reporte["errores"].append(f"Verificación backend: {e}")

# ============================================================================
# 7. GENERAR REPORTE
# ============================================================================
print_header("7️⃣ GENERANDO REPORTE")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
reporte_file = f"REPORTE_DIAGNOSTICO_{timestamp}.json"

try:
    with open(reporte_file, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)

    print_success(f"Reporte guardado en: {reporte_file}")

    # Generar resumen
    print_header("📊 RESUMEN")

    errores_count = len(reporte["errores"])

    if errores_count == 0:
        print_success("✅ TODOS LOS TESTS PASARON - SISTEMA FUNCIONAL")
    else:
        print_error(f"❌ {errores_count} ERRORES ENCONTRADOS")
        print("\nErrores:")
        for i, error in enumerate(reporte["errores"], 1):
            print(f"   {i}. {error}")

    # Verificaciones críticas
    print("\nVerificaciones críticas:")

    fix_presente = reporte["git"].get("fix_presente", False)
    print(f"   FIX crítico (061aa71): {'✅' if fix_presente else '❌'}")

    fix_aplicado = reporte["codigo"].get("fix_aplicado", False)
    print(f"   FIX aplicado (línea 4710): {'✅' if fix_aplicado else '❌'}")

    caja_negra_ok = reporte["caja_negra"].get("test_salud", {}).get("exitoso", False)
    print(f"   Caja negra funcional: {'✅' if caja_negra_ok else '❌'}")

    backend_corriendo = reporte["backend"].get("corriendo", False)
    print(f"   Backend corriendo: {'✅' if backend_corriendo else '❌'}")

    if backend_corriendo:
        backend_ok = reporte["backend"].get("procesa_correctamente", False)
        print(f"   Backend procesa correctamente: {'✅' if backend_ok else '❌'}")

        datos_gen = reporte["backend"].get("datos_generados_presente", False)
        print(f"   datos_generados presente: {'✅' if datos_gen else '❌'}")

    print(f"\n📄 Reporte completo: {reporte_file}")
    print(f"   Comparte este archivo para análisis detallado")

except Exception as e:
    print_error(f"Error generando reporte: {e}")

print_header("🏁 DIAGNÓSTICO COMPLETADO")
