from typing import TypedDict

class ContractAnalysisState(TypedDict):
    contract_image_path: str
    amendment_image_path: str

    contract_text: str
    amendment_text: str

    contextual_map: str