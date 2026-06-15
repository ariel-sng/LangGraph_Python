from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.models.state import AgentState
from src.models.route_decision import RouteDecision
from src.models.route_enum import Route

from src.config.settings import Settings

llm = ChatOpenAI(
    model                   = Settings.OPENAI_LOW_MODEL, 
    temperature             = 0,
    ).with_structured_output(RouteDecision)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Sos un orquestador de un sistema multiagente de una empresa."
            "Vas a recibir una consulta del usuario y tenés que seleccionar uno de los siguientes agentes: {agents}."
            "Reglas:"
            '''- Elegí una ruta únicamente si la consulta pertenece claramente a un único dominio.
            - Si la consulta combina dos o más dominios (por ejemplo HR y Legal, o Finance y Tech), devolvé 'unknown'.
            - Si la consulta es ambigua y podría pertenecer a más de un dominio, devolvé 'unknown'.
            - Si la consulta no corresponde a ninguno de los dominios disponibles, devolvé 'unknown'.
            - No intentes dividir la consulta ni resolverla parcialmente.'''
            "Además, proporcioná una breve explicación de la decisión tomada, no más de 30 palabras"
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