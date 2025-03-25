from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from config import Config
from models.analytics import log_request
from routes.analysis import main_bp
from routes.auth import auth_bp
from flask_migrate import Migrate
migrate = Migrate()

from dotenv import load_dotenv
import time
import os


def create_app(config_class=Config):
    """Factory function to create a Flask app instance."""
    app = Flask(__name__)
    load_dotenv()
    
    # Load configuration based on environment
    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        print('development')
        app.config.from_object('config.DevelopmentConfig')

    # Initialize the database
    db.init_app(app)

    # Set up migrations (optional but useful)
    Migrate(app, db)

    # Register blueprints (routes)
    app.register_blueprint(main_bp)
    
    # Only use if you have login functionality
    if os.getenv("ENABLE_AUTH").lower() == "true":
        print('auth')
        app.register_blueprint(auth_bp)
    else:
        print('no auth')

    # Other setup, such as middlewares or error handling, can go here
    # log request middleware
    @app.before_request
    def before_request():
        request.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        new_req_wait_time = time.time() + 10
        return log_request(response)
    
    return app
