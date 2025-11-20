from flask import Blueprint

api = Blueprint('api', __name__)

from . import todos  # noqa: E402, F401
