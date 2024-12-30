"""
Copyright (C) 2025 Josef Vetrovsky

This file is part of Imperium.

Imperium is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Imperium is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Imperium. If not, see <https://www.gnu.org/licenses/>. 
"""

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