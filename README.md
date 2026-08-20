# Bhawna Saini — Portfolio Website

A production-ready personal portfolio built with **Flask + MySQL**, featuring a premium dark
glassmorphism UI, an animated 3D network hero (Three.js), scroll animations (GSAP + AOS), a
typing effect (Typed.js), and a full admin dashboard to manage every piece of content —
no code edits required after setup.

---

## ✨ Features

- Responsive, accessible, SEO-friendly one-page portfolio (hero, about, skills, services,
  projects, certificates, achievements, gallery, contact)
- Animated 3D particle network hero built with Three.js
- Dark, glassmorphism UI with a violet → blue signature gradient and cyan accents
- Flask backend with MySQL (SQLAlchemy ORM) — auto-creates tables and seeds starter content
  on first run
- Session-based admin authentication (Flask-Login) with CSRF protection (Flask-WTF) on every form
- Full admin CRUD for: Profile, Skills, Projects, Certificates, Achievements, Services,
  Gallery, Social Links, and Contact Messages
- Image / PDF / video upload support (project images & videos, certificates, gallery photos,
  resume PDF, profile photo)
- Downloadable resume button pulls whatever PDF is uploaded in the admin panel
- Contact form that stores messages in the database, visible in the admin inbox
- Custom 404 / 500 error pages matching the site design

---

## 📁 Project Structure

```
portfolio/
├── app.py                  # App factory, extension setup, DB bootstrap/seed
├── config.py                # Configuration (reads from .env)
├── extensions.py             # Shared db / login_manager / csrf instances
├── models.py                 # SQLAlchemy models (all content types)
├── utils.py                   # File upload + slug helpers
├── requirements.txt
├── .env.example                # Copy to .env and fill in your values
├── database/
│   └── schema.sql               # Raw MySQL schema (optional manual import)
├── routes/
│   ├── main.py                   # Public site routes
│   ├── auth.py                    # Login / logout
│   └── admin.py                    # Admin dashboard + CRUD routes
├── templates/
│   ├── base.html, index.html, 404.html, 500.html
│   ├── auth/login.html
│   └── admin/                       # Dashboard + one page per content type
└── static/
    ├── css/style.css, admin.css
    ├── js/main.js
    ├── img/                          # Seeded profile + gallery photos
    └── uploads/                      # Admin-uploaded files, organized by type
```

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.10+
- MySQL Server 8+ (running locally or remotely)

### 2. Clone/copy the project and install dependencies
```bash
cd portfolio
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and set:
- `SECRET_KEY` — any long random string
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` — your MySQL credentials
- `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` — your admin login (used only the first
  time the app creates the database)

### 4. Create the database
```sql
CREATE DATABASE portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
That's it — you do **not** need to manually import `database/schema.sql`; the app creates all
tables automatically on first run. (The SQL file is provided in case you prefer to set up the
schema by hand before running the app.)

### 5. Run the app
```bash
python app.py
```
Visit **http://localhost:5000** for the public site and **http://localhost:5000/auth/login**
to log into the admin dashboard with the credentials you set in `.env`.

On first run, the app automatically seeds:
- Your admin account
- Your profile (from your resume), the photo you chose, and your resume PDF
- Your resume's skills, projects, certificates, and hackathon achievements
- A couple of starter services and social links

You can edit or delete any of this from the admin dashboard — nothing is hard-coded into
the templates.

---

## 🔑 Using the Admin Dashboard

1. Log in at `/auth/login`
2. From the sidebar you can manage:
   - **Profile** — name, title, bio, contact info, profile photo, resume PDF
   - **Skills** — grouped by category with proficiency bars
   - **Projects** — title, description, tech stack, category, image/video, GitHub & live demo
     links, "Featured" flag
   - **Certificates** — issuer, date, credential link or uploaded file
   - **Achievements** — timeline entries with icon and date
   - **Services** — what you offer, shown as cards
   - **Gallery** — photo grid
   - **Social Links** — icons + URLs shown in the contact section
   - **Messages** — everything submitted through the public contact form

Add your real **GitHub repo links** and **live demo links** to each project from the
Projects section whenever you're ready to share them — the form already has fields for both.

---

## 🌐 Deployment Notes

- Set `FLASK_ENV=production` and use a real WSGI server (e.g. **gunicorn**) instead of the
  Flask dev server:
  ```bash
  pip install gunicorn
  gunicorn -w 4 -b 0.0.0.0:8000 app:app
  ```
- Put a reverse proxy (Nginx) in front for TLS and static file serving.
- Set a strong, unique `SECRET_KEY` and `ADMIN_PASSWORD` in production — never commit `.env`.
- Make sure the MySQL user has privileges on `DB_NAME` and that `static/uploads/` is writable
  by the app process.
- Increase `MAX_CONTENT_LENGTH_MB` in `.env` if you need to upload larger videos.

---

## 🛠 Tech Stack

**Frontend:** HTML5, CSS3 (custom, no framework), vanilla JavaScript, Three.js, GSAP, AOS, Typed.js, Font Awesome
**Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF (CSRF)
**Database:** MySQL (via PyMySQL)
