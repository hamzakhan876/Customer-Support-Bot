
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The customer's message",
    )


class ChatResponse(BaseModel):
    intent: str
    answer: str
    source: str | None
    resolved: bool
