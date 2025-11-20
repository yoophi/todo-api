from app.application.dtos import TodoDTO
from app.domain.exceptions import TodoNotFoundException
from app.domain.repositories import TodoRepository


class GetTodoUseCase:
    """Todo 조회 유즈케이스"""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self, todo_id: int) -> TodoDTO:
        """
        ID로 Todo를 조회합니다.

        Args:
            todo_id: Todo ID

        Returns:
            Todo DTO

        Raises:
            TodoNotFoundException: Todo를 찾을 수 없을 때
        """
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundException(todo_id)

        return TodoDTO.from_entity(todo)
