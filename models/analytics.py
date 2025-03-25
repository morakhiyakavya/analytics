# analytics_models.py
import json
import time
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask import request
from create_app import db

# 1. Analytics Table (Logs requests)
class Analytics(db.Model):
    __tablename__ = 'analytics'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(300))
    method = db.Column(db.String(10))
    endpoint = db.Column(db.String(255))
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.Float)
    request_headers = db.Column(db.Text)  # Store headers as JSON
    request_data = db.Column(db.Text)  # Store request payload as JSON
    referrer = db.Column(db.String(255))

    # Foreign key relationship to User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Allow null for unauthenticated users

    def __init__(self, ip_address, user_agent, method, endpoint, status_code, response_time, request_headers, request_data, referrer=None, user_id=None):
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.method = method
        self.endpoint = endpoint
        self.status_code = status_code
        self.response_time = response_time
        self.request_headers = json.dumps(request_headers)
        self.request_data = json.dumps(request_data)
        self.referrer = referrer
        self.user_id = user_id


# 2. Error Logs Table
class ErrorLog(db.Model):
    __tablename__ = 'error_logs'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    message = db.Column(db.Text)
    stack_trace = db.Column(db.Text)
    endpoint = db.Column(db.String(255))
    user_agent = db.Column(db.String(300))
    ip_address = db.Column(db.String(50))
    status_code = db.Column(db.Integer)
    method = db.Column(db.String(10))

    def __init__(self, message, stack_trace, endpoint, user_agent, ip_address, status_code, method):
        self.message = message
        self.stack_trace = stack_trace
        self.endpoint = endpoint
        self.user_agent = user_agent
        self.ip_address = ip_address
        self.status_code = status_code
        self.method = method


# 3. ApiRateLimit Table (Tracks rate limit failures)
class ApiRateLimit(db.Model):
    __tablename__ = 'api_rate_limits'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50))
    endpoint = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    attempts = db.Column(db.Integer, default=1)
    status = db.Column(db.String(50), default='failed')  # e.g., 'failed' or 'success'

    def __init__(self, ip_address, endpoint, attempts, status):
        self.ip_address = ip_address
        self.endpoint = endpoint
        self.attempts = attempts
        self.status = status

# 1. User Model (for authenticated users) also for one superadmin to be there
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    # Relationship to Analytics table (one-to-many)
    analytics = db.relationship('Analytics', backref='user', lazy=True)

    def __init__(self, username, email, password_hash=None, role='user'):
        self.username = username
        self.email = email
        self.role = role
        if password_hash:
            self.set_password(password_hash)

    def set_password(self, password: str):
        """Hash the password and set the hashed value"""
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hashed password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


# Analytics Logging Function (for batching requests)
batch_entries = []
TIME_BOMB_INTERVAL = 10  # 10 seconds
batch_start_time = None
BATCH_SIZE = 10  # Set a reasonable batch size

def log_request(response):
    global batch_start_time

    """Function to log each API request into the analytics table."""
    duration = round(time.time() - request.start_time, 4)

    try:
        # Create an Analytics entry
        analytics_entry = Analytics(
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent"),
            method=request.method,
            endpoint=request.path,
            status_code=response.status_code,
            response_time=duration,
            request_headers=dict(request.headers),
            request_data=request.get_json(silent=True) or {},
            referrer=request.headers.get('Referer', None)
        )

        # Add to batch list
        batch_entries.append(analytics_entry)

        # Initialize the time bomb timer when the first entry is added
        if len(batch_entries) == 1:
            batch_start_time = time.time()

        # Check if the batch size is reached or if the time bomb interval has passed
        if len(batch_entries) >= BATCH_SIZE or (time.time() - batch_start_time >= TIME_BOMB_INTERVAL):
            db.session.bulk_save_objects(batch_entries)  # Bulk insert
            db.session.commit()
            batch_entries.clear()  # Reset the batch list
            batch_start_time = None  # Reset the time bomb

    except Exception as e:
        # Log the error to the server log and continue without affecting the response
        print(f"Error logging request: {e}")

    return response
