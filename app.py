from flask import Flask, url_for
import cloudinary
from config import Config
from extensions import db, login_manager, csrf
from models import Admin, Profile, Skill, Service, SocialLink, Project, Certificate, Achievement, GalleryItem
from utils import unique_slug


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
     @app.template_filter("media_url")
    def media_url(path):
        if not path:
            return ""

        if path.startswith(("http://", "https://")):
            return path

        return url_for("static", filename=path)

    # ---- Cloudinary ----
    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"],
        secure=True
    )

    # ---- Extensions ----
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # ---- Blueprints ----
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # ---- Template helpers ----
    from datetime import datetime

    @app.context_processor
    def inject_now():
        return {"current_year": datetime.utcnow().year}

    return app


def bootstrap_data(app):
    """
    Creates database tables (if they don't exist) and seeds a first-run
    admin account plus a starter profile so the site isn't empty on first load.
    Safe to run every time the app starts; it only inserts missing rows.
    """
    with app.app_context():
        db.create_all()

        if not Admin.query.first():
            admin = Admin(
                username=app.config["ADMIN_USERNAME"],
                email=app.config["ADMIN_EMAIL"],
            )
            admin.set_password(app.config["ADMIN_PASSWORD"])
            db.session.add(admin)

        if not Profile.query.first():
            db.session.add(Profile(
                full_name="Bhawna Saini",
                title="B.Tech IT Student & Full-Stack Developer",
                tagline="Building secure, thoughtful web experiences",
                bio=(
                    "Motivated B.Tech Information Technology student with a strong "
                    "foundation in programming and web development. Skilled in Python, "
                    "SQL, HTML, CSS, and JavaScript, with experience developing responsive "
                    "web applications and working with databases. Passionate about solving "
                    "real-world problems using technology."
                ),
                email="sainibhawna54184@gmail.com",
                phone="6396096208",
                location="Meerut, Uttar Pradesh, India",
                years_experience="Final Year Student",
                profile_image="img/profile.jpg",
                resume_file="uploads/resume/Bhawna_Saini_Resume.pdf",
            ))

        if not Skill.query.first():
            starter_skills = [
                ("Python", "Programming", 85),
                ("JavaScript", "Programming", 75),
                ("C++", "Programming", 60),
                ("HTML5", "Web Development", 90),
                ("CSS3", "Web Development", 88),
                ("Flask", "Web Development", 78),
                ("SQL", "Database", 80),
                ("MySQL", "Database", 75),
                ("Data Structures & Algorithms", "Core Concepts", 75),
                ("Git", "Tools", 65),
            ]
            for name, category, prof in starter_skills:
                db.session.add(Skill(name=name, category=category, proficiency=prof))

        if not Service.query.first():
            starter_services = [
                ("Full-Stack Web Development", "Building responsive, database-driven web applications end to end.", "fa-solid fa-code"),
                ("Security-Minded Development", "Designing applications with authentication, validation, and threat awareness built in.", "fa-solid fa-shield-halved"),
                ("Database Design", "Modeling clean, efficient MySQL schemas for real-world applications.", "fa-solid fa-database"),
            ]
            for title, desc, icon in starter_services:
                db.session.add(Service(title=title, description=desc, icon_class=icon))

        if not SocialLink.query.first():
            db.session.add(SocialLink(
                platform="LinkedIn",
                url="https://linkedin.com/in/bhawna-saini-177300337",
                icon_class="fa-brands fa-linkedin",
                display_order=1,
            ))
            db.session.add(SocialLink(
                platform="GitHub",
                url="#",
                icon_class="fa-brands fa-github",
                display_order=2,
            ))
            db.session.add(SocialLink(
                platform="Email",
                url="mailto:sainibhawna54184@gmail.com",
                icon_class="fa-solid fa-envelope",
                display_order=3,
            ))

        if not Project.query.first():
            starter_projects = [
                dict(
                    title="Cyber Threat Detection System",
                    short_description="Real-time system that detects and alerts on suspicious network activity and malware patterns.",
                    description=(
                        "A real-time cyber threat detection system capable of identifying and "
                        "alerting on suspicious network activities, malware patterns, and "
                        "potential security breaches. Uses machine learning techniques for "
                        "anomaly detection and presents threat data through an interactive "
                        "web-based dashboard. Final year project — ongoing."
                    ),
                    tech_stack="Python, HTML, CSS, JavaScript, SQL",
                    category="Security",
                    featured=True,
                    display_order=1,
                ),
                dict(
                    title="Food Recipe Website",
                    short_description="Responsive site to explore recipes with ingredients and preparation steps.",
                    description="A responsive website to explore food recipes with ingredients and preparation steps.",
                    tech_stack="HTML, CSS, JavaScript",
                    category="Web",
                    display_order=2,
                ),
                dict(
                    title="Syntax Checker",
                    short_description="Validates code syntax using input validation and basic programming logic.",
                    description="A syntax checking system to identify and validate syntax errors using basic programming logic and input validation.",
                    tech_stack="HTML, CSS, JavaScript, Python",
                    category="Tool",
                    display_order=3,
                ),
            ]
            for data in starter_projects:
                data["slug"] = unique_slug(Project, data["title"])
                db.session.add(Project(**data))

        if not Certificate.query.first():
            db.session.add(Certificate(title="Python for Data Science", issuer="Cognitive Class", display_order=1))
            db.session.add(Certificate(title="SQL and Relational Databases", issuer="Cognitive Class", display_order=2))

        if not Achievement.query.first():
            db.session.add(Achievement(
                title="OpenCode'25 Hackathon", description="Participant at IIIT Allahabad.",
                icon_class="fa-solid fa-trophy", display_order=1,
            ))
            db.session.add(Achievement(
                title="Code Clash Hackathon", description="Participant at IIT Jodhpur.",
                icon_class="fa-solid fa-trophy", display_order=2,
            ))
            db.session.add(Achievement(
                title="AI Powered Frontend Project Workshop", description="Workshop by Nexa Soul.",
                icon_class="fa-solid fa-chalkboard-user", display_order=3,
            ))

        if not GalleryItem.query.first():
            db.session.add(GalleryItem(image="img/gallery1.jpg", caption="", display_order=1))
            db.session.add(GalleryItem(image="img/gallery2.jpg", caption="", display_order=2))

        db.session.commit()


app = create_app()
bootstrap_data(app)

if __name__ == "__main__":
    app.run(debug=True)
