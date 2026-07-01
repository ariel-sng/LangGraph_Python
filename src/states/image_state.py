from typing import TypedDict, Any

class ContractAnalysisState(TypedDict):
    # Entradas
    contract_image_path: str
    amendment_image_path: str

    # Parsing
    contract_text: str
    amendment_text: str

    # Contextualización
    contract_context: str
    amendment_context: str

    # Extracción de cambios
    extraction_result: dict[str, Any]