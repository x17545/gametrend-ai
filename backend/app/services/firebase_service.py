import json
import os

import firebase_admin
from firebase_admin import credentials, firestore

from app.config import FIREBASE_SERVICE_ACCOUNT_PATH


def initialize_firebase():
    if firebase_admin._apps:
        return

    firebase_json = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_JSON"
    )

    if firebase_json:
        # Render 등 배포 환경
        service_account_info = json.loads(
            firebase_json
        )

        cred = credentials.Certificate(
            service_account_info
        )

    else:
        # 로컬 개발 환경
        cred = credentials.Certificate(
            FIREBASE_SERVICE_ACCOUNT_PATH
        )

    firebase_admin.initialize_app(cred)


initialize_firebase()

db = firestore.client()