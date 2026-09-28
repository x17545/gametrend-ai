DATA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_data_summary",
            "description": (
                "저장된 PUBG 플레이어 데이터의 요약 정보를 조회합니다. "
                "데이터 개수, 기간, 평균, 최대, 최소, 최근 값, "
                "최근 7일 평균, 이전 7일 평균, 변화율, 현재 추세를 반환합니다."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_conversations",
            "description": (
                "저장된 AI 대화 기록 목록을 최신순으로 조회합니다. "
                "최근 대화 제목이나 저장된 대화 내용을 확인할 때 사용합니다."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    },
]