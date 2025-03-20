import json
import time
from flask_sqlalchemy import SQLAlchemy
from flask import request

db = SQLAlchemy()

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

    def __init__(self, ip_address, user_agent, method, endpoint, status_code, response_time, request_headers, request_data):
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.method = method
        self.endpoint = endpoint
        self.status_code = status_code
        self.response_time = response_time
        self.request_headers = json.dumps(request_headers)
        self.request_data = json.dumps(request_data)

def log_request(response):
    """Function to log each API request into the analytics table."""
    duration = round(time.time() - request.start_time, 4)
    analytics_entry = Analytics(
        ip_address=request.remote_addr,
        user_agent=request.headers.get("User-Agent"),
        method=request.method,
        endpoint=request.path,
        status_code=response.status_code,
        response_time=duration,
        request_headers=dict(request.headers),
        request_data=request.get_json(silent=True) or {}
    )
    db.session.add(analytics_entry)
    db.session.commit()
    return response
