# 🚀 PLAN COMPLETO: PILI ULTRA INTELIGENTE CON LANGCHAIN

**Fecha:** 20 de Diciembre 2025
**Objetivo:** Transformar PILI en la IA local más inteligente especializada en generación de documentos profesionales
**Stack:** LangChain + Ollama + ChromaDB + Sentence Transformers

---

## 🎯 VISIÓN

PILI será un sistema de agentes especializados que:
- ✅ Conversa naturalmente sin reglas hardcodeadas
- ✅ Aprende de conversaciones pasadas
- ✅ Consulta normativas técnicas peruanas en tiempo real (RAG)
- ✅ Razona paso a paso para tomar decisiones
- ✅ Se ejecuta 100% LOCAL (sin APIs externas)
- ✅ Genera documentos profesionales impecables

---

## 📊 ARQUITECTURA PROPUESTA

```
┌─────────────────────────────────────────────────────────────────┐
│                    PILI ULTRA INTELIGENTE                       │
│                    (LangChain + Ollama Local)                   │
└─────────────────────────────────────────────────────────────────┘

┌────────────────────┐
│ PILI ORCHESTRATOR  │ ← Coordina los 3 especialistas
│  (ReAct Agent)     │
└────────────────────┘
         │
         ├──► ┌──────────────────────┐
         │    │ PILI COTIZADORA      │ ← Agent con 10 herramientas (servicios)
         │    │  (ReAct Agent)       │ ← Memoria conversacional
         │    │  + RAG Normativas    │ ← ChromaDB con CNE, RNE, ITSE
         │    └──────────────────────┘
         │
         ├──► ┌──────────────────────┐
         │    │ PILI PROYECTOS       │ ← Agent PMI experto
         │    │  (ReAct Agent)       │ ← Memoria + conocimiento PMI
         │    │  + RAG PMBOK         │ ← ChromaDB con PMBOK
         │    └──────────────────────┘
         │
         └──► ┌──────────────────────┐
              │ PILI INFORMES        │ ← Agent técnico/académico
              │  (ReAct Agent)       │ ← Memoria + normas APA
              │  + RAG APA 7th       │ ← ChromaDB con APA 7th
              └──────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│              COMPONENTES COMPARTIDOS                           │
├────────────────────────────────────────────────────────────────┤
│ • LLM Local: Ollama (llama3 8B o mistral 7B)                  │
│ • Embeddings: sentence-transformers/paraphrase-multilingual   │
│ • Vector Store: ChromaDB (local, sin servidor)                │
│ • Memoria: ConversationBufferMemory + PostgreSQL              │
│ • Cache: Faiss para búsquedas ultra-rápidas                   │
└────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ STACK TECNOLÓGICO DETALLADO

### 1. LangChain Core
```python
langchain==0.1.0
langchain-community==0.0.13
langchain-core==0.1.10
```

**Uso:**
- Agents ReAct para razonamiento paso a paso
- Chains para flujos complejos
- Memory para persistencia de conversaciones
- Tools para herramientas especializadas

### 2. LLM Local (Ollama)
```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Modelos recomendados (español)
ollama pull llama3:8b           # General, 8GB RAM
ollama pull mistral:7b-instruct # Mejor para instrucciones, 6GB RAM
ollama pull phi3:mini           # Ligero, 4GB RAM
```

**Uso:**
```python
from langchain_community.llms import Ollama

llm = Ollama(
    model="mistral:7b-instruct",
    temperature=0.3,  # Más determinístico para documentos
    base_url="http://localhost:11434"
)
```

### 3. Embeddings Locales
```python
sentence-transformers==3.4.0
```

**Modelo:**
```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'},  # o 'cuda' si tienes GPU
    encode_kwargs={'normalize_embeddings': True}
)
```

### 4. Vector Store (ChromaDB)
```python
chromadb==0.5.23
```

**Colecciones:**
1. `normativas_electricas_peru` - CNE, RNE, ITSE
2. `pmbok_espanol` - Guía PMBOK 7ma edición
3. `normas_apa_7` - APA 7th edition español
4. `cotizaciones_historicas` - Aprendizaje de cotizaciones pasadas

### 5. Memoria Persistente
```python
langchain-postgres==0.0.1
psycopg2-binary==2.9.9
```

**Schema:**
```sql
CREATE TABLE pili_conversations (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100),
    specialist VARCHAR(50),  -- cotizadora, proyectos, informes
    timestamp TIMESTAMP,
    user_message TEXT,
    assistant_response TEXT,
    metadata JSONB
);
```

---

## 🎯 IMPLEMENTACIÓN POR ESPECIALISTA

### 1. PILI COTIZADORA CON LANGCHAIN

#### Herramientas (Tools) Especializadas

```python
from langchain.agents import Tool
from langchain.tools import BaseTool

class CalculadoraElectricaTool(BaseTool):
    name = "calculadora_electrica"
    description = """
    Calcula carga eléctrica, calibre de conductores, protecciones.
    Input: JSON con área_m2, tipo_instalacion, voltaje
    Output: Resultados según CNE Perú
    """

    def _run(self, input_data: dict) -> dict:
        # Lógica de cálculo según CNE
        area = input_data['area_m2']
        # Cálculo de carga: 20 VA/m² residencial
        carga_total = area * 20
        # ... más cálculos
        return {"carga_total_va": carga_total, "conductor_recomendado": "14 AWG"}

class ConsultorNormativasTool(BaseTool):
    name = "consultor_normativas"
    description = """
    Consulta el CNE, RNE o reglamento ITSE.
    Input: pregunta sobre normativa
    Output: Artículo relevante con cita
    """

    def _run(self, query: str) -> str:
        # RAG sobre ChromaDB normativas
        docs = vector_store.similarity_search(query, k=3)
        return f"Según CNE Art. X: {docs[0].page_content}"

tools = [
    CalculadoraElectricaTool(),
    ConsultorNormativasTool(),
    Tool(name="validar_ruc", func=validar_ruc_sunat, description="Valida RUC en SUNAT"),
    Tool(name="calcular_igv", func=lambda x: float(x) * 0.18, description="Calcula IGV 18%"),
    # ... más herramientas específicas
]
```

#### Agent ReAct

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

cotizadora_prompt = PromptTemplate.from_template("""
Eres PILI Cotizadora, experta en cotizaciones eléctricas en Perú.

OBJETIVO: Guiar al usuario paso a paso para generar una cotización profesional.

REGLAS:
1. Detecta el servicio (instalación eléctrica, ITSE, puesta a tierra, etc.)
2. Pregunta datos faltantes UNO POR UNO (no bombardees con muchas preguntas)
3. Usa herramientas para cálculos y consultar normativas
4. Cuando tengas todos los datos, genera JSON estructurado

Herramientas disponibles:
{tools}

Historial conversación:
{chat_history}

Usuario: {input}

Razonamiento:
{agent_scratchpad}
""")

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=cotizadora_prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=ConversationBufferMemory(memory_key="chat_history"),
    verbose=True,
    max_iterations=10
)
```

#### RAG para Normativas

```python
# Cargar CNE en ChromaDB
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. Cargar documentos
cne_docs = load_pdf("storage/normativas/CNE_Peru_2011.pdf")
rne_docs = load_pdf("storage/normativas/RNE_Peru_2024.pdf")

# 2. Dividir en chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(cne_docs + rne_docs)

# 3. Crear vector store
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="storage/chroma_db/normativas",
    collection_name="normativas_peru"
)

# 4. Usar en herramienta
def consultar_normativa(pregunta: str) -> str:
    docs = vector_store.similarity_search(pregunta, k=3)
    return "\n".join([doc.page_content for doc in docs])
```

---

### 2. PILI PROYECTOS CON LANGCHAIN

#### Herramientas PMI

```python
class GanttGeneratorTool(BaseTool):
    name = "generar_gantt"
    description = "Genera cronograma Gantt válido desde descripción"

    def _run(self, fases: List[dict]) -> dict:
        # Valida dependencias, duraciones
        # Genera JSON compatible con mermaid.js
        return {"gantt_json": {...}, "diagram_mermaid": "..."}

class CalculadoraROITool(BaseTool):
    name = "calcular_roi"
    description = "Calcula ROI, TIR, VAN del proyecto"

    def _run(self, inversion: float, flujos: List[float]) -> dict:
        # Cálculos financieros
        roi = ((sum(flujos) - inversion) / inversion) * 100
        return {"roi_porcentaje": roi, "tir": ..., "van": ...}

class AnalizadorRiesgosTool(BaseTool):
    name = "analizar_riesgos"
    description = "Analiza riesgos del proyecto con matriz probabilidad-impacto"

    def _run(self, descripcion_proyecto: str) -> List[dict]:
        # LLM analiza y genera riesgos
        prompt = f"Analiza riesgos para: {descripcion_proyecto}"
        riesgos_raw = llm(prompt)
        # Parsea y estructura
        return [{"riesgo": "...", "probabilidad": 0.7, "impacto": 0.8}]
```

#### Agent PMI Experto

```python
proyectos_prompt = PromptTemplate.from_template("""
Eres PILI Proyectos, experta en gestión de proyectos según PMBOK 7.

CAPACIDADES:
1. Proyectos simples (5 pasos)
2. Proyectos complejos PMI (8 pasos + Gantt + Riesgos + KPIs)

METODOLOGÍA:
- Guía paso a paso
- Valida información con herramientas
- Genera Gantt automáticamente
- Analiza riesgos con matriz
- Calcula métricas financieras (ROI, TIR, VAN)

Herramientas: {tools}
Historial: {chat_history}
Usuario: {input}
Razonamiento: {agent_scratchpad}
""")

# Agent con herramientas PMI
pmi_agent = create_react_agent(llm, pmi_tools, proyectos_prompt)
```

---

### 3. PILI INFORMES CON LANGCHAIN

#### Herramientas APA

```python
class ValidadorAPATool(BaseTool):
    name = "validar_apa"
    description = "Valida formato APA 7th (citas, referencias, estructura)"

    def _run(self, texto: str) -> dict:
        # Verifica:
        # - Citas en texto (Apellido, Año)
        # - Referencias con DOI
        # - Formato de títulos
        return {"valido": True, "errores": []}

class GeneradorReferenciasTool(BaseTool):
    name = "generar_referencias"
    description = "Genera referencias APA 7th desde DOI o URL"

    def _run(self, doi_o_url: str) -> str:
        # Consulta CrossRef API
        # Genera referencia APA automáticamente
        return "Apellido, A. (2024). Título. Editorial."
```

#### RAG Normas APA

```python
# Cargar APA Manual 7th en ChromaDB
apa_manual = load_pdf("storage/normativas/APA_7th_Espanol.pdf")
apa_chunks = splitter.split_documents(apa_manual)

apa_vector_store = Chroma.from_documents(
    documents=apa_chunks,
    embedding=embeddings,
    persist_directory="storage/chroma_db/apa",
    collection_name="normas_apa_7"
)

def consultar_apa(pregunta: str) -> str:
    """Ej: '¿Cómo citar un sitio web sin autor?'"""
    docs = apa_vector_store.similarity_search(pregunta, k=2)
    return docs[0].page_content
```

---

## 🔄 FLUJO COMPLETO DE CONVERSACIÓN

### Ejemplo: Cotización Eléctrica

```
Usuario: "Necesito cotizar una instalación eléctrica para mi casa"

PILI Orchestrator (ReAct):
Thought: Usuario quiere cotización eléctrica → enrutar a PILI Cotizadora
Action: route_to_specialist("cotizadora")

PILI Cotizadora (ReAct):
Thought: Instalación eléctrica detectada. Necesito saber: tipo (residencial/comercial), área, puntos
Action: None
Response: "Perfecto, ¿es para vivienda, oficina o industria?"

Usuario: "Vivienda de 120 m²"

PILI Cotizadora:
Thought: Tipo=residencial, área=120m². Necesito puntos de luz y tomacorrientes
Action: calculadora_electrica({"area_m2": 120, "tipo": "residencial"})
Observation: Carga estimada 2400 VA
Thought: Ahora sé la carga base. Preguntar puntos específicos
Response: "Para 120 m² residencial, estimé 2400 VA de carga base. ¿Cuántos puntos de luz necesitas?"

Usuario: "20 puntos de luz y 15 tomacorrientes"

PILI Cotizadora:
Thought: Tengo todo. Generar cotización
Action: consultor_normativas("Conductor recomendado para 2400 VA")
Observation: "Según CNE Art. 50.102: Conductor mínimo 14 AWG para circuitos derivados"
Action: calcular_igv(2450.00)
Observation: 441.00
Response: {
  "puede_generar": true,
  "datos_cotizacion": {
    "cliente": "[PENDIENTE]",
    "servicio": "Instalación Eléctrica Residencial",
    "area_m2": 120,
    "items": [
      {"desc": "Tablero eléctrico 12 polos", "cant": 1, "precio": 450},
      {"desc": "Puntos de luz con cable 14 AWG", "cant": 20, "precio": 35},
      {"desc": "Tomacorrientes dobles", "cant": 15, "precio": 25},
      ...
    ],
    "subtotal": 2450.00,
    "igv": 441.00,
    "total": 2891.00,
    "normativa": "CNE Perú 2011, RNE"
  }
}

Usuario: "El cliente es Rogelio Infantas, RUC 20601140740"

PILI Cotizadora:
Action: validar_ruc("20601140740")
Observation: RUC válido - INFANTAS CONTRERAS ROGELIO
Response: "✅ Cotización completa. Cliente validado en SUNAT."
```

---

## 📥 INSTALACIÓN Y CONFIGURACIÓN

### Paso 1: Instalar Ollama

```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Descargar desde https://ollama.com/download

# Verificar instalación
ollama --version

# Descargar modelo
ollama pull mistral:7b-instruct
```

### Paso 2: Instalar dependencias Python

```bash
cd backend

# Agregar a requirements.txt
cat >> requirements.txt << EOF
# LangChain Stack
langchain==0.1.0
langchain-community==0.0.13
langchain-core==0.1.10
langchain-postgres==0.0.1

# LLM Local
langchain-ollama==0.1.0

# Vector Store
chromadb==0.5.23
faiss-cpu==1.8.0  # o faiss-gpu si tienes CUDA

# Embeddings
sentence-transformers==3.4.0
transformers==4.36.2
torch==2.1.2  # CPU version

# Utilidades
python-dotenv==1.0.0
tiktoken==0.5.2
EOF

# Instalar
pip install -r requirements.txt
```

### Paso 3: Configurar variables de entorno

```bash
# backend/.env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct
EMBEDDINGS_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
CHROMA_PERSIST_DIR=/storage/chroma_db
```

---

## 🧪 PRUEBAS EXHAUSTIVAS

### Test 1: PILI Cotizadora

```python
def test_cotizadora_instalacion_electrica():
    """Test conversación completa"""

    cotizadora = PILICotizadoraLangChain()

    # Mensaje 1
    resp1 = cotizadora.procesar("Necesito cotizar instalación eléctrica", [])
    assert "tipo" in resp1["respuesta"].lower() or "residencial" in resp1["respuesta"].lower()

    # Mensaje 2
    resp2 = cotizadora.procesar("Es residencial de 100 m²", historial)
    assert "puntos" in resp2["respuesta"].lower()

    # Mensaje 3
    resp3 = cotizadora.procesar("15 puntos de luz y 10 tomacorrientes", historial)
    assert resp3["puede_generar"] == True
    assert "items" in resp3["datos_cotizacion"]
    assert resp3["datos_cotizacion"]["total"] > 0
```

### Test 2: RAG Normativas

```python
def test_rag_normativas():
    """Test consulta CNE"""

    pregunta = "¿Qué calibre de conductor usar para 20A?"
    respuesta = consultar_normativa(pregunta)

    assert "14 AWG" in respuesta or "12 AWG" in respuesta
    assert "CNE" in respuesta
```

### Test 3: Memoria Persistente

```python
def test_memoria_conversaciones():
    """Test que recuerda conversaciones pasadas"""

    session_id = "test_123"

    # Conversación 1
    cotizadora.procesar("Hola, soy Rogelio", [], session_id=session_id)

    # Conversación 2 (días después)
    resp = cotizadora.procesar("Necesito otra cotización", [], session_id=session_id)

    # Debe recordar el nombre
    assert "Rogelio" in resp["respuesta"]
```

---

## 📊 MÉTRICAS DE ÉXITO

### KPIs a medir:

1. **Precisión conversacional:**
   - % de veces que detecta el servicio correcto: >95%
   - % de cotizaciones completas sin errores: >98%

2. **Velocidad:**
   - Tiempo de respuesta: <3 segundos (local)
   - Generación de documento: <5 segundos

3. **Calidad de documentos:**
   - Validación APA: 100% conforme
   - Cumplimiento normativo: 100%
   - Satisfacción usuario: >4.5/5

4. **Inteligencia:**
   - Respuestas fuera de contexto: <2%
   - Consultas RAG relevantes: >90%
   - Aprendizaje de conversaciones: medible con embeddings similarity

---

## 🎯 ROADMAP DE IMPLEMENTACIÓN

### Fase 1: Fundamentos (Días 1-2)
- [x] Instalar Ollama + modelos
- [ ] Configurar LangChain básico
- [ ] Crear primer agent ReAct simple
- [ ] Probar conversación básica

### Fase 2: PILICotizadora Inteligente (Días 3-4)
- [ ] Crear 10 herramientas especializadas
- [ ] Implementar agent ReAct completo
- [ ] Cargar CNE/RNE en ChromaDB
- [ ] RAG funcional
- [ ] 100 tests de conversaciones

### Fase 3: PILIProyectos PMI (Días 5-6)
- [ ] Herramientas PMI (Gantt, ROI, Riesgos)
- [ ] Agent PMI experto
- [ ] Cargar PMBOK en ChromaDB
- [ ] Generación de Gantt automático
- [ ] 50 tests de proyectos

### Fase 4: PILIInformes APA (Días 7-8)
- [ ] Herramientas APA
- [ ] Agent académico
- [ ] Cargar APA Manual en ChromaDB
- [ ] Validador APA automático
- [ ] 50 tests de informes

### Fase 5: Integración y Optimización (Días 9-10)
- [ ] Orchestrator con routing inteligente
- [ ] Memoria persistente PostgreSQL
- [ ] Cache con Faiss
- [ ] Pruebas end-to-end
- [ ] Documentación completa

---

## 🚀 SIGUIENTE PASO INMEDIATO

**AHORA MISMO:** Instalar Ollama y crear primer agent ReAct de prueba.

¿Arrancamos? Dame la señal y empiezo con Fase 1.
