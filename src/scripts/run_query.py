from langgraph.graph import StateGraph, START, END

from src.config.settings import Settings
from src.models.state import AgentState

from src.Agent import NODES, orchestrator_node, router

###          BUILD GRAPH         ###
graph_builder = StateGraph(AgentState)

graph_builder.add_node("orchestrator", orchestrator_node)
for node_name, node_fn in NODES.items():  # Con esto agrego todos los nodos directamente del diccionario >:)
    graph_builder.add_node(node_name, node_fn)


graph_builder.add_edge(START, "orchestrator")
graph_builder.add_conditional_edges(
    "orchestrator",
    router,
    { name: name for name in NODES } # acá también puedo iterar
)

for node_name, _ in NODES.items():  # Y todos terminan igual
    graph_builder.add_edge(node_name, END)

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
    print("="*60)
    print(result)
    print("="*60)