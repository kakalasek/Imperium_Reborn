from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    return app