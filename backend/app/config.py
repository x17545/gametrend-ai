import os

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv(
    "OPENAI_BASE_URL",
    "https://copa.codyssey.kr/v1",
)
OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5-mini",
)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://127.0.0.1:5500,http://localhost:5500",
).split(",")

FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv(
    "FIREBASE_SERVICE_ACCOUNT_PATH",
    "firebase-service-account.json",
)