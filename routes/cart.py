from flask import Blueprint
from controllers.cart import add_to_cart, remove_from_cart, get_products_in_cart

cart_bp = Blueprint('cart', __name__)


cart_bp.route('/add', methods=['POST'])(add_to_cart)
cart_bp.route('/remove', methods=['POST'])(remove_from_cart)
cart_bp.route('/<user_id>', methods=['GET'])(get_products_in_cart)

