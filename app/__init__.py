from flask import Flask

from app.commands import init_command
from app.config import config
from app.database import db
from app.extensions import cors, ma, migrate


def create_app(config_name="default", settings_override=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    if settings_override:
        app.config.update(settings_override)

    init_extensions(app)
    init_blueprint(app)
    init_command(app)

    return app


def init_blueprint(app):
    from app.views import main as main_bp
    from app.api import api as api_bp
    from app.swagger import swagger_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(swagger_bp, url_prefix="/swagger")


def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/*": {"origins": "*"}, })
    ma.init_app(app)
