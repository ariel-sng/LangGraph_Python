from typing import TypedDict, Any

from src.models.contract_change_output import ContractChangeOutput

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
    validated_output: ContractChangeOutput | None