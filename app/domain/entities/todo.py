from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Todo:
    """
    Todo 도메인 엔티티

    비즈니스 로직과 규칙을 포함하는 순수한 도메인 객체입니다.
    외부 프레임워크나 라이브러리에 의존하지 않습니다.
    """
    title: str
    user_id: int
    priority: int = 3
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """비즈니스 규칙 검증"""
        self.validate()

    def validate(self):
        """도메인 규칙 검증"""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")

        if len(self.title) > 255:
            raise ValueError("Title cannot exceed 255 characters")

        if self.priority < 1 or self.priority > 5:
            raise ValueError("Priority must be between 1 and 5")

        if self.user_id <= 0:
            raise ValueError("User ID must be positive")

    def update_title(self, new_title: str):
        """제목 업데이트"""
        if not new_title or not new_title.strip():
            raise ValueError("Title cannot be empty")

        if len(new_title) > 255:
            raise ValueError("Title cannot exceed 255 characters")

        self.title = new_title

    def update_priority(self, new_priority: int):
        """우선순위 업데이트"""
        if new_priority < 1 or new_priority > 5:
            raise ValueError("Priority must be between 1 and 5")

        self.priority = new_priority

    def is_owned_by(self, user_id: int) -> bool:
        """특정 사용자의 소유인지 확인"""
        return self.user_id == user_id
