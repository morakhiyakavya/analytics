from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return jsonify({"message": "Welcome to Flask Analytics!"})

@main_bp.route("/data")
def fetch_data():
    return jsonify({"message": "Fetched data successfully!"})
