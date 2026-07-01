from typing import cast

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.states.state import AgentState
from src.states.evaluator_result import EvaluationResult
from src.config.settings import Settings
from src.states.route_enum import Route


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Sos un evaluador de sistemas RAG.

            Tu tarea es evaluar qué tan bien la respuesta final utiliza el contexto recuperado para responder la consulta.

            El sistema posee los siguientes dominios de conocimiento: {domain}

            Funcionamiento del sistema:
            1. Un orquestador clasifica la consulta en uno de esos dominios o en "unknown".
            2. Si la ruta es un dominio válido, se recupera contexto desde un RAG y se genera una respuesta utilizando dicho contexto.
            3. Si la ruta es "unknown", NO se realiza recuperación de contexto y se devuelve directamente una respuesta indicando que la consulta no pertenece a ninguno de los dominios soportados.

            Importante:
            - Si la ruta es "unknown", NO penalices la ausencia de contexto.
            - Si la ruta es "unknown", evaluá únicamente si la respuesta rechaza correctamente la consulta o informa adecuadamente que está fuera del alcance del sistema.
            - Si la ruta pertenece a un dominio válido ({domain}), sí debés evaluar la calidad del uso del contexto recuperado.

            Criterios:
            - Relevancia del contexto para la pregunta.
            - Uso efectivo del contexto en la respuesta.
            - Fidelidad al contexto (sin inventar información).
            - Cobertura de la consulta.

            Asigná un puntaje de 1 a 10:
            - 1: respuesta incorrecta o desconectada del contexto.
            - 5: respuesta parcialmente correcta o incompleta.
            - 10: respuesta correcta, completa y basada claramente en el contexto.

            Respondé utilizando el formato estructurado solicitado.
            """,
        ),
        (
            "human",
            """
            Pregunta:
            {question}

            Contexto recuperado:
            {context}

            Respuesta:
            {answer}
            """,
        ),
    ]
)

llm = ChatOpenAI(
    model=Settings.OPENAI_HIGH_MODEL,
    temperature=0,
    max_completion_tokens=Settings.MAX_PROMPT_TOKENS
)

chain = prompt | llm.with_structured_output(EvaluationResult)


def evaluate(state: AgentState) -> EvaluationResult:
    context = "\n\n".join(
        chunk["text"]
        for chunk in state["context"]
    )

    domains = ", ".join(
        route.value
        for route in Route
        if route != Route.UNKNOWN
    )

    result = cast(
        EvaluationResult,
        chain.invoke(
            {
                "domain": domains,
                "question": state["question"],
                "context": context,
                "answer": state["answer"],
            }
        ),
    )

    return result