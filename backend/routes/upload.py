import os
from db.document_repository import save_document
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from config import Config
from loaders import extract_text
from agents.summarization_graph import create_summarization_graph
from rag.indexing import index_document

upload_bp = Blueprint("upload", __name__)


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS


@upload_bp.route("/", methods=["POST"])
def upload_file():
    print("📥 Upload request received")

    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(Config.UPLOAD_FOLDER, filename)

    file.save(save_path)
    print("✅ File saved successfully")

    try:
        # 1️⃣ Extract text
        extracted_text = extract_text(save_path)

        # 2️⃣ Run summarization graph
        graph = create_summarization_graph()
        result = graph.invoke({"text": extracted_text})

        # ✅ USE THE RIGHT OUTPUT
        summary = result["final_summary"]

        file_ext = os.path.splitext(filename)[1].lower().replace(".", "")

        # 3️⃣ Store in MongoDB
        document_id = save_document(
            filename=filename,
            file_type=file_ext,
            summary=summary,
            text_length=len(extracted_text),
            source_path=save_path
        )

        # 4️⃣ Index for RAG
        index_document(
            document_id=document_id,
            text=extracted_text,
            filename=filename
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # 5️⃣ Return to frontend
    return jsonify({
        "message": "File uploaded, summarized, and stored successfully",
        "document_id": document_id,
        "filename": filename,
        "summary": summary,                 # full bullet summary
        "summary_preview": summary[:500]    # optional
    }), 200

