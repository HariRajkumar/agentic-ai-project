import uuid
from datetime import datetime
from db.mongo import get_documents_collection


def save_document(
    filename: str,
    file_type: str,
    summary: str,
    text_length: int,
    source_path: str
) -> str:
    collection = get_documents_collection()

    document_id = str(uuid.uuid4())

    doc = {
        "document_id": document_id,
        "filename": filename,
        "file_type": file_type,
        "upload_time": datetime.utcnow(),
        "summary": summary,
        "text_length": text_length,
        "source_path": source_path,
        "status": "processed"
    }

    collection.insert_one(doc)
    return document_id
