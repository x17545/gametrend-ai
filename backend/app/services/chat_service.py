from openai import OpenAI

from app.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
)
from app.services.data_service import get_data_summary


client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)


def generate_chat_response(message: str) -> str:
    summary = get_data_summary()

    system_prompt = f"""
당신은 Steam 게임 플레이어 데이터를 분석하는 AI 도우미입니다.

현재 저장된 데이터 요약:
- 데이터 개수: {summary["count"]}
- 기간: {summary["start_date"]} ~ {summary["end_date"]}
- 평균 플레이어 수: {summary["average"]}
- 최대 플레이어 수: {summary["max"]}
- 최소 플레이어 수: {summary["min"]}
- 최근 플레이어 수: {summary["latest"]}
- 최근 7일 평균 플레이어 수: {summary["recent_7d_average"]}
- 이전 7일 평균 플레이어 수: {summary["previous_7d_average"]}
- 최근 7일 변화율: {summary["trend_change_percent"]}%
- 현재 추세: {summary["trend"]}

반드시 위 저장된 데이터를 근거로 답변하세요.
데이터에 없는 내용은 추측하지 마세요.
사용자에게 한국어로 간결하고 이해하기 쉽게 답변하세요.
"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        max_completion_tokens=4000,
    )

    return response.choices[0].message.content or ""