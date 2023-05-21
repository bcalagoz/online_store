from functools import wraps
from flask import request, jsonify
from utils.functions import decode_token


def login_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify(message='Token is missing'), 401

            try:
                payload = decode_token(token)
                if payload['role'] not in roles:
                    return jsonify(message='Unauthorized'), 401

            except Exception as ex:
                return jsonify(message=f"{ex}"), 400

            return f(*args, **kwargs)

        return decorated_function
    return decorator



