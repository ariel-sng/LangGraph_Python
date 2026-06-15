from typing import Any

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.Agent.state import AgentState

llm = ChatOpenAI(model="gpt-4o", temperature=0)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Sos un router de un sistema multiagente."
            "Respondé únicamente con una de estas opciones: rag.",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)

def orchestrator(state: AgentState) -> dict[str, Any]:
    """
        Decide qué camino seguirá el grafo.
        Por ahora todas las consultas van al RAG.
    """
    chain = prompt | llm

    result = chain.invoke({"question": state["question"]})

    return {"route": result.content}


def router(state: AgentState) -> str:
    """
        Devuelve el nombre del siguiente nodo.
    """
    
    direction = state["route"]

    if not isinstance(direction, str):
        return "unknown"
    
    return direction