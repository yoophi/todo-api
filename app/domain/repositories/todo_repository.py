from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities import Todo


class TodoRepository(ABC):
    """
    Todo Repository 인터페이스 (Port)

    도메인 계층에서 정의하는 추상 인터페이스로,
    구체적인 구현은 어댑터 계층에서 이루어집니다.
    """

    @abstractmethod
    def find_all(self) -> List[Todo]:
        """모든 Todo 조회"""
        pass

    @abstractmethod
    def find_by_id(self, todo_id: int) -> Optional[Todo]:
        """ID로 Todo 조회"""
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Todo]:
        """사용자 ID로 Todo 목록 조회"""
        pass

    @abstractmethod
    def save(self, todo: Todo) -> Todo:
        """Todo 저장 (생성 또는 업데이트)"""
        pass

    @abstractmethod
    def delete(self, todo_id: int) -> bool:
        """Todo 삭제"""
        pass

    @abstractmethod
    def exists(self, todo_id: int) -> bool:
        """Todo 존재 여부 확인"""
        pass
