from pathlib import Path
import argparse
import sys
from openai import OpenAI

from src.config.settings import Settings
from src.repositories.chroma_vector_store import ChromaVectorStore
from src.RAG.ingestion_service import RagIngestionService
from src.utils.document_loader import DocumentLoader
from src.RAG.embedding_generator import OpenAIEmbeddingGenerator
from src.utils.text_chunker import TextChunker


def main() -> None:
    
    ### MANEJO DE ARGUMENTOS ###
    
    parser = argparse.ArgumentParser(
        description="Ingesta documentos en Chroma usando chunks fijos o por oraciones."
    )
    parser.add_argument(
        "file_path",
        type=str,
        help="Ruta del archivo a procesar.",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Borrar la colección antes de la ingestión.",
    )
    parser.add_argument(
        "--chunk-strategy",
        choices=["fixed", "sentence"],
        default="fixed",
        help="Estrategia para dividir el texto en chunks.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Tamaño máximo aproximado de cada chunk en caracteres.",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=100,
        help="Overlap entre chunks solo para estrategia fixed.",
    )

    args = parser.parse_args()

    file_path = args.file_path

    ### CREACIÓN DE COMPONENTES  ###

    vector_store = ChromaVectorStore(
        persist_directory="storage/chroma",
        collection_name="documents"
    )

    if args.reload:
        print("Reload solicitado: borrando la colección existente antes de la ingestión...")
        vector_store.reset()
        print("Colección 'documents' reiniciada correctamente.")
        
    client = OpenAI(
        api_key=Settings.OPENAI_API_KEY,
    )

    ingestion_service = RagIngestionService(
        loader=DocumentLoader(),
        chunker=TextChunker(
            strategy=args.chunk_strategy,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
        ),
        embedding_generator=OpenAIEmbeddingGenerator(
            client=client,
            model=Settings.EMBEDDING_MODEL,
        ),
        vector_store=vector_store,
    )

    ### LA INGESTA  ###

    print("Preparando ingestión de documento...")
    print(f"  Archivo       : {file_path}")
    print(f"  Estrategia    : {args.chunk_strategy}")
    print(f"  Chunk size    : {args.chunk_size}")
    print(f"  Chunk overlap : {args.chunk_overlap}")
    print("  Vector store  : storage/chroma, colección 'documents'")

    try:
        ingestion_service.ingest(
            file_path=file_path,
            metadata={
                "file_name": Path(file_path).name, 
                # Por ahora, solo agrego como metada el nombre del archivo, pero se pueden agregar más metadatos a futuro
            },
        )
    except Exception as ex:
        print(f"ERROR inesperado durante la ingestión del archivo '{file_path}': {ex}")
        sys.exit(1)

    print(f"Ingestión completada correctamente para: {file_path}")


if __name__ == "__main__":
    main()