import sys
sys.path.insert(0, 'e:/TESLA_COTIZADOR-V3.0/backend')

print("=" * 60)
print("🔍 DIAGNÓSTICO DE IMPORTACIÓN DE ROUTERS")
print("=" * 60)

# Test 1: Importar __init__.py
print("\n1️⃣ Intentando importar app.routers...")
try:
    import app.routers
    print("✅ app.routers importado correctamente")
    print(f"   Contenido: {dir(app.routers)}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Importar chat_router
print("\n2️⃣ Intentando importar chat_router...")
try:
    from app.routers import chat_router
    print(f"✅ chat_router importado: {type(chat_router)}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Importar documentos_router
print("\n3️⃣ Intentando importar documentos_router...")
try:
    from app.routers import documentos_router
    print(f"✅ documentos_router importado: {type(documentos_router)}")
except Exception as e:
    print(f"❌ Error importando documentos_router: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Importar file_processor directamente
print("\n4️⃣ Intentando importar file_processor...")
try:
    from app.services import file_processor
    print(f"✅ file_processor importado: {type(file_processor)}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Importar magic
print("\n5️⃣ Intentando importar magic...")
try:
    import magic
    print(f"✅ magic importado: {magic}")
    print(f"   Versión: {magic.__version__ if hasattr(magic, '__version__') else 'N/A'}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("FIN DEL DIAGNÓSTICO")
print("=" * 60)
