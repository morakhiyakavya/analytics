import email
from random import seed
from flask import Blueprint, request, jsonify, session
from models.analytics import User
from create_app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register",methods = ["POST"])
def register():
    try:

        if not request.json:
            return jsonify({"Message":"Invalid Json"}), 400
        
        username = request.json.get('username')
        email = request.json.get('email')
        password_hash = request.json.get('password')

        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()
        
        return jsonify({"message": "User created successfully"}), 201
    
    except Exception as e:

        return jsonify({"message": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    # Your login logic goes here
    # For example, validate user credentials and create a session
    try:

        if not request.json:
            return jsonify({"message": "Invalid JSON"}), 400

        username = request.json.get('username')
        password = request.json.get('password')
        
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            
            return jsonify({"message": "Login successful"}), 200
        
        return jsonify({"message": "Invalid credentials"}), 401

    except Exception as e:

        return jsonify({"message": str(e)}), 500
    

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route('/profile', methods=['GET'])
def profile():
    # Profile route, only accessible to logged-in users
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 403
    user = User.query.get(user_id)
    return jsonify({
        "username": user.username,
        "email": user.email
    }), 200


# More routes like password change, user settings, etc. could be added here
