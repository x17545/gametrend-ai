from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )


class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    answer: str