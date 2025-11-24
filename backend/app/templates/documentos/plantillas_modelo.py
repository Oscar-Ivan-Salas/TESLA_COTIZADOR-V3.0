"""
PLANTILLAS MODELO PARA GENERACION DE DOCUMENTOS
RUTA: backend/app/templates/documentos/plantillas_modelo.py

Este archivo contiene las plantillas predefinidas para los 6 tipos de documentos
que el sistema puede generar. Estas plantillas sirven como FALLBACK cuando la IA
no esta disponible, asegurando que el sistema siempre pueda funcionar.

TIPOS DE DOCUMENTOS:
1. Cotizacion Simple
2. Cotizacion Compleja
3. Proyecto Simple
4. Proyecto Complejo (PMI)
5. Informe Tecnico
6. Informe Ejecutivo (APA)

SERVICIOS SOPORTADOS (10):
1. electrico-residencial
2. electrico-comercial
3. electrico-industrial
4. contraincendios
5. domotica
6. expedientes
7. saneamiento
8. itse
9. pozo-tierra
10. redes-cctv
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# PLANTILLA: COTIZACION SIMPLE
# ============================================================================

def plantilla_cotizacion_simple(
    servicio: str = "electrico-residencial",
    cliente: str = "Cliente Demo",
    area_m2: float = 100.0,
    datos_adicionales: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Genera plantilla de cotizacion simple para cualquier servicio.

    Esta plantilla se usa cuando:
    - La IA no esta disponible
    - Se necesita una cotizacion rapida
    - El usuario solicita modo offline

    Args:
        servicio: Codigo del servicio (electrico-residencial, etc.)
        cliente: Nombre del cliente
        area_m2: Area en metros cuadrados
        datos_adicionales: Datos extra opcionales

    Returns:
        JSON estructurado listo para generar documento
    """

    # Obtener items segun servicio
    items = _obtener_items_por_servicio(servicio, area_m2)

    # Calcular totales
    subtotal = sum(item["total"] for item in items)
    igv = subtotal * 0.18
    total = subtotal + igv

    # Obtener informacion del servicio
    info_servicio = SERVICIOS_INFO.get(servicio, SERVICIOS_INFO["electrico-residencial"])

    return {
        "tipo_documento": "cotizacion",
        "complejidad": "simple",
        "agente_responsable": "PILI Cotizadora",
        "datos_extraidos": {
            "numero": f"COT-{datetime.now().strftime('%Y%m%d%H%M')}-{servicio[:3].upper()}",
            "cliente": cliente,
            "proyecto": info_servicio["nombre"],
            "descripcion": f"Servicio de {info_servicio['nombre']} segun normativa {info_servicio['normativa']}",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "vigencia": "30 dias calendario",
            "items": items,
            "subtotal": round(subtotal, 2),
            "igv": round(igv, 2),
            "total": round(total, 2),
            "observaciones": _generar_observaciones_cotizacion(servicio, info_servicio),
            "normativa_aplicable": info_servicio["normativa"],
            "area_m2": area_m2
        },
        "metadata": {
            "generado_por": "Plantilla Local",
            "timestamp": datetime.now().isoformat(),
            "version": "3.0",
            "modo": "offline"
        }
    }


# ============================================================================
# PLANTILLA: COTIZACION COMPLEJA
# ============================================================================

def plantilla_cotizacion_compleja(
    servicio: str = "electrico-residencial",
    cliente: str = "Cliente Demo",
    area_m2: float = 200.0,
    datos_adicionales: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Genera plantilla de cotizacion compleja con mas detalles tecnicos.

    Incluye:
    - Mas items detallados
    - Desglose por etapas
    - Especificaciones tecnicas ampliadas
    - Cronograma estimado
    """

    # Obtener items expandidos
    items = _obtener_items_por_servicio(servicio, area_m2, expandido=True)

    # Calcular totales
    subtotal = sum(item["total"] for item in items)
    igv = subtotal * 0.18
    total = subtotal + igv

    info_servicio = SERVICIOS_INFO.get(servicio, SERVICIOS_INFO["electrico-residencial"])

    return {
        "tipo_documento": "cotizacion",
        "complejidad": "complejo",
        "agente_responsable": "PILI Cotizadora Senior",
        "datos_extraidos": {
            "numero": f"COT-{datetime.now().strftime('%Y%m%d%H%M')}-{servicio[:3].upper()}-PRO",
            "cliente": cliente,
            "proyecto": f"{info_servicio['nombre']} - Version Profesional",
            "descripcion": f"""Servicio profesional de {info_servicio['nombre']}.

ALCANCE DETALLADO:
- Ingenieria de detalle con calculos segun {info_servicio['normativa']}
- Suministro de materiales de primera calidad
- Instalacion por personal tecnico certificado
- Pruebas y puesta en marcha
- Documentacion tecnica completa
- Garantia de 12 meses""",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "vigencia": "30 dias calendario",
            "items": items,
            "subtotal": round(subtotal, 2),
            "igv": round(igv, 2),
            "total": round(total, 2),
            "observaciones": _generar_observaciones_cotizacion(servicio, info_servicio, detallado=True),
            "normativa_aplicable": info_servicio["normativa"],
            "area_m2": area_m2,
            "cronograma_estimado": _generar_cronograma_cotizacion(area_m2),
            "garantias": [
                "12 meses en mano de obra",
                "Garantia de fabricante en equipos",
                "Soporte tecnico por 6 meses"
            ],
            "condiciones_pago": [
                "50% adelanto a la firma del contrato",
                "30% al 50% de avance",
                "20% contra entrega y conformidad"
            ]
        },
        "metadata": {
            "generado_por": "Plantilla Local",
            "timestamp": datetime.now().isoformat(),
            "version": "3.0",
            "modo": "offline"
        }
    }


# ============================================================================
# PLANTILLA: PROYECTO SIMPLE
# ============================================================================

def plantilla_proyecto_simple(
    servicio: str = "electrico-residencial",
    cliente: str = "Cliente Demo",
    area_m2: float = 150.0,
    datos_adicionales: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Genera plantilla de proyecto simple con fases basicas.

    Incluye:
    - 5 fases principales
    - Cronograma simplificado
    - Recursos basicos
    - Entregables principales
    """

    info_servicio = SERVICIOS_INFO.get(servicio, SERVICIOS_INFO["electrico-residencial"])

    # Calcular duracion segun area
    duracion_base = max(15, int(area_m2 / 5))

    # Generar fases
    fases = [
        {
            "nombre": "Inicio y Planificacion",
            "duracion_dias": 5,
            "actividades": [
                "Levantamiento de informacion",
                "Elaboracion de propuesta tecnica",
                "Aprobacion de alcance y presupuesto"
            ],
            "entregable": "Plan de proyecto aprobado"
        },
        {
            "nombre": "Ingenieria y Diseno",
            "duracion_dias": max(7, int(area_m2 / 15)),
            "actividades": [
                "Calculos tecnicos segun normativa",
                "Elaboracion de planos",
                "Metrados y especificaciones"
            ],
            "entregable": "Expediente tecnico"
        },
        {
            "nombre": "Ejecucion",
            "duracion_dias": duracion_base,
            "actividades": [
                "Adquisicion de materiales",
                "Instalacion y montaje",
                "Supervision tecnica"
            ],
            "entregable": "Obra ejecutada"
        },
        {
            "nombre": "Pruebas y Puesta en Marcha",
            "duracion_dias": 5,
            "actividades": [
                "Pruebas de funcionamiento",
                "Ajustes y calibraciones",
                "Capacitacion"
            ],
            "entregable": "Sistema operativo"
        },
        {
            "nombre": "Cierre",
            "duracion_dias": 3,
            "actividades": [
                "Documentacion as-built",
                "Entrega de garantias",
                "Acta de conformidad"
            ],
            "entregable": "Proyecto cerrado"
        }
    ]

    duracion_total = sum(f["duracion_dias"] for f in fases)
    fecha_inicio = datetime.now()
    fecha_fin = fecha_inicio + timedelta(days=duracion_total)

    # Presupuesto estimado
    presupuesto = area_m2 * info_servicio.get("precio_base_m2", 50) * 1.18

    return {
        "tipo_documento": "proyecto",
        "complejidad": "simple",
        "agente_responsable": "PILI Coordinadora",
        "datos_extraidos": {
            "nombre": f"Proyecto {info_servicio['nombre']}",
            "codigo": f"PROY-{datetime.now().strftime('%Y%m%d')}-{servicio[:3].upper()}",
            "cliente": cliente,
            "descripcion": f"Proyecto de {info_servicio['nombre']} con gestion simplificada",
            "alcance": _generar_alcance_proyecto(servicio, info_servicio),
            "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
            "fecha_fin": fecha_fin.strftime("%d/%m/%Y"),
            "duracion_total_dias": duracion_total,
            "presupuesto_estimado": round(presupuesto, 2),
            "fases": fases,
            "recursos": _generar_recursos_basicos(),
            "riesgos": _generar_riesgos_basicos(),
            "entregables": [
                "Plan de proyecto",
                "Planos de instalacion",
                "Especificaciones tecnicas",
                "Memoria de calculo",
                "Protocolos de pruebas",
                "Planos as-built",
                "Certificados de garantia"
            ],
            "normativa_aplicable": info_servicio["normativa"]
        },
        "metadata": {
            "generado_por": "Plantilla Local",
            "timestamp": datetime.now().isoformat(),
            "version": "3.0",
            "modo": "offline"
        }
    }


# ============================================================================
# PLANTILLA: PROYECTO COMPLEJO (PMI)
# ============================================================================

def plantilla_proyecto_complejo(
    servicio: str = "electrico-residencial",
    cliente: str = "Cliente Demo",
    area_m2: float = 300.0,
    datos_adicionales: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Genera plantilla de proyecto complejo con metodologia PMI.

    Incluye:
    - 6 fases (incluye Gestion de Stakeholders)
    - Diagrama Gantt
    - Analisis de riesgos detallado
    - Matriz RACI
    - KPIs del proyecto
    """

    info_servicio = SERVICIOS_INFO.get(servicio, SERVICIOS_INFO["electrico-residencial"])

    # Calcular duracion segun area (mas tiempo por complejidad)
    duracion_base = max(20, int(area_m2 / 4))

    # Generar fases PMI completas
    fases = [
        {
            "nombre": "Inicio y Planificacion",
            "duracion_dias": 10,
            "actividades": [
                "Levantamiento de informacion detallada",
                "Elaboracion de Project Charter",
                "Definicion de alcance (WBS)",
                "Aprobacion de presupuesto"
            ],
            "entregable": "Project Charter aprobado"
        },
        {
            "nombre": "Gestion de Stakeholders",
            "duracion_dias": 3,
            "actividades": [
                "Identificacion de stakeholders",
                "Matriz de interes/poder",
                "Plan de comunicaciones",
                "Estrategia de engagement"
            ],
            "entregable": "Registro de stakeholders"
        },
        {
            "nombre": "Ingenieria y Diseno",
            "duracion_dias": max(12, int(area_m2 / 10)),
            "actividades": [
                "Calculos tecnicos avanzados",
                "Modelado y simulacion",
                "Planos de detalle",
                "Especificaciones tecnicas",
                "Revision por pares"
            ],
            "entregable": "Expediente tecnico certificado"
        },
        {
            "nombre": "Ejecucion",
            "duracion_dias": int(duracion_base * 1.5),
            "actividades": [
                "Gestion de adquisiciones",
                "Control de contratistas",
                "Instalacion y montaje",
                "Control de calidad continuo",
                "Gestion de cambios"
            ],
            "entregable": "Obra ejecutada con control"
        },
        {
            "nombre": "Pruebas y Puesta en Marcha",
            "duracion_dias": 8,
            "actividades": [
                "Pruebas FAT/SAT",
                "Comisionamiento",
                "Capacitacion a operadores",
                "Documentacion de operacion"
            ],
            "entregable": "Sistema comisionado"
        },
        {
            "nombre": "Cierre",
            "duracion_dias": 5,
            "actividades": [
                "Cierre administrativo",
                "Lecciones aprendidas",
                "Documentacion final",
                "Liberacion de recursos",
                "Acta de cierre"
            ],
            "entregable": "Proyecto cerrado formalmente"
        }
    ]

    duracion_total = sum(f["duracion_dias"] for f in fases)
    fecha_inicio = datetime.now()
    fecha_fin = fecha_inicio + timedelta(days=duracion_total)

    # Presupuesto estimado (mayor por complejidad)
    presupuesto = area_m2 * info_servicio.get("precio_base_m2", 50) * 1.5 * 1.18

    # Generar datos Gantt
    gantt_data = _generar_datos_gantt(fases, fecha_inicio)

    return {
        "tipo_documento": "proyecto",
        "complejidad": "complejo",
        "agente_responsable": "PILI Directora PMI",
        "datos_extraidos": {
            "nombre": f"Proyecto {info_servicio['nombre']} - PMI",
            "codigo": f"PROY-{datetime.now().strftime('%Y%m%d')}-{servicio[:3].upper()}-PMI",
            "cliente": cliente,
            "descripcion": f"Proyecto de {info_servicio['nombre']} con gestion PMI avanzada",
            "alcance": _generar_alcance_proyecto(servicio, info_servicio, detallado=True),
            "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
            "fecha_fin": fecha_fin.strftime("%d/%m/%Y"),
            "duracion_total_dias": duracion_total,
            "presupuesto_estimado": round(presupuesto, 2),
            "fases": fases,
            "recursos": _generar_recursos_pmi(),
            "riesgos": _generar_riesgos_pmi(),
            "entregables": [
                "Project Charter",
                "Plan de gestion del proyecto",
                "Registro de stakeholders",
                "WBS y diccionario",
                "Cronograma detallado (Gantt)",
                "Planos de instalacion",
                "Especificaciones tecnicas",
                "Plan de calidad",
                "Registro de riesgos",
                "Protocolos FAT/SAT",
                "Planos as-built",
                "Lecciones aprendidas",
                "Acta de cierre"
            ],
            "cronograma_gantt": gantt_data,
            "kpis": {
                "SPI": 1.0,  # Schedule Performance Index
                "CPI": 1.0,  # Cost Performance Index
                "EV": presupuesto * 0.5,  # Earned Value
                "PV": presupuesto * 0.5,  # Planned Value
                "AC": presupuesto * 0.5   # Actual Cost
            },
            "normativa_aplicable": info_servicio["normativa"]
        },
        "metadata": {
            "generado_por": "Plantilla Local",
            "timestamp": datetime.now().isoformat(),
            "version": "3.0",
            "modo": "offline"
        }
    }


# ============================================================================
# PLANTILLA: INFORME TECNICO
# ============================================================================

def plantilla_informe_tecnico(
    servicio: str = "electrico-residencial",
    cliente: str = "Cliente Demo",
    datos_adicionales: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Genera plantilla de informe tecnico estandar.

    Estructura:
    1. Introduccion
    2. Marco Normativo
    3. Descripcion Tecnica
    4. Metodologia
    5. Resultados
    """

    info_servicio = SERVICIOS_INFO.get(servicio, SERVICIOS_INFO["electrico-residencial"])

    secciones = [
        {
            "titulo": "1. Introduccion",
            "contenido": f"""El presente informe tecnico describe el proyecto de {info_servicio['nombre']}
desarrollado para el cliente {cliente}.

ANTECEDENTES:
El cliente requiere la implementacion de un sistema de {info_servicio['nombre']} que cumpla
con las normativas vigentes y los estandares de calidad requeridos.

OBJETIVOS:
- Disenar el sistema segun normativa {info_servicio['normativa']}
- Especificar materiales y equipos requeridos
- Definir metodologia de instalacion
- Establecer procedimientos de prueba""",
            "subsecciones": [
                "Antecedentes",
                "Objetivos del proyecto",
                "Alcance del informe"
            ]
        },
        {
            "titulo": "2. Marco Normativo",
            "contenido": f"""El proyecto se desarrolla bajo la normativa {info_servicio['normativa']}.

CODIGOS Y ESTANDARES APLICABLES:
- {info_servicio['normativa']}
- Reglamento Nacional de Edificaciones (RNE)
- Normas tecnicas peruanas aplicables

REQUISITOS REGULATORIOS:
- Certificacion de instalaciones
- Protocolos de seguridad
- Documentacion tecnica requerida""",
            "subsecciones": [
                "Normativa aplicable",
                "Codigos y estandares",
                "Requisitos regulatorios"
            ]
        },
        {
            "titulo": "3. Descripcion Tecnica",
            "contenido": f"""Descripcion detallada del sistema de {info_servicio['nombre']}.

CARACTERISTICAS PRINCIPALES:
- Sistema disenado segun {info_servicio['normativa']}
- Materiales de primera calidad
- Equipos con certificacion internacional

COMPONENTES DEL SISTEMA:
Se incluyen todos los componentes necesarios para la correcta operacion del sistema.""",
            "subsecciones": [
                "Caracteristicas tecnicas",
                "Componentes principales",
                "Especificaciones"
            ]
        },
        {
            "titulo": "4. Metodologia",
            "contenido": """Metodologia aplicada en el desarrollo del proyecto.

PROCESO DE DISENO:
1. Levantamiento de informacion
2. Calculos y dimensionamiento
3. Seleccion de equipos
4. Elaboracion de planos

VERIFICACIONES:
- Cumplimiento de normativa
- Compatibilidad de equipos
- Factores de seguridad""",
            "subsecciones": [
                "Proceso de diseno",
                "Calculos y verificaciones",
                "Pruebas realizadas"
            ]
        },
        {
            "titulo": "5. Resultados",
            "contenido": """Resultados obtenidos en la ejecucion del proyecto.

CUMPLIMIENTO DE ESPECIFICACIONES:
El sistema cumple con todas las especificaciones tecnicas requeridas.

PRUEBAS REALIZADAS:
Todas las pruebas se ejecutaron satisfactoriamente segun protocolos establecidos.

OBSERVACIONES:
Se recomienda seguimiento periodico para mantenimiento preventivo.""",
            "subsecciones": [
                "Cumplimiento de especificaciones",
                "Pruebas y verificaciones",
                "Observaciones"
            ]
        }
    ]

    return {
        "tipo_documento": "informe",
        "complejidad": "simple",
        "tipo_informe": "tecnico",
        "agente_responsable": "PILI Reportera",
        "datos_extraidos": {
            "titulo": f"Informe Tecnico - {info_servicio['nombre']}",
            "codigo": f"INF-{datetime.now().strftime('%Y%m%d')}-{servicio[:3].upper()}",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "autor": "Tesla Electricidad y Automatizacion S.A.C.",
            "cliente": cliente,
            "resumen_ejecutivo": f"""El presente informe tecnico presenta el desarrollo del proyecto de
{info_servicio['nombre']} para {cliente}. El proyecto se ejecuta bajo la normativa
{info_servicio['normativa']} y cumple con todos los requisitos tecnicos establecidos.""",
            "secciones": secciones,
            "conclusiones": [
                f"El proyecto de {info_servicio['nombre']} es tecnicamente viable",
                f"Cumple con la normativa {info_servicio['normativa']}",
                "Los calculos garantizan funcionamiento seguro",
                "Se recomienda seguimiento periodico"
            ],
            "recomendaciones": [
                "Iniciar el proyecto segun cronograma",
                "Asegurar disponibilidad de materiales",
                "Implementar control de calidad riguroso"
            ],
            "formato": "Tecnico estandar",
            "normativa_aplicable": info_servicio["normativa"]
        },
        "metadata": {
            "generado_por": "Plantilla Local",
            "timestamp": datetime.now().isoformat(),
            "version": "3.0",
            "modo": "offline"
        }
    }


# ============================================================================
# PLANTILLA: INFORME EJECUTIVO (APA)
# ============================================================================

def plantilla_informe_ejecutivo(
    servicio: str = "electrico-residencial",
    cliente: str = "Cliente Demo",
    presupuesto: float = 50000.0,
    datos_adicionales: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Genera plantilla de informe ejecutivo en formato APA.

    Incluye:
    - Executive Summary
    - Analisis financiero (ROI, TIR, Payback)
    - Metricas y KPIs
    - Graficos sugeridos
    - Bibliografia APA
    """

    info_servicio = SERVICIOS_INFO.get(servicio, SERVICIOS_INFO["electrico-residencial"])

    # Calcular metricas financieras
    roi_estimado = 25
    tir_proyectada = 30
    payback_meses = 18

    secciones = [
        {
            "titulo": "1. Executive Summary",
            "contenido": f"""Resumen ejecutivo del proyecto de {info_servicio['nombre']}.

CONTEXTO:
{cliente} requiere implementar un sistema de {info_servicio['nombre']} para optimizar
sus operaciones y cumplir con la normativa {info_servicio['normativa']}.

HALLAZGOS PRINCIPALES:
- Inversion requerida: ${presupuesto:,.2f} USD
- ROI estimado: {roi_estimado}%
- Periodo de retorno: {payback_meses} meses

RECOMENDACION:
Se recomienda aprobar el proyecto dada su alta viabilidad tecnica y financiera.""",
            "subsecciones": [
                "Contexto del proyecto",
                "Hallazgos principales",
                "Recomendaciones clave"
            ]
        },
        {
            "titulo": "2. Analisis de Situacion",
            "contenido": """Analisis detallado de la situacion actual.

CONTEXTO ORGANIZACIONAL:
La organizacion requiere modernizar sus instalaciones para mejorar eficiencia
y cumplir con regulaciones vigentes.

PROBLEMATICA IDENTIFICADA:
- Equipos obsoletos
- Incumplimiento normativo
- Ineficiencia operativa

OPORTUNIDADES:
- Reduccion de costos operativos
- Mejora en seguridad
- Cumplimiento regulatorio""",
            "subsecciones": [
                "Contexto organizacional",
                "Problematica identificada",
                "Oportunidades de mejora"
            ]
        },
        {
            "titulo": "3. Metricas y KPIs",
            "contenido": f"""Indicadores clave de desempeno del proyecto.

METRICAS DE EFICIENCIA:
- Reduccion de costos operativos: 20%
- Incremento de eficiencia: 35%
- Ahorro energetico anual: ${presupuesto * 0.15:,.2f} USD

COMPARATIVA CON BENCHMARKS:
El proyecto supera los estandares del mercado en terminos de ROI y eficiencia.""",
            "subsecciones": [
                "Metricas de eficiencia",
                "ROI estimado",
                "Comparativa con benchmarks"
            ]
        },
        {
            "titulo": "4. Analisis Financiero",
            "contenido": f"""Analisis de viabilidad financiera detallado.

INVERSION REQUERIDA:
- Inversion total: ${presupuesto:,.2f} USD
- Capital de trabajo: ${presupuesto * 0.1:,.2f} USD

RETORNO DE INVERSION:
- ROI: {roi_estimado}%
- TIR: {tir_proyectada}%
- Payback: {payback_meses} meses

FLUJO DE CAJA:
Se proyecta flujo de caja positivo a partir del mes 6.""",
            "subsecciones": [
                "Inversion requerida",
                "Retorno de inversion (ROI)",
                "Flujo de caja proyectado"
            ]
        },
        {
            "titulo": "5. Evaluacion de Riesgos",
            "contenido": """Analisis de riesgos y estrategias de mitigacion.

RIESGOS IDENTIFICADOS:
1. Retrasos en entrega de equipos (Probabilidad: Media, Impacto: Alto)
2. Variacion de precios de materiales (Probabilidad: Media, Impacto: Medio)
3. Cambios en alcance (Probabilidad: Alta, Impacto: Alto)

PLANES DE MITIGACION:
- Compra anticipada de materiales criticos
- Clausulas de precio fijo en contratos
- Control de cambios riguroso""",
            "subsecciones": [
                "Matriz de riesgos",
                "Planes de mitigacion",
                "Contingencias"
            ]
        },
        {
            "titulo": "6. Plan de Implementacion",
            "contenido": """Estrategia de implementacion recomendada.

CRONOGRAMA EJECUTIVO:
- Fase 1: Planificacion (2 semanas)
- Fase 2: Adquisiciones (3 semanas)
- Fase 3: Ejecucion (6 semanas)
- Fase 4: Cierre (1 semana)

RECURSOS REQUERIDOS:
Equipo multidisciplinario con experiencia en proyectos similares.

HITOS CRITICOS:
1. Aprobacion del proyecto
2. Inicio de obras
3. Comisionamiento
4. Cierre formal""",
            "subsecciones": [
                "Cronograma ejecutivo",
                "Recursos requeridos",
                "Hitos criticos"
            ]
        }
    ]

    return {
        "tipo_documento": "informe",
        "complejidad": "complejo",
        "tipo_informe": "ejecutivo",
        "agente_responsable": "PILI Directora Ejecutiva",
        "datos_extraidos": {
            "titulo": f"Informe Ejecutivo - {info_servicio['nombre']}",
            "codigo": f"INF-{datetime.now().strftime('%Y%m%d')}-{servicio[:3].upper()}-EXE",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "autor": "Tesla Electricidad y Automatizacion S.A.C.",
            "cliente": cliente,
            "resumen_ejecutivo": f"""El presente informe ejecutivo analiza la viabilidad del proyecto de
{info_servicio['nombre']} para {cliente}.

DATOS PRINCIPALES:
- Inversion total: ${presupuesto:,.2f} USD
- ROI estimado: {roi_estimado}%
- Periodo de retorno: {payback_meses} meses
- TIR proyectada: {tir_proyectada}%

El proyecto presenta alta viabilidad tecnica y financiera, recomendandose su aprobacion
e implementacion inmediata.""",
            "secciones": secciones,
            "conclusiones": [
                f"El proyecto es tecnicamente viable segun {info_servicio['normativa']}",
                f"El analisis financiero demuestra ROI de {roi_estimado}%",
                "Los riesgos son manejables con los planes propuestos",
                "Se recomienda aprobacion e implementacion inmediata"
            ],
            "recomendaciones": [
                "Aprobar el proyecto en el corto plazo",
                "Establecer comite de direccion para seguimiento",
                "Implementar por fases para mitigar riesgos",
                "Evaluar opciones de financiamiento"
            ],
            "metricas_clave": {
                "roi_estimado": roi_estimado,
                "payback_meses": payback_meses,
                "tir_proyectada": tir_proyectada,
                "ahorro_energetico_anual": presupuesto * 0.15,
                "reduccion_costos_operativos": 20,
                "incremento_eficiencia": 35,
                "nivel_satisfaccion_esperado": 95
            },
            "graficos_sugeridos": [
                "Dashboard ejecutivo de KPIs",
                "Analisis de ROI y payback",
                "Diagrama de Gantt",
                "Matriz de riesgos",
                "Flujo de caja proyectado",
                "Comparativa de escenarios"
            ],
            "bibliografia": [
                f"Ministerio de Energia y Minas. (2011). {info_servicio['normativa']}. Lima, Peru.",
                "Project Management Institute. (2021). PMBOK Guide - Seventh Edition. PMI.",
                "Reglamento Nacional de Edificaciones. (2023). Lima: MVCS."
            ],
            "formato": "APA 7ma edicion",
            "normativa_aplicable": info_servicio["normativa"]
        },
        "metadata": {
            "generado_por": "Plantilla Local",
            "timestamp": datetime.now().isoformat(),
            "version": "3.0",
            "modo": "offline"
        }
    }


# ============================================================================
# INFORMACION DE SERVICIOS
# ============================================================================

SERVICIOS_INFO = {
    "electrico-residencial": {
        "nombre": "Instalaciones Electricas Residenciales",
        "normativa": "CNE Suministro 2011",
        "precio_base_m2": 45.00
    },
    "electrico-comercial": {
        "nombre": "Instalaciones Electricas Comerciales",
        "normativa": "CNE Suministro 2011",
        "precio_base_m2": 65.00
    },
    "electrico-industrial": {
        "nombre": "Instalaciones Electricas Industriales",
        "normativa": "CNE Suministro 2011 + CNE Utilizacion",
        "precio_base_m2": 85.00
    },
    "contraincendios": {
        "nombre": "Sistemas Contra Incendios",
        "normativa": "NFPA 13, NFPA 72, NFPA 20",
        "precio_base_m2": 95.00
    },
    "domotica": {
        "nombre": "Domotica y Automatizacion",
        "normativa": "KNX/EIB, Z-Wave, Zigbee",
        "precio_base_m2": 120.00
    },
    "expedientes": {
        "nombre": "Expedientes Tecnicos de Edificacion",
        "normativa": "RNE, Normativa Municipal",
        "precio_base_m2": 15.00
    },
    "saneamiento": {
        "nombre": "Sistemas de Agua y Desague",
        "normativa": "RNE IS.010, IS.020",
        "precio_base_m2": 55.00
    },
    "itse": {
        "nombre": "Certificaciones ITSE",
        "normativa": "D.S. 002-2018-PCM",
        "precio_base_m2": 8.50
    },
    "pozo-tierra": {
        "nombre": "Sistemas de Puesta a Tierra",
        "normativa": "CNE Suministro Seccion 250",
        "precio_base_m2": 12.00
    },
    "redes-cctv": {
        "nombre": "Redes y CCTV",
        "normativa": "TIA/EIA-568, ANSI/TIA-942",
        "precio_base_m2": 80.00
    }
}


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def _obtener_items_por_servicio(servicio: str, area_m2: float, expandido: bool = False) -> List[Dict]:
    """Genera items de cotizacion segun servicio y area"""

    if servicio == "electrico-residencial":
        num_circuitos = max(6, int(area_m2 / 25))
        num_luces = int(area_m2 / 10)
        num_tomacorrientes = int(area_m2 / 15)

        items = [
            {
                "descripcion": "Tablero electrico monofasico 12 circuitos",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 450.00,
                "total": 450.00
            },
            {
                "descripcion": "Circuitos electricos (cable THW + tuberia PVC)",
                "cantidad": num_circuitos,
                "unidad": "cto",
                "precio_unitario": 120.00,
                "total": num_circuitos * 120.00
            },
            {
                "descripcion": "Puntos de iluminacion LED",
                "cantidad": num_luces,
                "unidad": "pto",
                "precio_unitario": 45.00,
                "total": num_luces * 45.00
            },
            {
                "descripcion": "Tomacorrientes dobles con toma tierra",
                "cantidad": num_tomacorrientes,
                "unidad": "pto",
                "precio_unitario": 35.00,
                "total": num_tomacorrientes * 35.00
            },
            {
                "descripcion": "Sistema de puesta a tierra",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": 850.00,
                "total": 850.00
            }
        ]

        if expandido:
            items.extend([
                {
                    "descripcion": "Tablero de medicion y proteccion",
                    "cantidad": 1,
                    "unidad": "und",
                    "precio_unitario": 380.00,
                    "total": 380.00
                },
                {
                    "descripcion": "Interruptores termo-magneticos",
                    "cantidad": num_circuitos,
                    "unidad": "und",
                    "precio_unitario": 45.00,
                    "total": num_circuitos * 45.00
                }
            ])

        return items

    # Default para otros servicios
    info = SERVICIOS_INFO.get(servicio, SERVICIOS_INFO["electrico-residencial"])
    total_base = area_m2 * info["precio_base_m2"]

    return [
        {
            "descripcion": f"Servicio de {info['nombre']}",
            "cantidad": area_m2,
            "unidad": "m2",
            "precio_unitario": info["precio_base_m2"],
            "total": total_base
        },
        {
            "descripcion": "Materiales y mano de obra",
            "cantidad": 1,
            "unidad": "glb",
            "precio_unitario": total_base * 0.3,
            "total": total_base * 0.3
        }
    ]


def _generar_observaciones_cotizacion(servicio: str, info_servicio: Dict, detallado: bool = False) -> str:
    """Genera observaciones para cotizacion"""

    obs = f"""OBSERVACIONES TECNICAS:

1. Trabajos ejecutados segun {info_servicio['normativa']}
2. Materiales de primera calidad con certificacion
3. Mano de obra especializada
4. Garantia de 12 meses
5. Precios en dolares americanos (USD)
6. Forma de pago: 50% adelanto, 50% contra entrega

Cotizacion valida por 30 dias."""

    if detallado:
        obs += """

CONDICIONES ADICIONALES:
- Incluye transporte de materiales
- Pruebas y puesta en marcha incluidas
- Capacitacion al personal del cliente
- Documentacion tecnica completa"""

    return obs


def _generar_cronograma_cotizacion(area_m2: float) -> List[Dict]:
    """Genera cronograma estimado para cotizacion compleja"""

    duracion_base = max(15, int(area_m2 / 5))

    return [
        {"etapa": "Ingenieria", "duracion": f"{max(5, int(duracion_base * 0.2))} dias"},
        {"etapa": "Adquisiciones", "duracion": f"{max(5, int(duracion_base * 0.2))} dias"},
        {"etapa": "Instalacion", "duracion": f"{int(duracion_base * 0.5)} dias"},
        {"etapa": "Pruebas", "duracion": f"{max(3, int(duracion_base * 0.1))} dias"}
    ]


def _generar_alcance_proyecto(servicio: str, info_servicio: Dict, detallado: bool = False) -> str:
    """Genera alcance del proyecto"""

    alcance = f"""ALCANCE DEL PROYECTO:

El proyecto comprende el diseno, suministro, instalacion y puesta en marcha de {info_servicio['nombre']}.

INCLUYE:
- Ingenieria de detalle con planos y especificaciones
- Suministro de materiales y equipos
- Instalacion segun {info_servicio['normativa']}
- Pruebas y puesta en marcha
- Capacitacion al personal
- Documentacion tecnica

NO INCLUYE:
- Obra civil no especificada
- Permisos municipales
- Equipos fuera de especificacion"""

    if detallado:
        alcance += """

EXCLUSIONES ADICIONALES:
- Trabajos en areas no contempladas
- Modificaciones a estructuras existentes
- Licencias de software de terceros"""

    return alcance


def _generar_recursos_basicos() -> List[Dict]:
    """Genera lista de recursos basicos del proyecto"""

    return [
        {
            "rol": "Jefe de Proyecto",
            "cantidad": 1,
            "dedicacion": "25%",
            "responsabilidad": "Coordinacion general"
        },
        {
            "rol": "Ingeniero Residente",
            "cantidad": 1,
            "dedicacion": "100%",
            "responsabilidad": "Ejecucion tecnica"
        },
        {
            "rol": "Tecnicos Instaladores",
            "cantidad": 3,
            "dedicacion": "100%",
            "responsabilidad": "Instalacion"
        },
        {
            "rol": "Inspector de Calidad",
            "cantidad": 1,
            "dedicacion": "50%",
            "responsabilidad": "Control de calidad"
        }
    ]


def _generar_recursos_pmi() -> List[Dict]:
    """Genera lista de recursos para proyecto PMI"""

    recursos = _generar_recursos_basicos()
    recursos.extend([
        {
            "rol": "Ingeniero de Diseno",
            "cantidad": 1,
            "dedicacion": "100%",
            "responsabilidad": "Calculos y diseno"
        },
        {
            "rol": "Coordinador de Adquisiciones",
            "cantidad": 1,
            "dedicacion": "50%",
            "responsabilidad": "Compras y logistica"
        },
        {
            "rol": "Especialista en Seguridad",
            "cantidad": 1,
            "dedicacion": "25%",
            "responsabilidad": "Plan de seguridad"
        }
    ])
    return recursos


def _generar_riesgos_basicos() -> List[Dict]:
    """Genera lista de riesgos basicos"""

    return [
        {
            "riesgo": "Retrasos en entrega de materiales",
            "probabilidad": "Media",
            "impacto": "Alto",
            "mitigacion": "Compra anticipada"
        },
        {
            "riesgo": "Condiciones climaticas adversas",
            "probabilidad": "Baja",
            "impacto": "Medio",
            "mitigacion": "Programacion flexible"
        },
        {
            "riesgo": "Cambios en alcance",
            "probabilidad": "Media",
            "impacto": "Alto",
            "mitigacion": "Control de cambios"
        }
    ]


def _generar_riesgos_pmi() -> List[Dict]:
    """Genera lista de riesgos para proyecto PMI"""

    riesgos = _generar_riesgos_basicos()
    riesgos.extend([
        {
            "riesgo": "Interferencias con otros contratistas",
            "probabilidad": "Alta",
            "impacto": "Medio",
            "mitigacion": "Coordinacion semanal"
        },
        {
            "riesgo": "Fallas en equipos especializados",
            "probabilidad": "Baja",
            "impacto": "Alto",
            "mitigacion": "Garantias extendidas"
        }
    ])
    return riesgos


def _generar_datos_gantt(fases: List[Dict], fecha_inicio: datetime) -> Dict[str, Any]:
    """Genera datos para diagrama Gantt"""

    gantt_data = {
        "fecha_inicio_proyecto": fecha_inicio.strftime("%Y-%m-%d"),
        "tareas": []
    }

    fecha_actual = fecha_inicio

    for idx, fase in enumerate(fases):
        fecha_fin_fase = fecha_actual + timedelta(days=fase["duracion_dias"])

        gantt_data["tareas"].append({
            "id": idx + 1,
            "nombre": fase["nombre"],
            "fecha_inicio": fecha_actual.strftime("%Y-%m-%d"),
            "fecha_fin": fecha_fin_fase.strftime("%Y-%m-%d"),
            "duracion": fase["duracion_dias"],
            "progreso": 0,
            "dependencias": [idx] if idx > 0 else []
        })

        fecha_actual = fecha_fin_fase

    return gantt_data


# ============================================================================
# FUNCION PRINCIPAL DE ACCESO
# ============================================================================

def obtener_plantilla(
    tipo_documento: str,
    complejidad: str = "simple",
    servicio: str = "electrico-residencial",
    cliente: str = "Cliente Demo",
    area_m2: float = 100.0,
    **kwargs
) -> Dict[str, Any]:
    """
    Funcion principal para obtener cualquier plantilla de documento.

    Esta funcion es el punto de entrada unico para el sistema de plantillas.
    Permite generar documentos de forma local sin necesidad de IA.

    Args:
        tipo_documento: "cotizacion", "proyecto" o "informe"
        complejidad: "simple" o "complejo"
        servicio: Codigo del servicio
        cliente: Nombre del cliente
        area_m2: Area en metros cuadrados
        **kwargs: Argumentos adicionales

    Returns:
        JSON estructurado listo para generar documento

    Ejemplo:
        >>> plantilla = obtener_plantilla(
        ...     tipo_documento="cotizacion",
        ...     complejidad="simple",
        ...     servicio="electrico-residencial",
        ...     cliente="Juan Perez",
        ...     area_m2=150
        ... )
    """

    logger.info(f"Generando plantilla: {tipo_documento} - {complejidad} - {servicio}")

    if tipo_documento == "cotizacion":
        if complejidad == "complejo":
            return plantilla_cotizacion_compleja(servicio, cliente, area_m2, kwargs)
        else:
            return plantilla_cotizacion_simple(servicio, cliente, area_m2, kwargs)

    elif tipo_documento == "proyecto":
        if complejidad == "complejo":
            return plantilla_proyecto_complejo(servicio, cliente, area_m2, kwargs)
        else:
            return plantilla_proyecto_simple(servicio, cliente, area_m2, kwargs)

    elif tipo_documento == "informe":
        if complejidad == "complejo":
            presupuesto = kwargs.get("presupuesto", area_m2 * 50 * 1.18)
            return plantilla_informe_ejecutivo(servicio, cliente, presupuesto, kwargs)
        else:
            return plantilla_informe_tecnico(servicio, cliente, kwargs)

    else:
        # Default: cotizacion simple
        return plantilla_cotizacion_simple(servicio, cliente, area_m2, kwargs)


# ============================================================================
# INSTANCIA PARA USO DIRECTO
# ============================================================================

logger.info("Plantillas modelo cargadas - Sistema de fallback local disponible")
