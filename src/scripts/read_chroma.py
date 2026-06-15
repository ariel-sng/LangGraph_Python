from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from src.config.settings import Settings
from pathlib import Path



embeddings = OpenAIEmbeddings(model=Settings.EMBEDDING_MODEL)

# Cargar el vector store persistido
vector_store = Chroma(
    persist_directory=str(Path("storage/chroma")),
    embedding_function=embeddings,
    collection_name="default",  # solo hay uno y le puse default
)

# Obtener todos los documentos almacenados
data = vector_store.get()
total = len(data["ids"])
print(data)

ids = data["ids"]
documents = data["documents"]
metadatas = data["metadatas"]

print(f"Total de chunks: {len(ids)}\n")

for i, (doc_id, doc, metadata) in enumerate(
    zip(ids, documents, metadatas), start=1
):
    print("=" * 80)
    print(f"Chunk {i}/{total}")
    print(f"ID: {doc_id}")
    print(f"Metadata: {metadata}")
    print("Contenido:")
    print(doc)
    print()