from flask import Blueprint
from controllers.category import get_all_category, create_category, update_category, delete_category

category_bp = Blueprint('category', __name__)

category_bp.route('/', methods=['GET'])(get_all_category)
category_bp.route('/', methods=['POST'])(create_category)
category_bp.route('/<category_id>', methods=['PUT'])(update_category)
category_bp.route('/<category_id>', methods=['DELETE'])(delete_category)
