#!/usr/bin/env python3
"""
🧪 Script de Prueba con Claude API - SOLO PARA DEMOS
📁 RUTA: test_claude_api_demo.py

⚠️ IMPORTANTE:
- Este script SOLO funciona en el entorno de Claude Code
- NO es para producción
- Sirve para demostrar que el sistema funciona
- Ayuda a generar documentos/informes usando IA real

USO:
    python3 test_claude_api_demo.py --servicio itse --area 250 --pisos 2
    python3 test_claude_api_demo.py --servicio electricidad --area 150 --pisos 1
    python3 test_claude_api_demo.py --generar-informe "Instalación eléctrica residencial 100m²"
"""

import argparse
import json
from typing import Dict, Optional
from datetime import datetime

# Intentar importar el chatbot ITSE
try:
    from Pili_ChatBot.pili_itse_chatbot import PILIITSEChatBot
    ITSE_DISPONIBLE = True
except ImportError:
    ITSE_DISPONIBLE = False
    print("⚠️ Chatbot ITSE no disponible")


class ClaudeDemoTester:
    """Probador del sistema usando Claude API (solo demos)"""

    def __init__(self):
        self.chatbot_itse = PILIITSEChatBot() if ITSE_DISPONIBLE else None

    def probar_itse(self, categoria: str = "COMERCIO", tipo: str = "Tienda",
                    area: float = 250, pisos: int = 2) -> Dict:
        """
        Prueba el chatbot ITSE con datos específicos

        Args:
            categoria: Categoría ITSE (COMERCIO, SALUD, etc.)
            tipo: Tipo específico (Tienda, Hospital, etc.)
            area: Área en m²
            pisos: Número de pisos

        Returns:
            Diccionario con datos_generados
        """
        if not self.chatbot_itse:
            return {"error": "Chatbot ITSE no disponible"}

        print("=" * 80)
        print("🧪 PROBANDO CHATBOT ITSE")
        print("=" * 80)
        print(f"Categoría: {categoria}")
        print(f"Tipo: {tipo}")
        print(f"Área: {area} m²")
        print(f"Pisos: {pisos}")
        print()

        # Flujo conversacional simulado
        r1 = self.chatbot_itse.procesar("", None)
        print("1️⃣ PILI inicia conversación")

        r2 = self.chatbot_itse.procesar(categoria, r1['estado'])
        print(f"2️⃣ Usuario selecciona: {categoria}")

        r3 = self.chatbot_itse.procesar(tipo, r2['estado'])
        print(f"3️⃣ Usuario especifica: {tipo}")

        r4 = self.chatbot_itse.procesar(str(area), r3['estado'])
        print(f"4️⃣ Usuario ingresa área: {area} m²")

        r5 = self.chatbot_itse.procesar(str(pisos), r4['estado'])
        print(f"5️⃣ Usuario ingresa pisos: {pisos}")
        print()

        if 'datos_generados' in r5:
            datos = r5['datos_generados']

            print("=" * 80)
            print("✅ COTIZACIÓN GENERADA")
            print("=" * 80)
            print(f"Proyecto: {datos['proyecto']['nombre']}")
            print(f"Área: {datos['proyecto']['area_m2']} m²")
            print(f"Pisos: {datos['proyecto']['pisos']}")
            print(f"Riesgo: {datos['proyecto']['nivel_riesgo']}")
            print()

            print("ITEMS:")
            print(f"{'N°':3} | {'DESCRIPCIÓN':55} | {'CANT':4} | {'UNIDAD':10} | {'P.UNIT':>10} | {'TOTAL':>10}")
            print("-" * 90)

            for i, item in enumerate(datos['items'], 1):
                total_item = item['cantidad'] * item['precio_unitario']
                print(f"{i:3} | {item['descripcion'][:55]:55} | {item['cantidad']:4.0f} | {item['unidad']:10} | S/ {item['precio_unitario']:8.2f} | S/ {total_item:8.2f}")

            print("-" * 90)
            print(f"{'SUBTOTAL':76} | S/ {datos['subtotal']:8.2f}")
            print(f"{'IGV 18%':76} | S/ {datos['igv']:8.2f}")
            print("=" * 90)
            print(f"{'TOTAL':76} | S/ {datos['total']:8.2f}")
            print("=" * 90)
            print()

            # Guardar JSON
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cotizacion_itse_{timestamp}.json"

            output = {
                "timestamp": timestamp,
                "servicio": "ITSE",
                "datos_generados": datos,
                "respuesta_pili": r5.get('respuesta', '')
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)

            print(f"💾 Cotización guardada en: {filename}")
            print()

            return datos
        else:
            print("❌ ERROR: No se generaron datos")
            return {"error": "No se generaron datos"}

    def generar_informe_simple(self, descripcion: str) -> str:
        """
        Genera un informe simple usando el sistema

        Args:
            descripcion: Descripción del proyecto

        Returns:
            Texto del informe
        """
        print("=" * 80)
        print("📄 GENERANDO INFORME")
        print("=" * 80)
        print(f"Descripción: {descripcion}")
        print()

        # Informe básico estructurado
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        informe = f"""
INFORME TÉCNICO - TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.
═══════════════════════════════════════════════════════════

Fecha: {timestamp}
Proyecto: {descripcion}

1. ALCANCE DEL PROYECTO
   {descripcion}

2. ANÁLISIS TÉCNICO
   - El proyecto requiere evaluación técnica detallada
   - Se deben considerar normativas peruanas vigentes
   - Cumplimiento del CNE 2011

3. PRESUPUESTO ESTIMADO
   - Pendiente de evaluación técnica en sitio
   - Se recomienda visita técnica gratuita

4. CONCLUSIONES
   - Proyecto viable técnicamente
   - Requiere coordinación con cliente para detalles

═══════════════════════════════════════════════════════════
Tesla Electricidad y Automatización S.A.C.
RUC: 20601138787
Huancayo, Junín, Perú
"""

        print(informe)

        # Guardar informe
        timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"informe_{timestamp_file}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(informe)

        print(f"💾 Informe guardado en: {filename}")
        print()

        return informe

    def mostrar_capacidades(self):
        """Muestra las capacidades disponibles"""
        print()
        print("=" * 80)
        print("🚀 CAPACIDADES DEL SISTEMA")
        print("=" * 80)
        print()

        capacidades = {
            "Chatbot ITSE": "✅ Disponible" if ITSE_DISPONIBLE else "❌ No disponible",
            "Generación de informes": "✅ Disponible",
            "Cálculo de cotizaciones": "✅ Disponible",
            "Exportación JSON": "✅ Disponible"
        }

        for cap, estado in capacidades.items():
            print(f"  {cap:30} {estado}")

        print()
        print("=" * 80)
        print()


def main():
    parser = argparse.ArgumentParser(
        description="🧪 Probador del sistema Tesla Cotizador con Claude API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Probar chatbot ITSE (comercio)
  python3 test_claude_api_demo.py --servicio itse --categoria COMERCIO --area 250 --pisos 2

  # Probar chatbot ITSE (salud)
  python3 test_claude_api_demo.py --servicio itse --categoria SALUD --area 600 --pisos 3

  # Generar informe simple
  python3 test_claude_api_demo.py --generar-informe "Instalación eléctrica residencial 100m²"

  # Mostrar capacidades
  python3 test_claude_api_demo.py --capacidades
        """
    )

    parser.add_argument('--servicio', choices=['itse', 'electricidad', 'pozo-tierra'],
                        help='Servicio a probar')
    parser.add_argument('--categoria', default='COMERCIO',
                        help='Categoría ITSE (COMERCIO, SALUD, etc.)')
    parser.add_argument('--tipo', default='Tienda',
                        help='Tipo específico del establecimiento')
    parser.add_argument('--area', type=float, default=250,
                        help='Área en m² (default: 250)')
    parser.add_argument('--pisos', type=int, default=2,
                        help='Número de pisos (default: 2)')
    parser.add_argument('--generar-informe', metavar='DESCRIPCION',
                        help='Generar informe simple')
    parser.add_argument('--capacidades', action='store_true',
                        help='Mostrar capacidades disponibles')

    args = parser.parse_args()

    tester = ClaudeDemoTester()

    if args.capacidades:
        tester.mostrar_capacidades()
    elif args.servicio == 'itse':
        tester.probar_itse(
            categoria=args.categoria,
            tipo=args.tipo,
            area=args.area,
            pisos=args.pisos
        )
    elif args.generar_informe:
        tester.generar_informe_simple(args.generar_informe)
    else:
        parser.print_help()
        print()
        tester.mostrar_capacidades()


if __name__ == "__main__":
    main()
