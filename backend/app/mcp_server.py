from mcp.server import MCPServer

from app.services.data_service import get_data_summary
from app.services.conversation_service import get_all_conversations


mcp = MCPServer("GameTrend AI")


@mcp.tool()
def get_player_data_summary():
    """저장된 PUBG 플레이어 데이터의 요약 통계를 조회합니다."""
    return get_data_summary()


@mcp.tool()
def get_saved_conversations():
    """저장된 AI 대화 기록 목록을 최신순으로 조회합니다."""
    return get_all_conversations()


if __name__ == "__main__":
    mcp.run()