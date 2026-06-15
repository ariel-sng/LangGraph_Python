from typing import Any

from langchain_core.tools import tool
from src.Agent.state import AgentState


def orchestrator(state: AgentState) -> dict[str, Any]:
    """
        Decide qué camino seguirá el grafo.
        Por ahora todas las consultas van al RAG.
    """

    return {"route": "rag"}


def router(state: AgentState) -> str:
    """
        Devuelve el nombre del siguiente nodo.
    """
    
    direction = state["route"]

    if not isinstance(direction, str):
        return "unknown"
    
    return direction