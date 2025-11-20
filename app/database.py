"""
Backward compatibility wrapper for database module.

기존 코드와의 호환성을 위해 유지됩니다.
새로운 코드에서는 app.infrastructure.database를 직접 사용하세요.
"""
from app.infrastructure.database import *  # noqa
