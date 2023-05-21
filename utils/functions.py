import bcrypt
import jwt
from datetime import timedelta
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def hash_password(password):
    # Convert the password to a byte array
    password = bytes(password, 'utf-8')

    # Generate a salt
    salt = bcrypt.gensalt()

    # Create a hash
    hashed_password = bcrypt.hashpw(password, salt)

    # Convert the byte array to a string and return
    return hashed_password.decode('utf-8')


def check_password(password, hashed_password):
    # Taking user entered password and hashed password and encoding them
    user_bytes = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    # checking password
    return bcrypt.checkpw(user_bytes, hashed_password)


def create_token(user_id, session_key, role):
    """
    Create JWT token
    """
    token_type = "access"
    # Access token expires in 30 minutes
    expire_time = datetime.utcnow() + timedelta(minutes=30)

    # Create the payload
    payload = {
        "user_id": user_id,
        "type": token_type,
        "exp": expire_time,
        "iat": datetime.utcnow(),
        "session_key": session_key,
        "role": role,
    }
    secret_key = os.getenv("MY_SECRET")
    # Create the token
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token


def decode_token(token) -> dict:
    """
    Decode the JWT token and return the payload
    """
    try:
        secret_key = os.getenv("MY_SECRET")
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        # The token has expired
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        # The token is invalid
        raise ValueError("Token is invalid")

    # Check if the token contains the required fields
    required_fields = ["user_id", "type", "exp", "iat", "session_key", "role"]
    if any(field not in payload for field in required_fields):
        raise ValueError("Token is missing required fields")

    # Get the user_id, token_type, expiration and creation times from the payload
    user_id = payload["user_id"]
    token_type = payload["type"]
    exp_time = datetime.utcfromtimestamp(payload["exp"])
    iat_time = datetime.utcfromtimestamp(payload["iat"])
    session_key = payload["session_key"]
    role = payload["role"]

    # Create the token_info dictionary
    token_info = {
        "user_id": user_id,
        "type": token_type,
        "exp_time": exp_time,
        "iat_time": iat_time,
        "session_key": session_key,
        "role": role
    }

    return token_info
