from flask import Blueprint, jsonify
from services.cost_tracking_service import fetch_do_cost_data

bp = Blueprint('cost_tracking', __name__, url_prefix='/api/cost_tracking')

@bp.route('/costs')
def get_costs():
    cost_data = fetch_do_cost_data()
    return jsonify(cost_data.to_dict(orient='records'))
