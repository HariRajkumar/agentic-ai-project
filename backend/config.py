import os
from dotenv import load_dotenv

# Load environment variables from .env (local dev only)
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "agentic_ai")

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    UPLOAD_FOLDER = os.path.abspath(os.getenv("UPLOAD_FOLDER", "uploads"))

    ALLOWED_EXTENSIONS = {
        "pdf", "ppt", "pptx", "txt", "docx", "png", "jpg", "jpeg"
    }

    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = ENV == "development"
