"""
Script para crear 30 clientes de prueba usando la API web
Genera datos realistas de empresas peruanas
"""
import requests
import time

# URL de la API
API_URL = "http://localhost:8000/api/clientes/"

# Lista de 30 clientes de prueba con datos realistas
clientes_prueba = [
    {"nombre": "CONSTRUCTORA ANDES S.A.C.", "ruc": "20601234567", "direccion": "Av. Ferrocarril 1234, Huancayo", "telefono": "964123456", "email": "contacto@constructoraandes.com"},
    {"nombre": "INVERSIONES MANTARO E.I.R.L.", "ruc": "20601234568", "direccion": "Jr. Real 456, Huancayo", "telefono": "964234567", "email": "ventas@inversionesmantaro.com"},
    {"nombre": "GRUPO EMPRESARIAL WANKA S.A.", "ruc": "20601234569", "direccion": "Av. Huancavelica 789, Huancayo", "telefono": "964345678", "email": "info@grupowanka.com"},
    {"nombre": "COMERCIAL JUNIN S.R.L.", "ruc": "20601234570", "direccion": "Jr. Ancash 321, Huancayo", "telefono": "964456789", "email": "comercial@comercialjunin.com"},
    {"nombre": "SERVICIOS GENERALES PERU S.A.C.", "ruc": "20601234571", "direccion": "Av. Mariscal Castilla 654, Huancayo", "telefono": "964567890", "email": "servicios@sgperu.com"},
    {"nombre": "MINERA CENTRAL S.A.", "ruc": "20601234572", "direccion": "Carretera Central Km 15, La Oroya", "telefono": "964678901", "email": "operaciones@mineracentral.com"},
    {"nombre": "AGROINDUSTRIAS VALLE S.A.C.", "ruc": "20601234573", "direccion": "Av. Agricultura 987, Concepción", "telefono": "964789012", "email": "contacto@agroindustriasvalle.com"},
    {"nombre": "TRANSPORTES RAPIDOS S.R.L.", "ruc": "20601234574", "direccion": "Jr. Comercio 147, Huancayo", "telefono": "964890123", "email": "logistica@transportesrapidos.com"},
    {"nombre": "HOTEL TURISMO JUNIN S.A.", "ruc": "20601234575", "direccion": "Av. Giráldez 258, Huancayo", "telefono": "964901234", "email": "reservas@hotelturismojunin.com"},
    {"nombre": "DISTRIBUIDORA ANDINA E.I.R.L.", "ruc": "20601234576", "direccion": "Jr. Puno 369, Huancayo", "telefono": "965012345", "email": "ventas@distribuidoraandina.com"},
    {"nombre": "TEXTILES PERU CENTRAL S.A.C.", "ruc": "20601234577", "direccion": "Av. Industrial 741, Huancayo", "telefono": "965123456", "email": "produccion@textilesperu.com"},
    {"nombre": "CONSULTORES ASOCIADOS S.A.", "ruc": "20601234578", "direccion": "Jr. Lima 852, Huancayo", "telefono": "965234567", "email": "info@consultoresasociados.com"},
    {"nombre": "INMOBILIARIA CENTRO S.R.L.", "ruc": "20601234579", "direccion": "Av. San Carlos 963, Huancayo", "telefono": "965345678", "email": "ventas@inmobiliariacentro.com"},
    {"nombre": "ALIMENTOS NUTRITIVOS S.A.C.", "ruc": "20601234580", "direccion": "Jr. Ayacucho 159, Huancayo", "telefono": "965456789", "email": "contacto@alimentosnutritivos.com"},
    {"nombre": "TECNOLOGIA DIGITAL PERU S.A.", "ruc": "20601234581", "direccion": "Av. Tecnológica 357, Huancayo", "telefono": "965567890", "email": "soporte@tecnodigitalperu.com"},
    {"nombre": "FARMACEUTICA SALUD S.A.C.", "ruc": "20601234582", "direccion": "Jr. Salud 468, Huancayo", "telefono": "965678901", "email": "ventas@farmaceuticasalud.com"},
    {"nombre": "EDUCACION SUPERIOR S.R.L.", "ruc": "20601234583", "direccion": "Av. Universitaria 579, Huancayo", "telefono": "965789012", "email": "admision@educacionsuperior.com"},
    {"nombre": "METALMECANICA ANDES S.A.", "ruc": "20601234584", "direccion": "Parque Industrial Mz A Lt 5, Huancayo", "telefono": "965890123", "email": "produccion@metalmecanicaandes.com"},
    {"nombre": "SEGURIDAD INTEGRAL S.A.C.", "ruc": "20601234585", "direccion": "Jr. Seguridad 680, Huancayo", "telefono": "965901234", "email": "operaciones@seguridadintegral.com"},
    {"nombre": "ENERGIA RENOVABLE PERU S.A.", "ruc": "20601234586", "direccion": "Av. Ecológica 791, Huancayo", "telefono": "966012345", "email": "proyectos@energiarenovable.com"},
    {"nombre": "LABORATORIOS CLINICOS S.R.L.", "ruc": "20601234587", "direccion": "Jr. Medicina 802, Huancayo", "telefono": "966123456", "email": "resultados@laboratoriosclinicos.com"},
    {"nombre": "PUBLICIDAD CREATIVA S.A.C.", "ruc": "20601234588", "direccion": "Av. Marketing 913, Huancayo", "telefono": "966234567", "email": "creatividad@publicidadcreativa.com"},
    {"nombre": "ARQUITECTURA MODERNA S.A.", "ruc": "20601234589", "direccion": "Jr. Diseño 124, Huancayo", "telefono": "966345678", "email": "proyectos@arquitecturamoderna.com"},
    {"nombre": "GANADERIA VALLE VERDE S.A.C.", "ruc": "20601234590", "direccion": "Fundo Los Pastos Km 8, Huancayo", "telefono": "966456789", "email": "ventas@ganaderiavalle.com"},
    {"nombre": "IMPORTACIONES GLOBALES S.R.L.", "ruc": "20601234591", "direccion": "Av. Comercio Internacional 235, Huancayo", "telefono": "966567890", "email": "importaciones@globalimport.com"},
    {"nombre": "RESTAURANTE GOURMET S.A.C.", "ruc": "20601234592", "direccion": "Jr. Gastronomía 346, Huancayo", "telefono": "966678901", "email": "reservas@restaurantegourmet.com"},
    {"nombre": "CARPINTERIA FINA S.A.", "ruc": "20601234593", "direccion": "Av. Artesanía 457, Huancayo", "telefono": "966789012", "email": "pedidos@carpinteriafina.com"},
    {"nombre": "LAVANDERIA INDUSTRIAL S.A.C.", "ruc": "20601234594", "direccion": "Jr. Limpieza 568, Huancayo", "telefono": "966890123", "email": "servicios@lavanderiaindustrial.com"},
    {"nombre": "EVENTOS CORPORATIVOS S.R.L.", "ruc": "20601234595", "direccion": "Av. Celebraciones 679, Huancayo", "telefono": "966901234", "email": "eventos@eventoscorporativos.com"},
    {"nombre": "RECICLAJE ECOLOGICO S.A.C.", "ruc": "20601234596", "direccion": "Parque Ecológico Mz B Lt 3, Huancayo", "telefono": "967012345", "email": "contacto@reciclajeecologico.com"}
]

def crear_clientes():
    """Crea los 30 clientes usando la API"""
    print("🚀 Iniciando creación de 30 clientes de prueba...\n")
    
    exitosos = 0
    fallidos = 0
    
    for i, cliente in enumerate(clientes_prueba, 1):
        try:
            print(f"[{i}/30] Creando: {cliente['nombre'][:40]}...")
            
            response = requests.post(API_URL, json=cliente, timeout=10)
            
            if response.status_code == 200 or response.status_code == 201:
                print(f"   ✅ Creado exitosamente (ID: {response.json().get('id', 'N/A')})")
                exitosos += 1
            else:
                print(f"   ❌ Error {response.status_code}: {response.text[:100]}")
                fallidos += 1
            
            # Pequeña pausa para no saturar el servidor
            time.sleep(0.3)
            
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Error: No se puede conectar al servidor en {API_URL}")
            print("   ℹ️  Asegúrate de que el backend esté corriendo en http://localhost:8000")
            fallidos += 1
            break
        except Exception as e:
            print(f"   ❌ Error inesperado: {str(e)}")
            fallidos += 1
    
    print(f"\n{'='*60}")
    print(f"📊 RESUMEN:")
    print(f"   ✅ Exitosos: {exitosos}")
    print(f"   ❌ Fallidos: {fallidos}")
    print(f"   📈 Total: {exitosos + fallidos}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    print("="*60)
    print("  CREADOR DE CLIENTES DE PRUEBA - TESLA COTIZADOR v3.0")
    print("="*60)
    print(f"API Endpoint: {API_URL}")
    print(f"Total de clientes a crear: {len(clientes_prueba)}")
    print("="*60 + "\n")
    
    input("Presiona ENTER para comenzar...")
    crear_clientes()
    
    print("\n✨ Proceso completado. Puedes verificar los clientes en la aplicación web.")
