from langchain_core.tools import tool
from src.Agent.state import AgentState


def orchestrator(state: AgentState):
    """
    Decide qué camino seguirá el grafo.
    Por ahora todas las consultas van al RAG.
    """

    state["route"] = "rag"
    return state


def router(state):
    """
    Devuelve el nombre del siguiente nodo.
    """
    return state["route"]