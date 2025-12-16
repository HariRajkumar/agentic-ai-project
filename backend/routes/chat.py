# from flask import Blueprint, request, jsonify
# from agents.chat_graph import create_chat_graph

# chat_bp = Blueprint("chat", __name__)

# graph = create_chat_graph()


# @chat_bp.route("/", methods=["POST"])
# def chat():
#     data = request.get_json()

#     if not data or "question" not in data:
#         return jsonify({"error": "Question is required"}), 400

#     result = graph.invoke({
#         "question": data["question"]
#     })

#     return jsonify({
#         "question": data["question"],
#         "answer": result["answer"]
#     }), 200

from flask import Blueprint, request, jsonify
from agents.chat_graph import create_chat_graph
from db.chat_repository import create_session

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Question is required"}), 400

    session_id = data.get("session_id")

    if not session_id:
        session_id = create_session()

    graph = create_chat_graph(session_id)

    result = graph.invoke({
        "question": data["question"]
    })

    return jsonify({
        "session_id": session_id,
        "question": data["question"],
        "answer": result["answer"]
    }), 200
