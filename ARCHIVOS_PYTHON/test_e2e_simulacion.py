import requests
import os
import time

BASE_URL = "http://127.0.0.1:8000"

# 1. Login (autenticación dummy)
def test_login():
    url = f"{BASE_URL}/api/auth/login"
    data = {"username": "testuser", "password": "testpass"}
    r = requests.post(url, json=data)
    if r.status_code == 200 and "access_token" in r.json():
        print("[OK] Login exitoso")
        return r.json()["access_token"]
    print(f"[FAIL] Login: {r.status_code} {r.text}")
    return None

# 2. Probar endpoints protegidos
def test_endpoint(path, token, payload=None, method="post"):
    url = f"{BASE_URL}{path}"
    headers = {"Authorization": f"Bearer {token}"}
    if method == "post":
        r = requests.post(url, json=payload or {}, headers=headers)
    else:
        r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print(f"[OK] {path} -> {r.json() if r.headers.get('content-type','').startswith('application/json') else 'Archivo descargado'}")
        return r
    print(f"[FAIL] {path}: {r.status_code} {r.text}")
    return None

# 3. Probar chat inteligente
def test_chat(token):
    payload = {
        "tipo_flujo": "profesional",
        "mensaje": "¿Cuánto cuesta una instalación eléctrica residencial de 100m2?",
        "historial": [],
        "contexto_adicional": "",
        "archivos_procesados": [],
        "generar_html": False
    }
    r = test_endpoint("/api/chat/", token, payload)
    if r and r.status_code == 200:
        respuesta = r.json().get("respuesta") or str(r.json())
        print(f"[CHAT] Respuesta: {respuesta}")
        if "no entiendo" in respuesta.lower() or "demo" in respuesta.lower():
            print("[WARN] El chat parece estar en modo demo o no es inteligente.")
        else:
            print("[OK] El chat responde de forma inteligente.")

# 4. Probar generación de cotización
def test_cotizacion(token):
    payload = {"cliente": "Cliente Demo", "proyecto": "Proyecto Demo", "items": [{"descripcion": "Cableado", "cantidad": 10, "unidad": "m", "precio_unitario": 5.0}]}
    r = test_endpoint("/api/cotizaciones/", token, payload)
    if r and r.status_code == 200:
        print("[OK] Cotización generada")

# 5. Probar generación de proyecto
def test_proyecto(token):
    payload = {"cliente": "Cliente Demo", "nombre_proyecto": "Proyecto Demo", "fases": [{"nombre": "Fase 1", "duracion": "5 días", "estado": "pendiente"}]}
    r = test_endpoint("/api/proyectos/", token, payload)
    if r and r.status_code == 200:
        print("[OK] Proyecto generado")

# 6. Probar generación de informe
def test_informe(token):
    payload = {"cliente": "Cliente Demo", "titulo_informe": "Informe Demo", "secciones": ["Resumen", "Conclusiones"]}
    r = test_endpoint("/api/informes/", token, payload)
    if r and r.status_code == 200:
        print("[OK] Informe generado")

# 7. Verificar archivos generados
def check_files():
    storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "storage", "generados"))
    print(f"[INFO] Verificando archivos en {storage_dir}")
    if os.path.exists(storage_dir):
        files = os.listdir(storage_dir)
        if files:
            print(f"[OK] Archivos generados: {files}")
        else:
            print("[FAIL] No se generaron archivos en storage/generados")
    else:
        print("[FAIL] Directorio de storage no existe")

def main():
    print("==== SIMULACIÓN INTEGRAL TESLA COTIZADOR ====")
    token = test_login()
    if not token:
        print("[FATAL] No se pudo obtener token. Abortando.")
        return
    time.sleep(1)
    test_chat(token)
    time.sleep(1)
    test_cotizacion(token)
    time.sleep(1)
    test_proyecto(token)
    time.sleep(1)
    test_informe(token)
    time.sleep(1)
    check_files()
    print("==== FIN DE SIMULACIÓN ====")

if __name__ == "__main__":
    main()
