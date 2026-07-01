from .unknown import unknown_node
from .legal import legal_node
from .tech import tech_node
from .finance import finance_node
from .hr import hr_node
from .orchestrator import orchestrator_node, router
from .answer import answer_node
from .evaluator import evaluate
from .image.parser_image import parse_contract_images_node
from .image.contextualizer import contextualization_node
from .image.extractor import extraction_node

NODES_RAG = {
    "legal": legal_node,
    "tech": tech_node,
    "finance": finance_node,
    "hr": hr_node,
}

NODES_IMG = {
    "parser_img": parse_contract_images_node,
    "contextualizer": contextualization_node,
    "extractor": extraction_node
}

NODES = {
    **NODES_RAG,
    "unknown": unknown_node
}

__all__ = [
    "unknown_node",
    "legal_node",
    "tech_node",
    "finance_node",
    "hr_node",
    "orchestrator_node",
    "router",
    "NODES_RAG",
]


