"""
Backward compatibility wrapper for models.

기존 코드와의 호환성을 위해 유지됩니다.
새로운 코드에서는 app.adapters.outbound.persistence.models를 사용하세요.
"""
from app.adapters.outbound.persistence.models import TodoModel as Todo  # noqa

__all__ = ['Todo']
