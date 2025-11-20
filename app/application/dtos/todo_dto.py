from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CreateTodoDTO:
    """Todo 생성을 위한 DTO"""
    title: str
    user_id: int
    priority: int = 3


@dataclass
class TodoDTO:
    """Todo 데이터 전송 객체"""
    id: int
    title: str
    priority: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, todo):
        """도메인 엔티티를 DTO로 변환"""
        return cls(
            id=todo.id,
            title=todo.title,
            priority=todo.priority,
            user_id=todo.user_id,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )
