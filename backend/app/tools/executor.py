from app.services.data_service import get_data_summary
from app.services.conversation_service import get_all_conversations


def execute_tool(tool_name: str):
    if tool_name == "get_data_summary":
        return get_data_summary()

    if tool_name == "get_conversations":
        return get_all_conversations()

    raise ValueError(f"지원하지 않는 도구입니다: {tool_name}")