import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Database configuration (PostgreSQL by default, fallback to SQLite)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://recipe_share_db_hl0b_user:9NVj74FofhRxSCckqpdkzKgdFVRdX1CN@dpg-d1ha0u6mcj7s73dldft0-a.oregon-postgres.render.com/recipe_share_db_hl0b'  
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret keys
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET = os.environ.get('JWT_SECRET', 'dev-jwt-secret')
    JWT_PASSWORD_RESET_SECRET = os.environ.get('JWT_PASSWORD_RESET_SECRET', 'dev-password-reset-secret')

    # Token expiration (in seconds)
    JWT_EXPIRATION_SECONDS = int(os.environ.get('JWT_EXPIRATION_SECONDS', 3600))  # 1 hour
    JWT_REFRESH_EXPIRATION_SECONDS = int(os.environ.get('JWT_REFRESH_EXPIRATION_SECONDS', 604800))  # 7 days
    JWT_PASSWORD_RESET_EXPIRATION_SECONDS = int(os.environ.get('JWT_PASSWORD_RESET_EXPIRATION_SECONDS', 900))  # 15 minutes

    # Secure cookie flag (True if running in production)
    SECURE_COOKIE = os.environ.get("FLASK_ENV", "").lower() == "production"

    # Debug flag (optional)
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    # Frontend URL for password reset
    RESET_FRONTEND_URL = os.environ.get('RESET_FRONTEND_URL', 'http://127.0.0.1:5173/reset-password')
