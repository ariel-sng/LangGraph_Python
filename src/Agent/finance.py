from typing import Any

from src.RAG.retrieve import retrieve_chunks
from src.models.state import AgentState

def finance_node(state: AgentState) -> dict[str, Any]:

    results = retrieve_chunks(
                    query =  state["question"],
                    source = "Finance"
                )

    return {"context": results}