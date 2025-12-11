"""
Script Simplificado de Población de Datos
Crea 30 clientes y 30 cotizaciones para testing
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.cotizacion import Cotizacion
from app.models.cliente import Cliente
from datetime import datetime
import random

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

def crear_clientes_demo(db: Session):
    """Crear 30 clientes de prueba"""
    
    empresas = [
        "Minera Las Bambas", "Compañía Minera Antamina", "Southern Copper Corporation",
        "Minera Yanacocha", "Cerro Verde", "Buenaventura", "Volcan Compañía Minera",
        "Minsur", "Hochschild Mining", "Pan American Silver", "Nexa Resources",
        "Minera Chinalco Perú", "Hudbay Minerals", "Minera Poderosa", "Consorcio Minero Horizonte",
        "Compañía de Minas Buenaventura", "Minera Aurífera Retamas", "Minera Barrick Misquichilca",
        "Gold Fields La Cima", "Minera IRL", "Minera Laytaruma", "Minera Colquisiri",
        "Minera Raura", "Minera Suyamarca", "Compañía Minera Casapalca", "Minera Argentum",
        "Minera Bateas", "Minera Condestable", "Minera Milpo", "Minera Atacocha"
    ]
    
    industrias = ["Minería", "Construcción", "Manufactura", "Energía"]
    ciudades = ["Lima", "Arequipa", "Cusco", "Huancayo", "Trujillo", "Cajamarca"]
    
    clientes_creados = []
    
    for i, empresa in enumerate(empresas, 1):
        cliente = Cliente(
            nombre=empresa,
            ruc=f"2060{i:07d}",
            direccion=f"Av. Principal {i*100}, Oficina {i}",
            telefono=f"90631{i:04d}",
            email=f"contacto{i}@{empresa.lower().replace(' ', '')}.com",
            ciudad=random.choice(ciudades),
            industria=random.choice(industrias),
            contacto_nombre=f"Ing. {['Carlos', 'María', 'José', 'Ana', 'Luis'][i % 5]} {['García', 'Rodríguez', 'López', 'Martínez', 'Fernández'][i % 5]}",
            notas=f"Cliente demo #{i} - Sector {random.choice(industrias)}"
        )
        db.add(cliente)
        clientes_creados.append(cliente)
    
    db.commit()
    print(f"OK - {len(clientes_creados)} clientes creados")
    return clientes_creados

def crear_cotizaciones_demo(db: Session, clientes: list):
    """Crear 30 cotizaciones (15 simples, 15 complejas)"""
    
    servicios_simples = [
        {"descripcion": "Instalación de tablero eléctrico trifásico 380V", "precio": 2500},
        {"descripcion": "Mantenimiento preventivo de subestación eléctrica", "precio": 3200},
        {"descripcion": "Cableado estructurado Cat6 para oficinas", "precio": 1800},
        {"descripcion": "Sistema de puesta a tierra para planta industrial", "precio": 4500},
        {"descripcion": "Instalación de sistema de iluminación LED", "precio": 2100},
    ]
    
    servicios_complejos = [
        {"descripcion": "Diseño e instalación de subestación eléctrica 22.9kV/440V", "precio": 45000},
        {"descripcion": "Sistema de automatización industrial con PLC Siemens", "precio": 38000},
        {"descripcion": "Instalación de sistema fotovoltaico 50kW", "precio": 52000},
        {"descripcion": "Modernización de tableros de distribución MT/BT", "precio": 28000},
        {"descripcion": "Sistema de respaldo eléctrico con UPS y grupo electrógeno", "precio": 65000},
    ]
    
    cotizaciones_creadas = []
    
    # 15 Cotizaciones Simples
    for i in range(15):
        cliente = random.choice(clientes)
        servicio = random.choice(servicios_simples)
        cantidad = random.randint(1, 5)
        
        items = [{
            "descripcion": servicio["descripcion"],
            "cantidad": cantidad,
            "unidad": "und",
            "precio_unitario": servicio["precio"]
        }]
        
        subtotal = cantidad * servicio["precio"]
        igv = subtotal * 0.18
        total = subtotal + igv
        
        cotizacion = Cotizacion(
            numero=f"COT-202512{i+1:03d}",
            cliente=cliente.nombre,
            cliente_id=cliente.id,
            proyecto=f"Proyecto {cliente.nombre[:20]} - Fase {i+1}",
            descripcion=f"Cotización para {servicio['descripcion'].lower()}",
            subtotal=subtotal,
            igv=igv,
            total=total,
            observaciones="Precios incluyen IGV. Instalación según CNE-Utilización. Garantía 12 meses.",
            vigencia="30 días",
            estado="enviada",
            items=items,
            metadata_adicional={"tipo": "simple", "prioridad": "media"}
        )
        db.add(cotizacion)
        cotizaciones_creadas.append(cotizacion)
    
    # 15 Cotizaciones Complejas
    for i in range(15, 30):
        cliente = random.choice(clientes)
        
        # Múltiples items para cotización compleja
        items = []
        for j in range(random.randint(3, 6)):
            servicio = random.choice(servicios_complejos)
            items.append({
                "descripcion": servicio["descripcion"],
                "cantidad": random.randint(1, 3),
                "unidad": "glb",
                "precio_unitario": servicio["precio"]
            })
        
        subtotal = sum(item["cantidad"] * item["precio_unitario"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        cotizacion = Cotizacion(
            numero=f"COT-202512{i+1:03d}",
            cliente=cliente.nombre,
            cliente_id=cliente.id,
            proyecto=f"Proyecto Industrial {cliente.nombre[:15]} - Modernización",
            descripcion=f"Cotización integral para modernización eléctrica de planta industrial",
            subtotal=subtotal,
            igv=igv,
            total=total,
            observaciones="Incluye ingeniería de detalle, suministro, instalación y puesta en marcha. Garantía 24 meses.",
            vigencia="45 días",
            estado="aprobada",
            items=items,
            metadata_adicional={
                "tipo": "compleja",
                "prioridad": "alta",
                "fases": ["Ingeniería", "Suministro", "Instalación", "Pruebas"]
            }
        )
        db.add(cotizacion)
        cotizaciones_creadas.append(cotizacion)
    
    db.commit()
    print(f"OK - {len(cotizaciones_creadas)} cotizaciones creadas (15 simples, 15 complejas)")
    return cotizaciones_creadas

def main():
    """Ejecutar población de datos"""
    db = SessionLocal()
    
    try:
        print("Iniciando poblacion de datos de prueba...")
        print("-" * 60)
        
        # 1. Crear clientes
        print("\nCreando clientes...")
        clientes = crear_clientes_demo(db)
        
        # 2. Crear cotizaciones
        print("\nCreando cotizaciones...")
        cotizaciones = crear_cotizaciones_demo(db, clientes)
        
        print("\n" + "=" * 60)
        print("POBLACION DE DATOS COMPLETADA")
        print("=" * 60)
        print(f"Resumen:")
        print(f"   - {len(clientes)} clientes")
        print(f"   - {len(cotizaciones)} cotizaciones (15 simples + 15 complejas)")
        print(f"   - TOTAL: {len(clientes) + len(cotizaciones)} registros")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
