"""
Script para crear datos DEMO para pruebas
Ejecutar: python crear_datos_demo.py
"""
import sys
from pathlib import Path

# Agregar el directorio app al path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal, engine, Base
from app.models.cliente import Cliente
from app.models.cotizacion import Cotizacion
from app.models.proyecto import Proyecto, EstadoProyecto
from datetime import datetime, timedelta

def crear_datos_demo():
    """Crea clientes, cotizaciones y proyectos de prueba"""

    print("🚀 Creando datos DEMO para pruebas...")

    # Crear todas las tablas si no existen
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas/verificadas")

    db = SessionLocal()

    try:
        # ============================================
        # CLIENTES DEMO - 50 CLIENTES VARIADOS
        # ============================================
        print("\n📋 Creando 50 clientes DEMO...")

        # Plantillas de datos
        empresas_construccion = ["CONSTRUCTORA", "EDIFICACIONES", "GRUPO CONSTRUCTOR", "INGENIEROS", "OBRAS"]
        empresas_industria = ["INDUSTRIAS", "MANUFACTURA", "FABRICA", "CORPORACION", "PRODUCTORA"]
        empresas_comercio = ["COMERCIAL", "DISTRIBUIDORA", "IMPORTADORA", "EXPORTADORA", "TRADING"]
        empresas_servicios = ["SERVICIOS", "CONSULTORES", "ASESORES", "SOLUCIONES", "SISTEMAS"]
        empresas_educacion = ["COLEGIO", "UNIVERSIDAD", "INSTITUTO", "ACADEMIA", "CENTRO EDUCATIVO"]
        empresas_salud = ["HOSPITAL", "CLINICA", "CENTRO MEDICO", "POLICLINICO", "SANATORIO"]

        nombres = ["ALFA", "BETA", "GAMMA", "DELTA", "OMEGA", "SIGMA", "TESLA", "EDISON", "VOLTA", "FARADAY",
                   "MAXWELL", "OHM", "WATT", "AMPERE", "HERTZ", "JOULE", "NEWTON", "PASCAL", "KELVIN", "GAUSS"]

        ciudades_peru = [
            "Lima", "Arequipa", "Cusco", "Trujillo", "Chiclayo", "Piura", "Iquitos", "Huancayo",
            "Tacna", "Ica", "Juliaca", "Pucallpa", "Chimbote", "Huánuco", "Tarapoto", "Cajamarca",
            "Puno", "Sullana", "Ayacucho", "Chincha", "Huaraz", "Tumbes", "Talara", "Jaén"
        ]

        industrias = ["construccion", "arquitectura", "industrial", "mineria", "educacion", "salud", "retail", "residencial"]

        clientes_demo = []

        # Generar 50 clientes
        for i in range(1, 51):
            # Seleccionar tipo de empresa
            if i <= 15:
                prefijo = empresas_construccion[i % len(empresas_construccion)]
                industria = "construccion"
            elif i <= 25:
                prefijo = empresas_industria[(i-15) % len(empresas_industria)]
                industria = "industrial"
            elif i <= 35:
                prefijo = empresas_comercio[(i-25) % len(empresas_comercio)]
                industria = "retail"
            elif i <= 40:
                prefijo = empresas_educacion[(i-35) % len(empresas_educacion)]
                industria = "educacion"
            elif i <= 45:
                prefijo = empresas_salud[(i-40) % len(empresas_salud)]
                industria = "salud"
            else:
                prefijo = empresas_servicios[(i-45) % len(empresas_servicios)]
                industria = "arquitectura"

            nombre_empresa = nombres[(i-1) % len(nombres)]
            razon_social = f"{prefijo} {nombre_empresa} S.A.C."

            # Generar RUC único
            ruc_base = 20100000000 + (i * 1000)
            ruc = str(ruc_base)

            # Ciudad aleatoria
            ciudad = ciudades_peru[(i-1) % len(ciudades_peru)]

            # Email y web
            slug = nombre_empresa.lower()
            email = f"contacto@{slug}.com.pe"
            web = f"www.{slug}.com.pe"

            # Teléfono
            telefono = f"9{str(10000000 + i * 1000)[:8]}"

            # Nombres de contacto variados
            nombres_contacto = ["Juan", "María", "Carlos", "Ana", "Roberto", "Patricia", "Luis", "Carmen", "Jorge", "Rosa"]
            apellidos_contacto = ["Pérez", "García", "Rodríguez", "López", "Martínez", "González", "Fernández", "Sánchez", "Ramírez", "Torres"]
            contacto_nombre = f"{nombres_contacto[i % len(nombres_contacto)]} {apellidos_contacto[i % len(apellidos_contacto)]}"

            cargos = ["Gerente General", "Jefe de Proyectos", "Jefe de Compras", "Gerente de Operaciones",
                     "Director", "Administrador", "Jefe de Mantenimiento", "Coordinador"]
            contacto_cargo = cargos[i % len(cargos)]

            # Tipo de cliente (80% activos, 20% leads)
            tipo = "activo" if i <= 40 else "lead"

            cliente = Cliente(
                nombre=razon_social,
                ruc=ruc,
                direccion=f"Av. Principal {100 + i}, Distrito {i}",
                ciudad=f"{ciudad}, Perú",
                telefono=telefono,
                email=email,
                web=web,
                contacto_nombre=contacto_nombre,
                contacto_cargo=contacto_cargo,
                contacto_telefono=telefono,
                contacto_email=f"{contacto_nombre.split()[0].lower()}@{slug}.com.pe",
                industria=industria,
                tipo_cliente=tipo,
                notas=f"Cliente DEMO #{i} - {industria.title()}" if i > 40 else None
            )

            clientes_demo.append(cliente)

        print(f"✅ Generados {len(clientes_demo)} clientes DEMO")

        # Verificar si ya existen clientes
        clientes_existentes = db.query(Cliente).count()

        if clientes_existentes > 0:
            print(f"⚠️  Ya existen {clientes_existentes} clientes en la BD")
            respuesta = input("¿Deseas eliminar todos y crear datos DEMO? (s/n): ")
            if respuesta.lower() != 's':
                print("❌ Operación cancelada")
                return

            # Eliminar todos los clientes existentes
            db.query(Cotizacion).delete()
            db.query(Proyecto).delete()
            db.query(Cliente).delete()
            db.commit()
            print("🗑️  Datos anteriores eliminados")

        # Agregar clientes demo
        for cliente in clientes_demo:
            db.add(cliente)

        db.commit()
        print(f"✅ {len(clientes_demo)} clientes DEMO creados")

        # ============================================
        # COTIZACIONES DEMO
        # ============================================
        print("\n💰 Creando cotizaciones DEMO...")

        # Obtener primeros clientes para asociar
        cliente1 = db.query(Cliente).filter(Cliente.ruc == "20100001000").first()
        cliente2 = db.query(Cliente).filter(Cliente.ruc == "20100002000").first()

        cotizaciones_demo = [
            Cotizacion(
                numero="COT-202501-0001",
                cliente=cliente1.nombre,
                proyecto="Instalación Eléctrica Edificio Central",
                descripcion="Instalación eléctrica completa para edificio de 5 pisos",
                subtotal=15000.00,
                igv=2700.00,
                total=17700.00,
                observaciones="Precios incluyen IGV. Instalación según CNE-Utilización.",
                vigencia="30 días",
                estado="enviada",
                cliente_id=cliente1.id,
                items=[
                    {
                        "descripcion": "Tablero eléctrico trifásico 36 polos",
                        "cantidad": 1,
                        "precio_unitario": 2500.00,
                        "total": 2500.00
                    },
                    {
                        "descripcion": "Cable THW 10 AWG (metro)",
                        "cantidad": 500,
                        "precio_unitario": 8.50,
                        "total": 4250.00
                    },
                    {
                        "descripcion": "Tomacorrientes dobles con línea a tierra",
                        "cantidad": 60,
                        "precio_unitario": 25.00,
                        "total": 1500.00
                    }
                ]
            ),
            Cotizacion(
                numero="COT-202501-0002",
                cliente=cliente2.nombre,
                proyecto="Sistema CCTV Oficinas",
                descripcion="Instalación de 8 cámaras de seguridad HD",
                subtotal=5000.00,
                igv=900.00,
                total=5900.00,
                vigencia="15 días",
                estado="borrador",
                cliente_id=cliente2.id,
                items=[
                    {
                        "descripcion": "Cámara IP HD 1080p con visión nocturna",
                        "cantidad": 8,
                        "precio_unitario": 450.00,
                        "total": 3600.00
                    },
                    {
                        "descripcion": "DVR 8 canales con disco 1TB",
                        "cantidad": 1,
                        "precio_unitario": 800.00,
                        "total": 800.00
                    }
                ]
            )
        ]

        for cot in cotizaciones_demo:
            db.add(cot)

        db.commit()
        print(f"✅ {len(cotizaciones_demo)} cotizaciones DEMO creadas")

        # ============================================
        # PROYECTOS DEMO
        # ============================================
        print("\n📁 Creando proyectos DEMO...")

        proyectos_demo = [
            Proyecto(
                nombre="Automatización Industrial Planta Lima",
                descripcion="Proyecto de automatización completa de línea de producción",
                cliente=cliente1.nombre,
                estado=EstadoProyecto.EN_PROGRESO,
                cliente_id=cliente1.id,
                fecha_inicio=datetime.now() - timedelta(days=30),
                metadata_adicional={
                    "presupuesto": 50000.00,
                    "duracion_meses": 6,
                    "responsable": "Ing. Tesla"
                }
            ),
            Proyecto(
                nombre="Certificado ITSE Hospital Central",
                descripcion="Tramitación y certificación ITSE para hospital",
                cliente=db.query(Cliente).offset(40).first().nombre,
                estado=EstadoProyecto.PLANIFICACION,
                cliente_id=db.query(Cliente).offset(40).first().id,
                metadata_adicional={
                    "presupuesto": 8000.00,
                    "duracion_meses": 2
                }
            )
        ]

        for proyecto in proyectos_demo:
            db.add(proyecto)

        db.commit()
        print(f"✅ {len(proyectos_demo)} proyectos DEMO creados")

        # ============================================
        # RESUMEN
        # ============================================
        print("\n" + "="*60)
        print("✅ DATOS DEMO CREADOS EXITOSAMENTE")
        print("="*60)
        print(f"📋 Clientes:      {db.query(Cliente).count()}")
        print(f"💰 Cotizaciones:  {db.query(Cotizacion).count()}")
        print(f"📁 Proyectos:     {db.query(Proyecto).count()}")
        print("="*60)
        print("\n🎉 ¡Listo para hacer pruebas!")
        print("💡 Ahora puedes usar el selector de clientes y verás datos precargados")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    crear_datos_demo()
