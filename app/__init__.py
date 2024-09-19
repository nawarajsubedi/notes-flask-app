from flask import Flask

from app.config import Config
from app.routes import main_bp
from app.extensions import db, migrate
from app.models import User, Note


def create_app(config_class=Config):
    """
    Flask Application Factory to create and configure the app instance.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    return app


def register_blueprints(app: Flask):
    """
    Register all blueprints with the Flask application instance.
    """
    app.register_blueprint(main_bp, url_prefix="/api/v1")
