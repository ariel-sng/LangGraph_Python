from typing import TypedDict, Optional


class AgentState(TypedDict):
    question: str
    route: Optional[str]
    context: Optional[str]
    answer: Optional[str]