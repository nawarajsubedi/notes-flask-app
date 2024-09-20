from flask import Flask
from flask_cors import CORS
from celery import Celery, Task
from app.config import Config
from app.extensions import db, migrate
from app.routes import main_bp


def create_app(config_class=Config):
    """
    Flask Application Factory to create and configure the app instance.
    """
    app = Flask(__name__)

    app.config.from_object(config_class)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=Config.REDIS_URL,
            result_backend=Config.REDIS_URL,
            task_ignore_result=True,
        ),
    )

    # Configure CORS
    CORS(app)

    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    register_blueprints(app)

    return app


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def register_blueprints(app: Flask):
    """
    Register all blueprints with the Flask application instance.
    """
    app.register_blueprint(main_bp, url_prefix="/api/v1")
