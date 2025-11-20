"""
Backward compatibility wrapper for exceptions.

기존 코드와의 호환성을 위해 유지됩니다.
새로운 코드에서는 app.domain.exceptions를 사용하세요.
"""
from app.domain.exceptions import *  # noqa
