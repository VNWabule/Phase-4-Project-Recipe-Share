from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from server.models import Comment, db
from server.routes.auth_helpers import require_auth

class CommentsResource(Resource):
    def get(self, comment_id=None):
        if comment_id:
            comment = Comment.query.get(comment_id)
            if comment:
                return comment.to_dict(), 200
            return {"error": "Comment not found"}, 404

        comments = Comment.query.all()
        return [c.to_dict() for c in comments], 200

    @require_auth
    def post(self, user):
        data = request.get_json()
        try:
            if not all(k in data for k in ("content", "recipe_id")):
                raise KeyError("Missing one or more required fields.")

            new_comment = Comment(
                content=data["content"],
                user_id=user.id,
                recipe_id=data["recipe_id"]
            )
            db.session.add(new_comment)
            db.session.commit()

            return new_comment.to_dict(), 201

        except KeyError as e:
            return {"error": str(e)}, 400
        except ValueError as e:
            return {"error": f"Validation error: {str(e)}"}, 422
        except IntegrityError:
            db.session.rollback()
            return {"error": "Foreign key error or duplicate comment."}, 409
        except Exception as e:
            db.session.rollback()
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @require_auth
    def put(self, comment_id, user):
        comment = Comment.query.get(comment_id)
        if not comment:
            return {"error": "Comment not found"}, 404
        if comment.user_id != user.id:
            return {"error": "Forbidden — not your comment"}, 403

        data = request.get_json()
        try:
            if "content" in data:
                comment.content = data["content"]
            if "rating" in data:
                comment.rating = data["rating"]

            db.session.commit()
            return comment.to_dict(), 200

        except ValueError as e:
            db.session.rollback()
            return {"error": f"Validation error: {str(e)}"}, 422
        except Exception as e:
            db.session.rollback()
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @require_auth
    def delete(self, comment_id, user):
        comment = Comment.query.get(comment_id)
        if not comment:
            return {"error": "Comment not found"}, 404
        if comment.user_id != user.id:
            return {"error": "Forbidden — not your comment"}, 403

        db.session.delete(comment)
        db.session.commit()
        return {"message": "Comment deleted"}, 200
    
class RecipeCommentsResource(Resource):
    def get(self, recipe_id):
        comments = Comment.query.filter_by(recipe_id=recipe_id).all()
        return [c.to_dict() for c in comments], 200

