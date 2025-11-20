from app.domain.exceptions import PermissionDeniedException, TodoNotFoundException
from app.domain.repositories import TodoRepository


class DeleteTodoUseCase:
    """Todo 삭제 유즈케이스"""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self, todo_id: int, user_id: int) -> bool:
        """
        Todo를 삭제합니다.

        Args:
            todo_id: 삭제할 Todo ID
            user_id: 요청한 사용자 ID

        Returns:
            삭제 성공 여부

        Raises:
            TodoNotFoundException: Todo를 찾을 수 없을 때
            PermissionDeniedException: 권한이 없을 때
        """
        # Todo 조회
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundException(todo_id)

        # 권한 확인
        if not todo.is_owned_by(user_id):
            raise PermissionDeniedException("You don't have permission to delete this todo")

        # 삭제
        return self.todo_repository.delete(todo_id)
