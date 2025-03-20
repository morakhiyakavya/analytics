import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base config class with shared settings."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')  # Ensure to set a strong secret
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')  # Set environment (dev/prod) explicitly
    
class DevelopmentConfig(Config):
    """Development-specific config."""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:123@localhost:5432/flask_analytics_dev"  # Default dev DB URI
    )
    SQLALCHEMY_ECHO = False  # Optional: log SQL queries in development
    
class ProductionConfig(Config):
    """Production-specific config."""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:123@localhost:5432/flask_analytics_prod")
    
    SQLALCHEMY_ECHO = False  # Don't log SQL queries in production
    SQLALCHEMY_POOL_SIZE = 10  # Adjust the connection pool size for production
    SQLALCHEMY_MAX_OVERFLOW = 20  # Max overflow for DB connections in production
