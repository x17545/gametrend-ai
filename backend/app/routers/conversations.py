from fastapi import APIRouter, HTTPException

from app.models.conversation import ConversationCreate
from app.services.conversation_service import (
    create_conversation,
    delete_conversation,
    get_all_conversations,
    get_conversation,
)


router = APIRouter(
    prefix="/api/conversations",
    tags=["Conversations"],
)


@router.post("")
def add_conversation(data: ConversationCreate):
    return create_conversation(data)


@router.get("")
def list_conversations():
    return get_all_conversations()


@router.get("/{conversation_id}")
def read_conversation(conversation_id: str):
    result = get_conversation(conversation_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return result


@router.delete("/{conversation_id}")
def remove_conversation(conversation_id: str):
    success = delete_conversation(conversation_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return {
        "message": "Conversation deleted successfully",
        "id": conversation_id,
    }