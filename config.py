import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """Central application configuration, populated from environment variables."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-me")

    # ---- Database ----
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(basedir, "portfolio.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ---- Admin bootstrap ----
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

    # ---- Uploads ----
    BASE_DIR = basedir
    UPLOAD_FOLDER = os.path.join(basedir, "static", "uploads")
    MAX_CONTENT_LENGTH = int(
        os.environ.get("MAX_CONTENT_LENGTH_MB", 25)
    ) * 1024 * 1024

    ALLOWED_IMAGE_EXTENSIONS = {
        "png", "jpg", "jpeg", "webp", "gif", "svg"
    }

    ALLOWED_DOCUMENT_EXTENSIONS = {"pdf"}

    ALLOWED_VIDEO_EXTENSIONS = {
        "mp4", "webm", "mov"
    }

    # Subfolders per content type
    UPLOAD_SUBFOLDERS = {
        "project": "projects",
        "certificate": "certificates",
        "gallery": "gallery",
        "resume": "resume",
        "video": "videos",
        "achievement": "achievements",
        "profile": "profile",
    }
