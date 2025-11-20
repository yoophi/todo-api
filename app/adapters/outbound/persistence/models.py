from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.infrastructure.database import db


class TodoModel(db.Model):
    """
    Todo SQLAlchemy 모델

    데이터베이스 영속성을 위한 모델입니다.
    이는 어댑터 계층에 속하며, 도메인 엔티티와 분리되어 있습니다.
    """
    __tablename__ = 'tdods'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    priority = Column(Integer, default=3)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def to_entity(self):
        """SQLAlchemy 모델을 도메인 엔티티로 변환"""
        from app.domain.entities import Todo

        return Todo(
            id=self.id,
            title=self.title,
            priority=self.priority,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_entity(cls, todo):
        """도메인 엔티티를 SQLAlchemy 모델로 변환"""
        return cls(
            id=todo.id,
            title=todo.title,
            priority=todo.priority,
            user_id=todo.user_id,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )

    def update_from_entity(self, todo):
        """도메인 엔티티로부터 속성 업데이트"""
        self.title = todo.title
        self.priority = todo.priority
        self.user_id = todo.user_id
