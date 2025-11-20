"""
Backward compatibility wrapper for API.

기존 코드와의 호환성을 위해 유지됩니다.
새로운 코드에서는 app.adapters.inbound.api를 사용하세요.
"""
from app.adapters.inbound.api import api  # noqa

__all__ = ['api']
