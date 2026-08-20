from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import (
    Profile, Skill, Project, Certificate, Achievement,
    Service, GalleryItem, SocialLink, ContactMessage
)
from utils import save_uploaded_file, delete_uploaded_file, unique_slug

admin_bp = Blueprint("admin", __name__)


# ---------------------------------------------------------------- Dashboard
@admin_bp.route("/")
@login_required
def dashboard():
    stats = {
        "projects": Project.query.count(),
        "skills": Skill.query.count(),
        "certificates": Certificate.query.count(),
        "achievements": Achievement.query.count(),
        "services": Service.query.count(),
        "gallery": GalleryItem.query.count(),
        "messages": ContactMessage.query.count(),
        "unread_messages": ContactMessage.query.filter_by(is_read=False).count(),
    }
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    return render_template("admin/dashboard.html", stats=stats, recent_messages=recent_messages)


# ---------------------------------------------------------------- Profile
@admin_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile = Profile.query.first()
    if not profile:
        profile = Profile()
        db.session.add(profile)
        db.session.commit()

    if request.method == "POST":
        profile.full_name = request.form.get("full_name", "").strip()
        profile.title = request.form.get("title", "").strip()
        profile.tagline = request.form.get("tagline", "").strip()
        profile.bio = request.form.get("bio", "").strip()
        profile.email = request.form.get("email", "").strip()
        profile.phone = request.form.get("phone", "").strip()
        profile.location = request.form.get("location", "").strip()
        profile.years_experience = request.form.get("years_experience", "").strip()

        image_file = request.files.get("profile_image")
        if image_file and image_file.filename:
            new_path = save_uploaded_file(image_file, "profile")
            if new_path:
                delete_uploaded_file(profile.profile_image)
                profile.profile_image = new_path

        resume_file = request.files.get("resume_file")
        if resume_file and resume_file.filename:
            new_path = save_uploaded_file(resume_file, "resume")
            if new_path:
                delete_uploaded_file(profile.resume_file)
                profile.resume_file = new_path

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("admin.profile"))

    return render_template("admin/profile.html", profile=profile)


# ---------------------------------------------------------------- Skills
@admin_bp.route("/skills")
@login_required
def skills_list():
    skills = Skill.query.order_by(Skill.category.asc(), Skill.display_order.asc()).all()
    return render_template("admin/skills.html", skills=skills)


@admin_bp.route("/skills/save", methods=["POST"])
@admin_bp.route("/skills/save/<int:skill_id>", methods=["POST"])
@login_required
def skills_save(skill_id=None):
    skill = Skill.query.get(skill_id) if skill_id else Skill()
    skill.name = request.form.get("name", "").strip()
    skill.category = request.form.get("category", "General").strip() or "General"
    skill.proficiency = int(request.form.get("proficiency", 80) or 80)
    skill.icon_class = request.form.get("icon_class", "").strip()
    skill.display_order = int(request.form.get("display_order", 0) or 0)
    if not skill_id:
        db.session.add(skill)
    db.session.commit()
    flash("Skill saved.", "success")
    return redirect(url_for("admin.skills_list"))


@admin_bp.route("/skills/delete/<int:skill_id>", methods=["POST"])
@login_required
def skills_delete(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash("Skill deleted.", "info")
    return redirect(url_for("admin.skills_list"))


# ---------------------------------------------------------------- Projects
@admin_bp.route("/projects")
@login_required
def projects_list():
    projects = Project.query.order_by(Project.display_order.asc(), Project.created_at.desc()).all()
    return render_template("admin/projects.html", projects=projects)


@admin_bp.route("/projects/new", methods=["GET"])
@login_required
def projects_new_form():
    return render_template("admin/project_form.html", project=None)


@admin_bp.route("/projects/edit/<int:project_id>", methods=["GET"])
@login_required
def projects_edit_form(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template("admin/project_form.html", project=project)


@admin_bp.route("/projects/save", methods=["POST"])
@admin_bp.route("/projects/save/<int:project_id>", methods=["POST"])
@login_required
def projects_save(project_id=None):
    project = Project.query.get(project_id) if project_id else Project()
    title = request.form.get("title", "").strip()
    project.title = title
    project.short_description = request.form.get("short_description", "").strip()
    project.description = request.form.get("description", "").strip()
    project.tech_stack = request.form.get("tech_stack", "").strip()
    project.category = request.form.get("category", "Web").strip() or "Web"
    project.github_link = request.form.get("github_link", "").strip()
    project.live_link = request.form.get("live_link", "").strip()
    project.featured = bool(request.form.get("featured"))
    project.display_order = int(request.form.get("display_order", 0) or 0)

    if not project_id:
        project.slug = unique_slug(Project, title)
        db.session.add(project)
    elif request.form.get("regenerate_slug"):
        project.slug = unique_slug(Project, title, exclude_id=project_id)

    image_file = request.files.get("image")
    if image_file and image_file.filename:
        new_path = save_uploaded_file(image_file, "project")
        if new_path:
            delete_uploaded_file(project.image)
            project.image = new_path

    video_file = request.files.get("video")
    if video_file and video_file.filename:
        new_path = save_uploaded_file(video_file, "video")
        if new_path:
            delete_uploaded_file(project.video)
            project.video = new_path

    db.session.commit()
    flash("Project saved.", "success")
    return redirect(url_for("admin.projects_list"))


@admin_bp.route("/projects/delete/<int:project_id>", methods=["POST"])
@login_required
def projects_delete(project_id):
    project = Project.query.get_or_404(project_id)
    delete_uploaded_file(project.image)
    delete_uploaded_file(project.video)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted.", "info")
    return redirect(url_for("admin.projects_list"))


# ---------------------------------------------------------------- Certificates
@admin_bp.route("/certificates")
@login_required
def certificates_list():
    certificates = Certificate.query.order_by(Certificate.display_order.asc()).all()
    return render_template("admin/certificates.html", certificates=certificates)


@admin_bp.route("/certificates/save", methods=["POST"])
@admin_bp.route("/certificates/save/<int:cert_id>", methods=["POST"])
@login_required
def certificates_save(cert_id=None):
    cert = Certificate.query.get(cert_id) if cert_id else Certificate()
    cert.title = request.form.get("title", "").strip()
    cert.issuer = request.form.get("issuer", "").strip()
    cert.issue_date = request.form.get("issue_date", "").strip()
    cert.credential_link = request.form.get("credential_link", "").strip()
    cert.display_order = int(request.form.get("display_order", 0) or 0)
    if not cert_id:
        db.session.add(cert)

    cert_file = request.files.get("file")
    if cert_file and cert_file.filename:
        new_path = save_uploaded_file(cert_file, "certificate")
        if new_path:
            delete_uploaded_file(cert.file)
            cert.file = new_path

    db.session.commit()
    flash("Certificate saved.", "success")
    return redirect(url_for("admin.certificates_list"))


@admin_bp.route("/certificates/delete/<int:cert_id>", methods=["POST"])
@login_required
def certificates_delete(cert_id):
    cert = Certificate.query.get_or_404(cert_id)
    delete_uploaded_file(cert.file)
    db.session.delete(cert)
    db.session.commit()
    flash("Certificate deleted.", "info")
    return redirect(url_for("admin.certificates_list"))


# ---------------------------------------------------------------- Achievements
@admin_bp.route("/achievements")
@login_required
def achievements_list():
    achievements = Achievement.query.order_by(Achievement.display_order.asc()).all()
    return render_template("admin/achievements.html", achievements=achievements)


@admin_bp.route("/achievements/save", methods=["POST"])
@admin_bp.route("/achievements/save/<int:ach_id>", methods=["POST"])
@login_required
def achievements_save(ach_id=None):
    ach = Achievement.query.get(ach_id) if ach_id else Achievement()
    ach.title = request.form.get("title", "").strip()
    ach.description = request.form.get("description", "").strip()
    ach.date = request.form.get("date", "").strip()
    ach.icon_class = request.form.get("icon_class", "fa-solid fa-trophy").strip()
    ach.display_order = int(request.form.get("display_order", 0) or 0)
    if not ach_id:
        db.session.add(ach)

    image_file = request.files.get("image")
    if image_file and image_file.filename:
        new_path = save_uploaded_file(image_file, "achievement")
        if new_path:
            delete_uploaded_file(ach.image)
            ach.image = new_path

    db.session.commit()
    flash("Achievement saved.", "success")
    return redirect(url_for("admin.achievements_list"))


@admin_bp.route("/achievements/delete/<int:ach_id>", methods=["POST"])
@login_required
def achievements_delete(ach_id):
    ach = Achievement.query.get_or_404(ach_id)
    delete_uploaded_file(ach.image)
    db.session.delete(ach)
    db.session.commit()
    flash("Achievement deleted.", "info")
    return redirect(url_for("admin.achievements_list"))


# ---------------------------------------------------------------- Services
@admin_bp.route("/services")
@login_required
def services_list():
    services = Service.query.order_by(Service.display_order.asc()).all()
    return render_template("admin/services.html", services=services)


@admin_bp.route("/services/save", methods=["POST"])
@admin_bp.route("/services/save/<int:service_id>", methods=["POST"])
@login_required
def services_save(service_id=None):
    service = Service.query.get(service_id) if service_id else Service()
    service.title = request.form.get("title", "").strip()
    service.description = request.form.get("description", "").strip()
    service.icon_class = request.form.get("icon_class", "fa-solid fa-code").strip()
    service.display_order = int(request.form.get("display_order", 0) or 0)
    if not service_id:
        db.session.add(service)
    db.session.commit()
    flash("Service saved.", "success")
    return redirect(url_for("admin.services_list"))


@admin_bp.route("/services/delete/<int:service_id>", methods=["POST"])
@login_required
def services_delete(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash("Service deleted.", "info")
    return redirect(url_for("admin.services_list"))


# ---------------------------------------------------------------- Gallery
@admin_bp.route("/gallery")
@login_required
def gallery_list():
    items = GalleryItem.query.order_by(GalleryItem.display_order.asc()).all()
    return render_template("admin/gallery.html", items=items)


@admin_bp.route("/gallery/save", methods=["POST"])
@login_required
def gallery_save():
    image_file = request.files.get("image")
    if not image_file or not image_file.filename:
        flash("Please choose an image to upload.", "danger")
        return redirect(url_for("admin.gallery_list"))

    new_path = save_uploaded_file(image_file, "gallery")
    item = GalleryItem(
        image=new_path,
        caption=request.form.get("caption", "").strip(),
        display_order=int(request.form.get("display_order", 0) or 0),
    )
    db.session.add(item)
    db.session.commit()
    flash("Gallery image added.", "success")
    return redirect(url_for("admin.gallery_list"))


@admin_bp.route("/gallery/delete/<int:item_id>", methods=["POST"])
@login_required
def gallery_delete(item_id):
    item = GalleryItem.query.get_or_404(item_id)
    delete_uploaded_file(item.image)
    db.session.delete(item)
    db.session.commit()
    flash("Gallery image deleted.", "info")
    return redirect(url_for("admin.gallery_list"))


# ---------------------------------------------------------------- Social links
@admin_bp.route("/social-links")
@login_required
def social_links_list():
    links = SocialLink.query.order_by(SocialLink.display_order.asc()).all()
    return render_template("admin/social_links.html", links=links)


@admin_bp.route("/social-links/save", methods=["POST"])
@admin_bp.route("/social-links/save/<int:link_id>", methods=["POST"])
@login_required
def social_links_save(link_id=None):
    link = SocialLink.query.get(link_id) if link_id else SocialLink()
    link.platform = request.form.get("platform", "").strip()
    link.url = request.form.get("url", "").strip()
    link.icon_class = request.form.get("icon_class", "").strip()
    link.display_order = int(request.form.get("display_order", 0) or 0)
    if not link_id:
        db.session.add(link)
    db.session.commit()
    flash("Social link saved.", "success")
    return redirect(url_for("admin.social_links_list"))


@admin_bp.route("/social-links/delete/<int:link_id>", methods=["POST"])
@login_required
def social_links_delete(link_id):
    link = SocialLink.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash("Social link deleted.", "info")
    return redirect(url_for("admin.social_links_list"))


# ---------------------------------------------------------------- Messages
@admin_bp.route("/messages")
@login_required
def messages_list():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/messages.html", messages=messages)


@admin_bp.route("/messages/read/<int:msg_id>", methods=["POST"])
@login_required
def messages_mark_read(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.is_read = True
    db.session.commit()
    return redirect(url_for("admin.messages_list"))


@admin_bp.route("/messages/delete/<int:msg_id>", methods=["POST"])
@login_required
def messages_delete(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash("Message deleted.", "info")
    return redirect(url_for("admin.messages_list"))
