import base64
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from src.observability.langfuse import langfuse 
from src.states.image_state import ContractAnalysisState

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

VISION_PROMPT = """
Sos un asistente especializado en la transcripción de documentos legales.

Tu tarea es extraer el texto completo del contrato contenido en la imagen de la forma más fiel posible.

Instrucciones:
- Transcribí el contenido exactamente como aparece en el documento.
- Conservá la numeración de las secciones, los títulos, los párrafos, las listas y la estructura del documento siempre que sea posible.
- No resumas, interpretes ni reformules el contenido.
- No corrijas errores ortográficos o gramaticales presentes en el documento.
- Si alguna palabra o fragmento es ilegible, reemplazalo con [UNREADABLE].
- Devolvé únicamente el texto extraído, sin comentarios, explicaciones ni formato adicional.
""".strip()

def _extract_text_from_image(image_path):
    
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": VISION_PROMPT,
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_b64}"
                },
            },
        ]
    )

    response = llm.invoke([message])
    return response.content


def parse_contract_images_node( state: ContractAnalysisState ) -> dict:
    """
    Lee el contrato original y la enmienda y devuelve el texto interpretado por GPT-4o Vision.
    """

    # Riquísimo como generar spans ensució tanto el código, gracias langfuse :D

    #### CONTRATO ####
    with langfuse.start_as_current_observation(
        as_type="span",
        name="parse_original_contract",
    ) as span_contract:
        
        contract_text = _extract_text_from_image(state["contract_image_path"])
        
        # Registro path de la imagen y el largo del texto transcripto del contrato
        register_parser(state["contract_image_path"], span_contract, contract_text)


    #### ENMIENDA ####
    with langfuse.start_as_current_observation(
        as_type="span",
        name="parse_amendment_contract",
    ) as span_amendment:
        
        amendment_text = _extract_text_from_image(state["amendment_image_path"])
        
        # Registro path de la imagen y el largo del texto transcripto de la enmienda
        register_parser(state["amendment_image_path"], span_amendment, amendment_text)

    return {
        "contract_text": contract_text,
        "amendment_text": amendment_text,
    }

def register_parser(path, span_contract, contract_text):
    span_contract.update(
            input={
                "image_path": path,
            },
            output={
                "characters_extracted": len(contract_text),
            }
        )