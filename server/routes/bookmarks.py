from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from server.models import Bookmark, db
from server.routes.auth_helpers import require_auth

class BookmarksResource(Resource):
    def get(self, bookmark_id=None):
        if bookmark_id:
            bookmark = Bookmark.query.get(bookmark_id)
            if bookmark:
                return bookmark.to_dict(), 200
            return {"error": "Bookmark not found"}, 404

        bookmarks = Bookmark.query.all()
        return [b.to_dict() for b in bookmarks], 200

    @require_auth
    def post(self, user):
        data = request.get_json()
        try:
            if "recipe_id" not in data:
                raise KeyError("Missing required field: recipe_id")

            new_bookmark = Bookmark(
                notes=data.get("notes", ""),
                user_id=user.id,
                recipe_id=data["recipe_id"]
            )

            db.session.add(new_bookmark)
            db.session.commit()

            return new_bookmark.to_dict(), 201

        except KeyError as e:
            return {"error": str(e)}, 400
        except ValueError as e:
            db.session.rollback()
            return {"error": f"Validation error: {str(e)}"}, 422
        except IntegrityError:
            db.session.rollback()
            return {"error": "Invalid recipe_id or duplicate bookmark."}, 409
        except Exception as e:
            db.session.rollback()
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @require_auth
    def put(self, bookmark_id, user):
        bookmark = Bookmark.query.get(bookmark_id)
        if not bookmark:
            return {"error": "Bookmark not found"}, 404
        if bookmark.user_id != user.id:
            return {"error": "Forbidden — not your bookmark"}, 403

        data = request.get_json()
        try:
            if "notes" in data:
                bookmark.notes = data["notes"]

            db.session.commit()
            return bookmark.to_dict(), 200

        except ValueError as e:
            db.session.rollback()
            return {"error": f"Validation error: {str(e)}"}, 422
        except Exception as e:
            db.session.rollback()
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @require_auth
    def delete(self, bookmark_id, user):
        bookmark = Bookmark.query.get(bookmark_id)
        if not bookmark:
            return {"error": "Bookmark not found"}, 404
        if bookmark.user_id != user.id:
            return {"error": "Forbidden — not your bookmark"}, 403

        db.session.delete(bookmark)
        db.session.commit()
        return {"message": "Bookmark deleted"}, 200
