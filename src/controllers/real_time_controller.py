from flask import Blueprint, jsonify
from services.real_time_service import fetch_do_cost_data

bp = Blueprint('real_time', __name__, url_prefix='/api/real_time')

@bp.route('/costs')
def get_costs():
    cost_data = fetch_do_cost_data()
    return jsonify(cost_data.to_dict(orient='records'))
