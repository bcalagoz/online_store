from flask import Blueprint
from controllers.user import register, login , activate_user, deactivate_user


auth_bp = Blueprint('auth', __name__)

auth_bp.route('/register', methods=["GET", "POST"])(register)
auth_bp.route('/login', methods=["GET", "POST"])(login)
auth_bp.route('/activate/<user_id>', methods=["PUT"])(activate_user)
auth_bp.route('/deactivate/<user_id>', methods=["PUT"])(deactivate_user)

