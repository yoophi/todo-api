from typing import List

from app.application.dtos import TodoDTO
from app.domain.repositories import TodoRepository


class ListTodosUseCase:
    """Todo 목록 조회 유즈케이스"""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self) -> List[TodoDTO]:
        """
        모든 Todo를 조회합니다.

        Returns:
            Todo DTO 목록
        """
        todos = self.todo_repository.find_all()
        return [TodoDTO.from_entity(todo) for todo in todos]
