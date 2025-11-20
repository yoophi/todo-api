class DomainException(Exception):
    """도메인 계층 기본 예외"""
    pass


class TodoNotFoundException(DomainException):
    """Todo를 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, todo_id: int):
        self.todo_id = todo_id
        super().__init__(f"Todo with id {todo_id} not found")


class PermissionDeniedException(DomainException):
    """권한이 없을 때 발생하는 예외"""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)


class ValidationException(DomainException):
    """검증 실패 시 발생하는 예외"""
    def __init__(self, message: str):
        super().__init__(message)
