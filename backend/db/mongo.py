from pymongo import MongoClient
from config import Config

_client = None
_db = None


def get_db():
    global _client, _db

    if _db is None:
        if not Config.MONGODB_URI:
            raise RuntimeError("MONGODB_URI not set")

        _client = MongoClient(Config.MONGODB_URI)
        _db = _client[Config.MONGODB_DB_NAME]

    return _db


def get_documents_collection():
    db = get_db()
    return db["documents"]
