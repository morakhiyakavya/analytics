from flask import request, g, jsonify
from datetime import datetime
from models.models import db, WebTraffic
import uuid

def session_middleware():
    session_id = request.cookies.get('session_id')
    
    if not session_id:
        session_id = str(uuid.uuid4())  # Generate new session ID
    g.session_id = session_id  # Store in global request context

    return session_id