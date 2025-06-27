from flask_restful import Resource, reqparse
from server.models import User, db
from server.routes.auth_helpers import require_auth
from sqlalchemy.exc import IntegrityError

class UsersResource(Resource):
    @require_auth
    def get(self, user):
        users = User.query.all()
        user_list = [{
            "id": u.id,
            "username": u.username,
            "email": u.email
        } for u in users]
        return user_list, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='Username is required')
        parser.add_argument('email', required=True, help='Email is required')
        parser.add_argument('password', required=True, help='Password is required')
        args = parser.parse_args()

        # Check uniqueness
        if User.query.filter_by(username=args['username']).first():
            return {"error": "Username already taken."}, 400
        if User.query.filter_by(email=args['email']).first():
            return {"error": "Email already registered."}, 400

        user = User(username=args['username'], email=args['email'])
        user.password = args['password']  # use password setter

        try:
            db.session.add(user)
            db.session.commit()
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }, 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "User creation failed."}, 500


class UserResource(Resource):
    @require_auth
    def put(self, user_id, user):
        if user.id != user_id:
            return {"error": "Forbidden – you can only update your own account."}, 403

        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('password')
        args = parser.parse_args()

        if args['username']:
            user.username = args['username']
        if args['email']:
            user.email = args['email']
        if args['password']:
            user.password = args['password']

        try:
            db.session.commit()
            return {"message": "User updated successfully."}, 200
        except IntegrityError:
            db.session.rollback()
            return {"error": "Username or email may already be taken."}, 400

    @require_auth
    def delete(self, user_id, user):
        if user.id != user_id:
            return {"error": "Forbidden – you can only delete your own account."}, 403

        db.session.delete(user)
        db.session.commit()
        return {"message": "User account deleted successfully."}, 200
