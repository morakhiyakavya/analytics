from flask import Blueprint, jsonify, request, current_app
from models.analytics import Analytics, ApiRateLimit, ErrorLog, User, batch_entries
from models.users import UserSession
from flask_sqlalchemy import SQLAlchemy
import json
from create_app import db
import time



main_bp = Blueprint('main', __name__)


# Helper function to log analytics
def log_analytics_entry(data, response):
    """Optional: Logs the request to the Analytics table."""
    if not current_app.config['ENABLE_LOGGING']:
        return

    duration = round(time.time() - request.start_time, 4)  # Assuming you have a request.start_time set
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

    db.session.add(analytics_entry)
    db.session.commit()

# A super admin who will get all the data.
@main_bp.route('/create-superadmin')
def create_superadmin():
    if User.query.filter_by(role='superadmin').first():
        return jsonify({"message": "Superadmin already exists"}), 400
    user = User(username='superadmin', email='testingpurpose760@gmail.com', password_hash='superadmin', role='superadmin')
    db.session.add(user)
    db.session.commit()
    return user

# 1. **Add User Route with Optional Logging**
@main_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Validate required fields
    if not all(field in data for field in ('username', 'email', 'password_hash')):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new User object
    user = User(username=data['username'], email=data['email'], password_hash=data['password_hash'])

    try:
        db.session.add(user)
        db.session.commit()

        # Optional: Log analytics data if ENABLE_LOGGING is True
        log_analytics_entry(data, user)

        return jsonify({"message": "User created successfully", "id": user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating user: {str(e)}"}), 500

# 2. **Add Analytics Entry Route with Optional Logging**
@main_bp.route('/analytics', methods=['POST'])
def create_analytics():
    data = request.get_json()

    # Validate required fields
    required_fields = ['ip_address', 'user_agent', 'method', 'endpoint', 'status_code', 'response_time', 'request_headers', 'request_data']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new Analytics object
    analytics = Analytics(
        ip_address=data['ip_address'],
        user_agent=data['user_agent'],
        method=data['method'],
        endpoint=data['endpoint'],
        status_code=data['status_code'],
        response_time=data['response_time'],
        request_headers=data['request_headers'],
        request_data=data['request_data'],
        referrer=data.get('referrer')
    )

    try:
        db.session.add(analytics)
        db.session.commit()

        # Optional: Log analytics if ENABLE_LOGGING is True
        log_analytics_entry(data, analytics)

        return jsonify({"message": "Analytics entry created successfully", "id": analytics.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating analytics entry: {str(e)}"}), 500

# 3. **Add User Session Route with Optional Logging**
@main_bp.route('/user_sessions', methods=['POST'])
def create_user_session():
    data = request.get_json()

    # Validate required fields
    required_fields = ['session_id', 'ip_address', 'user_agent']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new UserSession object
    session = UserSession(
        session_id=data['session_id'],
        ip_address=data['ip_address'],
        user_agent=data['user_agent'],
        location=data.get('location'),
        pages_visited=data.get('pages_visited')
    )

    try:
        db.session.add(session)
        db.session.commit()

        # Optional: Log analytics if ENABLE_LOGGING is True
        log_analytics_entry(data, session)

        return jsonify({"message": "User session created successfully", "id": session.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating user session: {str(e)}"}), 500

# 4. **Add Error Log Route with Optional Logging**
@main_bp.route('/error_logs', methods=['POST'])
def create_error_log():
    data = request.get_json()

    # Validate required fields
    required_fields = ['message', 'stack_trace', 'endpoint', 'user_agent', 'ip_address', 'status_code', 'method']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new ErrorLog object
    error_log = ErrorLog(
        message=data['message'],
        stack_trace=data['stack_trace'],
        endpoint=data['endpoint'],
        user_agent=data['user_agent'],
        ip_address=data['ip_address'],
        status_code=data['status_code'],
        method=data['method']
    )

    try:
        db.session.add(error_log)
        db.session.commit()

        # Optional: Log analytics if ENABLE_LOGGING is True
        log_analytics_entry(data, error_log)

        return jsonify({"message": "Error log created successfully", "id": error_log.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating error log: {str(e)}"}), 500

# 5. **Add API Rate Limit Log Route with Optional Logging**
@main_bp.route('/api_rate_limits', methods=['POST'])
def create_api_rate_limit():
    data = request.get_json()

    # Validate required fields
    required_fields = ['ip_address', 'endpoint', 'attempts', 'status']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new ApiRateLimit object
    rate_limit = ApiRateLimit(
        ip_address=data['ip_address'],
        endpoint=data['endpoint'],
        attempts=data['attempts'],
        status=data['status']
    )

    try:
        db.session.add(rate_limit)
        db.session.commit()

        # Optional: Log analytics if ENABLE_LOGGING is True
        log_analytics_entry(data, rate_limit)

        return jsonify({"message": "API rate limit log created successfully", "id": rate_limit.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating API rate limit log: {str(e)}"}), 500


@main_bp.route("/analytics")
def get_analytics():
    if batch_entries:
        try:
            # Commit any pending batch entries
            db.session.bulk_save_objects(batch_entries)
            db.session.commit()
            print(f"Flushing batch of {len(batch_entries)} entries.")
        except Exception as e:
            return jsonify({"error": f"Error flushing data: {e}"}), 500
        finally:
            # Clear the batch entries after flushing
            batch_entries.clear()

    # Fetch and return the analytics data
    analytics_data = Analytics.query.all()  # You could filter this by time, status, etc.
    return jsonify([{
        "id": a.id,
        "timestamp": a.timestamp,
        "ip_address": a.ip_address,
        "user_agent": a.user_agent,
        "method": a.method,
        "endpoint": a.endpoint,
        "status_code": a.status_code,
        "response_time": a.response_time,
        "request_headers": json.loads(a.request_headers),
        "request_data": json.loads(a.request_data),
        "referrer": a.referrer
    } for a in analytics_data]), 200