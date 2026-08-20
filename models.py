from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class Admin(UserMixin, db.Model):
    """The single admin account that can log into the dashboard."""

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)


class Profile(db.Model):
    """Singleton row holding the owner's personal/about information."""

    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), default="")
    title = db.Column(db.String(160), default="")
    tagline = db.Column(db.String(240), default="")
    bio = db.Column(db.Text, default="")
    email = db.Column(db.String(120), default="")
    phone = db.Column(db.String(30), default="")
    location = db.Column(db.String(120), default="")
    profile_image = db.Column(db.String(255), default="")
    resume_file = db.Column(db.String(255), default="")
    years_experience = db.Column(db.String(20), default="")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), default="General")
    proficiency = db.Column(db.Integer, default=80)  # 0-100
    icon_class = db.Column(db.String(120), default="")  # e.g. devicon class
    display_order = db.Column(db.Integer, default=0)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False)
    short_description = db.Column(db.String(300), default="")
    description = db.Column(db.Text, default="")
    tech_stack = db.Column(db.String(300), default="")  # comma separated
    category = db.Column(db.String(80), default="Web")
    image = db.Column(db.String(255), default="")
    video = db.Column(db.String(255), default="")
    github_link = db.Column(db.String(255), default="")
    live_link = db.Column(db.String(255), default="")
    featured = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Certificate(db.Model):
    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(160), default="")
    issue_date = db.Column(db.String(40), default="")
    credential_link = db.Column(db.String(255), default="")
    file = db.Column(db.String(255), default="")  # image or pdf
    display_order = db.Column(db.Integer, default=0)


class Achievement(db.Model):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    date = db.Column(db.String(40), default="")
    icon_class = db.Column(db.String(120), default="fa-solid fa-trophy")
    image = db.Column(db.String(255), default="")
    display_order = db.Column(db.Integer, default=0)


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, default="")
    icon_class = db.Column(db.String(120), default="fa-solid fa-code")
    display_order = db.Column(db.Integer, default=0)


class GalleryItem(db.Model):
    __tablename__ = "gallery"

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(200), default="")
    display_order = db.Column(db.Integer, default=0)


class SocialLink(db.Model):
    __tablename__ = "social_links"

    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(60), nullable=False)  # e.g. GitHub, LinkedIn
    url = db.Column(db.String(255), nullable=False)
    icon_class = db.Column(db.String(120), default="fa-brands fa-github")
    display_order = db.Column(db.Integer, default=0)


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), default="")
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
