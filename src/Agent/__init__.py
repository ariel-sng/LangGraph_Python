from .unknown import unknown_node
from .legal import legal_node
from .tech import tech_node
from .finance import finance_node
from .hr import hr_node
from .orchestrator import orchestrator_node, router
from .answer import answer_node
from .evaluator import evaluate

NODES_RAG = {
    "legal": legal_node,
    "tech": tech_node,
    "finance": finance_node,
    "hr": hr_node,
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

