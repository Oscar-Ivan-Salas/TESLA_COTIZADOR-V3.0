# ESPECIFICACIONES TÉCNICAS - 10 SERVICIOS TESLA ELECTRICIDAD

> **Documento técnico para definición de datos de cotización**
> **Fecha**: 2025-12-30
> **Versión**: 1.0
> **Basado en**: CNE 2011, D.S. 002-2018-PCM, NFPA, normativas peruanas

---

## 📋 ÍNDICE

1. [ITSE - Certificados de Inspección](#1-itse---certificados-de-inspección)
2. [Instalaciones Eléctricas](#2-instalaciones-eléctricas)
3. [Pozo a Tierra](#3-pozo-a-tierra)
4. [Sistemas Contraincendios](#4-sistemas-contraincendios)
5. [Domótica](#5-domótica)
6. [CCTV](#6-cctv)
7. [Redes de Datos](#7-redes-de-datos)
8. [Automatización Industrial](#8-automatización-industrial)
9. [Expedientes Técnicos](#9-expedientes-técnicos)
10. [Saneamiento](#10-saneamiento)

---

## 🎯 OBJETIVO DEL DOCUMENTO

Este documento define **QUÉ DATOS TÉCNICOS** debe recopilar el chat PILI para cada uno de los 10 servicios que ofrece Tesla Electricidad, con el fin de generar cotizaciones precisas.

**IMPORTANTE**: El frontend YA recopila:
- Datos del cliente (nombre, RUC, dirección, teléfono, email)
- Tipo de servicio seleccionado
- Industria
- Descripción general del proyecto

**El chat SOLO debe recopilar**: Datos técnicos específicos necesarios para calcular items de cotización.

---

## ESTRUCTURA POR SERVICIO

Cada servicio contiene:

1. **Descripción del Servicio**
2. **Normativa Aplicable**
3. **Datos Técnicos a Recopilar** (4-7 campos)
4. **Fórmulas de Cálculo**
5. **Generación de Items de Cotización**
6. **Ejemplo de Conversación**
7. **Tabla de Precios de Referencia**

---

# SERVICIOS

## 1. ITSE - Certificados de Inspección

### 📝 Descripción del Servicio

Certificado de Inspección Técnica de Seguridad en Edificaciones (ITSE) obligatorio para todo establecimiento comercial, industrial o de servicios en Perú según D.S. 002-2018-PCM.

### 📚 Normativa Aplicable

- **D.S. 002-2018-PCM**: Reglamento de Inspecciones Técnicas de Seguridad en Edificaciones
- **Manual CENEPRED**: Manual de Ejecución de ITSE
- **Ordenanzas Municipales**: Variables por municipio (Lima, Huancayo, etc.)

### 🔍 Datos Técnicos a Recopilar

#### 1. Categoría del Establecimiento
**Pregunta**: "¿Qué tipo de establecimiento es?"

**Opciones**:
- Salud (hospitales, clínicas, centros médicos)
- Educación (colegios, universidades, institutos)
- Hospedaje (hoteles, hostales)
- Comercio (tiendas, centros comerciales, mercados)
- Oficinas (administrativas, corporativas)
- Industria (fábricas, plantas, talleres)
- Entretenimiento (cines, teatros, discotecas)
- Almacén (depósitos, almacenes)

#### 2. Tipo Específico
**Pregunta**: "Especifica el tipo exacto" (depende de categoría)

**Ejemplos**:
- Salud: Hospital, Clínica, Posta médica, Consultorio
- Comercio: Tienda, Centro comercial, Mercado, Farmacia
- Industria: Fábrica, Planta de producción, Taller mecánico

#### 3. Área Total (m²)
**Pregunta**: "¿Cuál es el área total del establecimiento en metros cuadrados?"

**Validación**: Número > 0
**Formato**: 150.5 m²

#### 4. Número de Pisos
**Pregunta**: "¿Cuántos pisos tiene el establecimiento?"

**Validación**: Número entero >= 1
**Formato**: 3 pisos

#### 5. Municipio/Ubicación
**Pregunta**: "¿En qué municipio se encuentra?"

**Opciones comunes**:
- Lima (diversos distritos)
- Huancayo
- Arequipa
- Cusco
- Trujillo
- (Otros)

#### 6. Nivel de Riesgo (CALCULADO AUTOMÁTICAMENTE)
**Fórmula**: Basado en D.S. 002-2018-PCM

```python
def calcular_nivel_riesgo(categoria, area, pisos):
    """
    Calcula nivel de riesgo según D.S. 002-2018-PCM

    Criterios:
    - MUY ALTO: Salud (hospitales), Educación (>500 alumnos), >5 pisos, >3000m²
    - ALTO: Industria, Comercio grande, Hospedaje, 3-5 pisos, 500-3000m²
    - MEDIO: Comercio mediano, Oficinas, 2 pisos, 100-500m²
    - BAJO: Comercio pequeño, 1 piso, <100m²
    """

    # Categorías de MUY ALTO RIESGO
    if categoria in ["Salud - Hospital", "Salud - Clínica"]:
        return "MUY ALTO"

    if pisos > 5 or area > 3000:
        return "MUY ALTO"

    # Categorías de ALTO RIESGO
    if categoria.startswith("Industria") or categoria == "Entretenimiento":
        return "ALTO"

    if pisos >= 3 or area > 500:
        return "ALTO"

    # MEDIO RIESGO
    if area > 100 or pisos == 2:
        return "MEDIO"

    # BAJO RIESGO
    return "BAJO"
```

### 💰 Generación de Items de Cotización

```python
def generar_items_itse(datos):
    """
    Genera items de cotización para ITSE

    Args:
        datos = {
            "categoria": "Comercio - Tienda",
            "tipo_especifico": "Farmacia",
            "area": 120,
            "pisos": 1,
            "municipio": "Huancayo",
            "nivel_riesgo": "MEDIO"  # calculado
        }

    Returns:
        items = [
            {
                "descripcion": "Certificado ITSE Nivel MEDIO - Municipalidad de Huancayo",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 450.00,
                "subtotal": 450.00
            },
            {
                "descripcion": "Plano de arquitectura con cálculo de aforo (120 m²)",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 300.00,
                "subtotal": 300.00
            },
            ...
        ]
    """

    items = []
    riesgo = datos["nivel_riesgo"]
    area = datos["area"]
    municipio = datos["municipio"]

    # PRECIOS BASE SEGÚN MUNICIPIO Y RIESGO
    precios_municipales = {
        "Huancayo": {
            "BAJO": 250,
            "MEDIO": 450,
            "ALTO": 850,
            "MUY ALTO": 1500
        },
        "Lima": {
            "BAJO": 350,
            "MEDIO": 650,
            "ALTO": 1200,
            "MUY ALTO": 2500
        }
    }

    # ITEM 1: Certificado ITSE
    precio_certificado = precios_municipales.get(municipio, precios_municipales["Huancayo"])[riesgo]

    items.append({
        "descripcion": f"Certificado ITSE Nivel {riesgo} - Municipalidad de {municipio}",
        "cantidad": 1,
        "unidad": "und",
        "precio_unitario": precio_certificado,
        "subtotal": precio_certificado
    })

    # ITEM 2: Plano de Arquitectura
    items.append({
        "descripcion": f"Plano de arquitectura con cálculo de aforo ({area} m²)",
        "cantidad": 1,
        "unidad": "und",
        "precio_unitario": 300.00,
        "subtotal": 300.00
    })

    # ITEM 3: Plano de Evacuación
    items.append({
        "descripcion": f"Plano de señalización y rutas de evacuación ({area} m²)",
        "cantidad": 1,
        "unidad": "und",
        "precio_unitario": 250.00,
        "subtotal": 250.00
    })

    # ITEM 4: Plano Eléctrico (si aplica)
    if riesgo in ["ALTO", "MUY ALTO"]:
        items.append({
            "descripcion": "Plano de instalaciones eléctricas con tableros y cargas",
            "cantidad": 1,
            "unidad": "und",
            "precio_unitario": 400.00,
            "subtotal": 400.00
        })

    # ITEM 5: Certificado de Pozo a Tierra
    items.append({
        "descripcion": "Certificado de medición de pozo a tierra vigente",
        "cantidad": 1,
        "unidad": "und",
        "precio_unitario": 200.00,
        "subtotal": 200.00
    })

    # ITEM 6: Plan de Seguridad
    if riesgo in ["ALTO", "MUY ALTO"]:
        items.append({
            "descripcion": "Plan de Seguridad del establecimiento",
            "cantidad": 1,
            "unidad": "und",
            "precio_unitario": 350.00,
            "subtotal": 350.00
        })

    # ITEM 7: Protocolos de Equipos Contraincendios (si aplica)
    if riesgo in ["ALTO", "MUY ALTO"]:
        items.append({
            "descripcion": "Protocolos de operatividad de equipos contraincendios",
            "cantidad": 1,
            "unidad": "und",
            "precio_unitario": 300.00,
            "subtotal": 300.00
        })

    return items
```

### 💬 Ejemplo de Conversación

```
PILI: ¡Hola! Veo que necesitas un Certificado ITSE. Te voy a hacer algunas preguntas técnicas para preparar tu cotización.

Los datos del cliente ya los tenemos, solo necesito información técnica del establecimiento.

¿Qué tipo de establecimiento es?

[Botones: Salud | Educación | Hospedaje | Comercio | Oficinas | Industria | Entretenimiento | Almacén]

USUARIO: Comercio

PILI: Perfecto, es un establecimiento comercial. ¿Qué tipo específico?

[Botones: Tienda | Centro Comercial | Mercado | Farmacia | Restaurante | Otro]

USUARIO: Farmacia

PILI: Entendido, es una farmacia. ¿Cuál es el área total en metros cuadrados (m²)?

USUARIO: 120

PILI: 120 m². ¿Cuántos pisos tiene el establecimiento?

[Botones: 1 piso | 2 pisos | 3 pisos | 4+ pisos]

USUARIO: 1 piso

PILI: ¿En qué municipio se encuentra?

[Botones: Lima | Huancayo | Arequipa | Cusco | Otro]

USUARIO: Huancayo

PILI: Perfecto, déjame calcular el nivel de riesgo según D.S. 002-2018-PCM...

✅ **Análisis completado**:
- Establecimiento: Comercio - Farmacia
- Área: 120 m²
- Pisos: 1
- Ubicación: Huancayo
- **Nivel de Riesgo: MEDIO**

Según la normativa, tu establecimiento requiere ITSE POSTERIOR (puedes solicitar la licencia primero, inspección después).

He generado una cotización con 5 items necesarios:

1. Certificado ITSE Nivel MEDIO - S/ 450.00
2. Plano de arquitectura con aforo - S/ 300.00
3. Plano de evacuación - S/ 250.00
4. Certificado de pozo a tierra - S/ 200.00
5. Asesoría y trámite - S/ 150.00

**TOTAL: S/ 1,350.00** (incluye IGV)

¿Deseas generar el documento Word con la cotización completa?

[Botones: Generar Cotización Word | Modificar Datos | Agregar Servicios Adicionales]
```

### 📊 Tabla de Precios de Referencia

#### Certificados ITSE según Riesgo y Municipio

| Municipio | BAJO | MEDIO | ALTO | MUY ALTO |
|-----------|------|-------|------|----------|
| **Huancayo** | S/ 250 | S/ 450 | S/ 850 | S/ 1,500 |
| **Lima** | S/ 350 | S/ 650 | S/ 1,200 | S/ 2,500 |
| **Arequipa** | S/ 280 | S/ 500 | S/ 900 | S/ 1,800 |
| **Cusco** | S/ 300 | S/ 550 | S/ 1,000 | S/ 2,000 |

#### Documentos Técnicos

| Documento | Precio |
|-----------|--------|
| Plano de arquitectura con aforo | S/ 300 |
| Plano de evacuación | S/ 250 |
| Plano eléctrico con tableros | S/ 400 |
| Certificado pozo a tierra | S/ 200 |
| Plan de seguridad | S/ 350 |
| Protocolos equipos contraincendios | S/ 300 |
| Memoria descriptiva | S/ 200 |

---

## 2. Instalaciones Eléctricas

### 📝 Descripción del Servicio

Diseño, cálculo y ejecución de instalaciones eléctricas en baja tensión para edificaciones residenciales, comerciales e industriales, cumpliendo el Código Nacional de Electricidad - Utilización (CNE).

### 📚 Normativa Aplicable

- **CNE-Utilización 2011**: Código Nacional de Electricidad
- **EM.010**: Norma Técnica de Instalaciones Eléctricas Interiores (RNE)
- **NTP 370.301**: Instalaciones Eléctricas en Edificios
- **CNE Suministro**: Para acometidas y conexión con red pública

### 🔍 Datos Técnicos a Recopilar

#### 1. Tipo de Instalación
**Pregunta**: "¿Qué tipo de instalación eléctrica necesitas?"

**Opciones**:
- **Residencial**: Casa, departamento, edificio multifamiliar
- **Comercial**: Oficina, tienda, local comercial, centro comercial
- **Industrial**: Fábrica, planta, taller industrial

#### 2. Área Total (m²)
**Pregunta**: "¿Cuál es el área total a instalar en m²?"

**Validación**: Número > 0
**Uso**: Para estimar carga instalada según CNE Regla 050-200

#### 3. Número de Niveles/Pisos
**Pregunta**: "¿Cuántos niveles o pisos tiene?"

**Validación**: Número entero >= 1

#### 4. Carga Estimada o Uso Principal
**Pregunta**: "¿Cuál es el uso principal de la instalación?"

**Opciones por tipo**:

**Residencial**:
- Vivienda básica (iluminación + tomacorrientes)
- Vivienda con equipos especiales (aire acondicionado, terma eléctrica, cocina eléctrica)
- Vivienda con sistema fotovoltaico

**Comercial**:
- Oficinas administrativas (computadoras, iluminación)
- Local comercial (iluminación, vitrinas, equipos de refrigeración)
- Restaurante/cafetería (cocina eléctrica, equipos de refrigeración)

**Industrial**:
- Maquinaria ligera (<10 HP)
- Maquinaria mediana (10-50 HP)
- Maquinaria pesada (>50 HP)

#### 5. Tensión de Servicio
**Pregunta**: "¿Qué tensión de servicio requieres?"

**Opciones**:
- **Monofásico 220V** (residencial pequeño, <5 kW)
- **Bifásico 220V** (residencial mediano, 5-10 kW)
- **Trifásico 220V/380V** (comercial, industrial, >10 kW)

#### 6. Equipos Especiales (Opcional)
**Pregunta**: "¿Hay equipos especiales que requieran circuitos dedicados?"

**Opciones múltiples**:
- Aire acondicionado (indicar cantidad y potencia)
- Terma eléctrica
- Cocina eléctrica
- Ascensor/montacargas
- Bomba de agua
- Equipos industriales (especificar)

### 💰 Fórmulas de Cálculo

#### Cálculo de Máxima Demanda (MD) según CNE 050-200

```python
def calcular_maxima_demanda(area, tipo_instalacion, uso_principal):
    """
    Calcula la Máxima Demanda (MD) según CNE-Utilización Regla 050-200

    Tabla CNE 050-200 - Carga Unitaria por Área:
    - Vivienda: 20-30 W/m²
    - Oficinas: 30-40 W/m²
    - Comercio: 40-60 W/m²
    - Industrial: 50-100 W/m² (variable)
    """

    # Carga unitaria según tipo (W/m²)
    cargas_unitarias = {
        "Residencial - Básica": 20,
        "Residencial - Equipos especiales": 30,
        "Comercial - Oficinas": 35,
        "Comercial - Local comercial": 50,
        "Comercial - Restaurante": 60,
        "Industrial - Ligera": 50,
        "Industrial - Mediana": 75,
        "Industrial - Pesada": 100
    }

    clave = f"{tipo_instalacion} - {uso_principal}"
    carga_unitaria = cargas_unitarias.get(clave, 40)

    # Carga instalada (CI)
    carga_instalada_W = area * carga_unitaria
    carga_instalada_kW = carga_instalada_W / 1000

    # Factor de demanda según CNE (varía por tipo y tamaño)
    # Vivienda: 100% primeros 3kW, 35% exceso
    # Comercio: 100% primeros 10kW, 50% exceso
    # Industrial: Variable según equipos

    if tipo_instalacion == "Residencial":
        if carga_instalada_kW <= 3:
            md_kW = carga_instalada_kW
        else:
            md_kW = 3 + (carga_instalada_kW - 3) * 0.35

    elif tipo_instalacion == "Comercial":
        if carga_instalada_kW <= 10:
            md_kW = carga_instalada_kW
        else:
            md_kW = 10 + (carga_instalada_kW - 10) * 0.50

    else:  # Industrial
        md_kW = carga_instalada_kW * 0.70  # Factor 70%

    return {
        "carga_instalada_kW": round(carga_instalada_kW, 2),
        "maxima_demanda_kW": round(md_kW, 2),
        "corriente_A": round(md_kW * 1000 / (380 * 1.732), 2)  # Trifásico
    }
```

#### Dimensionamiento de Conductores según CNE Tabla 3-1

```python
def dimensionar_conductores(corriente_A, instalacion="tubería"):
    """
    Selecciona calibre de conductor según CNE Tabla 3-1
    (Conductores de cobre THW, 75°C)
    """

    # Tabla CNE 3-1 simplificada
    calibres = [
        {"AWG": "14", "corriente_max": 20},
        {"AWG": "12", "corriente_max": 25},
        {"AWG": "10", "corriente_max": 35},
        {"AWG": "8", "corriente_max": 50},
        {"AWG": "6", "corriente_max": 65},
        {"AWG": "4", "corriente_max": 85},
        {"AWG": "2", "corriente_max": 115},
        {"AWG": "1/0", "corriente_max": 150},
        {"AWG": "2/0", "corriente_max": 175},
        {"AWG": "3/0", "corriente_max": 200},
        {"AWG": "4/0", "corriente_max": 230},
    ]

    # Factor de seguridad 1.25
    corriente_requerida = corriente_A * 1.25

    for calibre in calibres:
        if calibre["corriente_max"] >= corriente_requerida:
            return calibre["AWG"]

    return "MAYOR A 4/0 (CONSULTAR)"
```

### 💰 Generación de Items de Cotización

```python
def generar_items_instalacion_electrica(datos):
    """
    Genera items de cotización para instalación eléctrica

    Args:
        datos = {
            "tipo_instalacion": "Comercial",
            "uso_principal": "Local comercial",
            "area": 200,
            "pisos": 2,
            "tension": "Trifásico 380V",
            "equipos_especiales": ["Aire acondicionado 3HP", "Bomba agua"]
        }
    """

    items = []

    # Calcular máxima demanda
    calculo = calcular_maxima_demanda(
        datos["area"],
        datos["tipo_instalacion"],
        datos["uso_principal"]
    )

    md_kW = calculo["maxima_demanda_kW"]
    corriente_A = calculo["corriente_A"]

    # ITEM 1: Diseño y Cálculo (Ingeniería)
    items.append({
        "descripcion": f"Diseño y cálculo eléctrico - {datos['tipo_instalacion']} {datos['area']}m² - MD: {md_kW} kW",
        "cantidad": 1,
        "unidad": "glb",
        "precio_unitario": 800.00,
        "subtotal": 800.00
    })

    # ITEM 2: Tablero General
    if md_kW < 10:
        precio_tablero = 450
        desc_tablero = "Tablero general empotrado 12 polos + interruptores termomagnéticos"
    elif md_kW < 20:
        precio_tablero = 850
        desc_tablero = "Tablero general empotrado 24 polos + interruptores termomagnéticos"
    else:
        precio_tablero = 1500
        desc_tablero = "Tablero general tipo gabinete metálico + interruptores termomagnéticos"

    items.append({
        "descripcion": desc_tablero,
        "cantidad": 1,
        "unidad": "und",
        "precio_unitario": precio_tablero,
        "subtotal": precio_tablero
    })

    # ITEM 3: Acometida eléctrica
    calibre_acometida = dimensionar_conductores(corriente_A)

    items.append({
        "descripcion": f"Acometida eléctrica {datos['tension']} - Cable {calibre_acometida} AWG THW-90",
        "cantidad": 15,  # metros promedio
        "unidad": "m",
        "precio_unitario": 25.00,
        "subtotal": 375.00
    })

    # ITEM 4: Circuitos de iluminación
    num_circuitos_luz = int((datos["area"] / 50) + 1)  # 1 circuito cada 50m²

    items.append({
        "descripcion": "Circuito de iluminación - Cable 2.5mm² THW, tubería PVC-P 20mm, cajas",
        "cantidad": num_circuitos_luz,
        "unidad": "pto",
        "precio_unitario": 120.00,
        "subtotal": num_circuitos_luz * 120.00
    })

    # ITEM 5: Circuitos de tomacorrientes
    num_circuitos_toma = int((datos["area"] / 40) + 1)  # 1 circuito cada 40m²

    items.append({
        "descripcion": "Circuito de tomacorrientes dobles - Cable 4mm² THW, tubería PVC-P 25mm",
        "cantidad": num_circuitos_toma,
        "unidad": "pto",
        "precio_unitario": 150.00,
        "subtotal": num_circuitos_toma * 150.00
    })

    # ITEM 6: Sistema de puesta a tierra
    items.append({
        "descripcion": "Sistema de puesta a tierra completo - Pozo + conductor + conexiones",
        "cantidad": 1,
        "unidad": "glb",
        "precio_unitario": 600.00,
        "subtotal": 600.00
    })

    # ITEM 7: Equipos especiales (si aplica)
    if "equipos_especiales" in datos and datos["equipos_especiales"]:
        for equipo in datos["equipos_especiales"]:
            items.append({
                "descripcion": f"Circuito dedicado para {equipo} - Cable, protecciones, instalación",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 350.00,
                "subtotal": 350.00
            })

    # ITEM 8: Mano de obra e instalación
    precio_mo = datos["area"] * 15  # S/ 15 por m²

    items.append({
        "descripcion": f"Mano de obra e instalación completa - {datos['area']} m²",
        "cantidad": 1,
        "unidad": "glb",
        "precio_unitario": precio_mo,
        "subtotal": precio_mo
    })

    # ITEM 9: Planos eléctricos y memoria de cálculo
    items.append({
        "descripcion": "Planos eléctricos (alumbrado, tomacorrientes, diagrama unifilar) + memoria de cálculo",
        "cantidad": 1,
        "unidad": "glb",
        "precio_unitario": 500.00,
        "subtotal": 500.00
    })

    return items
```

### 💬 Ejemplo de Conversación

```
PILI: ¡Perfecto! Vamos a cotizar tu instalación eléctrica.

Necesito algunos datos técnicos (los datos del cliente ya los tenemos).

¿Qué tipo de instalación necesitas?

[Botones: Residencial | Comercial | Industrial]

USUARIO: Comercial

PILI: Entendido, instalación comercial. ¿Cuál es el área total en metros cuadrados?

USUARIO: 200

PILI: 200 m². ¿Cuántos pisos tiene la edificación?

[Botones: 1 piso | 2 pisos | 3 pisos | Más de 3]

USUARIO: 2 pisos

PILI: ¿Cuál es el uso principal del local?

[Botones: Oficinas | Local Comercial | Restaurante | Otro]

USUARIO: Local Comercial

PILI: ¿Qué tipo de tensión de servicio requieres?

[Botones: Monofásico 220V | Bifásico 220V | Trifásico 380V]

USUARIO: Trifásico 380V

PILI: ¿Hay equipos especiales que requieran circuitos dedicados? (Puedes seleccionar varios)

[Botones: Aire Acondicionado | Bomba de Agua | Ninguno | Otro]

USUARIO: Aire Acondicionado

PILI: ¿Cuántos aires acondicionados y de qué potencia?

USUARIO: 3 equipos de 3HP cada uno

PILI: Perfecto, déjame calcular la instalación según el CNE...

✅ **Cálculos completados**:
- Tipo: Comercial - Local comercial
- Área: 200 m² × 2 pisos
- Carga instalada: 10 kW
- Máxima demanda: 10 kW
- Corriente: 15.2 A
- Tensión: Trifásico 380V
- Conductor acometida: 10 AWG

He generado una cotización con 9 items:

1. Diseño y cálculo eléctrico - S/ 800.00
2. Tablero general 24 polos - S/ 850.00
3. Acometida eléctrica 10 AWG - S/ 375.00
4. Circuitos de iluminación (5 puntos) - S/ 600.00
5. Circuitos tomacorrientes (6 puntos) - S/ 900.00
6. Sistema puesta a tierra - S/ 600.00
7. Circuitos AA (3 equipos) - S/ 1,050.00
8. Mano de obra - S/ 3,000.00
9. Planos y memoria - S/ 500.00

**SUBTOTAL: S/ 8,675.00**
**IGV 18%: S/ 1,561.50**
**TOTAL: S/ 10,236.50**

¿Deseas generar el documento?

[Botones: Generar Cotización | Modificar | Ver Detalle Técnico]
```

### 📊 Tabla de Precios de Referencia

#### Cargas Unitarias (CNE 050-200)

| Tipo de Instalación | W/m² | Factor Demanda |
|---------------------|------|----------------|
| Vivienda básica | 20 W/m² | 100% primeros 3kW, 35% resto |
| Vivienda con equipos | 30 W/m² | 100% primeros 3kW, 35% resto |
| Oficinas | 35 W/m² | 100% primeros 10kW, 50% resto |
| Comercio | 50 W/m² | 100% primeros 10kW, 50% resto |
| Restaurante | 60 W/m² | 80% total |
| Industrial ligera | 50 W/m² | 70% total |
| Industrial pesada | 100 W/m² | 70% total |

#### Precios de Materiales y Servicios

| Item | Precio |
|------|--------|
| Diseño y cálculo eléctrico | S/ 800 |
| Tablero 12 polos | S/ 450 |
| Tablero 24 polos | S/ 850 |
| Tablero industrial | S/ 1,500 |
| Cable THW 14 AWG (metro) | S/ 3.50 |
| Cable THW 10 AWG (metro) | S/ 6.50 |
| Cable THW 6 AWG (metro) | S/ 12.00 |
| Circuito iluminación (punto) | S/ 120 |
| Circuito tomacorriente (punto) | S/ 150 |
| Sistema pozo a tierra | S/ 600 |
| Mano de obra (m²) | S/ 15 |
| Planos y memoria | S/ 500 |

---


## 3. Pozo a Tierra (Puesta a Tierra)

### 📝 Descripción del Servicio

Sistema de puesta a tierra para protección de personas y equipos eléctricos/electrónicos contra descargas eléctricas, sobretensiones y corrientes de fuga. Obligatorio según CNE-Utilización para toda instalación eléctrica.

### 📚 Normativa Aplicable

- **CNE-Utilización Regla 060-712**: Valor máximo 25 Ω para electrodo único
- **CNE-Utilización Sección 060**: Sistemas de puesta a tierra
- **IEEE Std 142**: Grounding of Industrial and Commercial Power Systems
- **NFPA 780**: Standard for the Installation of Lightning Protection Systems
- **INDECI**: Exige certificado vigente para ITSE

### 🔍 Datos Técnicos a Recopilar

#### 1. Tipo de Aplicación
**Pregunta**: "¿Para qué tipo de instalación es el pozo a tierra?"

**Opciones**:
- **Residencial**: Casa, departamento
- **Comercial**: Oficina, tienda, local comercial
- **Industrial**: Fábrica, planta, taller
- **Data Center / Telecomunicaciones**: Servidores, equipos de red
- **Subestación Eléctrica**: Transformadores, celdas MT
- **Torre de Comunicaciones**: Antenas, repetidoras
- **Sistemas Especiales**: Equipos médicos, laboratorios

#### 2. Tensión del Sistema
**Pregunta**: "¿Qué tensión maneja el sistema eléctrico?"

**Opciones**:
- Baja Tensión - Monofásico 220V
- Baja Tensión - Trifásico 380V
- Media Tensión - 10 kV
- Media Tensión - 22.9 kV
- Alta Tensión - Mayor a 33 kV

#### 3. Valor de Resistencia Requerido
**Pregunta**: "¿Qué valor de resistencia necesitas alcanzar?"

**Opciones y recomendaciones**:
- **≤ 25 Ω** - Mínimo legal CNE (aplicaciones convencionales)
- **≤ 10 Ω** - Recomendado para comercios e industrias
- **≤ 5 Ω** - Buena práctica NFPA/IEEE (equipos sensibles)
- **≤ 3 Ω** - Equipos electrónicos, telecomunicaciones
- **≤ 1 Ω** - Centros de control, subestaciones, data centers

#### 4. Tipo de Terreno
**Pregunta**: "¿Qué tipo de terreno es?"

**Opciones** (afecta resistividad):
- **Arcilloso/Húmedo**: ρ = 50-200 Ω·m (buena conductividad)
- **Tierra cultivable**: ρ = 100-500 Ω·m (conductividad media)
- **Arenoso/Seco**: ρ = 500-3000 Ω·m (baja conductividad)
- **Rocoso**: ρ = 3000-10000 Ω·m (muy baja conductividad)
- **No sé / Requiere medición**: Se incluirá estudio de resistividad

#### 5. Área Disponible para Instalación
**Pregunta**: "¿Cuánto espacio hay disponible para el pozo?"

**Opciones**:
- **Amplio** (>10 m²): Pozo vertical profundo o malla horizontal
- **Medio** (5-10 m²): Pozo vertical estándar
- **Reducido** (<5 m²): Pozo vertical compacto o químico
- **Muy limitado**: Sistema de electrodos especiales

#### 6. ¿Requiere Certificado?
**Pregunta**: "¿Necesitas certificado de medición?"

**Opciones**:
- **Sí - Para ITSE**: Certificado oficial con protocolo
- **Sí - Para proyecto**: Certificado + planos
- **No - Solo instalación**: Sin certificado

### 💰 Fórmulas de Cálculo

#### Resistencia de Electrodo Vertical (Varilla Copperweld)

```python
import math

def calcular_resistencia_electrodo_vertical(rho, L, d):
    """
    Fórmula de Dwight para electrodo vertical

    Args:
        rho: Resistividad del terreno (Ω·m)
        L: Longitud de la varilla (m)
        d: Diámetro de la varilla (m)

    Returns:
        Resistencia en Ω

    Fórmula: R = (ρ / 2πL) × ln(8L/d - 1)
    """
    R = (rho / (2 * math.pi * L)) * math.log((8 * L / d) - 1)
    return round(R, 2)
```

#### Número de Varillas Necesarias (Configuración en Paralelo)

```python
def calcular_numero_varillas(R_objetivo, R_una_varilla, eficiencia=0.65):
    """
    Calcula cuántas varillas en paralelo se necesitan

    Args:
        R_objetivo: Resistencia que se desea alcanzar (Ω)
        R_una_varilla: Resistencia de una sola varilla (Ω)
        eficiencia: Factor de eficiencia (0.6-0.7 típico)

    Returns:
        Número de varillas necesarias

    Fórmula: N = R_una / (R_objetivo × eficiencia)
    """
    N = R_una_varilla / (R_objetivo * eficiencia)
    return math.ceil(N)  # Redondear hacia arriba
```

### 📊 Tabla de Precios de Referencia

#### Valores de Resistencia Recomendados

| Aplicación | Valor Máximo | Normativa |
|------------|-------------|-----------|
| **Legal mínimo CNE** | 25 Ω | CNE 060-712 |
| **Residencial** | 10 Ω | Recomendado |
| **Comercial / Industrial** | 5 Ω | NFPA/IEEE |
| **Equipos electrónicos** | 3 Ω | IEEE 142 |
| **Data Center / Telecom** | 1 Ω | TIA-942 |
| **Subestaciones** | <1 Ω | IEEE 80 |

#### Resistividad del Terreno

| Tipo de Terreno | Resistividad (Ω·m) | Dificultad |
|----------------|-------------------|-----------|
| Arcilloso húmedo | 50-200 | Fácil |
| Tierra cultivable | 100-500 | Media |
| Arenoso seco | 500-3000 | Difícil |
| Rocoso | 3000-10000 | Muy difícil |

#### Precios de Materiales

| Material | Precio |
|----------|--------|
| Varilla Copperweld 2.4m × 5/8" | S/ 85.00 |
| Varilla Copperweld 3.0m × 5/8" | S/ 110.00 |
| Conector grapa | S/ 12.00 |
| Cable desnudo Cu 16mm² (metro) | S/ 12.00 |
| Cable desnudo Cu 25mm² (metro) | S/ 18.00 |
| Tratamiento químico (por varilla) | S/ 120.00 |
| Caja de registro | S/ 150.00 |
| Excavación (m³) | S/ 45.00 |
| Medición + Certificado ITSE | S/ 250.00 |
| Medición + Certificado Proyecto | S/ 400.00 |
| Estudio de resistividad | S/ 350.00 |

---

## 4. Sistemas Contraincendios

### 📝 Descripción del Servicio

Diseño, instalación y mantenimiento de sistemas de protección contra incendios incluyendo detección, alarma, extinción automática (rociadores), extintores portátiles y señalización, cumpliendo normativa NFPA y RNE.

### 📚 Normativa Aplicable

- **NFPA 72**: Código Nacional de Alarmas de Incendio y Señalización
- **NFPA 13**: Instalación de Sistemas de Rociadores
- **NFPA 10**: Extintores Portátiles
- **NFPA 101**: Código de Seguridad Humana
- **RNE A.130**: Requisitos de Seguridad (Perú)
- **D.S. 002-2018-PCM**: ITSE (exige sistemas contraincendios según riesgo)

### 🔍 Datos Técnicos a Recopilar

#### 1. Tipo de Edificación
**Pregunta**: "¿Qué tipo de edificación es?"

**Opciones**:
- **Comercial**: Tienda, centro comercial, oficina
- **Industrial**: Fábrica, almacén, planta
- **Residencial**: Edificio multifamiliar, condominio
- **Educación**: Colegio, universidad
- **Salud**: Hospital, clínica
- **Hospedaje**: Hotel, hostal
- **Entretenimiento**: Cine, teatro, discoteca

#### 2. Área Total (m²)
**Pregunta**: "¿Cuál es el área total de la edificación?"

**Validación**: Número > 0
**Uso**: Determinar cantidad de detectores y rociadores

#### 3. Número de Pisos
**Pregunta**: "¿Cuántos pisos tiene?"

**Opciones**:
- 1-2 pisos
- 3-5 pisos
- 6-10 pisos
- Más de 10 pisos

**Nota**: >15 metros o >20 niveles requiere rociadores automáticos según RNE

#### 4. Nivel de Riesgo
**Pregunta**: "¿Qué nivel de riesgo tiene según actividad?"

**Opciones** (según NFPA):
- **Riesgo Leve**: Oficinas, escuelas, hoteles
- **Riesgo Ordinario Grupo 1**: Comercio, estacionamientos
- **Riesgo Ordinario Grupo 2**: Almacenes, talleres ligeros
- **Riesgo Extra Alto**: Industrias químicas, inflamables

#### 5. Componentes Requeridos
**Pregunta**: "¿Qué componentes necesitas?" (Múltiple selección)

**Opciones**:
- **Detección y Alarma**: Detectores de humo, estaciones manuales, panel central
- **Rociadores Automáticos**: Sistema de sprinklers
- **Extintores Portátiles**: PQS, CO2, agua presurizada
- **Señalización**: Señales fotoluminiscentes, luces de emergencia
- **Gabinetes Contraincendios**: Mangueras, válvulas
- **Sistema de Evacuación**: Luces, sirenas

#### 6. Fuente de Agua
**Pregunta**: "¿Hay fuente de agua disponible para rociadores?"

**Opciones**:
- Sí - Red pública con presión adecuada
- Sí - Cisterna + bomba contraincendios
- No - Solo extintores y detección

### 💰 Fórmulas de Cálculo

#### Cantidad de Detectores de Humo (NFPA 72)

```python
def calcular_detectores_humo(area_m2, altura_techo):
    """
    Calcula cantidad de detectores según NFPA 72

    Regla: 1 detector cada 60-90 m² (depende de altura)

    Args:
        area_m2: Área total en m²
        altura_techo: Altura del techo en metros

    Returns:
        Número de detectores
    """

    # Área de cobertura por detector
    if altura_techo <= 3:
        area_cobertura = 90  # m² por detector
    elif altura_techo <= 6:
        area_cobertura = 75
    else:
        area_cobertura = 60  # Techos altos

    num_detectores = math.ceil(area_m2 / area_cobertura)

    return num_detectores
```

#### Cantidad de Rociadores (NFPA 13)

```python
def calcular_rociadores(area_m2, nivel_riesgo):
    """
    Calcula cantidad de rociadores según NFPA 13

    Regla:
    - Riesgo Leve: 1 rociador cada 18-20 m²
    - Riesgo Ordinario: 1 rociador cada 9-12 m²
    - Riesgo Extra: 1 rociador cada 6-9 m²
    """

    areas_cobertura = {
        "Leve": 18,
        "Ordinario Grupo 1": 12,
        "Ordinario Grupo 2": 9,
        "Extra Alto": 6
    }

    area_por_rociador = areas_cobertura.get(nivel_riesgo, 12)
    num_rociadores = math.ceil(area_m2 / area_por_rociador)

    return num_rociadores
```

#### Cantidad de Extintores (NFPA 10)

```python
def calcular_extintores(area_m2, nivel_riesgo, tipo_edificacion):
    """
    Calcula cantidad de extintores según NFPA 10

    Regla:
    - Riesgo Leve: 1 extintor cada 280 m² (distancia máx 23m)
    - Riesgo Ordinario: 1 extintor cada 140 m² (distancia máx 15m)
    - Riesgo Extra: 1 extintor cada 90 m² (distancia máx 9m)
    """

    areas_cobertura = {
        "Leve": 280,
        "Ordinario Grupo 1": 140,
        "Ordinario Grupo 2": 140,
        "Extra Alto": 90
    }

    area_por_extintor = areas_cobertura.get(nivel_riesgo, 140)
    num_extintores = math.ceil(area_m2 / area_por_extintor)

    # Mínimo 2 extintores por piso
    num_extintores = max(num_extintores, 2)

    return num_extintores
```

### 📊 Tabla de Precios de Referencia

#### Detección y Alarma

| Equipo | Precio |
|--------|--------|
| Detector de humo fotoeléctrico | S/ 80.00 |
| Detector de humo iónico | S/ 95.00 |
| Detector de temperatura | S/ 75.00 |
| Estación manual de alarma | S/ 65.00 |
| Panel central 4-8 zonas | S/ 850.00 |
| Panel central 16-32 zonas | S/ 1,800.00 |
| Sirena estroboscópica | S/ 120.00 |
| Batería respaldo 12V 7Ah | S/ 85.00 |

#### Rociadores Automáticos

| Componente | Precio |
|------------|--------|
| Rociador sprinkler estándar | S/ 45.00 |
| Tubería acero SCH 40 1" (metro) | S/ 28.00 |
| Tubería acero SCH 40 2" (metro) | S/ 55.00 |
| Válvula de control 2" | S/ 450.00 |
| Bomba contraincendios 10HP | S/ 5,500.00 |
| Bomba contraincendios 20HP | S/ 9,800.00 |
| Cisterna 10m³ | S/ 3,500.00 |

#### Extintores

| Tipo | Capacidad | Precio |
|------|-----------|--------|
| PQS (Polvo Químico Seco) | 6 kg | S/ 85.00 |
| PQS | 9 kg | S/ 120.00 |
| PQS | 12 kg | S/ 155.00 |
| CO2 | 6 kg | S/ 280.00 |
| Agua Presurizada | 10 L | S/ 140.00 |
| Rodante PQS | 50 kg | S/ 850.00 |

#### Señalización

| Item | Precio |
|------|--------|
| Señal fotoluminiscente 20×30cm | S/ 12.00 |
| Luz de emergencia LED 2×8W | S/ 95.00 |
| Gabinete contraincendios completo | S/ 650.00 |
| Manguera 1.5" × 30m | S/ 280.00 |

---

## 5. Domótica

### 📝 Descripción del Servicio

Automatización inteligente de edificios y hogares usando protocolo KNX estándar internacional (ISO/IEC 14543), permitiendo control integrado de iluminación, climatización, seguridad, persianas y multimedia.

### 📚 Normativa Aplicable

- **ISO/IEC 14543-3**: Estándar KNX
- **UNE-EN 50.090**: Sistemas electrónicos para viviendas y edificios (HBES)
- **UNE-EN 13.321**: Sistemas de automatización y control de edificios (BACS)

### 🔍 Datos Técnicos a Recopilar

1. **Área a automatizar (m²)**: Para calcular cantidad de dispositivos
2. **Número de habitaciones/zonas**: División lógica del sistema
3. **Funciones requeridas** (múltiple):
   - Iluminación inteligente (on/off, dimmer, escenas)
   - Control de persianas/cortinas
   - Climatización (termostatos, válvulas)
   - Seguridad (sensores movimiento, contactos)
   - Multimedia (audio/video distribuido)
   - Control de acceso
4. **Tipo de interfaz**:
   - Pulsadores KNX en pared
   - Pantallas táctiles
   - Control desde smartphone/tablet
   - Control por voz (Alexa/Google)
5. **Presupuesto aproximado**: Básico / Medio / Premium

### 💰 Tabla de Precios Referencia

| Componente KNX | Precio |
|----------------|--------|
| Fuente alimentación 640mA | S/ 380.00 |
| Acoplador de línea | S/ 150.00 |
| Actuador 4 canales on/off | S/ 420.00 |
| Actuador dimmer 4 canales | S/ 680.00 |
| Actuador persianas 4 canales | S/ 580.00 |
| Pulsador 2 teclas | S/ 280.00 |
| Pulsador 4 teclas | S/ 350.00 |
| Sensor movimiento KNX | S/ 320.00 |
| Termostato KNX | S/ 450.00 |
| Pantalla táctil 7" | S/ 1,850.00 |
| Cable bus KNX (metro) | S/ 4.50 |
| Programación e ingeniería | S/ 800-2000 |

---

## 6. CCTV (Videovigilancia)

### 📝 Descripción del Servicio

Sistemas de circuito cerrado de televisión para seguridad y vigilancia, cumpliendo Decreto Legislativo 1218 y Ley 29733 de Protección de Datos Personales en Perú.

### 📚 Normativa Aplicable

- **D.L. 1218**: Regula uso de cámaras de videovigilancia
- **D.S. 007-2020-IN**: Reglamento del D.L. 1218
- **Ley 29733**: Protección de Datos Personales

### 🔍 Datos Técnicos a Recopilar

1. **Área a cubrir (m²)** y **Perímetro (m)**
2. **Número de puntos de cámara estimados**
3. **Tipo de cámara** (múltiple):
   - Domo fijo interior
   - Bullet exterior
   - PTZ (Pan-Tilt-Zoom)
   - 360° (Ojo de pez)
4. **Resolución requerida**:
   - HD 720p (1MP)
   - Full HD 1080p (2MP) - **Recomendado**
   - 2K (4MP)
   - 4K (8MP) - Zonas críticas
5. **Tipo de grabación**:
   - Continua 24/7
   - Por detección de movimiento
   - Programada (horarios)
6. **Días de almacenamiento**: 15 / 30 / 60 / 90 días
7. **Visión nocturna**: Sí (infrarrojo) / No

### 💰 Tabla de Precios Referencia

| Equipo | Precio |
|--------|--------|
| Cámara domo 2MP interior | S/ 180.00 |
| Cámara bullet 2MP exterior IP66 | S/ 220.00 |
| Cámara PTZ 2MP 20× zoom | S/ 1,450.00 |
| Cámara 4K 8MP | S/ 480.00 |
| DVR/NVR 4 canales | S/ 350.00 |
| DVR/NVR 8 canales | S/ 580.00 |
| DVR/NVR 16 canales | S/ 980.00 |
| Disco duro 1TB vigilancia | S/ 220.00 |
| Disco duro 4TB vigilancia | S/ 550.00 |
| Monitor LED 19" | S/ 320.00 |
| Fuente 12V 5A | S/ 45.00 |
| Cable coaxial RG59 (metro) | S/ 2.80 |
| Cable UTP Cat6 exterior (metro) | S/ 3.50 |

---

## 7. Redes de Datos (Cableado Estructurado)

### 📝 Descripción del Servicio

Infraestructura de cableado estructurado para redes LAN empresariales, cumpliendo estándares TIA/EIA 568 y soportando Gigabit Ethernet y tecnologías futuras.

### 📚 Normativa Aplicable

- **ANSI/TIA-568.E**: Cableado de telecomunicaciones para edificios comerciales
- **TIA-569**: Espacios y rutas de telecomunicaciones
- **TIA-606**: Administración de infraestructura de telecomunicaciones
- **ISO/IEC 11801**: Cableado genérico para edificios

### 🔍 Datos Técnicos a Recopilar

1. **Número de puntos de red**: Cantidad de tomas RJ45
2. **Categoría de cable**:
   - **Cat5e** (100 MHz, 1 Gbps) - Económico
   - **Cat6** (250 MHz, 1 Gbps) - **Recomendado**
   - **Cat6A** (500 MHz, 10 Gbps) - Alta performance
3. **Distribución**:
   - Distancia promedio punto a rack
   - Número de pisos
4. **Rack de comunicaciones**:
   - Mural 6U-12U (hasta 20 puntos)
   - Piso 42U (20-100 puntos)
5. **Equipamiento activo**:
   - Switch no administrable
   - Switch administrable
   - Firewall
   - Access Points WiFi
6. **Certificación**: ¿Requiere certificación Fluke?

### 💰 Tabla de Precios Referencia

| Item | Precio |
|------|--------|
| Punto de red Cat6 completo | S/ 120.00 |
| Cable UTP Cat6 caja 305m | S/ 420.00 |
| Jack RJ45 Cat6 | S/ 4.50 |
| Patch panel 24 puertos Cat6 | S/ 180.00 |
| Patch cord Cat6 1m | S/ 8.00 |
| Patch cord Cat6 3m | S/ 12.00 |
| Rack mural 9U | S/ 380.00 |
| Rack piso 42U | S/ 2,200.00 |
| Switch 8 puertos Gigabit | S/ 180.00 |
| Switch 24 puertos Gigabit | S/ 650.00 |
| Access Point WiFi 6 | S/ 350.00 |
| Certificación Fluke (por punto) | S/ 15.00 |

---

## 8. Automatización Industrial

### 📝 Descripción del Servicio

Sistemas de control y automatización de procesos industriales usando PLCs, SCADA, sensores, actuadores y redes industriales para manufactura, procesamiento y control de maquinaria.

### 📚 Normativa Aplicable

- **IEC 61131-3**: Lenguajes de programación PLC
- **IEC 61508**: Seguridad funcional sistemas eléctricos
- **ISO 12100**: Seguridad de maquinaria

### 🔍 Datos Técnicos a Recopilar

1. **Tipo de proceso a automatizar**:
   - Línea de producción/ensamblaje
   - Control de maquinaria
   - Dosificación/mezcla
   - Transporte/logística
   - Empaque/etiquetado
2. **Cantidad de señales**:
   - Entradas digitales (sensores on/off)
   - Salidas digitales (actuadores, contactores)
   - Entradas analógicas (temperatura, presión, caudal)
   - Salidas analógicas (variadores, válvulas proporcionales)
3. **Marca PLC preferida**:
   - Siemens (S7-1200, S7-1500)
   - Allen Bradley
   - Schneider Electric
   - Omron
   - Nacional (bajo costo)
4. **Interfaz HMI**: ¿Requiere pantalla táctil?
5. **Sistema SCADA**: ¿Necesita supervisión remota?
6. **Variadores de velocidad**: Cantidad y potencia

### 💰 Tabla de Precios Referencia

| Equipo | Precio |
|--------|--------|
| PLC Siemens S7-1200 CPU 1214C | S/ 2,800.00 |
| PLC económico 20 I/O | S/ 850.00 |
| HMI táctil 7" | S/ 1,200.00 |
| HMI táctil 10" | S/ 1,850.00 |
| Sensor inductivo M18 | S/ 65.00 |
| Sensor fotoeléctrico | S/ 120.00 |
| Sensor de temperatura PT100 | S/ 180.00 |
| Contactor 16A | S/ 45.00 |
| Variador 1HP 220V | S/ 480.00 |
| Variador 5HP 380V | S/ 1,350.00 |
| Licencia SCADA 50 tags | S/ 2,500.00 |
| Programación PLC (día) | S/ 400.00 |

---

## 9. Expedientes Técnicos

### 📝 Descripción del Servicio

Elaboración de expedientes técnicos completos para proyectos de construcción e infraestructura, cumpliendo normativa de contrataciones públicas y privadas en Perú.

### 📚 Normativa Aplicable

- **Ley 30225**: Ley de Contrataciones del Estado
- **D.S. 344-2018-EF**: Reglamento de Ley de Contrataciones
- **Guía MEF**: Pautas para elaboración de expedientes técnicos
- **RNE**: Reglamento Nacional de Edificaciones

### 🔍 Datos Técnicos a Recopilar

1. **Tipo de proyecto**:
   - Edificación (vivienda, comercio, industria)
   - Infraestructura eléctrica
   - Infraestructura sanitaria
   - Vial/transporte
   - Telecomunicaciones
2. **Especialidades requeridas** (múltiple):
   - Arquitectura
   - Estructuras
   - Instalaciones eléctricas
   - Instalaciones sanitarias
   - Instalaciones mecánicas
3. **Valor referencial estimado**: Rango presupuestal
4. **Plazo de ejecución estimado**: Meses
5. **¿Es para obra pública?**: Sí / No
6. **Estudios básicos disponibles**:
   - Topografía
   - Mecánica de suelos
   - Impacto ambiental

### 💰 Componentes del Expediente

1. **Memoria Descriptiva**: Justificación técnica del proyecto
2. **Memoria de Cálculo**: Cálculos estructurales, eléctricos, sanitarios
3. **Planos**: Arquitectura, estructuras, instalaciones
4. **Especificaciones Técnicas**: Materiales y procesos constructivos
5. **Metrados**: Cuantificación de partidas
6. **Presupuesto**: Análisis de precios unitarios
7. **Valor Referencial**: Costo total del proyecto
8. **Fórmula Polinómica**: Reajuste de precios
9. **Cronograma**: Calendario de avance (Gantt)
10. **Estudios Complementarios**: Suelos, topografía, etc.

### 💰 Tabla de Precios Referencia

| Especialidad | % del Valor Obra | Mínimo |
|--------------|-----------------|--------|
| Arquitectura | 3-5% | S/ 3,000 |
| Estructuras | 2-4% | S/ 2,500 |
| Inst. Eléctricas | 2-3% | S/ 2,000 |
| Inst. Sanitarias | 2-3% | S/ 2,000 |
| Estudio de suelos | - | S/ 1,500 |
| Topografía | - | S/ 1,200 |

---

## 10. Saneamiento (Instalaciones Sanitarias)

### 📝 Descripción del Servicio

Diseño y ejecución de sistemas de agua potable fría/caliente, desagüe, drenaje pluvial y sistemas de bombeo para edificaciones, según Reglamento Nacional de Edificaciones.

### 📚 Normativa Aplicable

- **IS.010 RNE**: Instalaciones Sanitarias para Edificaciones
- **IS.020 RNE**: Tanques sépticos
- **OS.030**: Almacenamiento de agua potable
- **OS.050**: Redes de distribución de agua

### 🔍 Datos Técnicos a Recopilar

1. **Tipo de edificación**:
   - Vivienda unifamiliar
   - Multifamiliar
   - Comercial
   - Industrial
2. **Número de baños completos**
3. **Número de aparatos sanitarios**:
   - Inodoros
   - Lavatorios
   - Duchas
   - Lavaderos
   - Otros (urinarios, tinas, etc.)
4. **Número de pisos**: Para cálculo de presión
5. **Sistema de agua caliente**: Sí / No
   - Terma eléctrica
   - Terma a gas
   - Sistema solar
6. **Sistema de bombeo**: ¿Requiere cisterna + tanque elevado?
7. **Área total (m²)**: Para desagüe y drenaje pluvial

### 💰 Fórmulas de Cálculo

#### Dotación de Agua (IS.010)

```
Vivienda: 150 L/persona/día
Comercio: Variable según uso
Oficinas: 6 L/persona/día
```

#### Volumen de Cisterna

```
V_cisterna = Dotación_diaria × 1.5 (50% reserva)
```

#### Volumen de Tanque Elevado

```
V_tanque = Dotación_diaria × 0.33 (1/3 de dotación)
```

### 💰 Tabla de Precios Referencia

| Item | Precio |
|------|--------|
| Inodoro Trebol blanco | S/ 250.00 |
| Lavatorio Trebol blanco | S/ 180.00 |
| Ducha completa | S/ 120.00 |
| Tubería PVC SAP 2" (metro) | S/ 8.50 |
| Tubería PVC SAP 4" (metro) | S/ 18.00 |
| Tubería PVC SAL 2" (metro) | S/ 9.20 |
| Tubería PVC SAL 4" (metro) | S/ 21.00 |
| Bomba 1HP | S/ 650.00 |
| Electrobomba 2HP | S/ 980.00 |
| Tanque elevado 1100 L | S/ 580.00 |
| Terma eléctrica 50 L | S/ 380.00 |
| Terma eléctrica 80 L | S/ 520.00 |

---

## 🎯 RESUMEN EJECUTIVO

### Servicios Completados

✅ **10 de 10 servicios definidos**:

1. ✅ ITSE - Certificados de Inspección
2. ✅ Instalaciones Eléctricas
3. ✅ Pozo a Tierra
4. ✅ Sistemas Contraincendios
5. ✅ Domótica
6. ✅ CCTV
7. ✅ Redes de Datos
8. ✅ Automatización Industrial
9. ✅ Expedientes Técnicos
10. ✅ Saneamiento

### Prioridad de Implementación (FASE 1)

**Cotizaciones Simples - Implementar primero**:
1. **ITSE** (patrón ya validado en pili_itse_chatbot.py)
2. **Pozo a Tierra** (cálculo directo, ~5-6 items)
3. **CCTV** (fórmula simple por área)
4. **Redes de Datos** (cálculo por puntos)

**Proyectos Simples - Implementar segundo**:
5. **Instalaciones Eléctricas básicas** (residencial/comercial pequeño)
6. **Saneamiento** (viviendas simples)

### Siguiente Paso

**Implementar chatbots usando patrón caja negra**:
- Crear `pili_pozo_tierra_chatbot.py` (siguiente más simple)
- Crear `pili_cctv_chatbot.py`
- Crear `pili_redes_chatbot.py`
- Expandir `pili_itse_chatbot.py` con documentos adicionales

---

**FIN DEL DOCUMENTO**

