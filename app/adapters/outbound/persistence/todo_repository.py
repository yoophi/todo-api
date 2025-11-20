from typing import List, Optional

from app.domain.entities import Todo
from app.domain.repositories import TodoRepository
from app.infrastructure.database import db
from .models import TodoModel


class SQLAlchemyTodoRepository(TodoRepository):
    """
    SQLAlchemy를 사용한 Todo Repository 구현

    도메인 계층에서 정의한 TodoRepository 인터페이스를
    SQLAlchemy를 사용하여 구현합니다.
    """

    def find_all(self) -> List[Todo]:
        """모든 Todo 조회"""
        models = db.session.query(TodoModel).all()
        return [model.to_entity() for model in models]

    def find_by_id(self, todo_id: int) -> Optional[Todo]:
        """ID로 Todo 조회"""
        model = db.session.query(TodoModel).get(todo_id)
        return model.to_entity() if model else None

    def find_by_user_id(self, user_id: int) -> List[Todo]:
        """사용자 ID로 Todo 목록 조회"""
        models = db.session.query(TodoModel).filter_by(user_id=user_id).all()
        return [model.to_entity() for model in models]

    def save(self, todo: Todo) -> Todo:
        """Todo 저장 (생성 또는 업데이트)"""
        if todo.id is None:
            # 새로운 Todo 생성
            model = TodoModel.from_entity(todo)
            db.session.add(model)
        else:
            # 기존 Todo 업데이트
            model = db.session.query(TodoModel).get(todo.id)
            if model:
                model.update_from_entity(todo)
            else:
                # ID가 있지만 DB에 없는 경우 새로 생성
                model = TodoModel.from_entity(todo)
                db.session.add(model)

        db.session.commit()
        db.session.refresh(model)

        return model.to_entity()

    def delete(self, todo_id: int) -> bool:
        """Todo 삭제"""
        model = db.session.query(TodoModel).get(todo_id)
        if model:
            db.session.delete(model)
            db.session.commit()
            return True
        return False

    def exists(self, todo_id: int) -> bool:
        """Todo 존재 여부 확인"""
        return db.session.query(TodoModel).filter_by(id=todo_id).count() > 0
