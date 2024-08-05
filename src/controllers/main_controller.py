from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/cost-tracking')
def real_time_dashboard():
    return render_template('real_time_dashboard.html')
