from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_digest = db.Column(db.String, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    recipes = db.relationship('Recipe', back_populates='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')
    bookmarks = db.relationship('Bookmark', back_populates='user', cascade='all, delete-orphan')

    bookmarked_recipes = association_proxy('bookmarks', 'recipe')

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "recipes": [r.to_dict_basic() for r in self.recipes],
            "comments": [c.to_dict_basic() for c in self.comments],
            "bookmarked_recipes": [r.id for r in self.bookmarked_recipes] 
        }

    def to_dict_basic(self):
        return {
            "id": self.id,
            "username": self.username
        }

    @validates('email')
    def validate_email(self, key, value):
        if '@' not in value or '.' not in value:
            raise ValueError("Invalid email format.")
        return value

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plain_text_password):
        self.password_digest = generate_password_hash(plain_text_password)

    def authenticate(self, plain_text_password):
        return check_password_hash(self.password_digest, plain_text_password)


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    cook_time = db.Column(db.Integer)
    image_url = db.Column(db.String, nullable=True)
    average_rating = db.Column(db.Float, default=0.0)


    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='recipes')
    comments = db.relationship('Comment', back_populates='recipe', cascade='all, delete-orphan')
    bookmarks = db.relationship('Bookmark', back_populates='recipe', cascade='all, delete-orphan')

    bookmarked_by_users = association_proxy('bookmarks', 'user')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "cook_time": self.cook_time,
            "image_url": self.image_url,
            "average_rating": self.average_rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user": self.user.to_dict_basic(), 
            "comments": [comment.to_dict() for comment in self.comments]
        }

    def to_dict_basic(self):
        return {
            "id": self.id,
            "title": self.title,
            "average_rating": self.average_rating
        }


    @validates('title', 'ingredients', 'instructions')
    def validate_not_empty(self, key, value):
        if not value or not value.strip():
            raise ValueError(f"{key.capitalize()} cannot be empty.")
        return value

    @validates('cook_time')
    def validate_cook_time(self, key, value):
        if value is not None and (not isinstance(value, int) or value < 0):
            raise ValueError("Cook time must be a non-negative integer.")
        return value


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    recipe = db.relationship('Recipe', back_populates='comments')

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user": self.user.to_dict_basic(),
            "recipe_id": self.recipe_id
        }

    def to_dict_basic(self):
        return {
            "id": self.id,
            "content": self.content,
            "rating": self.rating
        }

    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value.strip()) < 3:
            raise ValueError("Comment content must be at least 3 characters.")
        return value

    @validates("rating")
    def validate_rating(self, key, value):
        if value is not None:
            if not (1 <= value <= 5):
                raise ValueError("Rating must be between 1 and 5.")
        return value



class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.Text)


    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

    user = db.relationship('User', back_populates='bookmarks')
    recipe = db.relationship('Recipe', back_populates='bookmarks')

    def to_dict(self):
        return {
            "id": self.id,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user_id": self.user_id,
            "recipe_id": self.recipe_id,
            "recipe": {
                "id": self.recipe.id,
                "title": self.recipe.title,
                "image_url": self.recipe.image_url,
            }
        }
    
    def to_dict_basic(self):
        return {
            "id": self.id,
            "recipe_id": self.recipe_id
        }


    @validates('notes')
    def validate_notes(self, key, value):
        if value and len(value.strip()) < 2:
            raise ValueError("If provided, notes must be at least 2 characters.")
        return value
