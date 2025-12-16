import uuid
from datetime import datetime
from db.mongo import get_db


def create_session() -> str:
    db = get_db()
    session_id = str(uuid.uuid4())

    db.chat_sessions.insert_one({
        "session_id": session_id,
        "created_at": datetime.utcnow(),
        "last_updated": datetime.utcnow(),
        "messages": []
    })

    return session_id


def add_message(session_id: str, role: str, content: str):
    db = get_db()
    db.chat_sessions.update_one(
        {"session_id": session_id},
        {
            "$push": {
                "messages": {
                    "role": role,
                    "content": content,
                    "timestamp": datetime.utcnow()
                }
            },
            "$set": {
                "last_updated": datetime.utcnow()
            }
        }
    )


def get_messages(session_id: str, limit: int = 12):
    db = get_db()
    session = db.chat_sessions.find_one({"session_id": session_id})

    if not session:
        return []

    return session["messages"][-limit:]
