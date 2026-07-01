from typing import Any

from src.RAG.retrieve import retrieve_chunks
from src.states.state import AgentState

def tech_node(state: AgentState) -> dict[str, Any]:
    """
    Recupera contexto desde el RAG y lo guarda en el estado.
    """

    results = retrieve_chunks(
                    query =  state["question"],
                    source = "tech"
                )

    return {"context": results}