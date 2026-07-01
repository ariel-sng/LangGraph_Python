from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.models.image_state import ContractAnalysisState

CONTEXTUALIZATION_PROMPT = """
Sos un asistente especializado en el análisis de documentos legales.

Vas a recibir un documento (contrato o enmienda).

Tu tarea es generar un mapa estructurado del documento.

Para cada sección:
- Identificá el número o identificador de la sección (si existe).
- Indicá el título de la sección (si existe).
- Describí brevemente el propósito general de esa sección.
- Conservá el orden original del documento.

No resumas el contrato completo.
No identifiques cambios.
No devuelvas JSON.

Respondé únicamente con un texto estructurado que represente la organización del documento.
""".strip()

contextualization_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            CONTEXTUALIZATION_PROMPT,
        ),
        (
            "human",
            """<DOCUMENT> 
            {document} 
            </DOCUMENT>""".strip(),
        ),
    ]
)


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

contextualization_chain = contextualization_prompt | llm


def contextualization_agent(document):
    '''Recibe un contrato/enmienda y devuelve un mapa estructural del documento'''
    response = contextualization_chain.invoke(
        {
            "document": document,
        }
    )
    return response.content


def contextualization_node(state: ContractAnalysisState) -> dict:
    contract_context = contextualization_agent(state["contract_text"])
    amendment_context = contextualization_agent(state["amendment_text"])

    return {
        "contract_context": contract_context,
        "amendment_context": amendment_context,
    }