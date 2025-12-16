from flask import Blueprint, jsonify

summarize_bp = Blueprint("summarize", __name__)

@summarize_bp.route("/", methods=["POST"])
def summarize():
    return jsonify({"message": "Summarize endpoint ready"})
