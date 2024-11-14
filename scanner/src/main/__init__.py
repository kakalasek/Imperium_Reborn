from flask import Blueprint

main_bp = Blueprint('scanner_bp', __name__)

from . import routes