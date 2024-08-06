from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard/cost-tracking/')
def cost_tracking():
    return render_template('cost_tracking_dashboard.html')

@bp.route('/dashboard/cost-saving/')
def cost_saving():
    return render_template('cost_saving_dashboard.html')
