from typing import Literal

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=5000)


class ConversationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    messages: list[ConversationMessage]