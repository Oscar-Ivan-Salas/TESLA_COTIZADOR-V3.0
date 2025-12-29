#!/usr/bin/env python3
"""
Script para ejecutar tests de Generadores Profesionales
FASE 3: Testing

Ejecuta todos los tests y genera reporte
"""
import subprocess
import sys
from pathlib import Path


def main():
    """Ejecuta tests con pytest"""
    print("=" * 80)
    print("TESTS DE GENERADORES PROFESIONALES - FASE 3")
    print("=" * 80)
    print()

    # Verificar que pytest está instalado
    try:
        import pytest
    except ImportError:
        print("❌ ERROR: pytest no está instalado")
        print("   Instalar con: pip install pytest pytest-cov")
        return 1

    # Directorio de tests
    tests_dir = Path(__file__).parent / "tests"

    if not tests_dir.exists():
        print(f"❌ ERROR: Directorio de tests no encontrado: {tests_dir}")
        return 1

    print(f"📁 Directorio de tests: {tests_dir}")
    print()

    # Comandos de pytest
    commands = [
        # Test básico con verbose
        {
            "name": "Tests Básicos (Verbose)",
            "cmd": ["pytest", str(tests_dir), "-v"],
            "description": "Ejecuta todos los tests con salida detallada"
        },
        # Test con coverage
        {
            "name": "Tests con Coverage",
            "cmd": [
                "pytest",
                str(tests_dir),
                "--cov=app/services/professional/generators",
                "--cov-report=term-missing",
                "--cov-report=html"
            ],
            "description": "Ejecuta tests con reporte de cobertura"
        },
        # Test solo de estructura (rápido)
        {
            "name": "Tests Rápidos (Solo Estructura)",
            "cmd": [
                "pytest",
                str(tests_dir),
                "-v",
                "-k",
                "estructura or routing or importa"
            ],
            "description": "Tests rápidos de estructura e imports"
        }
    ]

    # Pedir al usuario qué tipo de test ejecutar
    print("Opciones de ejecución:")
    for i, cmd_info in enumerate(commands, 1):
        print(f"  {i}. {cmd_info['name']}")
        print(f"     {cmd_info['description']}")
        print()

    try:
        choice = input("Seleccione opción (1-3, Enter para opción 1): ").strip()
        if not choice:
            choice = "1"
        choice_idx = int(choice) - 1
        if choice_idx < 0 or choice_idx >= len(commands):
            choice_idx = 0
    except (ValueError, KeyboardInterrupt):
        choice_idx = 0
        print()

    selected = commands[choice_idx]
    print()
    print(f"Ejecutando: {selected['name']}")
    print(f"Comando: {' '.join(selected['cmd'])}")
    print("=" * 80)
    print()

    # Ejecutar pytest
    try:
        result = subprocess.run(
            selected['cmd'],
            cwd=Path(__file__).parent,
            check=False
        )
        return result.returncode
    except FileNotFoundError:
        print("❌ ERROR: pytest no se encuentra en PATH")
        print("   Asegúrese de estar en el entorno virtual correcto")
        return 1


if __name__ == "__main__":
    sys.exit(main())
