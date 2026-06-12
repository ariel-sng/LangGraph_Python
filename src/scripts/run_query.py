import argparse
import sys

from openai import OpenAI



from src.config.settings import Settings
from src.repositories.chroma_vector_store import ChromaVectorStore

from src.RAG.embedding_generator import OpenAIEmbeddingGenerator
from src.RAG.query_services import RagQueryService
from src.RAG.llm_generator import LLMGenerator
from src.RAG.prompt_builder import PromptBuilder


def main() -> None:

    ### MANEJO DE ARGUMENTOS ###

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "question",
        type=str,
    )

    parser.add_argument(
        "--k",
        type=int,
        default=5,
    )

    args = parser.parse_args()

    ### CREACIÓN DE COMPONENTES  ###

    client = OpenAI(
        api_key=Settings.OPENAI_API_KEY,
    )

    openai_embedding_generator = OpenAIEmbeddingGenerator(
        client=client,
        model=Settings.EMBEDDING_MODEL,
    )

    vector = ChromaVectorStore(
            persist_directory="storage/chroma",
            collection_name="documents"
            )
    
    prompt_builder = PromptBuilder()
    llm_generator = LLMGenerator(client=client, model="gpt-3.5-turbo")
    
    query_service = RagQueryService(
        embedding_generator=openai_embedding_generator,
        vector_store=vector,
        prompt_builder=prompt_builder,
        llm_generator=llm_generator
    )

    ### CONSULTA AL RAG  ###

    print("Iniciando consulta al modelo RAG...")
    print(f"  Pregunta    : {args.question}")
    print(f"  Resultados K: {args.k}")
    print("  Vector store: storage/chroma, colección 'documents'")

    try:
        result = query_service.answer(
            question=args.question,
            k=args.k,
        )

        print("\n--- Respuesta generada ---")
        print(result.answer)
        print("--- Fin de la respuesta ---\n")

        query_service.save_rag_result(
            result=result,
            output_file=Settings.RAG_RESULT_FILE,
        )
        print(f"Resultados guardados en: {Settings.RAG_RESULT_FILE}")
    except Exception as e:
        print(f"Error al generar la respuesta para la pregunta '{args.question}': {e}")
        sys.exit(1)


    """
    results = query_service.search(
        question=args.question,
        k=args.k,
    )


    for i, result in enumerate(results, start=1):
        print(f"[{i}]")
        print(f"Similarity: {result.similarity:.4f}")

        file_name = result.metadata.get("file_name")

        if file_name:
            print(f"File: {file_name}")

        print()
        print(result.document)
        print("\n" + "-" * 80 + "\n")
    """


if __name__ == "__main__":
    main()