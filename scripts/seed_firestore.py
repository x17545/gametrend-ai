import csv
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore


BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = (
    BASE_DIR
    / "data"
    / "steam_players.csv"
)

SERVICE_ACCOUNT_PATH = (
    BASE_DIR
    / "backend"
    / "firebase-service-account.json"
)

COLLECTION_NAME = "data"


if not firebase_admin._apps:
    cred = credentials.Certificate(
        SERVICE_ACCOUNT_PATH
    )

    firebase_admin.initialize_app(cred)


db = firestore.client()


def clear_data_collection():
    docs = db.collection(
        COLLECTION_NAME
    ).stream()

    count = 0

    for doc in docs:
        doc.reference.delete()
        count += 1

    print(
        f"기존 데이터 {count}개 삭제 완료"
    )


def seed_data():
    count = 0

    with open(
        CSV_PATH,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            date = row["date"]

            payload = {
                "date": date,
                "value": float(row["value"]),
                "memo": row["memo"],
            }

            db.collection(
                COLLECTION_NAME
            ).document(date).set(payload)

            count += 1

    print(
        f"PUBG 데이터 {count}개 저장 완료"
    )


if __name__ == "__main__":
    clear_data_collection()
    seed_data()