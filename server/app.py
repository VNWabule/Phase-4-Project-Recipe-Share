from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api

from .models import db
from .config import Config

from server.routes.users import UsersResource, UserResource
from server.routes.recipes import RecipesResource
from server.routes.comments import CommentsResource, RecipeCommentsResource
from server.routes.bookmarks import BookmarksResource
from server.routes.auth import (
    RegisterResource, LoginResource, LogoutResource, CheckSessionResource,
    RefreshTokenResource, RequestPasswordResetResource, ResetPasswordResource
)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
CORS(app, supports_credentials=True)
api = Api(app)

api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(RecipesResource, '/recipes')
api.add_resource(RecipeCommentsResource, '/recipes/<int:recipe_id>/comments')
api.add_resource(CommentsResource, '/comments', '/comments/<int:comment_id>')
api.add_resource(BookmarksResource, '/bookmarks', '/bookmarks/<int:bookmark_id>')
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(CheckSessionResource, '/check_session')
api.add_resource(RefreshTokenResource, '/refresh')
api.add_resource(RequestPasswordResetResource, '/request_password_reset')
api.add_resource(ResetPasswordResource, '/reset_password')

@app.route('/')
def home():
    return {'message': 'RecipeShare API is running!'}

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=5555)
