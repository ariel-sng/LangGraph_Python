from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config.settings import Settings
from src.states.image_state import ContractAnalysisState
from src.models.contract_change_output import ContractChangeOutput

from src.observability.langfuse import langfuse 
from src.utils.llm_chain import invoke_chain_with_error_handling


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

"sections_changed": ["..."],
"topics_touched": ["..."],
"summary_of_the_change": "..."

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
    timeout=Settings.OPENAI_API_TIMEOUT,
    max_completion_tokens=Settings.MAX_PROMPT_TOKENS,
).with_structured_output(ContractChangeOutput)


extraction_chain = extraction_prompt | structured_llm


def extraction_node(state: ContractAnalysisState) -> dict:
    with langfuse.start_as_current_observation(
        as_type="span",
        name="extraction_agent",
    ) as span:

        response = invoke_chain_with_error_handling(
            extraction_chain,
            {
                "contract": state["contract_text"],
                "contract_context": state["contract_context"],
                "amendment": state["amendment_text"],
                "amendment_context": state["amendment_context"],
            },
            error_context="extraction_chain",
        )

        model_dump_fn = getattr(response, "model_dump", None)
        output_data = model_dump_fn() if callable(model_dump_fn) else response 
        # por algún motivo, se rompía al aplicar 'response.model_dump()', no sé porque esto funciona

        span.update(
            input=state,
            output=output_data,
        )

    return {
        "validated_output": response,
    }
