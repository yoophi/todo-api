from flask import Flask

from app.commands import init_command
from app.infrastructure.config import config
from app.infrastructure.database import db
from app.infrastructure.extensions import cors, ma, migrate


def create_app(config_name="default", settings_override=None):
    """
    Flask 애플리케이션 팩토리

    헥사고날 아키텍처 구조로 재구성된 애플리케이션입니다.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    if settings_override:
        app.config.update(settings_override)

    init_extensions(app)
    init_blueprints(app)
    init_command(app)

    return app


def init_blueprints(app):
    """Blueprint 등록"""
    from app.views import main as main_bp
    from app.adapters.inbound.api import api as api_bp
    from app.swagger import swagger_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(swagger_bp, url_prefix="/swagger")


def init_extensions(app):
    """Flask 확장 초기화"""
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    ma.init_app(app)
