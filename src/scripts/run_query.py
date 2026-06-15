from langfuse.langchain import CallbackHandler
from src.utils.graph_builder import build_graph


langfuse_handler = CallbackHandler()


graph_builder = build_graph()
graph = graph_builder.compile()



while True:
    query = input("Pregunta ('exit' para terminar): ")

    if query.lower() == "exit":
        break

    result = graph.invoke(
        {
            "question": query,
            "route": "",
            "routing_reason": "",
            "context": [],
            "answer": "",
        }, 
        config={
            "callbacks": [langfuse_handler]
        }
    )
    print("="*100)
    print("Respuesta del grafo: ")
    print(result["answer"])
    print("="*100)