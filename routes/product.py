from flask import Blueprint
from controllers.product import get_all_products, create_product, update_product, delete_product, filter_products_by_category

product_bp = Blueprint('product', __name__)

product_bp.route('/', methods=['GET'])(get_all_products)
product_bp.route('/filter', methods=['GET'])(filter_products_by_category)
product_bp.route('/', methods=['POST'])(create_product)
product_bp.route('/<product_id>', methods=['PUT'])(update_product)
product_bp.route('/<product_id>', methods=['DELETE'])(delete_product)
