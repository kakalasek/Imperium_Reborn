from flask import Blueprint

password_cracker_bp = Blueprint('password_cracker_bp', __name__, template_folder='templates')

from . import routes