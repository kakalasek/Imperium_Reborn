from src import create_app

flask_app, db = create_app()
celery_app = flask_app.extensions["celery"]