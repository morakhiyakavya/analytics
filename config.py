import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    """Base config class with shared settings."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')  # Default secret

    # Default to disable logging, can be set to True for logging enabled
    ENABLE_LOGGING = False

class DevelopmentConfig(Config):
    """Development-specific config."""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:123@localhost:5432/flask_analytics_dev")
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production-specific config."""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:123@localhost:5432/flask_analytics_prod")
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 10  # Adjust the connection pool size for production
    SQLALCHEMY_MAX_OVERFLOW = 20  # Max overflow for DB connections in production
