# RAG
Sistema de procesamiento de documentos y consultas con generación aumentada por recuperación. Utiliza ChromaDB como vector store y OpenAI como LLM.

---

## Requisitos Previos

- **Python 3.11 o superior**
- **UV** (gestor de paquetes Python moderno)

### Instalar UV

Si no tenés UV instalado, ejecutá:

```bash
pip install uv
```

O descargalo desde: https://docs.astral.sh/uv/getting-started/

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/ariel-sng/RAG_Python
cd "Henry - IA/RAG_Python"
```

### 2. Instalar dependencias con UV

```bash
uv sync
```

Esto leerá el archivo `pyproject.toml` e instalará todas las dependencias automáticamente.

### 3. Configurar variables de entorno

Creá un archivo `.env` en la raíz del proyecto:

```env
OPENAI_API_KEY=tu_clave_openai_aqui
EMBEDDING_MODEL=text-embedding-3-small
MAX_PROMPT_TOKENS=4096
OUTPUT_DIRECTORY=output
```

**Notas:**
- `OPENAI_API_KEY`: Requerido. Obtené tu clave en https://platform.openai.com/api-keys
- `EMBEDDING_MODEL`: Modelo de embeddings (default: text-embedding-3-small)
- `MAX_PROMPT_TOKENS`: Límite máximo de tokens para el prompt (default: 4096)
- `OUTPUT_DIRECTORY`: Carpeta donde se guardan los resultados (default: output)

---

## Dependencias

El proyecto usa las siguientes librerías (especificadas en `pyproject.toml`):

- **chromadb** ≥1.5.9 - Vector store para almacenar y recuperar embeddings
- **openai** ≥2.38.0 - Cliente de OpenAI para LLM y embeddings
- **python-dotenv** ≥1.2.2 - Manejo de variables de entorno
- **tiktoken** ≥0.4.0 - Contador de tokens para OpenAI

---

## Uso

### Pipeline 1: Indexación de Documentos

Carga un documento de texto en ChromaDB con chunking y embeddings.

#### Comando Básico

```bash
uv run python -m src.scripts.run_ingestion <archivo> [opciones]
```

#### Opciones

| Opción | Descripción | Default |
|--------|-------------|---------|
| `<archivo>` | Ruta del archivo de texto a indexar | Requerido |
| `--reload` | Limpia la colección antes de indexar | No activo |
| `--chunk-strategy` | Estrategia de división: `fixed` o `sentence` | `fixed` |
| `--chunk-size` | Tamaño máximo de cada chunk (caracteres) | `500` |
| `--chunk-overlap` | Solapamiento entre chunks (solo para `fixed`) | `100` |

#### Ejemplos

**Indexar con estrategia fija (default):**
```bash
uv run python -m src.scripts.run_ingestion documents/FAQ.txt
```

**Indexar limpiando la colección anterior:**
```bash
uv run python -m src.scripts.run_ingestion documents/FAQ.txt --reload
```

**Indexar con estrategia por oraciones:**
```bash
uv run python -m src.scripts.run_ingestion documents/FAQ.txt --chunk-strategy sentence --reload
```

**Indexar con estrategia fija y tamaños personalizados:**
```bash
uv run python -m src.scripts.run_ingestion documents/FAQ.txt --chunk-strategy fixed --chunk-size 1000 --chunk-overlap 200 --reload
```

#### Estrategias de Chunking

**Fixed (Fijo)**
- Divide el texto en fragmentos de tamaño uniforme
- Usa `chunk_size` y `chunk_overlap` para controlar solapamiento
- Ideal para chunks uniformes sin depender de la estructura del texto
- Ejemplo: 500 caracteres con 100 de overlap

**Sentence (Oraciones)**
- Agrupa oraciones hasta alcanzar el `chunk_size`
- Preserva unidades semánticas naturales (no parte oraciones)
- No usa overlap, mantiene coherencia del contenido
- Ideal para textos largos con estructura clara

---

### Pipeline 2: Consultas RAG

Realiza consultas sobre los documentos indexados. Recupera chunks relevantes y genera respuestas con el LLM.

#### Comando Básico

```bash
uv run python -m src.scripts.run_query <pregunta> [opciones]
```

#### Opciones

| Opción | Descripción | Default |
|--------|-------------|---------|
| `<pregunta>` | Pregunta a responder (entre comillas) | Requerido |
| `--k` | Número de chunks a recuperar | `5` |

#### Ejemplos

**Consulta simple:**
```bash
uv run python -m src.scripts.run_query "¿Qué es la búsqueda semántica?"
```

**Consulta con número reducido de chunks:**
```bash
uv run python -m src.scripts.run_query "¿Qué es RAG?" --k 3
```

**Consulta con más contexto:**
```bash
uv run python -m src.scripts.run_query "¿Cómo funciona la generación aumentada por recuperación?" --k 10
```

#### Salida

La consulta genera:
1. **Respuesta**: Texto generado por el LLM basado en los chunks recuperados
2. **Archivo JSON**: Guarda resultado en `output/rag_result.json` con estructura:
   - `question`: Pregunta realizada
   - `system_answer`: Respuesta del LLM
   - `chunks`: Lista de chunks recuperados con metadatos

**Nota**: Los resultados se **acumulan** en el JSON. Cada nueva consulta se agrega a la lista sin sobrescribir resultados anteriores.

---

### Herramientas Adicionales

#### Leer Chunks de ChromaDB

Inspecciona los chunks almacenados en el vector store:

```bash
uv run python -m src.scripts.read_chroma
```

---

## Estructura del Proyecto

```
.
├── README.md                          # Este archivo
├── pyproject.toml                     # Configuración de dependencias (UV)
├── .env                               # Variables de entorno (no versionar)
│
├── documents/                         # Documentos de entrada
│   └── FAQ.txt                        # Ejemplo: FAQ sobre RAG
│
├── src/
│   ├── config/
│   │   └── settings.py                # Configuración centralizada
│   │
│   ├── models/
│   │   ├── search_result.py           # Dataclass SearchResult
│   │   └── rag_search_result.py       # Dataclass RAGSearchResult
│   │
│   ├── RAG/
│   │   ├── query_services.py          # Servicio principal de consultas
│   │   ├── embedding_generator.py     # Generador de embeddings (OpenAI)
│   │   ├── ingestion_service.py       # Orquestador del pipeline de indexación
│   │   ├── llm_generator.py           # Generador de respuestas (LLM)
│   │   └── prompt_builder.py          # Constructor de prompts
│   │
│   ├── repositories/
│   │   ├── vector_store.py            # Interfaz del vector store
│   │   └── chroma_vector_store.py     # Implementación con ChromaDB
│   │
│   ├── utils/
│   │   ├── text_chunker.py            # Divisor de texto (fixed/sentence)
│   │   └── document_loader.py         # Cargador de archivos
│   │
│   └── scripts/
│       ├── run_ingestion.py           # CLI para indexación
│       ├── run_query.py               # CLI para consultas
│       └── read_chroma.py             # CLI para inspeccionar chunks
│
├──tests/
│   └── utils/
│       ├── test_document_loader.py     (7 tests)
│       └── test_text_chunker.py        (17 tests)
│
├── storage/
│   └── chroma/                        # Base de datos ChromaDB (persistente)
│       ├── chroma.sqlite3
│       └── [colecciones]/
│
└── output/
    └── rag_result.json                # Resultados acumulados de consultas

```

### Descripción de Componentes Clave

| Archivo | Propósito |
|---------|-----------|
| `src/config/settings.py` | Centraliza toda la configuración (API keys, modelos, límites de tokens) |
| `src/models/search_result.py` | Define la estructura de datos para resultados (question, answer, chunks) |
| `src/RAG/query_services.py` | Lógica principal: búsqueda, limitación de tokens, generación de respuestas |
| `src/RAG/embedding_generator.py` | Convierte texto a embeddings usando OpenAI |
| `src/RAG/llm_generator.py` | Genera respuestas usando el modelo LLM de OpenAI |
| `src/RAG/prompt_builder.py` | Construye el prompt combinando pregunta y contexto |
| `src/utils/text_chunker.py` | Divide documentos en chunks (estrategias: fixed, sentence) |
| `src/repositories/chroma_vector_store.py` | Almacena y recupera embeddings en ChromaDB |
| `src/scripts/run_ingestion.py` | Punto de entrada CLI para indexar documentos |
| `src/scripts/run_query.py` | Punto de entrada CLI para consultas RAG |

---

## Flujo de Trabajo Completo

### 1. Preparación
```bash
# Creá archivo .env con tus credenciales
# Colocá documentos en ./documents/
```

### 2. Indexación
```bash
# Indexar documento con estrategia por oraciones
uv run python -m src.scripts.run_ingestion documents/FAQ.txt --chunk-strategy sentence --reload
```

### 3. Consulta
```bash
# Realizar consulta
uv run python -m src.scripts.run_query "¿Qué es RAG?" --k 5

# Resultado guardado en output/rag_result.json
```

### 4. Inspección (opcional)
```bash
# Ver chunks almacenados
uv run python -m src.scripts.read_chroma
```

---

## Notas Importantes

- **Límite de tokens**: Se valida automáticamente con `MAX_PROMPT_TOKENS` para evitar costos excesivos en OpenAI
- **Acumulación de resultados**: Cada consulta agrega un nuevo resultado al JSON sin sobrescribir
- **ChromaDB persistente**: Los embeddings se guardan en `storage/chroma/` y persisten entre sesiones
- **Estrategia recomendada**: Usa `sentence` para documentos con estructura clara; `fixed` para contenido más uniforme

## Tests básicos

### Opción 1: Todos los tests
```bash
pytest
```

### Opción 2: Tests específicos de módulo
```bash
# Document Loader
pytest tests/utils/test_document_loader.py -v

# Text Chunker
pytest tests/utils/test_text_chunker.py -v


