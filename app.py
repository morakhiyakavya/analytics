from flask import Flask, request
from models.analytics import db, log_request
from routes.main import main_bp
from config import Config
import time

app = Flask(__name__)
app.config.from_object(Config)

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
