"""
🔍 TESLA COTIZADOR - SISTEMA DE DIAGNÓSTICO COMPLETO
Verifica TODA la instalación y genera reporte de errores
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple

class TeslaDiagnostico:
    def __init__(self):
        self.errores = []
        self.advertencias = []
        self.ok = []
        self.base_path = Path(__file__).parent.parent
        
    def log_error(self, mensaje: str):
        """Registrar error"""
        self.errores.append(f"❌ {mensaje}")
        print(f"❌ ERROR: {mensaje}")
        
    def log_warning(self, mensaje: str):
        """Registrar advertencia"""
        self.advertencias.append(f"⚠️ {mensaje}")
        print(f"⚠️ WARNING: {mensaje}")
        
    def log_ok(self, mensaje: str):
        """Registrar OK"""
        self.ok.append(f"✅ {mensaje}")
        print(f"✅ OK: {mensaje}")
    
    def verificar_estructura_directorios(self) -> bool:
        """Verificar que existan todos los directorios necesarios"""
        print("\n" + "="*60)
        print("📁 VERIFICANDO ESTRUCTURA DE DIRECTORIOS")
        print("="*60)
        
        directorios_requeridos = [
            "backend",
            "backend/app",
            "backend/app/core",
            "backend/app/models",
            "backend/app/routers",
            "backend/app/services",
            "backend/app/schemas",
            "backend/templates",
            "backend/storage/generated",
            "backend/storage/uploads",
            "frontend",
            "frontend/src",
            "frontend/src/services",
        ]
        
        todo_ok = True
        for dir_path in directorios_requeridos:
            full_path = self.base_path / dir_path
            if full_path.exists():
                self.log_ok(f"Directorio existe: {dir_path}")
            else:
                self.log_error(f"Directorio NO existe: {dir_path}")
                todo_ok = False
                
        return todo_ok
    
    def verificar_archivos_criticos(self) -> bool:
        """Verificar que existan archivos críticos"""
        print("\n" + "="*60)
        print("📄 VERIFICANDO ARCHIVOS CRÍTICOS")
        print("="*60)
        
        archivos_criticos = [
            ("backend/app/main.py", "Main de FastAPI"),
            ("backend/app/__init__.py", "Init de app"),
            ("backend/app/core/config.py", "Configuración"),
            ("backend/app/core/database.py", "Base de datos"),
            ("backend/app/routers/__init__.py", "Init de routers"),
            ("backend/app/routers/cotizaciones.py", "Router cotizaciones"),
            ("backend/app/routers/proyectos.py", "Router proyectos"),
            ("backend/app/routers/documentos.py", "Router documentos"),
            ("backend/app/routers/chat.py", "Router chat"),
            ("backend/app/services/__init__.py", "Init de services"),
            ("backend/app/services/word_generator.py", "Generador Word"),
            ("backend/app/services/pdf_generator.py", "Generador PDF"),
            ("backend/.env", "Variables de entorno"),
            ("backend/requirements.txt", "Dependencias Python"),
            ("frontend/package.json", "Configuración frontend"),
            ("frontend/src/services/api.js", "API client"),
        ]
        
        todo_ok = True
        for archivo, descripcion in archivos_criticos:
            full_path = self.base_path / archivo
            if full_path.exists():
                size = full_path.stat().st_size
                self.log_ok(f"{descripcion}: {archivo} ({size} bytes)")
            else:
                self.log_error(f"{descripcion} NO existe: {archivo}")
                todo_ok = False
                
        return todo_ok
    
    def verificar_imports_main(self) -> bool:
        """Verificar imports en main.py"""
        print("\n" + "="*60)
        print("📦 VERIFICANDO IMPORTS EN MAIN.PY")
        print("="*60)
        
        main_path = self.base_path / "backend" / "app" / "main.py"
        if not main_path.exists():
            self.log_error("main.py no existe")
            return False
            
        contenido = main_path.read_text(encoding='utf-8')
        
        imports_requeridos = [
            ("from fastapi import FastAPI", "FastAPI"),
            ("from fastapi.middleware.cors import CORSMiddleware", "CORS"),
            ("app = FastAPI", "Creación de app"),
            ("app.add_middleware", "Middleware CORS"),
            ("app.include_router", "Registro de routers"),
        ]
        
        todo_ok = True
        for import_str, descripcion in imports_requeridos:
            if import_str in contenido:
                self.log_ok(f"{descripcion} encontrado")
            else:
                self.log_error(f"{descripcion} NO encontrado: {import_str}")
                todo_ok = False
                
        return todo_ok
    
    def verificar_routers_registrados(self) -> bool:
        """Verificar que los routers estén registrados"""
        print("\n" + "="*60)
        print("🔌 VERIFICANDO REGISTRO DE ROUTERS")
        print("="*60)
        
        main_path = self.base_path / "backend" / "app" / "main.py"
        if not main_path.exists():
            return False
            
        contenido = main_path.read_text(encoding='utf-8')
        
        routers_esperados = [
            ("cotizaciones", "/api/cotizaciones"),
            ("proyectos", "/api/proyectos"),
            ("documentos", "/api/documentos"),
            ("chat", "/api/chat"),
        ]
        
        todo_ok = True
        for router_name, prefix in routers_esperados:
            if f'prefix="{prefix}"' in contenido or f"prefix='{prefix}'" in contenido:
                self.log_ok(f"Router {router_name} registrado con {prefix}")
            else:
                self.log_error(f"Router {router_name} NO registrado con {prefix}")
                todo_ok = False
                
        return todo_ok
    
    def verificar_dependencias_python(self) -> bool:
        """Verificar dependencias de Python"""
        print("\n" + "="*60)
        print("🐍 VERIFICANDO DEPENDENCIAS DE PYTHON")
        print("="*60)
        
        dependencias_criticas = [
            "fastapi",
            "uvicorn",
            "sqlalchemy",
            "pydantic",
            "python-dotenv",
            "python-docx",
            "reportlab",
            "chromadb",
            "python-magic-bin",
        ]
        
        todo_ok = True
        for dep in dependencias_criticas:
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "show", dep],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    # Extraer versión
                    for line in result.stdout.split('\n'):
                        if line.startswith('Version:'):
                            version = line.split(':')[1].strip()
                            self.log_ok(f"{dep} instalado (v{version})")
                            break
                else:
                    self.log_error(f"{dep} NO instalado")
                    todo_ok = False
            except Exception as e:
                self.log_error(f"Error verificando {dep}: {str(e)}")
                todo_ok = False
                
        return todo_ok
    
    def verificar_env(self) -> bool:
        """Verificar archivo .env"""
        print("\n" + "="*60)
        print("⚙️ VERIFICANDO ARCHIVO .ENV")
        print("="*60)
        
        env_path = self.base_path / "backend" / ".env"
        if not env_path.exists():
            self.log_error(".env NO existe")
            return False
            
        contenido = env_path.read_text(encoding='utf-8')
        
        variables_importantes = [
            "DATABASE_URL",
            "GEMINI_API_KEY",
            "ALLOWED_EXTENSIONS",
        ]
        
        todo_ok = True
        for var in variables_importantes:
            if var in contenido:
                self.log_ok(f"Variable {var} encontrada")
            else:
                self.log_warning(f"Variable {var} NO encontrada")
                
        # Verificar formato de ALLOWED_EXTENSIONS
        if 'ALLOWED_EXTENSIONS=' in contenido:
            for line in contenido.split('\n'):
                if line.startswith('ALLOWED_EXTENSIONS='):
                    valor = line.split('=', 1)[1].strip()
                    if valor.startswith('[') and valor.endswith(']'):
                        self.log_ok("ALLOWED_EXTENSIONS tiene formato correcto (array JSON)")
                    else:
                        self.log_error(f"ALLOWED_EXTENSIONS formato incorrecto: {valor}")
                        todo_ok = False
                    break
                    
        return todo_ok
    
    def verificar_puertos(self) -> bool:
        """Verificar que los puertos estén libres/en uso correctamente"""
        print("\n" + "="*60)
        print("🔌 VERIFICANDO PUERTOS")
        print("="*60)
        
        import socket
        
        def check_port(port: int, nombre: str) -> bool:
            """Verificar si un puerto está en uso"""
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                self.log_ok(f"Puerto {port} ({nombre}) está EN USO - ✅ Servidor corriendo")
                return True
            else:
                self.log_warning(f"Puerto {port} ({nombre}) está LIBRE - ⚠️ Servidor NO corriendo")
                return False
        
        backend_running = check_port(8000, "Backend")
        frontend_running = check_port(3000, "Frontend")
        
        return backend_running and frontend_running
    
    def test_backend_endpoints(self) -> bool:
        """Test de endpoints del backend"""
        print("\n" + "="*60)
        print("🧪 TESTING ENDPOINTS DEL BACKEND")
        print("="*60)
        
        try:
            import requests
        except ImportError:
            self.log_error("requests no instalado - pip install requests")
            return False
        
        endpoints_test = [
            ("http://localhost:8000/", "Root"),
            ("http://localhost:8000/health", "Health"),
            ("http://localhost:8000/docs", "Documentación"),
            ("http://localhost:8000/openapi.json", "OpenAPI Schema"),
            ("http://localhost:8000/api/cotizaciones", "Cotizaciones"),
        ]
        
        todo_ok = True
        for url, nombre in endpoints_test:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    self.log_ok(f"{nombre}: {url} (200 OK)")
                elif response.status_code == 404:
                    self.log_error(f"{nombre}: {url} (404 NOT FOUND)")
                    todo_ok = False
                else:
                    self.log_warning(f"{nombre}: {url} ({response.status_code})")
            except requests.exceptions.ConnectionError:
                self.log_error(f"{nombre}: NO puede conectar a {url}")
                todo_ok = False
            except Exception as e:
                self.log_error(f"{nombre}: Error - {str(e)}")
                todo_ok = False
                
        return todo_ok
    
    def generar_reporte(self) -> str:
        """Generar reporte final"""
        print("\n" + "="*60)
        print("📊 REPORTE FINAL")
        print("="*60)
        
        total_ok = len(self.ok)
        total_warnings = len(self.advertencias)
        total_errores = len(self.errores)
        
        print(f"\n✅ Checks OK: {total_ok}")
        print(f"⚠️ Advertencias: {total_warnings}")
        print(f"❌ Errores: {total_errores}")
        
        if total_errores == 0:
            print("\n🎉 ¡TODO ESTÁ BIEN! Sistema funcionando correctamente")
            estado = "FUNCIONAL"
        elif total_errores <= 3:
            print("\n⚠️ Sistema funcional con advertencias menores")
            estado = "FUNCIONAL CON WARNINGS"
        else:
            print("\n❌ Sistema tiene ERRORES CRÍTICOS que deben corregirse")
            estado = "CON ERRORES"
        
        # Generar reporte detallado
        reporte = f"""
{'='*60}
REPORTE DE DIAGNÓSTICO - TESLA COTIZADOR V3.0
{'='*60}

Estado General: {estado}

Checks OK: {total_ok}
Advertencias: {total_warnings}
Errores Críticos: {total_errores}

{'='*60}
ERRORES ENCONTRADOS
{'='*60}
"""
        
        if self.errores:
            for error in self.errores:
                reporte += f"{error}\n"
        else:
            reporte += "✅ No se encontraron errores\n"
        
        reporte += f"""
{'='*60}
ADVERTENCIAS
{'='*60}
"""
        
        if self.advertencias:
            for warning in self.advertencias:
                reporte += f"{warning}\n"
        else:
            reporte += "✅ No hay advertencias\n"
        
        reporte += f"""
{'='*60}
ACCIONES RECOMENDADAS
{'='*60}
"""
        
        if total_errores > 0:
            reporte += "\n🔧 CORRECCIONES NECESARIAS:\n\n"
            
            if any("main.py" in e for e in self.errores):
                reporte += "1. Reemplazar backend/app/main.py con versión corregida\n"
            
            if any("Router" in e and "NO registrado" in e for e in self.errores):
                reporte += "2. Verificar registro de routers en main.py\n"
            
            if any(".env" in e for e in self.errores):
                reporte += "3. Corregir archivo .env con formato correcto\n"
            
            if any("instalado" in e for e in self.errores):
                reporte += "4. Instalar dependencias faltantes: pip install -r requirements.txt\n"
            
            if any("Puerto" in e for e in self.errores):
                reporte += "5. Iniciar backend: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000\n"
            
            if any("404" in e for e in self.errores):
                reporte += "6. Endpoints retornan 404 - routers no están registrados correctamente\n"
        else:
            reporte += "\n✅ Sistema funcionando correctamente\n"
        
        return reporte
    
    def ejecutar_diagnostico_completo(self):
        """Ejecutar diagnóstico completo"""
        print("\n" + "="*60)
        print("🔍 TESLA COTIZADOR - DIAGNÓSTICO COMPLETO")
        print("="*60)
        print(f"📁 Directorio base: {self.base_path}\n")
        
        # Ejecutar todas las verificaciones
        self.verificar_estructura_directorios()
        self.verificar_archivos_criticos()
        self.verificar_imports_main()
        self.verificar_routers_registrados()
        self.verificar_dependencias_python()
        self.verificar_env()
        self.verificar_puertos()
        self.test_backend_endpoints()
        
        # Generar reporte
        reporte = self.generar_reporte()
        
        # Guardar reporte
        reporte_path = self.base_path / "DIAGNOSTICO_REPORTE.txt"
        reporte_path.write_text(reporte, encoding='utf-8')
        print(f"\n📄 Reporte guardado en: {reporte_path}")
        
        return len(self.errores) == 0


if __name__ == "__main__":
    diagnostico = TeslaDiagnostico()
    exito = diagnostico.ejecutar_diagnostico_completo()
    
    sys.exit(0 if exito else 1)