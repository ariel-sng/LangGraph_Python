from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.states.image_state import ContractAnalysisState
from src.models.contract_change_output import ContractChangeOutput


EXTRACTOR_PROMPT = """
    Sos un asistente especializado en el análisis comparativo de documentos legales.

    Vas a recibir:
    - El contrato original.
    - La enmienda.
    - Un mapa estructurado de ambos documentos.

    Tu tarea consiste exclusivamente en identificar todos los cambios introducidos por la enmienda.

    Para cada diferencia, determiná si corresponde a:
    - Una adición.
    - Una eliminación.
    - Una modificación.

    Utilizá el mapa estructurado únicamente como contexto para comprender qué secciones se corresponden entre sí.

    Respondé únicamente con un objeto JSON que contenga exactamente los siguientes campos:

    {
    "sections_changed": [
        "..."
    ],
    "topics_touched": [
        "..."
    ],
    "summary_of_the_change": "..."
    }

    No agregues texto antes ni después del JSON.
    """.strip()

extraction_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            EXTRACTOR_PROMPT,
        ),
        (
            "human",
            """
            ## Contrato original

            {contract}

            ---

            ## Estructura del contrato

            {contract_context}

            ---

            ## Enmienda

            {amendment}

            ---

            ## Estructura de la enmienda

            {amendment_context}
            """.strip(),
        ),
    ]
)


structured_llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
).with_structured_output(ContractChangeOutput)


extraction_chain = extraction_prompt | structured_llm


def extraction_node(state: ContractAnalysisState) -> dict :
    response = extraction_chain.invoke(
        {
            "contract": state["contract_text"],
            "contract_context": state["contract_context"],
            "amendment": state["amendment_text"],
            "amendment_context": state["amendment_context"],
        }
    )

    return {
        "validated_output": response,
    }