#!/usr/bin/env python3
"""
Script para crear 30 usuarios de prueba en la base de datos
Distribución: 20 Free, 7 Pro, 3 Enterprise
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.usuario import Usuario

# Crear todas las tablas
print("🔧 Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas")

# Datos de 30 usuarios peruanos realistas
USUARIOS = [
    # ========== USUARIOS FREE (20) ==========
    {
        "nombre": "Juan Carlos",
        "apellido": "Pérez García",
        "email": "jperez@gmail.com",
        "telefono": "+51 964 123 456",
        "empresa": "CONSTRUCTORA LIMA SAC",
        "cargo": "Ingeniero Eléctrico",
        "departamento": "Lima",
        "ciudad": "Lima",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "María Elena",
        "apellido": "García Rodríguez",
        "email": "mgarcia@hotmail.com",
        "telefono": "+51 987 234 567",
        "empresa": "INDUSTRIAS DEL SUR EIRL",
        "cargo": "Gerente de Proyectos",
        "departamento": "Arequipa",
        "ciudad": "Arequipa",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Carlos Alberto",
        "apellido": "Mendoza Silva",
        "email": "cmendoza@outlook.com",
        "telefono": "+51 975 345 678",
        "empresa": "ELECTRICIDAD ANDINA SAC",
        "cargo": "Técnico Electricista",
        "departamento": "Cusco",
        "ciudad": "Cusco",
        "plan": "free",
        "ia_preferida": "groq"
    },
    {
        "nombre": "Ana Lucía",
        "apellido": "Torres Vega",
        "email": "atorres@yahoo.com",
        "telefono": "+51 963 456 789",
        "empresa": "SERVICIOS GENERALES NORTE",
        "cargo": "Ingeniera Civil",
        "departamento": "Piura",
        "ciudad": "Piura",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Roberto",
        "apellido": "Sánchez Huamán",
        "email": "rsanchez@gmail.com",
        "telefono": "+51 986 567 890",
        "empresa": "PROYECTOS ELÉCTRICOS SAC",
        "cargo": "Supervisor de Obra",
        "departamento": "Junín",
        "ciudad": "Huancayo",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Patricia",
        "apellido": "Rojas Chávez",
        "email": "projas@hotmail.com",
        "telefono": "+51 974 678 901",
        "empresa": "CONSTRUCTORA CENTRAL",
        "cargo": "Administradora",
        "departamento": "Junín",
        "ciudad": "Huancayo",
        "plan": "free",
        "ia_preferida": "groq"
    },
    {
        "nombre": "Jorge Luis",
        "apellido": "Vargas Paredes",
        "email": "jvargas@gmail.com",
        "telefono": "+51 962 789 012",
        "empresa": "MINERA HUANCAYO SAC",
        "cargo": "Ingeniero de Seguridad",
        "departamento": "Junín",
        "ciudad": "La Oroya",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Carmen Rosa",
        "apellido": "Flores Quispe",
        "email": "cflores@outlook.com",
        "telefono": "+51 985 890 123",
        "empresa": "TEXTIL PERU SA",
        "cargo": "Jefa de Mantenimiento",
        "departamento": "Lima",
        "ciudad": "Lima",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Luis Fernando",
        "apellido": "Castro Morales",
        "email": "lcastro@yahoo.com",
        "telefono": "+51 973 901 234",
        "empresa": "AGROINDUSTRIAL VALLE",
        "cargo": "Ingeniero Mecánico",
        "departamento": "La Libertad",
        "ciudad": "Trujillo",
        "plan": "free",
        "ia_preferida": "groq"
    },
    {
        "nombre": "Sofía",
        "apellido": "Ramírez León",
        "email": "sramirez@gmail.com",
        "telefono": "+51 961 012 345",
        "empresa": "CLINICA SAN JUAN",
        "cargo": "Coordinadora de Infraestructura",
        "departamento": "Lambayeque",
        "ciudad": "Chiclayo",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Miguel Ángel",
        "apellido": "Herrera Ponce",
        "email": "mherrera@hotmail.com",
        "telefono": "+51 984 123 456",
        "empresa": "UNIVERSIDAD ANDINA",
        "cargo": "Director de Infraestructura",
        "departamento": "Puno",
        "ciudad": "Puno",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Isabel",
        "apellido": "Gutiérrez Arias",
        "email": "igutierrez@gmail.com",
        "telefono": "+51 972 234 567",
        "empresa": "MUNICIPALIDAD DE HUANCAYO",
        "cargo": "Ingeniera Municipal",
        "departamento": "Junín",
        "ciudad": "Huancayo",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Fernando",
        "apellido": "Díaz Ccama",
        "email": "fdiaz@outlook.com",
        "telefono": "+51 960 345 678",
        "empresa": "HOTEL TURISMO SAC",
        "cargo": "Gerente de Operaciones",
        "departamento": "Cusco",
        "ciudad": "Cusco",
        "plan": "free",
        "ia_preferida": "groq"
    },
    {
        "nombre": "Claudia",
        "apellido": "Moreno Quispe",
        "email": "cmoreno@yahoo.com",
        "telefono": "+51 983 456 789",
        "empresa": "RESTAURANTE EL DORADO",
        "cargo": "Administradora",
        "departamento": "Lima",
        "ciudad": "Miraflores",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Ricardo",
        "apellido": "Vega Huamán",
        "email": "rvega@gmail.com",
        "telefono": "+51 971 567 890",
        "empresa": "CENTRO COMERCIAL PLAZA",
        "cargo": "Jefe de Mantenimiento",
        "departamento": "Lima",
        "ciudad": "San Isidro",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Daniela",
        "apellido": "Campos Rivera",
        "email": "dcampos@hotmail.com",
        "telefono": "+51 959 678 901",
        "empresa": "COLEGIO SAN MARTIN",
        "cargo": "Directora",
        "departamento": "Junín",
        "ciudad": "Huancayo",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Andrés",
        "apellido": "Ortiz Paredes",
        "email": "aortiz@gmail.com",
        "telefono": "+51 982 789 012",
        "empresa": "POSTA MÉDICA CENTRAL",
        "cargo": "Administrador",
        "departamento": "Junín",
        "ciudad": "Concepción",
        "plan": "free",
        "ia_preferida": "groq"
    },
    {
        "nombre": "Gabriela",
        "apellido": "Reyes Huamán",
        "email": "greyes@outlook.com",
        "telefono": "+51 970 890 123",
        "empresa": "MERCADO MODELO SAC",
        "cargo": "Gerente General",
        "departamento": "Junín",
        "ciudad": "Huancayo",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Pablo",
        "apellido": "Cruz Quispe",
        "email": "pcruz@yahoo.com",
        "telefono": "+51 958 901 234",
        "empresa": "COOPERATIVA VALLE VERDE",
        "cargo": "Presidente",
        "departamento": "Junín",
        "ciudad": "Huancayo",
        "plan": "free",
        "ia_preferida": "gemini"
    },
    {
        "nombre": "Valeria",
        "apellido": "Jiménez León",
        "email": "vjimenez@gmail.com",
        "telefono": "+51 981 012 345",
        "empresa": "DISCOTECA MAXIMO",
        "cargo": "Gerente de Local",
        "departamento": "Lima",
        "ciudad": "Barranco",
        "plan": "free",
        "ia_preferida": "gemini"
    },

    # ========== USUARIOS PRO (7) ==========
    {
        "nombre": "Eduardo",
        "apellido": "Salazar Huamán",
        "email": "esalazar@constructora-elite.com",
        "telefono": "+51 998 123 456",
        "empresa": "CONSTRUCTORA ELITE SAC",
        "cargo": "Gerente General",
        "departamento": "Lima",
        "ciudad": "San Isidro",
        "plan": "pro",
        "ia_preferida": "claude"
    },
    {
        "nombre": "Mónica",
        "apellido": "Bustamante Rivera",
        "email": "mbustamante@minera-peru.com",
        "telefono": "+51 997 234 567",
        "empresa": "MINERA PERU SA",
        "cargo": "Jefa de Proyectos",
        "departamento": "Junín",
        "ciudad": "La Oroya",
        "plan": "pro",
        "ia_preferida": "gpt-4"
    },
    {
        "nombre": "Alejandro",
        "apellido": "Paredes Ccama",
        "email": "aparedes@hospital-regional.gob.pe",
        "telefono": "+51 996 345 678",
        "empresa": "HOSPITAL REGIONAL HUANCAYO",
        "cargo": "Director de Infraestructura",
        "departamento": "Junín",
        "ciudad": "Huancayo",
        "plan": "pro",
        "ia_preferida": "claude"
    },
    {
        "nombre": "Carolina",
        "apellido": "Mendoza Arias",
        "email": "cmendoza@fabrica-textil.com",
        "telefono": "+51 995 456 789",
        "empresa": "FABRICA TEXTIL ANDINA",
        "cargo": "Gerente de Producción",
        "departamento": "Lima",
        "ciudad": "Lima",
        "plan": "pro",
        "ia_preferida": "gpt-4"
    },
    {
        "nombre": "Diego",
        "apellido": "Rojas Paredes",
        "email": "drojas@procesadora-alimentos.com",
        "telefono": "+51 994 567 890",
        "empresa": "PROCESADORA DE ALIMENTOS SAC",
        "cargo": "Jefe de Planta",
        "departamento": "Arequipa",
        "ciudad": "Arequipa",
        "plan": "pro",
        "ia_preferida": "claude"
    },
    {
        "nombre": "Lucía",
        "apellido": "Fernández Quispe",
        "email": "lfernandez@smart-home.pe",
        "telefono": "+51 993 678 901",
        "empresa": "SMART HOME PERU",
        "cargo": "Directora Técnica",
        "departamento": "Lima",
        "ciudad": "Miraflores",
        "plan": "pro",
        "ia_preferida": "gpt-4"
    },
    {
        "nombre": "Raúl",
        "apellido": "Torres Ccama",
        "email": "rtorres@edificio-inteligente.com",
        "telefono": "+51 992 789 012",
        "empresa": "EDIFICIO INTELIGENTE SAC",
        "cargo": "Gerente de Automatización",
        "departamento": "Lima",
        "ciudad": "San Isidro",
        "plan": "pro",
        "ia_preferida": "claude"
    },

    # ========== USUARIOS ENTERPRISE (3) ==========
    {
        "nombre": "Víctor Hugo",
        "apellido": "Huamán Rojas",
        "email": "vhuaman@corporacion-tesla.com",
        "telefono": "+51 999 123 456",
        "empresa": "CORPORACION TESLA PERU",
        "cargo": "CEO",
        "departamento": "Lima",
        "ciudad": "San Isidro",
        "plan": "enterprise",
        "ia_preferida": "claude"
    },
    {
        "nombre": "Sandra",
        "apellido": "Quispe Paredes",
        "email": "squispe@universidad-nacional.edu.pe",
        "telefono": "+51 999 234 567",
        "empresa": "UNIVERSIDAD NACIONAL DEL CENTRO",
        "cargo": "Rectora",
        "departamento": "Junín",
        "ciudad": "Huancayo",
        "plan": "enterprise",
        "ia_preferida": "gpt-4"
    },
    {
        "nombre": "Alberto",
        "apellido": "Ccama Huamán",
        "email": "accama@municipalidad-huancayo.gob.pe",
        "telefono": "+51 999 345 678",
        "empresa": "MUNICIPALIDAD PROVINCIAL DE HUANCAYO",
        "cargo": "Alcalde",
        "departamento": "Junín",
        "ciudad": "Huancayo",
        "plan": "enterprise",
        "ia_preferida": "claude"
    },
]


def crear_usuarios():
    """Crea los 30 usuarios en la base de datos"""
    db: Session = SessionLocal()

    try:
        # Verificar si ya existen usuarios
        count = db.query(Usuario).count()
        if count > 0:
            print(f"⚠️  Ya existen {count} usuarios en la BD")
            respuesta = input("¿Deseas eliminarlos y crear nuevos? (s/n): ")
            if respuesta.lower() != 's':
                print("❌ Operación cancelada")
                return

            # Eliminar usuarios existentes
            db.query(Usuario).delete()
            db.commit()
            print("✅ Usuarios existentes eliminados")

        print("\n🚀 Creando 30 usuarios de prueba...\n")
        print("=" * 80)

        usuarios_creados = []
        for i, datos in enumerate(USUARIOS, 1):
            # Configurar tokens según plan
            planes = {
                "free": 1000,
                "pro": 10000,
                "enterprise": 100000
            }

            usuario = Usuario(
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                email=datos["email"],
                telefono=datos["telefono"],
                empresa=datos["empresa"],
                cargo=datos["cargo"],
                departamento=datos["departamento"],
                ciudad=datos["ciudad"],
                plan=datos["plan"],
                tokens_mensuales=planes[datos["plan"]],
                tokens_usados=0,
                fecha_reset_tokens=datetime.now() + timedelta(days=30),
                ia_preferida=datos["ia_preferida"],
                activo=True
            )

            db.add(usuario)
            usuarios_creados.append(usuario)

            # Emoji según plan
            emoji_plan = {
                "free": "🆓",
                "pro": "⭐",
                "enterprise": "👑"
            }

            print(f"{emoji_plan[datos['plan']]} [{i:2d}/30] {datos['nombre']} {datos['apellido']}")
            print(f"    📧 {datos['email']}")
            print(f"    🏢 {datos['empresa']}")
            print(f"    💼 {datos['cargo']}")
            print(f"    📍 {datos['ciudad']}, {datos['departamento']}")
            print(f"    🎯 Plan: {datos['plan'].upper()} | IA: {datos['ia_preferida']} | Tokens: {planes[datos['plan']]:,}")
            print()

        # Commit a la base de datos
        db.commit()

        print("=" * 80)
        print("\n✅ USUARIOS CREADOS EXITOSAMENTE\n")

        # Estadísticas
        print("📊 ESTADÍSTICAS:")
        print(f"   Total usuarios: 30")
        print(f"   - Plan Free: 20 usuarios (1,000 tokens/mes c/u)")
        print(f"   - Plan Pro: 7 usuarios (10,000 tokens/mes c/u)")
        print(f"   - Plan Enterprise: 3 usuarios (100,000 tokens/mes c/u)")
        print()
        print(f"💰 CAPACIDAD TOTAL:")
        print(f"   Free: 20 × 1,000 = 20,000 tokens/mes")
        print(f"   Pro: 7 × 10,000 = 70,000 tokens/mes")
        print(f"   Enterprise: 3 × 100,000 = 300,000 tokens/mes")
        print(f"   ─────────────────────────────────────")
        print(f"   TOTAL: 390,000 tokens/mes")
        print()

        # Verificar con query
        total_db = db.query(Usuario).count()
        free_count = db.query(Usuario).filter(Usuario.plan == "free").count()
        pro_count = db.query(Usuario).filter(Usuario.plan == "pro").count()
        enterprise_count = db.query(Usuario).filter(Usuario.plan == "enterprise").count()

        print("✅ VERIFICACIÓN EN BASE DE DATOS:")
        print(f"   Total en BD: {total_db}")
        print(f"   Free: {free_count}")
        print(f"   Pro: {pro_count}")
        print(f"   Enterprise: {enterprise_count}")
        print()

        if total_db == 30:
            print("🎉 ¡PERFECTO! Todos los usuarios se crearon correctamente")
        else:
            print(f"⚠️  Advertencia: Se esperaban 30 usuarios pero hay {total_db}")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("🤖 TESLA COTIZADOR V3.0 - Creador de Usuarios de Prueba")
    print("=" * 80)
    print()
    crear_usuarios()
    print("\n" + "=" * 80)
    print("✅ Proceso completado")
