import os
import re
import uuid
import cloudinary
import cloudinary.uploader

from werkzeug.utils import secure_filename
from flask import current_app


def _extension(filename):
    return filename.rsplit(".", 1)[1].lower() if "." in filename else ""


def is_allowed_file(filename, allowed_sets):
    """allowed_sets: list of set()s of allowed extensions to check against."""
    ext = _extension(filename)
    for allowed in allowed_sets:
        if ext in allowed:
            return True
    return False


def save_uploaded_file(file_storage, content_type):
    """
    Uploads an uploaded file to Cloudinary with a unique safe filename.

    Returns the Cloudinary URL to store in the database,
    or None if there was no file.
    """
    if not file_storage or file_storage.filename == "":
        return None

    cfg = current_app.config

    allowed = (
        cfg["ALLOWED_IMAGE_EXTENSIONS"]
        | cfg["ALLOWED_DOCUMENT_EXTENSIONS"]
        | cfg["ALLOWED_VIDEO_EXTENSIONS"]
    )

    if not is_allowed_file(file_storage.filename, [allowed]):
        raise ValueError("File type not allowed.")

    # Create a safe unique filename
    original_name = file_storage.filename
    ext = _extension(original_name)

    safe_name = secure_filename(
        original_name.rsplit(".", 1)[0]
    )

    unique_name = f"{safe_name}-{uuid.uuid4().hex[:8]}"

    # Folder based on content type
    subfolder = cfg["UPLOAD_SUBFOLDERS"].get(content_type, "misc")

    # Upload to Cloudinary
    result = cloudinary.uploader.upload(
        file_storage,
        public_id=unique_name,
        folder=f"portfolio/{subfolder}",
        resource_type="auto"
    )

    # Return Cloudinary URL
    return result.get("secure_url")


def delete_uploaded_file(relative_path):
    """
    Deletes a previously uploaded file from Cloudinary.

    The database should contain the Cloudinary URL.
    """
    if not relative_path:
        return

    # If this is an old/local path, simply ignore it.
    if not relative_path.startswith("http"):
        return

    try:
        # Extract public_id from Cloudinary URL
        # Example:
        # https://res.cloudinary.com/.../image/upload/v123/portfolio/images/photo.jpg

        upload_marker = "/upload/"
        if upload_marker not in relative_path:
            return

        public_path = relative_path.split(upload_marker, 1)[1]

        # Remove version if present
        parts = public_path.split("/")

        if parts and parts[0].startswith("v") and parts[0][1:].isdigit():
            parts = parts[1:]

        public_id_with_ext = "/".join(parts)

        # Remove file extension
        public_id = os.path.splitext(public_id_with_ext)[0]

        cloudinary.uploader.destroy(
            public_id,
            resource_type="image"
        )

    except Exception:
        # Don't crash the application if deletion fails
        pass


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or uuid.uuid4().hex[:8]


def unique_slug(model, base_text, exclude_id=None):
    """Generates a unique slug for the given model, appending -2, -3, ... if needed."""
    base = slugify(base_text)
    slug = base
    counter = 2

    while True:
        query = model.query.filter_by(slug=slug)

        if exclude_id:
            query = query.filter(model.id != exclude_id)

        if not query.first():
            return slug

        slug = f"{base}-{counter}"
        counter += 1