from pydantic import BaseModel

class RouteDecision(BaseModel):
    route: str
    routing_reason: str