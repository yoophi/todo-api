from app.application.dtos import CreateTodoDTO, TodoDTO
from app.domain.entities import Todo
from app.domain.repositories import TodoRepository


class CreateTodoUseCase:
    """Todo 생성 유즈케이스"""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self, dto: CreateTodoDTO) -> TodoDTO:
        """
        Todo를 생성합니다.

        Args:
            dto: Todo 생성 데이터

        Returns:
            생성된 Todo DTO

        Raises:
            ValueError: 검증 실패 시
        """
        # 도메인 엔티티 생성 (비즈니스 규칙 검증 포함)
        todo = Todo(
            title=dto.title,
            user_id=dto.user_id,
            priority=dto.priority
        )

        # 저장
        saved_todo = self.todo_repository.save(todo)

        # DTO로 변환하여 반환
        return TodoDTO.from_entity(saved_todo)
