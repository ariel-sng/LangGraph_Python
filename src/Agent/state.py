from typing import Any, TypedDict, Optional

class AgentState(TypedDict):
    question: str
    route: Optional[str]
    context: list[dict[str, Any]]
    answer: Optional[str]