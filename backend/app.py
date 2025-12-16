import os
from flask import Flask, jsonify
from config import Config

# Route blueprints (will be implemented later)
from routes.upload import upload_bp
from routes.summarize import summarize_bp
from routes.chat import chat_bp


def create_app():
    # Ensure upload folder exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(upload_bp, url_prefix="/api/upload")
    app.register_blueprint(summarize_bp, url_prefix="/api/summarize")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")

    # Health check
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "environment": Config.ENV
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        debug=Config.DEBUG,
        use_reloader=False
    )

