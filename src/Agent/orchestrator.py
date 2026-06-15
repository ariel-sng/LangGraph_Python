from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.models.state import AgentState
from src.models.route_decision import RouteDecision
from src.models.route_enum import Route

llm = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0
    ).with_structured_output(RouteDecision)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Sos un orquestador de un sistema multiagente de una empresa."
            "Vas a recibir una consulta del usuario y tenés que seleccionar uno de los siguientes agentes: {agents}."
            "En caso de que la consulta no cumpla ninguno de los temas, o directo no sea una consulta, devolvé unknown.",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)

###         ORQUESTADOR           ###
def orchestrator_node(state: AgentState) -> dict[str, Any]:
    """
        Decide qué camino seguirá el grafo.
    """
    chain = prompt | llm

    agents = ", ".join(
        route.value
        for route in Route
        if route != Route.UNKNOWN
    )

    result = chain.invoke(
            {
                "agents": agents,
                "question": state["question"]
            }
        )

    # Tengo que meter estos 'type: ignore' porque el IDE no infiere que el LLM retorna un 'RouteDecision'
    return {
        "route": result.route,  # type: ignore
        "routing_reason": result.routing_reason # type: ignore
        }

###         ROUTER           ###
def router(state: AgentState) -> str:
    """
        Devuelve el nombre del siguiente nodo.
    """
    routes = [r.value for r in Route]
    direction = state["route"]

    if direction is None or (direction not in routes):
        return "unknown"
    
    return direction