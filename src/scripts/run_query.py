from langgraph.graph import StateGraph, START, END

from src.config.settings import Settings
from src.models.state import AgentState

from src.Agent import NODES_RAG, orchestrator_node, router, answer_node

###          BUILD GRAPH         ###
graph_builder = StateGraph(AgentState)

graph_builder.add_node("orchestrator", orchestrator_node)
graph_builder.add_node("answer", answer_node)

for node_name, node_fn in NODES_RAG.items():  # Con esto agrego todos los nodos directamente del diccionario >:)
    graph_builder.add_node(node_name, node_fn)


graph_builder.add_edge(START, "orchestrator")
graph_builder.add_conditional_edges(
    "orchestrator",
    router,
    { name: name for name in NODES_RAG } # acá también puedo iterar
)

for node_name, _ in NODES_RAG.items():  # Y todos terminan igual
    graph_builder.add_edge(node_name, "answer")

graph_builder.add_edge("answer", END)

graph = graph_builder.compile()

while True:
    query = input("Pregunta ('salir' para terminar): ")

    if query.lower() == "salir":
        break

    result = graph.invoke(
        {
            "question": query,
            "route": "",
            "routing_reason": "",
            "context": [],
            "answer": "",
        }
    )
    print("="*100)
    print("Respuesta del grafo")
    print(result["answer"])
    print("="*100)