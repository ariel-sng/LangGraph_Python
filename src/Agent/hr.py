from typing import Any

from src.RAG.retrieve import retrieve_chunks
from src.states.state import AgentState

def hr_node(state: AgentState) -> dict[str, Any]:

    results = retrieve_chunks(
                    query =  state["question"],
                    source = "HR"
                )

    return {"context": results}