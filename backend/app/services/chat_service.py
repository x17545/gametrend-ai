import json

from openai import OpenAI

from app.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
)
from app.tools.definitions import DATA_TOOLS
from app.tools.executor import execute_tool
from app.services.data_service import get_data_summary


client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)


def generate_chat_response(message: str) -> str:
    # 요약 API와 같은 서비스 함수를 재사용하여 요청마다 최신 통계를 조회합니다.
    summary = get_data_summary()
    system_prompt = """
당신은 Steam 게임 플레이어 데이터를 분석하는 AI 도우미입니다.

사용자가 저장된 PUBG 플레이어 데이터의
개수, 기간, 평균, 최대, 최소, 최근 값,
최근 7일 평균, 이전 7일 평균, 변화율,
현재 추세 등에 대해 질문하면
아래 시스템 프롬프트에 포함된 데이터 요약을 먼저 참고하세요.
요약을 다시 조회할 필요가 있으면 get_data_summary 도구를 사용하세요.

사용자가 저장된 대화 기록, 최근 대화 제목,
이전 대화 내용 등에 대해 질문하면
get_conversations 도구를 사용해 저장된 대화 목록을 조회하세요.

제공된 데이터 요약과 도구에서 받은 데이터를 근거로만 답변하세요.
요약의 count가 0이면 저장된 데이터가 없다고 안내하세요.
null인 통계는 계산할 수 없는 값이며 0으로 해석하지 마세요.
데이터에 없는 내용은 추측하지 마세요.
사용자에게 한국어로 간결하고 이해하기 쉽게 답변하세요.
"""
    system_prompt += "\n현재 저장된 PUBG 플레이어 데이터 요약(JSON):\n"
    system_prompt += json.dumps(summary, ensure_ascii=False)

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": message,
        },
    ]

    first_response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        tools=DATA_TOOLS,
        tool_choice="auto",
        max_completion_tokens=4000,
    )

    assistant_message = first_response.choices[0].message

    # GPT가 도구를 호출하지 않은 경우 바로 답변 반환
    if not assistant_message.tool_calls:
        return assistant_message.content or ""

    # GPT가 요청한 tool call 정보를 대화에 추가
    messages.append(
        {
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in assistant_message.tool_calls
            ],
        }
    )

    # 요청된 도구 실행
    for tool_call in assistant_message.tool_calls:
        print(f"[TOOL CALL] {tool_call.function.name}")

        tool_result = execute_tool(
            tool_call.function.name
        )

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    tool_result,
                    ensure_ascii=False,
                ),
            }
        )

    # 도구 실행 결과를 받은 뒤 GPT가 최종 답변 생성
    final_response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        max_completion_tokens=4000,
    )

    return (
        final_response.choices[0].message.content
        or ""
    )
