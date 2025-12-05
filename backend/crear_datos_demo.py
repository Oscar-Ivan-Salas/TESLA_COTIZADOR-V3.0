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
        # CLIENTES DEMO
        # ============================================
        print("\n📋 Creando clientes DEMO...")

        clientes_demo = [
            Cliente(
                nombre="CONSTRUCTORA ABC S.A.C.",
                ruc="20123456789",
                direccion="Av. La Marina 2000, San Miguel",
                ciudad="Lima, Perú",
                telefono="987654321",
                email="contacto@constructoraabc.com",
                web="www.constructoraabc.com",
                contacto_nombre="Juan Pérez",
                contacto_cargo="Gerente de Proyectos",
                contacto_telefono="987654321",
                contacto_email="jperez@constructoraabc.com",
                industria="construccion",
                tipo_cliente="activo",
                notas="Cliente frecuente, buenos pagos"
            ),
            Cliente(
                nombre="EDIFICACIONES XYZ EIRL",
                ruc="20987654321",
                direccion="Jr. Los Pinos 350, Miraflores",
                ciudad="Lima, Perú",
                telefono="912345678",
                email="info@edificacionesxyz.pe",
                contacto_nombre="María González",
                contacto_cargo="Jefa de Compras",
                contacto_telefono="912345678",
                contacto_email="mgonzalez@edificacionesxyz.pe",
                industria="arquitectura",
                tipo_cliente="activo"
            ),
            Cliente(
                nombre="INDUSTRIAS DEMO S.A.",
                ruc="20555666777",
                direccion="Av. Industrial 1500, Ate",
                ciudad="Lima, Perú",
                telefono="999888777",
                email="ventas@industriasdemo.com",
                contacto_nombre="Carlos Ramírez",
                contacto_cargo="Gerente General",
                contacto_telefono="999888777",
                contacto_email="cramirez@industriasdemo.com",
                industria="industrial",
                tipo_cliente="lead",
                notas="Cliente nuevo, interesado en automatización"
            ),
            Cliente(
                nombre="COLEGIO TESLA",
                ruc="20111222333",
                direccion="Av. La Cultura 800, Cusco",
                ciudad="Cusco, Perú",
                telefono="966554433",
                email="administracion@colegiotesla.edu.pe",
                contacto_nombre="Ana Torres",
                contacto_cargo="Directora",
                contacto_telefono="966554433",
                contacto_email="atorres@colegiotesla.edu.pe",
                industria="educacion",
                tipo_cliente="activo"
            ),
            Cliente(
                nombre="HOSPITAL CENTRAL",
                ruc="20444555666",
                direccion="Jr. Salud 200, Huancayo",
                ciudad="Huancayo, Junín - Perú",
                telefono="955443322",
                email="compras@hospitalcentral.gob.pe",
                contacto_nombre="Dr. Roberto Sánchez",
                contacto_cargo="Jefe de Mantenimiento",
                contacto_telefono="955443322",
                contacto_email="rsanchez@hospitalcentral.gob.pe",
                industria="salud",
                tipo_cliente="activo",
                notas="Requiere certificaciones especiales"
            )
        ]

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

        # Obtener primer cliente para asociar
        cliente1 = db.query(Cliente).filter(Cliente.ruc == "20123456789").first()
        cliente2 = db.query(Cliente).filter(Cliente.ruc == "20987654321").first()

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
                cliente="HOSPITAL CENTRAL",
                estado=EstadoProyecto.PLANIFICACION,
                cliente_id=db.query(Cliente).filter(Cliente.ruc == "20444555666").first().id,
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
