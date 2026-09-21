from datetime import datetime, timezone

from app.services.firebase_service import db


COLLECTION_NAME = "conversations"


def create_conversation(data):
    doc_ref = db.collection(COLLECTION_NAME).document()

    payload = {
        "title": data.title,
        "messages": [
            message.model_dump()
            for message in data.messages
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    doc_ref.set(payload)

    return {
        "id": doc_ref.id,
        **payload,
    }


def get_all_conversations():
    docs = db.collection(COLLECTION_NAME).stream()

    result = []

    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        result.append(item)

    result.sort(
        key=lambda item: item.get("created_at", ""),
        reverse=True,
    )

    return result


def get_conversation(conversation_id):
    doc_ref = db.collection(COLLECTION_NAME).document(conversation_id)
    snapshot = doc_ref.get()

    if not snapshot.exists:
        return None

    item = snapshot.to_dict()
    item["id"] = snapshot.id

    return item


def delete_conversation(conversation_id):
    doc_ref = db.collection(COLLECTION_NAME).document(conversation_id)
    snapshot = doc_ref.get()

    if not snapshot.exists:
        return False

    doc_ref.delete()

    return True