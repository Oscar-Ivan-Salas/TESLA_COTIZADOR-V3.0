"""
Script Completo: Agregar Proyectos e Informes
Completa la BD con los 6 tipos de documentos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.proyecto import Proyecto
from app.models.cliente import Cliente
from datetime import datetime, timedelta
import random

def agregar_proyectos(db: Session):
    """Agregar 10 proyectos (5 simples + 5 complejos)"""
    
    # Obtener clientes existentes
    clientes = db.query(Cliente).all()
    if not clientes:
        print("ERROR: No hay clientes en la BD. Ejecuta poblar_datos_simple.py primero.")
        return []
    
    proyectos_creados = []
    
    # 5 Proyectos Simples
    print("\nCreando 5 proyectos simples...")
    for i in range(5):
        cliente = random.choice(clientes)
        proyecto = Proyecto(
            nombre=f"Mantenimiento Electrico {cliente.nombre[:20]}",
            descripcion=f"Proyecto de mantenimiento preventivo y correctivo de instalaciones electricas para {cliente.nombre}. Incluye revision de tableros, medicion de puesta a tierra y termografia.",
            cliente=cliente.nombre,
            cliente_id=cliente.id,
            fecha_inicio=datetime.now() - timedelta(days=random.randint(10, 60)),
            fecha_fin=datetime.now() + timedelta(days=random.randint(30, 90)),
            estado="en_progreso",
            metadata_adicional={
                "tipo": "simple",
                "categoria": "mantenimiento",
                "alcance": "Mantenimiento preventivo",
                "duracion_estimada": "2-3 meses"
            }
        )
        db.add(proyecto)
        proyectos_creados.append(proyecto)
    
    # 5 Proyectos Complejos (con fases detalladas)
    print("Creando 5 proyectos complejos...")
    for i in range(5, 10):
        cliente = random.choice(clientes)
        proyecto = Proyecto(
            nombre=f"Modernizacion Industrial {cliente.nombre[:15]}",
            descripcion=f"Proyecto integral de modernizacion de sistemas electricos y automatizacion para {cliente.nombre}. Incluye diseno, suministro, instalacion y puesta en marcha de subestacion electrica, tableros de distribucion y sistema SCADA.",
            cliente=cliente.nombre,
            cliente_id=cliente.id,
            fecha_inicio=datetime.now() - timedelta(days=random.randint(30, 120)),
            fecha_fin=datetime.now() + timedelta(days=random.randint(120, 240)),
            estado="planificacion",
            metadata_adicional={
                "tipo": "complejo",
                "categoria": "modernizacion",
                "alcance": "Modernizacion integral",
                "duracion_estimada": "6-12 meses",
                "fases": [
                    {
                        "nombre": "Ingenieria de Detalle",
                        "duracion": "4 semanas",
                        "estado": "completado",
                        "entregables": ["Planos electricos", "Memoria de calculo", "Especificaciones tecnicas"]
                    },
                    {
                        "nombre": "Suministro de Equipos",
                        "duracion": "8 semanas",
                        "estado": "en_progreso",
                        "entregables": ["Transformador", "Tableros MT/BT", "Sistema SCADA"]
                    },
                    {
                        "nombre": "Instalacion y Montaje",
                        "duracion": "12 semanas",
                        "estado": "pendiente",
                        "entregables": ["Obra civil", "Montaje electrico", "Cableado"]
                    },
                    {
                        "nombre": "Pruebas y Puesta en Marcha",
                        "duracion": "4 semanas",
                        "estado": "pendiente",
                        "entregables": ["Protocolos de pruebas", "Capacitacion", "Manuales"]
                    }
                ],
                "presupuesto_estimado": random.randint(150000, 350000),
                "equipo": [
                    {"rol": "Jefe de Proyecto", "nombre": "Ing. Carlos Rodriguez"},
                    {"rol": "Ingeniero Electrico", "nombre": "Ing. Maria Lopez"},
                    {"rol": "Supervisor de Obra", "nombre": "Tec. Jose Martinez"}
                ]
            }
        )
        db.add(proyecto)
        proyectos_creados.append(proyecto)
    
    db.commit()
    print(f"OK - {len(proyectos_creados)} proyectos creados (5 simples + 5 complejos)")
    return proyectos_creados

def agregar_informes(db: Session):
    """Agregar 10 informes como metadata en proyectos existentes"""
    
    # Obtener proyectos existentes
    proyectos = db.query(Proyecto).all()
    if len(proyectos) < 10:
        print("ERROR: Se necesitan al menos 10 proyectos. Ejecuta este script despues de crear proyectos.")
        return []
    
    informes_creados = []
    
    # 5 Informes Simples (agregar metadata a proyectos simples)
    print("\nCreando 5 informes simples...")
    proyectos_simples = [p for p in proyectos if p.metadata_adicional.get("tipo") == "simple"][:5]
    
    for i, proyecto in enumerate(proyectos_simples):
        informe_data = {
            "tipo_informe": "simple",
            "numero": f"INF-S-{datetime.now().year}{i+1:03d}",
            "fecha_emision": datetime.now().strftime("%Y-%m-%d"),
            "titulo": f"Informe Tecnico - {proyecto.nombre}",
            "resumen": f"Informe de avance del proyecto {proyecto.nombre}. Se han completado las actividades de inspeccion y diagnostico.",
            "secciones": [
                {
                    "titulo": "Introduccion",
                    "contenido": f"El presente informe detalla el estado actual del proyecto {proyecto.nombre}, ejecutado para {proyecto.cliente}."
                },
                {
                    "titulo": "Actividades Realizadas",
                    "contenido": "- Inspeccion visual de instalaciones\n- Medicion de puesta a tierra\n- Termografia de tableros electricos\n- Revision de protecciones"
                },
                {
                    "titulo": "Hallazgos",
                    "contenido": "Se identificaron 3 observaciones menores que requieren atencion. No se encontraron condiciones criticas de seguridad."
                },
                {
                    "titulo": "Conclusiones",
                    "contenido": "El proyecto avanza segun lo programado. Se recomienda implementar las observaciones identificadas."
                }
            ],
            "conclusiones": [
                "El sistema electrico se encuentra en condiciones operativas aceptables",
                "Se requiere mantenimiento preventivo en 3 tableros secundarios",
                "El proyecto cumple con el cronograma establecido"
            ],
            "recomendaciones": [
                "Implementar programa de mantenimiento preventivo trimestral",
                "Actualizar planos electricos conforme a obra",
                "Capacitar al personal de operacion"
            ]
        }
        
        # Actualizar metadata del proyecto
        if proyecto.metadata_adicional is None:
            proyecto.metadata_adicional = {}
        proyecto.metadata_adicional["informe"] = informe_data
        informes_creados.append(informe_data)
    
    # 5 Informes Complejos/Ejecutivos (agregar metadata a proyectos complejos)
    print("Creando 5 informes ejecutivos...")
    proyectos_complejos = [p for p in proyectos if p.metadata_adicional.get("tipo") == "complejo"][:5]
    
    for i, proyecto in enumerate(proyectos_complejos):
        informe_data = {
            "tipo_informe": "ejecutivo",
            "numero": f"INF-E-{datetime.now().year}{i+1:03d}",
            "fecha_emision": datetime.now().strftime("%Y-%m-%d"),
            "titulo": f"Informe Ejecutivo - {proyecto.nombre}",
            "resumen_ejecutivo": f"Informe ejecutivo del proyecto {proyecto.nombre} para {proyecto.cliente}. El proyecto presenta un avance del 45% con cumplimiento del cronograma y presupuesto.",
            "kpis": [
                {"nombre": "Avance Fisico", "valor": "45%", "meta": "50%", "estado": "En rango"},
                {"nombre": "Avance Financiero", "valor": "42%", "meta": "50%", "estado": "Bajo control"},
                {"nombre": "Cumplimiento Cronograma", "valor": "95%", "meta": "100%", "estado": "Aceptable"},
                {"nombre": "Seguridad (Dias sin accidentes)", "valor": "120", "meta": "90", "estado": "Excelente"}
            ],
            "secciones": [
                {
                    "titulo": "Resumen Ejecutivo",
                    "contenido": f"El proyecto {proyecto.nombre} se encuentra en fase de ejecucion con un avance general del 45%. Se han completado exitosamente las fases de ingenieria y suministro."
                },
                {
                    "titulo": "Estado del Proyecto",
                    "contenido": "Fase actual: Instalacion y Montaje\nAvance: 45%\nPresupuesto ejecutado: S/ 180,000\nPersonal asignado: 15 personas"
                },
                {
                    "titulo": "Logros Principales",
                    "contenido": "- Ingenieria de detalle aprobada por cliente\n- Suministro de equipos completado\n- Obra civil al 80%\n- Cero accidentes laborales"
                },
                {
                    "titulo": "Riesgos y Mitigacion",
                    "contenido": "Riesgo identificado: Retraso en entrega de transformador (5 dias)\nMitigacion: Reprogramacion de actividades criticas"
                },
                {
                    "titulo": "Proyeccion Financiera",
                    "contenido": f"Presupuesto total: S/ {proyecto.metadata_adicional.get('presupuesto_estimado', 250000):,.2f}\nEjecutado: S/ 180,000\nPor ejecutar: S/ 120,000\nMargen proyectado: 15%"
                }
            ],
            "conclusiones": [
                "El proyecto mantiene un avance satisfactorio acorde al cronograma",
                "Los indicadores de seguridad superan las metas establecidas",
                "El presupuesto se encuentra bajo control con margen positivo",
                "La satisfaccion del cliente es alta segun ultimas reuniones"
            ],
            "recomendaciones": [
                "Acelerar actividades de montaje para recuperar 5 dias de retraso",
                "Mantener enfoque en seguridad y calidad",
                "Programar reunion de avance con cliente para siguiente mes",
                "Iniciar preparativos para fase de pruebas y comisionamiento"
            ],
            "proximos_pasos": [
                {"actividad": "Completar montaje de tableros MT", "fecha": "15/12/2025"},
                {"actividad": "Inicio de cableado de fuerza", "fecha": "20/12/2025"},
                {"actividad": "Instalacion de sistema SCADA", "fecha": "05/01/2026"}
            ]
        }
        
        # Actualizar metadata del proyecto
        if proyecto.metadata_adicional is None:
            proyecto.metadata_adicional = {}
        proyecto.metadata_adicional["informe"] = informe_data
        informes_creados.append(informe_data)
    
    db.commit()
    print(f"OK - {len(informes_creados)} informes creados (5 simples + 5 ejecutivos)")
    return informes_creados

def main():
    """Ejecutar poblacion completa"""
    db = SessionLocal()
    
    try:
        print("Completando base de datos con proyectos e informes...")
        print("-" * 60)
        
        # 1. Agregar proyectos
        proyectos = agregar_proyectos(db)
        
        # 2. Agregar informes
        informes = agregar_informes(db)
        
        print("\n" + "=" * 60)
        print("POBLACION COMPLETADA")
        print("=" * 60)
        print(f"Resumen:")
        print(f"   - {len(proyectos)} proyectos (5 simples + 5 complejos)")
        print(f"   - {len(informes)} informes (5 simples + 5 ejecutivos)")
        print(f"   - TOTAL AGREGADO: {len(proyectos) + len(informes)} registros")
        print("=" * 60)
        print("\nAhora la BD tiene datos para los 6 tipos de documentos:")
        print("   1. Cotizaciones Simples")
        print("   2. Cotizaciones Complejas")
        print("   3. Proyectos Simples")
        print("   4. Proyectos Complejos (Gantt)")
        print("   5. Informes Simples")
        print("   6. Informes Ejecutivos")
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
