# Agent/rag_agent.py

from src.RAG.retrieve import retrieve_chunks


def rag_retriever(state):
    """
    Recupera contexto desde el RAG y lo guarda en el estado.
    """

    results = retrieve_chunks(state["question"])

    state["context"] = "\n\n".join(
        chunk["text"] for chunk in results
    )

    return state