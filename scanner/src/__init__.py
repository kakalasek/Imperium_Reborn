from flask import Flask
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        CELERY=dict(
            broker_url="redis://redis",
            result_backend="redis://redis",
            task_ignore_results=True
        )
    )

    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import db
    db.init_app(app)

    from .main.tasks import add_scan

    from .celery import celery_init_app
    celery_init_app(app)

    from .main import main_bp
    app.register_blueprint(main_bp)

    return (app, db)