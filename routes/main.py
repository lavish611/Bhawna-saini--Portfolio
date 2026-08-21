import os
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, send_from_directory, current_app, jsonify
)
from extensions import db
from models import (
    Profile, Skill, Project, Certificate, Achievement,
    Service, GalleryItem, SocialLink, ContactMessage
)
from kafka_config import send_kafka_event

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    profile = Profile.query.first()
    skills = Skill.query.order_by(Skill.display_order.asc(), Skill.category.asc()).all()
    projects = Project.query.order_by(Project.display_order.asc(), Project.created_at.desc()).all()
    certificates = Certificate.query.order_by(Certificate.display_order.asc()).all()
    achievements = Achievement.query.order_by(Achievement.display_order.asc()).all()
    services = Service.query.order_by(Service.display_order.asc()).all()
    gallery = GalleryItem.query.order_by(GalleryItem.display_order.asc()).all()
    social_links = SocialLink.query.order_by(SocialLink.display_order.asc()).all()

    # Group skills by category for a cleaner display
    skills_by_category = {}
    for s in skills:
        skills_by_category.setdefault(s.category, []).append(s)

    return render_template(
        "index.html",
        profile=profile,
        skills_by_category=skills_by_category,
        projects=projects,
        certificates=certificates,
        achievements=achievements,
        services=services,
        gallery=gallery,
        social_links=social_links,
    )


@main_bp.route("/resume/download")
def download_resume():
    profile = Profile.query.first()
    if not profile or not profile.resume_file:
        flash("Resume not available yet.", "warning")
        return redirect(url_for("main.index"))
    directory = os.path.join(current_app.config["BASE_DIR"], "static")
    return send_from_directory(directory, profile.resume_file, as_attachment=True)


@main_bp.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please fill in your name, email, and message.", "danger")
        return redirect(url_for("main.index") + "#contact")

    entry = ContactMessage(name=name, email=email, subject=subject, message=message)
    db.session.add(entry)
    db.session.commit()
    try:
        send_kafka_event(
            f"New contact message from {name} ({email}): {subject}"
        )
    except Exception as e:
        print(f"Kafka event failed: {e}")

    flash("Thanks for reaching out! I'll get back to you soon.", "success")
    return redirect(url_for("main.index") + "#contact")


@main_bp.app_errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@main_bp.app_errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500
