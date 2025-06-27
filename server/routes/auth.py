from flask import request, make_response, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from server.models import User, db
from server.routes.auth_helpers import (
    generate_access_token,
    generate_refresh_token,
    verify_token,
    verify_refresh_token,
    generate_password_reset_token,
    verify_password_reset_token,
    send_reset_email
)
import os

SECURE_COOKIE = os.environ.get("FLASK_SECURE_COOKIE", "False").lower() == "true"


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return {"error": "All fields are required."}, 400

        user = User(username=username, email=email)
        user.password = password

        try:
            db.session.add(user)
            db.session.commit()

            access_token = generate_access_token(user.id)
            refresh_token = generate_refresh_token(user.id)

            response_data = {
                "message": "User registered successfully.",
                "token": access_token,
                "user": user.to_dict()
            }

            response = make_response(jsonify(response_data), 201)
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                samesite='Strict',
                secure=SECURE_COOKIE
            )

            return response

        except IntegrityError:
            db.session.rollback()
            return {"error": "Username or email already exists."}, 409


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            access_token = generate_access_token(user.id)
            refresh_token = generate_refresh_token(user.id)

            response_data = {
                "message": "Login successful.",
                "token": access_token,
                "user": user.to_dict()
            }

            response = make_response(jsonify(response_data), 200)
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                samesite='Strict',
                secure=SECURE_COOKIE
            )

            return response

        return {"error": "Invalid username or password."}, 401


class LogoutResource(Resource):
    def delete(self):
        response_data = {"message": "Logout successful."}
        response = make_response(jsonify(response_data), 200)
        response.set_cookie(
            "refresh_token",
            "",
            expires=0,
            httponly=True,
            samesite='Strict',
            secure=SECURE_COOKIE
        )
        return response


class CheckSessionResource(Resource):
    def get(self):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Authorization token required."}, 401

        token = auth_header.split(" ")[1]
        user_id = verify_token(token)

        if not user_id:
            return {"error": "Invalid or expired token."}, 401

        user = User.query.get(user_id)

        if user:
            return {"user": user.to_dict()}, 200
        return {"error": "User not found."}, 404


class RefreshTokenResource(Resource):
    def post(self):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            return {"error": "Refresh token missing."}, 401

        user_id = verify_refresh_token(refresh_token)

        if not user_id:
            return {"error": "Invalid or expired refresh token."}, 401

        new_access_token = generate_access_token(user_id)

        return {
            "access_token": new_access_token
        }, 200


class RequestPasswordResetResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")

        if not email:
            return {"error": "Email is required."}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found."}, 404

        reset_token = generate_password_reset_token(user.id)

        send_reset_email(user.email, reset_token)

        return {
            "message": "Password reset instructions sent to email (simulated)."
        }, 200


class ResetPasswordResource(Resource):
    def post(self):
        data = request.get_json()
        token = data.get("token")
        new_password = data.get("new_password")

        if not token or not new_password:
            return {"error": "Token and new password required."}, 400

        user_id = verify_password_reset_token(token)
        if not user_id:
            return {"error": "Invalid or expired token."}, 400

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found."}, 404

        user.password = new_password
        db.session.commit()

        return {"message": "Password reset successful."}, 200
