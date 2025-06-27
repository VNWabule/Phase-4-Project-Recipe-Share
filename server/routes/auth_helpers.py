import jwt
from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from functools import wraps
from server.models import User


def generate_token(user_id, expires_in_seconds):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in_seconds)
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')


def generate_access_token(user_id):
    return generate_token(
        user_id,
        current_app.config.get('JWT_ACCESS_EXPIRATION', 3600)
    )


def generate_refresh_token(user_id):
    expires = current_app.config.get('JWT_REFRESH_EXPIRATION_SECONDS', 604800)
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires)
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')

def generate_password_reset_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }
    return jwt.encode(payload, current_app.config['JWT_PASSWORD_RESET_SECRET'], algorithm='HS256')


def verify_password_reset_token(token):
    try:
        payload = jwt.decode(token, current_app.config['JWT_PASSWORD_RESET_SECRET'], algorithms=['HS256'])
        return payload['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        return payload['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


verify_token = decode_token 


def verify_refresh_token(token):
    return decode_token(token)


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Authorization token required"}, 401  # ✅ Plain dict, not jsonify

        token = auth_header.split(" ")[1]
        user_id = verify_token(token)

        if not user_id:
            return {"error": "Invalid or expired token"}, 401  # ✅

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404  # ✅

        return f(*args, user=user, **kwargs)

    return decorated


def send_reset_email(email, token):
    reset_link = f"{current_app.config['RESET_FRONTEND_URL']}?token={token}"
    print(f"[MOCK EMAIL] Reset link sent to {email}: {reset_link}")

