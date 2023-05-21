from flask import jsonify, request
from models.user import User
from models.auth import Auth
from utils.functions import hash_password, check_password, create_token
import uuid
from controllers import login_required
from schemas.user import register_login_schema
from schemas import validate_json


@validate_json(register_login_schema)
def register():
    try:
        body = request.get_json()
        username = body.get('username')
        password = body.get('password')
        password = hash_password(password)  # Hash the password

        User(username=username, password=password).save()
        return jsonify({'message': 'User successfully created.'}), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500


@validate_json(register_login_schema)
def login():
    try:
        body = request.get_json()
        username = body.get('username')
        password = body.get('password')

        user = User.objects.get(username=username) # Get user from database

        if not check_password(password, user.password): # Check if password is correct
            return jsonify({'error': 'Invalid credentials'}), 401

        if not user.is_active: # Check if user is active
            return jsonify({'error': 'User is not active'}), 401

        session_key = uuid.uuid4().hex
        access_token = create_token(user_id=str(user.id), session_key=session_key, role=user.role.value)

        Auth(user=user, session_key=session_key).save() # Save the token to the database

        return jsonify({'message': 'Logged in successfully', 'access_token': access_token, 'user_id': str(user.id)}), 200

    except User.DoesNotExist: # If user does not exist
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500


@login_required(['admin'])
def activate_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return jsonify({'message': 'User activated successfully'})
    except User.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@login_required(['admin'])
def deactivate_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return jsonify({'message': 'User deactivated successfully'})
    except User.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
