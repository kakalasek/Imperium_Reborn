from flask import render_template
from . import home_bp

@home_bp.route('/')
@home_bp.route('/home')
def home_route():
    return render_template('home.html')