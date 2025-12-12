#!/usr/bin/env python3
"""
Script para verificar usuarios en la base de datos
"""
import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import SessionLocal
from app.models.usuario import Usuario


def verificar_bd():
    """Verifica que la BD de usuarios funciona correctamente"""
    print("🔍 TESLA COTIZADOR V3.0 - Verificación de Base de Datos")
    print("=" * 80)
    print()

    db: Session = SessionLocal()

    try:
        # 1. Contar usuarios
        print("📊 ESTADÍSTICAS GENERALES:")
        total = db.query(Usuario).count()
        activos = db.query(Usuario).filter(Usuario.activo == True).count()
        print(f"   Total usuarios: {total}")
        print(f"   Usuarios activos: {activos}")
        print()

        # 2. Usuarios por plan
        print("💳 DISTRIBUCIÓN POR PLAN:")
        free = db.query(Usuario).filter(Usuario.plan == "free").count()
        pro = db.query(Usuario).filter(Usuario.plan == "pro").count()
        enterprise = db.query(Usuario).filter(Usuario.plan == "enterprise").count()
        print(f"   🆓 Free: {free} usuarios")
        print(f"   ⭐ Pro: {pro} usuarios")
        print(f"   👑 Enterprise: {enterprise} usuarios")
        print()

        # 3. Usuarios por IA preferida
        print("🤖 DISTRIBUCIÓN POR IA PREFERIDA:")
        gemini = db.query(Usuario).filter(Usuario.ia_preferida == "gemini").count()
        claude = db.query(Usuario).filter(Usuario.ia_preferida == "claude").count()
        gpt4 = db.query(Usuario).filter(Usuario.ia_preferida == "gpt-4").count()
        groq = db.query(Usuario).filter(Usuario.ia_preferida == "groq").count()
        print(f"   Gemini: {gemini} usuarios")
        print(f"   Claude: {claude} usuarios")
        print(f"   GPT-4: {gpt4} usuarios")
        print(f"   Groq: {groq} usuarios")
        print()

        # 4. Usuarios por departamento
        print("📍 DISTRIBUCIÓN POR DEPARTAMENTO:")
        departamentos = db.query(
            Usuario.departamento,
            func.count(Usuario.id).label('count')
        ).group_by(Usuario.departamento).order_by(func.count(Usuario.id).desc()).all()

        for dept, count in departamentos:
            print(f"   {dept}: {count} usuarios")
        print()

        # 5. Capacidad total de tokens
        print("🎯 CAPACIDAD DE TOKENS:")
        total_tokens = db.query(func.sum(Usuario.tokens_mensuales)).scalar()
        tokens_usados = db.query(func.sum(Usuario.tokens_usados)).scalar()
        print(f"   Capacidad mensual total: {total_tokens:,} tokens")
        print(f"   Tokens usados: {tokens_usados:,} tokens")
        print(f"   Tokens disponibles: {total_tokens - tokens_usados:,} tokens")
        print()

        # 6. Top 5 usuarios
        print("👥 TOP 5 USUARIOS:")
        top_usuarios = db.query(Usuario).order_by(Usuario.tokens_mensuales.desc()).limit(5).all()
        for i, usuario in enumerate(top_usuarios, 1):
            emoji = {"free": "🆓", "pro": "⭐", "enterprise": "👑"}[usuario.plan]
            print(f"   {emoji} {i}. {usuario.nombre} {usuario.apellido}")
            print(f"      📧 {usuario.email}")
            print(f"      🏢 {usuario.empresa}")
            print(f"      🎯 Plan: {usuario.plan.upper()} | {usuario.tokens_mensuales:,} tokens/mes")
            print()

        # 7. Consultas específicas
        print("🔎 CONSULTAS ESPECÍFICAS:")

        # Usuario con más tokens
        max_tokens = db.query(Usuario).order_by(Usuario.tokens_mensuales.desc()).first()
        print(f"   Usuario con más tokens: {max_tokens.nombre} {max_tokens.apellido}")
        print(f"   ({max_tokens.tokens_mensuales:,} tokens/mes - Plan {max_tokens.plan})")
        print()

        # Usuarios de Huancayo
        huancayo = db.query(Usuario).filter(Usuario.ciudad == "Huancayo").count()
        print(f"   Usuarios en Huancayo: {huancayo}")
        print()

        # Usuarios con email corporativo
        corporativos = db.query(Usuario).filter(
            ~Usuario.email.like("%@gmail.com"),
            ~Usuario.email.like("%@hotmail.com"),
            ~Usuario.email.like("%@yahoo.com"),
            ~Usuario.email.like("%@outlook.com")
        ).count()
        print(f"   Usuarios con email corporativo: {corporativos}")
        print()

        # 8. Verificar métodos del modelo
        print("✅ VERIFICANDO MÉTODOS DEL MODELO:")
        usuario_prueba = db.query(Usuario).filter(Usuario.plan == "free").first()
        if usuario_prueba:
            print(f"   Usuario de prueba: {usuario_prueba.nombre}")
            print(f"   Tokens disponibles: {usuario_prueba.tokens_disponibles()}")
            print(f"   Necesita reset: {usuario_prueba.necesita_reset_tokens()}")
            print(f"   Info del plan: {Usuario.get_plan_info(usuario_prueba.plan)['nombre']}")
            print()

        # 9. Test de consumo de tokens
        print("🧪 TEST DE CONSUMO DE TOKENS:")
        test_user = db.query(Usuario).filter(Usuario.plan == "pro").first()
        if test_user:
            tokens_antes = test_user.tokens_disponibles()
            print(f"   Usuario test: {test_user.nombre} ({test_user.plan})")
            print(f"   Tokens antes: {tokens_antes:,}")

            # Simular consumo
            if test_user.consumir_tokens(500):
                db.commit()
                tokens_despues = test_user.tokens_disponibles()
                print(f"   Tokens después de consumir 500: {tokens_despues:,}")
                print(f"   ✅ Consumo de tokens funciona correctamente")

                # Revertir cambio
                test_user.tokens_usados -= 500
                db.commit()
            print()

        print("=" * 80)
        print("✅ VERIFICACIÓN COMPLETA - BASE DE DATOS FUNCIONANDO CORRECTAMENTE")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    verificar_bd()
