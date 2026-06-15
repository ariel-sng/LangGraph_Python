from langgraph.graph import StateGraph, START, END

from src.config.settings import Settings

from src.Agent.state import AgentState
from src.Agent.orchestrator import orchestrator, router
from src.Agent.rag_agent import rag_retriever

print(Settings.OPENAI_API_KEY)

graph_builder = StateGraph(AgentState)

graph_builder.add_node("orchestrator", orchestrator)
graph_builder.add_node("rag_retriever", rag_retriever)
graph_builder.add_edge(START, "orchestrator")

graph_builder.add_conditional_edges(
    "orchestrator",
    router,
    {
        "rag": "rag_retriever",
    },
)

graph_builder.add_edge("rag_retriever", END)

graph = graph_builder.compile()

while True:
    query = input("Pregunta ('salir' para terminar): ")

    if query.lower() == "salir":
        break

    result = graph.invoke(
        {
            "question": query,
            "route": "",
            "context": [],
            "answer": "",
        }
    )

    print(result)