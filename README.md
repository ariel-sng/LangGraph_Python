# LangGraph_Python

Sistema multiagente en el que un Agente Orquestador clasifique la intención de la consulta del usuario 

Este proyecto recibe una consulta, el orquestador decide la ruta y el flujo continúa con un nodo específico:
`finance`, `hr`, `tech`, `legal` o `unknown`.

---

## 1. Instalar UV y dependencias

1. Instalar UV si no está presente:

```bash
pip install uv
```

2. Clonar el repositorio:

```bash
git clone https://github.com/ariel-sng/LangGraph_Python
cd "TicketGPT - U3"
```

3. Instalar dependencias:

```bash
uv sync
```

---

## 2. Configurar el entorno

Crear un archivo `.env` en la raíz con estas variables:

```env
OPENAI_API_KEY=tu_clave_openai_aqui
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_HIGH_MODEL=gpt-5
OPENAI_LOW_MODEL=gpt-5-nano
MAX_PROMPT_TOKENS=4096
```

---

## 3. Cómo funciona

- `src.Agent.orchestrator` es el nodo central.
- El orquestador usa un LLM para elegir un dominio.
- Los agentes de dominio están en `src/Agent` e incluyen: `/finance.py`, `hr.py`, `tech.py`, `legal.py` y `unknown.py`.
- El grafo de ejecución está en `src/utils/graph_builder.py`.

Flujo principal:

`pregunta -> orchestrator -> agente de dominio -> respuesta`

Si la consulta no pertenece claramente a un dominio, se enruta a `unknown`.

---

## 4. Ejecutar la ingestión

### Qué hace

`src/scripts/run_ingestion.py` procesa los archivos `documents/*.md` y los divide en chunks para su uso posterior.

### Comando

```bash
uv run python -m src.scripts.run_ingestion --method fixed --chunk-size 500 --chunk-overlap 100
```

### Flags disponibles

- `--method`: `fixed` o `sentence`.
- `--chunk-size`: tamaño máximo de chunk en caracteres.
- `--chunk-overlap`: solapamiento entre chunks (solo para `fixed`).

### Ejemplo

```bash
uv run python -m src.scripts.run_ingestion --method sentence --chunk-size 500
```

---

## 5. Ejecutar consultas

### Qué hace

`src/scripts/run_query.py` abre un bucle interactivo que pide preguntas y muestra respuestas del grafo de agentes.

### Comando

```bash
uv run python -m src.scripts.run_query
```

### Uso

- Escribe la pregunta.
- Presiona Enter.
- Escribe `exit` para finalizar.

---

## 6. Inspeccionar chunks en ChromaDB

Para ver los chunks almacenados:

```bash
uv run python -m src.scripts.read_chroma
```

---

## 7. Archivos clave

- `src/config/settings.py`: carga `.env`.
- `src/utils/graph_builder.py`: construye el grafo y las rutas.
- `src/Agent/orchestrator.py`: toma la decisi�n de ruta.
- `src/Agent/finance.py`, `hr.py`, `tech.py`, `legal.py`, `unknown.py`: agentes de dominio.
- `src/scripts/run_ingestion.py`: ingesti�n de documentos.
- `src/scripts/run_query.py`: consulta interactiva.
- `src/scripts/read_chroma.py`: muestra los chunks guardados.

---

## 8. Dependencias principales

Las dependencias del proyecto están en `pyproject.toml` y incluyen:

- `chromadb`
- `langchain`, `langchain-chroma`, `langchain-openai`, `langchain-text-splitters`, `langchain-community`
- `langfuse`
- `openai`
- `python-dotenv`
- `tiktoken`
