from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.models.state import AgentState
from src.models.route_enum import Route

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Sos un asistente que responde preguntas utilizando únicamente el contexto proporcionado."
            "Recibís la información de un RAG."
            "Los posibles RAGs pueden ser de los siguientes dominios: {agents}."
            "Tu consulta fue provista por el dominio '{domain}'"
            "Si el contexto no contiene información suficiente para responder, indicá claramente que no encontraste información relevante."
            "No inventes información.",
        ),
        (
            "human",
            "<Query>{question}</Query>"
            "<Context>{context}</Context>",
        ),
    ]
)

chain = prompt | llm

def answer_node(state: AgentState) -> dict[str, Any]:
    
    context = _get_context(state)
    print("-"*80)
    print(f"Contexto: {context}")
    print("-"*80)

    agents = ", ".join(
        route.value
        for route in Route
        if route != Route.UNKNOWN
    )

    result = chain.invoke(
        {
            "agents": agents,
            "domain": state["route"],
            "question": state["question"],
            "context": context,
        }
    )

    return {
        "answer": result.content,
    }

def _get_context(state: AgentState):
    return "\n\n".join(
        chunk["text"]
        for chunk in state["context"]
    )