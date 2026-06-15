from .rag_agent import rag_retriever_node
from .unknown import unknown_node
from .legal import legal_node
from .tech import tech_node
from .finance import finance_node
from .hr import hr_node
from .orchestrator import orchestrator_node, router

NODES = {
    "unknown": unknown_node,
    "legal": legal_node,
    "tech": tech_node,
    "finance": finance_node,
    "hr": hr_node,
}

__all__ = [
    "rag_retriever_node",
    "unknown_node",
    "legal_node",
    "tech_node",
    "finance_node",
    "hr_node",
    "orchestrator_node",
    "router",
    "NODES",
]

