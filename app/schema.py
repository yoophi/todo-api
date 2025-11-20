"""
Backward compatibility wrapper for schemas.

기존 코드와의 호환성을 위해 유지됩니다.
새로운 코드에서는 app.adapters.inbound.api.schemas를 사용하세요.
"""
from app.adapters.inbound.api.schemas import TodoSchema  # noqa
from app.swagger import swagger_definition  # noqa

# Swagger 정의를 위해 TodoSchema에 데코레이터 적용
TodoSchema = swagger_definition(TodoSchema)

__all__ = ['TodoSchema']
