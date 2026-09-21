from statistics import mean

from app.services.firebase_service import db


COLLECTION_NAME = "data"


def create_data(data):
    doc_ref = db.collection(COLLECTION_NAME).document()

    payload = {
        "date": data.date.isoformat(),
        "value": data.value,
        "memo": data.memo,
    }

    doc_ref.set(payload)

    return {
        "id": doc_ref.id,
        **payload,
    }


def get_all_data():
    docs = db.collection(COLLECTION_NAME).stream()

    result = []

    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        result.append(item)

    result.sort(key=lambda item: item["date"])

    return result


def update_data(data_id, data):
    doc_ref = db.collection(COLLECTION_NAME).document(data_id)

    snapshot = doc_ref.get()

    if not snapshot.exists:
        return None

    payload = {
        "date": data.date.isoformat(),
        "value": data.value,
        "memo": data.memo,
    }

    doc_ref.set(payload)

    return {
        "id": data_id,
        **payload,
    }


def delete_data(data_id):
    doc_ref = db.collection(COLLECTION_NAME).document(data_id)

    snapshot = doc_ref.get()

    if not snapshot.exists:
        return False

    doc_ref.delete()

    return True


def get_data_summary():
    data_list = get_all_data()

    if not data_list:
        return {
            "count": 0,
            "start_date": None,
            "end_date": None,
            "average": None,
            "max": None,
            "min": None,
            "latest": None,
            "recent_7d_average": None,
            "previous_7d_average": None,
            "trend_change_percent": None,
            "trend": "no_data",
        }

    values = [
        float(item["value"])
        for item in data_list
    ]

    latest_value = values[-1]

    # 최근 14개 이상 데이터가 있을 때
    if len(values) >= 14:
        previous_7_days = values[-14:-7]
        recent_7_days = values[-7:]

        previous_7d_average = mean(previous_7_days)
        recent_7d_average = mean(recent_7_days)

        if previous_7d_average != 0:
            trend_change_percent = (
                (
                    recent_7d_average
                    - previous_7d_average
                )
                / previous_7d_average
            ) * 100
        else:
            trend_change_percent = 0

        # ±1% 이내는 유지로 판단
        if trend_change_percent > 1:
            trend = "increasing"
        elif trend_change_percent < -1:
            trend = "decreasing"
        else:
            trend = "stable"

    else:
        # 데이터가 14개 미만이면 첫 값과 마지막 값 비교
        previous_7d_average = None
        recent_7d_average = None
        trend_change_percent = None

        if latest_value > values[0]:
            trend = "increasing"
        elif latest_value < values[0]:
            trend = "decreasing"
        else:
            trend = "stable"

    return {
        "count": len(data_list),
        "start_date": data_list[0]["date"],
        "end_date": data_list[-1]["date"],
        "average": round(mean(values), 2),
        "max": max(values),
        "min": min(values),
        "latest": latest_value,

        "recent_7d_average": (
            round(recent_7d_average, 2)
            if recent_7d_average is not None
            else None
        ),

        "previous_7d_average": (
            round(previous_7d_average, 2)
            if previous_7d_average is not None
            else None
        ),

        "trend_change_percent": (
            round(trend_change_percent, 2)
            if trend_change_percent is not None
            else None
        ),

        "trend": trend,
    }