import os
import re
import uuid
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
    Saves an uploaded file into static/uploads/<subfolder>/ with a unique,
    safe filename. Returns the relative path (from static/) to store in the DB,
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

    subfolder = cfg["UPLOAD_SUBFOLDERS"].get(content_type, "misc")
    target_dir = os.path.join(cfg["UPLOAD_FOLDER"], subfolder)
    os.makedirs(target_dir, exist_ok=True)

    ext = _extension(file_storage.filename)
    safe_name = secure_filename(file_storage.filename.rsplit(".", 1)[0])
    unique_name = f"{safe_name}-{uuid.uuid4().hex[:8]}.{ext}"

    file_storage.save(os.path.join(target_dir, unique_name))
    return f"uploads/{subfolder}/{unique_name}"


def delete_uploaded_file(relative_path):
    """Deletes a file previously saved via save_uploaded_file, if it exists."""
    if not relative_path:
        return
    cfg = current_app.config
    full_path = os.path.join(cfg["BASE_DIR"], "static", relative_path)
    if os.path.isfile(full_path):
        try:
            os.remove(full_path)
        except OSError:
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
