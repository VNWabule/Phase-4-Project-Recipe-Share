from flask_restful import Resource, reqparse
from flask import request, jsonify
from server.models import Recipe, db
from sqlalchemy.exc import IntegrityError
from server.routes.auth_helpers import require_auth

class RecipesResource(Resource):
    def get(self, recipe_id=None):
        if recipe_id:
            recipe = Recipe.query.get(recipe_id)
            if not recipe:
                return {"error": "Recipe not found"}, 404
            return recipe.to_dict(), 200

        recipes = Recipe.query.all()
        return [r.to_dict() for r in recipes], 200

    @require_auth
    def post(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, help="Title is required")
        parser.add_argument('ingredients', required=True, help="Ingredients are required")
        parser.add_argument('instructions', required=True, help="Instructions are required")
        parser.add_argument('cook_time', type=int)
        args = parser.parse_args()

        try:
            recipe = Recipe(
                title=args['title'],
                ingredients=args['ingredients'],
                instructions=args['instructions'],
                cook_time=args['cook_time'],
                user_id=user.id
            )
            db.session.add(recipe)
            db.session.commit()
            return recipe.to_dict(), 201

        except IntegrityError:
            db.session.rollback()
            return {"error": "Invalid data or duplicate entry"}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @require_auth
    def put(self, recipe_id, user):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return {"error": "Recipe not found"}, 404
        if recipe.user_id != user.id:
            return {"error": "Forbidden — not your recipe"}, 403

        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('ingredients')
        parser.add_argument('instructions')
        parser.add_argument('cook_time', type=int)
        args = parser.parse_args()

        try:
            if args['title'] is not None:
                recipe.title = args['title']
            if args['ingredients'] is not None:
                recipe.ingredients = args['ingredients']
            if args['instructions'] is not None:
                recipe.instructions = args['instructions']
            if args['cook_time'] is not None:
                if args['cook_time'] < 0:
                    return {"error": "Cook time must be non-negative"}, 400
                recipe.cook_time = args['cook_time']

            db.session.commit()
            return recipe.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @require_auth
    def delete(self, recipe_id, user):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return {"error": "Recipe not found"}, 404
        if recipe.user_id != user.id:
            return {"error": "Forbidden — not your recipe"}, 403

        db.session.delete(recipe)
        db.session.commit()
        return {"message": "Recipe deleted successfully"}, 200
