# LangGraph_Python

**Flujo multiagente RAG y comparación de contratos por imagenes**

El proyecto incluye dos fases separadas:
- **PI Nº3**: un flujo RAG multiagente para consultas de texto.
- **PI Nº4**: un agente de comparación de contratos basado en imágenes que recibe contrato y enmienda.

---

## 1. Instalar UV y dependencias

1. Instalar UV si no está presente:

```bash
pip install uv
```

2. Clonar el repositorio:

```bash
git clone https://github.com/ariel-sng/LangGraph_Python
cd "LangGraph_Python"
```

3. Instalar dependencias:

```bash
uv sync
```

---

## 2. Configurar el entorno

Crear un archivo `.env` en la raíz con estas variables:

```env
OPENAI_API_KEY=tu_clave_openai_aca
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_HIGH_MODEL=gpt-5
OPENAI_LOW_MODEL=gpt-5-nano
MAX_PROMPT_TOKENS=4096
LANGFUSE_SECRET_KEY=tu_clave_secreta_langfuse_aca
LANGFUSE_PUBLIC_KEY=tu_clave_publica_langfuse_aca
LANGFUSE_BASE_URL="https://us.cloud.langfuse.com"
```

---

## PI 3 — Multiagente RAG

### Cómo funciona

- `src/agent/orchestrator.py` es el nodo central.
- El orquestador usa un LLM para elegir un dominio.
- Los agentes de dominio están en `src/agent` e incluyen: `finance.py`, `hr.py`, `tech.py`, `legal.py` y `unknown.py`.
- El grafo de ejecución está en `src/utils/graph_builder.py`.

Flujo principal:

`pregunta -> orchestrator -> agente de dominio -> respuesta`

Si la consulta no pertenece claramente a un dominio, se enruta a `unknown`.

### Ejecutar la ingestión

`src/scripts/run_ingest.py` procesa los archivos `documents/*.md` y los divide en chunks para su uso posterior.

```bash
uv run python -m src.scripts.run_ingest --method fixed --chunk-size 500 --chunk-overlap 100
```

Flags disponibles:
- `--method`: `fixed` o `sentence`.
- `--chunk-size`: tamaño máximo de chunk en caracteres.
- `--chunk-overlap`: solapamiento entre chunks (solo para `fixed`).

Ejemplo:

```bash
uv run python -m src.scripts.run_ingest --method sentence --chunk-size 500
```

### Ejecutar consultas

`src/scripts/run_query.py` abre un bucle interactivo que pide preguntas y muestra respuestas del grafo de agentes.

```bash
uv run python -m src.scripts.run_query
```

Flags disponibles:
- `--no-eval`: omite la ejecución del agente evaluador y muestra solo la respuesta.

Uso:
- Escribe la pregunta.
- Presiona Enter.
- Escribe `exit` para finalizar.

### Evaluador

El evaluador es un componente externo al grafo de LangGraph que se ejecuta una vez finalizado el flujo. Su función es analizar la consulta, el contexto recuperado por el RAG y la respuesta generada para asignar un puntaje y una justificación sobre la calidad del uso del contexto. Si la ruta seleccionada es unknown, evalúa únicamente que la respuesta rechace correctamente una consulta fuera del alcance del sistema.


### Inspeccionar chunks en ChromaDB

```bash
uv run python -m src.scripts.read_chroma
```

---

## PI 4 — Comparación de contratos con LangGraph

### Qué hace

Este módulo recibe dos documentos: un contrato y una enmienda.

El flujo hace lo siguiente:
- El primer nodo parsea las imágenes y extrae el texto de cada documento,
- El segundo nodo genera un mapa conceptual/estructura del contrato y de la enmienda por separado,
- El tercer nodo identifica y devuelve las diferencias entre ambos.

Todo esto se ejecuta con LangGraph.

### Ejecutar comparación

```bash
uv run -m src.scripts.run_comparison contrato enmienda
```

Donde `contrato` y `enmienda` son los nombres de los documentos dentro de `contracts/`, específicamente deben ser imágenes.

---

## Archivos clave

- `src/config/settings.py`: carga `.env`.
- `src/utils/graph_builder.py`: construye el grafo.
####  PI 3
- `src/agent/orchestrator.py`: toma la decisión de ruta.
- `src/agent/finance.py`, `hr.py`, `tech.py`, `legal.py`, `unknown.py`: agentes de dominio.
- `src/scripts/run_ingest.py`: ingestión de documentos.
- `src/scripts/read_chroma.py`: muestra los chunks guardados.
- `src/scripts/run_query.py`: consulta interactiva.
#### PI 4
- - `src/agent/image/parser_image.py`, `contextualizer.py`, `extractor.py`: agentes de dominio.
- `src/scripts/run_comparison.py`: ejecuta el agente de comparación de contratos de PI 4.

---

## Dependencias principales

Las dependencias principales del proyecto están en `pyproject.toml` y incluyen:

- `chromadb`
- `langchain`
- `langfuse`
- `openai`
- `python-dotenv`
- `tiktoken`
