from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard/cost_tracking')
def cost_tracking_dashboard():
    return render_template('cost_tracking_dashboard.html')
