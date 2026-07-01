from src.states.state import AgentState

def unknown_node(state: AgentState):
    print(f"Consulta rechazada: {state['routing_reason']}")
    return { "answer": state['routing_reason']}