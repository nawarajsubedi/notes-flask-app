from functools import wraps
from datetime import datetime, timedelta
from dateutil import parser
import pytz
import jwt

from flask import g, request, jsonify
from flask import current_app as app
from flask import jsonify

from app.config import Config
from app.models import User


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if " " in auth_header else None

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({"message": "Invalid or expired token!"}), 401

        decoded_data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_data["sub"]

        g.user = User.query.get(user_id)
        return f(*args, **kwargs)

    return decorated_function


def generate_jwt_token(user_id):
    """
    Generate a JWT token with user_id payload.
    """
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),  # Token expires in 1 hour
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")


def verify_jwt_token(token):
    """
    Verify JWT token and return the payload if valid.
    """
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def parse_datetime(datetime_str: str) -> datetime:
    """
    Parse a datetime string with timezone and return it in UTC.
    """
    # Parse the input string to a datetime object with timezone info
    local_datetime = parser.parse(datetime_str)

    # Convert to UTC and return the result
    utc_datetime = local_datetime.astimezone(pytz.UTC)

    return utc_datetime


def create_response(message, status_code, data=None, token=None):
    response = {
        "message": message,
    }

    if data is not None:
        response["data"] = data

    if token is not None:
        response["token"] = token

    return jsonify(response), status_code
