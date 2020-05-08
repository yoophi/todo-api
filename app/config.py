import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEFAULT_SECRET_KEY = \
    "yaimaumoej8Tee3fooCh9Mah3xohGh3ooK2eid4ibieGheef1chai1Beengeib8S"

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_USER = os.environ.get('DB_USER', 'user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_DATABASE = os.environ.get('DB_DATABASE', 'todos')

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/"
    f"{DB_DATABASE}"
)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or DEFAULT_SECRET_KEY
    JSONIFY_PRETTYPRINT_REGULAR = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("DEV_DATABASE_URL") or SQLALCHEMY_DATABASE_URI


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("TEST_DATABASE_URL") or "sqlite://"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("DATABASE_URL") or SQLALCHEMY_DATABASE_URI

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler

        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.INFO)
        app.logger.addHandler(syslog_handler)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "docker": DockerConfig,
    "unix": UnixConfig,
    "default": DevelopmentConfig,
}
