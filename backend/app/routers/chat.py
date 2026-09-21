from fastapi import APIRouter, HTTPException

from app.models.chat import ChatRequest
from app.services.chat_service import generate_chat_response
from app.services.conversation_service import create_conversation
from app.models.conversation import ConversationCreate


router = APIRouter(
    prefix="/api/chat",
    tags=["AI Chat"],
)


@router.post("")
def chat(request: ChatRequest):
    try:
        answer = generate_chat_response(request.message)

        conversation_data = ConversationCreate(
            title=request.message[:50],
            messages=[
                {
                    "role": "user",
                    "content": request.message,
                },
                {
                    "role": "assistant",
                    "content": answer,
                },
            ],
        )

        saved_conversation = create_conversation(
            conversation_data
        )

        return {
            "conversation_id": saved_conversation["id"],
            "message": request.message,
            "answer": answer,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI API 호출 실패: {str(e)}",
        )