"""
Script para forzar la carga de routers y ver el error exacto
"""

import sys
sys.path.insert(0, 'e:/TESLA_COTIZADOR-V3.0/backend')

print("🔍 Intentando importar routers como lo hace main.py...")
print()

try:
    print("📦 Importando: from app.routers import chat, cotizaciones, proyectos, informes, documentos, system, auth")
    from app.routers import chat, cotizaciones, proyectos, informes, documentos, system, auth
    print("✅ ¡IMPORTACIÓN EXITOSA!")
    print()
    print("📊 Routers disponibles:")
    print(f"   - chat.router: {hasattr(chat, 'router')}")
    print(f"   - cotizaciones.router: {hasattr(cotizaciones, 'router')}")
    print(f"   - proyectos.router: {hasattr(proyectos, 'router')}")
    print(f"   - informes.router: {hasattr(informes, 'router')}")
    print(f"   - documentos.router: {hasattr(documentos, 'router')}")
    print(f"   - system.router: {hasattr(system, 'router')}")
    print(f"   - auth.router: {hasattr(auth, 'router')}")
    print()
    print("🎉 CONCLUSIÓN: Los routers se pueden importar correctamente")
    print("⚠️  El problema debe estar en cómo main.py maneja la importación")
    
except ImportError as e:
    print(f"❌ ERROR DE IMPORTACIÓN: {e}")
    print()
    print("📄 Detalles del error:")
    import traceback
    traceback.print_exc()
    print()
    print("💡 SOLUCIÓN:")
    print("   Instalar dependencias faltantes:")
    print("   pip install -r backend/requirements_professional.txt")
    
except Exception as e:
    print(f"❌ ERROR INESPERADO: {e}")
    import traceback
    traceback.print_exc()
