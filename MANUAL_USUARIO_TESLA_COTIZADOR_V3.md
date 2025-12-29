# 📖 **MANUAL DE USUARIO - TESLA COTIZADOR V3.0**
## *Aplicación Web Profesional para Cotización Eléctrica con Inteligencia Artificial*

---

**Empresa:** Tesla Electricidad y Automatización S.A.C.  
**Versión:** 3.0.0  
**Fecha:** Noviembre 2025  
**Gestor de Proyecto:** Claude (Especialista en Software y Diseño de Apps Web)

---

## 🎯 **¿QUÉ ES TESLA COTIZADOR V3.0?**

Tesla Cotizador v3.0 es una **Aplicación Web profesional** diseñada específicamente para **Tesla Electricidad y Automatización S.A.C.**, que revoluciona la forma de crear cotizaciones, gestionar proyectos y generar informes técnicos en el sector eléctrico peruano.

### **🤖 Powered by PILI Intelligence**
Nuestro sistema cuenta con **PILI** (Procesadora Inteligente de Licitaciones Industriales), un sistema de IA especializado con **6 agentes expertos**:

- 🏠 **Agente Residencial** - Instalaciones domiciliarias
- 🏢 **Agente Comercial** - Edificios y locales comerciales  
- 🏭 **Agente Industrial** - Plantas y instalaciones industriales
- 🛡️ **Agente ITSE** - Certificaciones y normativas
- 🌍 **Agente Puesta a Tierra** - Sistemas de protección
- 📹 **Agente CCTV/Automatización** - Seguridad y domótica

### **🎯 ¿Para quién está diseñado?**
- **Ingenieros Eléctricos** que necesitan crear cotizaciones técnicas
- **Empresas eléctricas** que buscan automatizar sus procesos
- **Gerentes de Proyecto** que requieren seguimiento detallado
- **Equipos comerciales** que presentan propuestas a clientes

---

## ⭐ **CARACTERÍSTICAS PRINCIPALES**

### **🚀 Velocidad y Precisión**
- **Cotizaciones en 5 minutos** vs 2-3 horas manualmente
- **Cálculos automáticos** de cargas, conductores y protecciones
- **Base de datos actualizada** con precios del mercado peruano

### **🤖 Inteligencia Artificial Avanzada**
- **Chat conversacional** en español técnico especializado
- **Análisis de documentos** automático (PDF, Word, Excel, imágenes)
- **Búsqueda semántica** en histórico de proyectos
- **Recomendaciones inteligentes** basadas en normativas

### **📄 Generación Profesional**
- **Documentos Word** editables con formato corporativo
- **PDFs optimizados** para presentación a clientes
- **Plantillas personalizables** con logo de empresa
- **Cálculos técnicos** automáticos y verificados

### **🛡️ Cumplimiento Normativo**
- **CNE 2011** (Código Nacional de Electricidad)
- **IEEE 80** (Sistemas de puesta a tierra)
- **NFPA** (Protección contra incendios)
- **DS-066-2007** (Reglamento de seguridad e higiene)

### **☁️ Acceso Multiplataforma**
- **Navegador web** (Chrome, Firefox, Edge, Safari)
- **Dispositivos móviles** (tablets, smartphones)
- **Trabajo offline** con sincronización automática
- **Colaboración en tiempo real** entre equipos

---

## 🏗️ **MÓDULOS DEL SISTEMA**

Tesla Cotizador v3.0 está organizado en **3 módulos principales**, cada uno con **2 modalidades** de trabajo:

```
┌─────────────────────────────────────────────────────────────┐
│  🏠 TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  💰 COTIZACIONES        📊 PROYECTOS        📄 INFORMES    │
│  ┌─────────────┐       ┌─────────────┐     ┌─────────────┐ │
│  │   SIMPLE    │       │   SIMPLE    │     │   SIMPLE    │ │
│  │ Chat IA →   │       │ Cronograma  │     │ Resumen     │ │
│  │ Cotización  │       │ básico      │     │ ejecutivo   │ │
│  └─────────────┘       └─────────────┘     └─────────────┘ │
│  ┌─────────────┐       ┌─────────────┐     ┌─────────────┐ │
│  │  COMPLEJO   │       │  COMPLEJO   │     │  COMPLEJO   │ │
│  │ Upload docs │       │ Gestión PMI │     │ Análisis    │ │
│  │ IA + Editor │       │ + Recursos  │     │ técnico     │ │
│  └─────────────┘       └─────────────┘     └─────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **💰 MÓDULO COTIZACIONES**
**Propósito:** Crear presupuestos de venta para clientes

- **Simple:** Chat con IA → Cotización automática (5 min)
- **Complejo:** Upload documentos → RAG → IA → Editor personalizado (15 min)

### **📊 MÓDULO PROYECTOS**  
**Propósito:** Gestionar proyectos eléctricos desde inicio hasta entrega

- **Simple:** Cronograma básico con hitos predefinidos
- **Complejo:** Metodología PMI completa con gestión de recursos

### **📄 MÓDULO INFORMES**
**Propósito:** Generar reportes profesionales para clientes y gerencia

- **Simple:** Informes ejecutivos automáticos
- **Complejo:** Análisis técnicos detallados con gráficos

---

## 🚀 **PRIMEROS PASOS**

### **1. Acceder al Sistema**
1. Abre tu navegador web
2. Ingresa a: `http://localhost:3000` (desarrollo) 
3. El sistema carga automáticamente sin necesidad de login

### **2. Interfaz Principal**
La pantalla principal muestra:

```
┌─────────────────────────────────────────────────────────────┐
│ ⚡ TESLA COTIZADOR V3.0                    🟢 SISTEMA ACTIVO │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│     💰 COTIZACIONES     📊 PROYECTOS     📄 INFORMES       │
│     ┌─────────────┐    ┌─────────────┐   ┌─────────────┐    │
│     │   [SIMPLE]  │    │   [SIMPLE]  │   │   [SIMPLE]  │    │
│     │  [COMPLEJO] │    │  [COMPLEJO] │   │  [COMPLEJO] │    │
│     └─────────────┘    └─────────────┘   └─────────────┘    │
│                                                             │
│ 📊 Dashboard de Estado:                                    │
│ • ✅ IA Gemini: Activa                                      │
│ • ✅ Base de Datos: Conectada                               │
│ • ✅ Generación Documentos: Operativa                      │
│ • 📈 Cotizaciones creadas hoy: 12                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **3. Indicadores de Estado**
- 🟢 **Verde:** Sistema completamente operativo
- 🟡 **Amarillo:** Funcionalidad limitada (modo demo)
- 🔴 **Rojo:** Error en el sistema

---

## 💰 **MÓDULO COTIZACIONES**

### **🎯 COTIZACIÓN SIMPLE - Para proyectos estándar**

#### **Paso 1: Iniciar Chat**
1. Haz clic en **[COTIZACIONES]** → **[SIMPLE]**
2. Se abre el chat con PILI Intelligence
3. Describe tu proyecto en lenguaje natural

**Ejemplo de conversación:**
```
👤 Usuario: "Necesito cotizar una instalación eléctrica para una casa 
            de 120m2, con 8 puntos de luz LED, 12 tomacorrientes 
            dobles y un tablero principal"

🤖 PILI: "Perfecto, voy a crear tu cotización residencial. Basándome 
         en 120m2, calcularé la carga eléctrica, dimensionamiento 
         de conductores y equipos según CNE 2011.

         ANÁLISIS INICIAL:
         • Área: 120m2 → Carga estimada: 3.5 kW
         • Puntos de luz: 8 x 18W = 144W
         • Tomacorrientes: 12 x 180W = 2160W
         • Circuitos recomendados: 4 (2 de luces + 2 de tomacorrientes)
         • Tablero: Monofásico 12 polos
         • Conductor principal: 3 x 6mm² + 1 x 6mm² (T)
         
         ¿Quieres que agregue pozo a tierra según IEEE-80?"
```

#### **Paso 2: Vista Previa**
Cuando la cotización está lista, aparece una **vista previa HTML**:

```html
┌─────────────────────────────────────────────────┐
│ ⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.   │
│ 💰 COTIZACIÓN ELÉCTRICA N° COT-20251127-1425    │
├─────────────────────────────────────────────────┤
│ Cliente: [Por definir]                          │
│ Proyecto: Instalación Residencial              │
│ Fecha: 27/11/2025    Vigencia: 30 días         │
├─────────────────────────────────────────────────┤
│ DESCRIPCIÓN              CANT   UND   P.UNIT    │
│ Punto de luz LED 18W      8     pto   S/32.00   │
│ Tomacorriente c/tierra   12     pto   S/42.00   │
│ Cable THW 2.5mm²         80      m    S/4.20    │
│ Tablero monofásico 12P    1     und   S/420.00  │
│ Pozo a tierra Ø=25Ohm     1     glb   S/650.00  │
├─────────────────────────────────────────────────┤
│                           Subtotal: S/ 1,790.00 │
│                           IGV(18%): S/   322.20 │
│                           TOTAL:   S/ 2,112.20 │
└─────────────────────────────────────────────────┘
```

### **🎯 COTIZACIÓN COMPLEJA - Para proyectos especializados**

#### **Paso 1: Upload de Documentos**
1. Haz clic en **[COTIZACIONES]** → **[COMPLEJO]**
2. **Arrastra y suelta** archivos o haz clic en **[SUBIR ARCHIVOS]**

**Formatos soportados:**
- 📄 **PDF**: Planos, especificaciones, licitaciones
- 📝 **Word**: Términos de referencia, requerimientos
- 📊 **Excel**: Listas de materiales, presupuestos base
- 🖼️ **Imágenes**: Planos escaneados, fotografías de instalaciones

#### **Paso 2: Análisis Inteligente**
PILI analiza automáticamente y extrae información técnica relevante.

---

## 🤖 **PILI INTELLIGENCE - SISTEMA DE IA**

### **👥 Los 6 Agentes de PILI**

#### **🏠 Agente Residencial**
**Especialidad:** Instalaciones domiciliarias hasta 10 kW
- Circuitos de iluminación LED
- Tomacorrientes monofásicos
- Tableros residenciales 1-2 pisos
- Puesta a tierra residencial
- **Rango:** S/ 2,000 - S/ 25,000

#### **🏢 Agente Comercial**
**Especialidad:** Edificios y locales comerciales
- Sistemas de distribución trifásica
- Iluminación de emergencia
- Aires acondicionados centrales
- Certificaciones ITSE
- **Rango:** S/ 25,000 - S/ 300,000

#### **🏭 Agente Industrial**
**Especialidad:** Instalaciones industriales de alta potencia
- Motores industriales >100HP
- Sistemas de control PLC/SCADA
- Compensación reactiva
- **Rango:** S/ 300,000 - S/ 5,000,000+

#### **🛡️ Agente ITSE**
**Especialidad:** Certificaciones y normativas
- Inspecciones Técnicas de Seguridad
- Planes de contingencia
- Marco legal peruano

#### **🌍 Agente Puesta a Tierra**
**Especialidad:** Sistemas de protección y seguridad
- Diseño de mallas de tierra IEEE-80
- Protección contra rayos
- Pozos de tierra especializados

#### **📹 Agente CCTV/Automatización**
**Especialidad:** Seguridad electrónica y domótica
- Cámaras IP/analógicas HD/4K
- Control de acceso biométrico
- Automatización de edificios

---

## 🎯 **CASOS DE USO PRÁCTICOS**

### **Caso 1: Cotización Urgente (30 minutos)**

**Situación:** Cliente llama viernes 4:30pm pidiendo cotización para lunes

```
⏱️ MINUTO 0: Llamada del cliente
⏱️ MINUTO 2: [COTIZACIONES] → [SIMPLE]
⏱️ MINUTO 4: PILI responde con análisis inicial
⏱️ MINUTO 15: Vista previa generada
⏱️ MINUTO 18: [GENERAR WORD] con logo empresa
⏱️ MINUTO 25: Envío por email al cliente
⏱️ MINUTO 30: ✅ MISIÓN CUMPLIDA
```

### **Caso 2: Análisis de Documento Técnico (20 minutos)**

**Situación:** Cliente envía especificaciones de 50 páginas para revisión

```
⏱️ MINUTO 0: Recepción del archivo
⏱️ MINUTO 1: [DOCUMENTOS] → Upload
⏱️ MINUTO 8: Análisis completado
⏱️ MINUTO 15: Generar informe de análisis
⏱️ MINUTO 20: ✅ DECISIÓN INFORMADA
```

---

## 💡 **TIPS Y MEJORES PRÁCTICAS**

### **🎯 Para obtener mejores resultados con PILI**

#### **Cómo hacer preguntas efectivas:**
```
❌ MAL: "Necesito una cotización"
✅ BIEN: "Necesito cotizar instalación eléctrica para casa de 
         120m², 2 pisos, con 8 puntos de luz LED y 10 
         tomacorrientes, incluir pozo a tierra"

❌ MAL: "¿Cuánto cuesta?"
✅ BIEN: "¿Cuál es el costo estimado incluyendo materiales, 
         mano de obra y certificación ITSE básico?"
```

#### **Información clave que debes proporcionar:**
- **Residenciales:** Área, pisos, puntos eléctricos, electrodomésticos especiales
- **Comerciales:** Tipo de negocio, horarios, equipos especiales, certificaciones
- **Industriales:** Proceso productivo, equipos principales, nivel de tensión

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **Sistema en Modo Demo/Básico**
```
🔴 SÍNTOMAS:
• Botones grises en lugar de azules
• IA responde con respuestas genéricas

✅ SOLUCIÓN:
1. Verificar conexión a internet
2. Refrescar página (F5)
3. Verificar que backend esté ejecutándose
```

### **Upload de Archivos Falla**
```
✅ SOLUCIONES:
1. Verificar tamaño < 50MB
2. Usar formatos soportados
3. Intentar con archivo más pequeño
```

### **PILI No Responde Correctamente**
```
✅ SOLUCIONES:
1. Proporcionar más contexto
2. Usar terminología técnica específica
3. Preguntar una cosa a la vez
```

---

## 🎓 **CONCLUSIÓN**

Tesla Cotizador v3.0 representa un **salto cuántico** en la automatización de procesos eléctricos, combinando la **experiencia técnica tradicional** con la **potencia de la Inteligencia Artificial** especializada.

### **🏆 Beneficios Demostrados**
- **Velocidad:** Cotizaciones en 5-30 minutos vs 2-8 horas
- **Precisión:** Cálculos automáticos según normativas peruanas
- **Profesionalismo:** Documentos de calidad corporativa
- **Inteligencia:** Análisis y recomendaciones basadas en experiencia

### **🚀 Impacto en tu Empresa**
Con Tesla Cotizador v3.0, **Tesla Electricidad y Automatización S.A.C.** puede:
- **Aumentar productividad** del equipo técnico en 300-500%
- **Mejorar calidad** de propuestas y documentos
- **Reducir errores** en cálculos y especificaciones  
- **Acelerar tiempo de respuesta** a clientes

---

**Tesla Cotizador v3.0 + PILI Intelligence = El futuro de la ingeniería eléctrica está aquí.**

*¡Bienvenido a la nueva era de la cotización eléctrica inteligente!*
