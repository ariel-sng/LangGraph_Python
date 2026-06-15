from typing import cast

from langfuse.langchain import CallbackHandler
from src.models.state import AgentState
from src.utils.graph_builder import build_graph
from src.Agent import evaluate

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

    
    print("========================")
    print("COMIENZO DE LA RESPUESTA")
    print("========================\n")

    print(result["answer"])
    
    print("\n========================")
    print("   FIN DE LA RESPUESTA  ")
    print("========================")
    print("-"*100)
    print("========================")
    print("COMIENZO DE LA EVALUACIÓN")
    print("========================\n")

    state = cast(
        AgentState,
        result
    )

    evaluation = evaluate(state)
    print(f"Razonamiento del evaluador: {evaluate(state).reasoning}\n")
    print(f"Score: {evaluate(state).score}/10")


    print("\n========================")
    print("  FIN DE LA EVALUACIÓN")
    print("========================\n")