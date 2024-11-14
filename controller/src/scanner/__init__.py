from flask import Blueprint

scanner_bp = Blueprint('scanner_bp', __name__, template_folder='templates')

from . import routes