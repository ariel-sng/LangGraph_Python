from langgraph.graph import StateGraph, START, END

from src.models.state import AgentState
from src.Agent import NODES_RAG, NODES, orchestrator_node, router, answer_node


# Diagrama de formato del grafo:
#
#
#                               +--->   [HR]  -----+
#                               |                  |
#                               |                  |
#                               +--->[Finance]-----+
#                               |                  |
#                               |                  |
#[START] ---> [ORQUESTADOR] ----+--->  [Tech] -----+---> [answer] ---+
#                               |                  |                 |
#                               |                  |                 |
#                               +---> [Legal] -----+                 |
#                               |                                    |
#                               |                                    v
#                               +--->[unknown]-------------------> [END]
                               
#
# Todos los nodos de NODES se conectan a "answer" después de procesar,
# excepto "unknown" que va directo a END.

def build_graph():
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("orchestrator", orchestrator_node)
    graph_builder.add_node("answer", answer_node)

    for node_name, node_fn in NODES.items():  # Con esto agrego todos los nodos directamente del diccionario >:)
        graph_builder.add_node(node_name, node_fn)


    graph_builder.add_edge(START, "orchestrator")
    graph_builder.add_conditional_edges(
    "orchestrator",
        router,
        { name: name for name in NODES } # acá también puedo iterar
    )

    for node_name, _ in NODES_RAG.items():  # Todos menos el unknown van a answer, unknown va directo al final
        graph_builder.add_edge(node_name, "answer")

    graph_builder.add_edge("answer", END)
    graph_builder.add_edge("unknown", END)
    return graph_builder