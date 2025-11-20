"""
Dependency Injection Container

헥사고날 아키텍처에서 의존성 주입을 관리하는 컨테이너입니다.
여기서 구체적인 구현체(어댑터)를 생성하고 주입합니다.
"""

from app.adapters.outbound.persistence import SQLAlchemyTodoRepository
from app.domain.repositories import TodoRepository

# 싱글톤 인스턴스
_todo_repository = None


def get_todo_repository() -> TodoRepository:
    """
    Todo Repository 인스턴스를 반환합니다.

    싱글톤 패턴으로 구현되어 있으며,
    애플리케이션 전체에서 하나의 인스턴스를 공유합니다.
    """
    global _todo_repository

    if _todo_repository is None:
        _todo_repository = SQLAlchemyTodoRepository()

    return _todo_repository


def reset_container():
    """
    컨테이너를 초기화합니다.
    주로 테스트 환경에서 사용됩니다.
    """
    global _todo_repository
    _todo_repository = None
