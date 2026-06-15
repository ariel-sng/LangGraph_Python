# Agent/rag_agent.py

from typing import Any

from src.RAG.retrieve import retrieve_chunks


def rag_retriever(state) -> dict[str, Any]:
    """
    Recupera contexto desde el RAG y lo guarda en el estado.
    """

    results = retrieve_chunks(state["question"])

    return {"context": results}