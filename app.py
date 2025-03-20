from flask import Flask, request
from models.analytics import db, log_request
from routes.main import main_bp
from config import DevelopmentConfig, ProductionConfig
from dotenv import load_dotenv
import time
import os


# Load environment variables
load_dotenv()

app = Flask(__name__)
# Use the appropriate config based on the environment
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Initialize the database
db.init_app(app)

# Register Blueprints (Routes)
app.register_blueprint(main_bp)

# Middleware to track request start time
@app.before_request
def start_timer():
    request.start_time = time.time()

# Middleware to log request analytics after each request
@app.after_request
def log_request_middleware(response):
    return log_request(response)

# Run the application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)
