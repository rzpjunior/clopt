from flask import Blueprint, jsonify
from services.do_service import fetch_do_cost_data

bp = Blueprint('do', __name__, url_prefix='/api/do')

@bp.route('/costs')
def get_costs():
    cost_data = fetch_do_cost_data()
    return jsonify(cost_data.to_dict(orient='records'))
