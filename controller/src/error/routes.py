from flask import render_template
from . import error_bp

@error_bp.app_errorhandler(404)
def not_found(e):
    """
    This is a special error handler for the 404 error
    """
    return render_template('err.html', message='Page Not Found'), 404