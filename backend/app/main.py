from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS
from app.routers import chat, conversations, data
from app.services.firebase_service import db

app = FastAPI(
    title="GameTrend AI API",
    description="Steam 플레이어 추세 분석 및 AI 채팅 API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(data.router)
app.include_router(conversations.router)


@app.get("/")
def root():
    return {
        "message": "GameTrend AI API is running",
        "status": "ok",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/firebase-test")
def firebase_test():
    try:
        doc_ref = db.collection("test").document("connection")
        doc_ref.set({
            "message": "Firebase connection successful"
        })

        result = doc_ref.get()

        return {
            "status": "success",
            "data": result.to_dict(),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }