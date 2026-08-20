-- ============================================================
-- Portfolio Website — MySQL Schema
-- Create the database, then import this file:
--   mysql -u root -p portfolio_db < database/schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS portfolio_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE portfolio_db;

-- ---------------------------------------------------------- admins
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------- profile
CREATE TABLE IF NOT EXISTS profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) DEFAULT '',
    title VARCHAR(160) DEFAULT '',
    tagline VARCHAR(240) DEFAULT '',
    bio TEXT,
    email VARCHAR(120) DEFAULT '',
    phone VARCHAR(30) DEFAULT '',
    location VARCHAR(120) DEFAULT '',
    profile_image VARCHAR(255) DEFAULT '',
    resume_file VARCHAR(255) DEFAULT '',
    years_experience VARCHAR(20) DEFAULT '',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------- skills
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    category VARCHAR(80) DEFAULT 'General',
    proficiency INT DEFAULT 80,
    icon_class VARCHAR(120) DEFAULT '',
    display_order INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------- projects
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(160) NOT NULL,
    slug VARCHAR(180) NOT NULL UNIQUE,
    short_description VARCHAR(300) DEFAULT '',
    description TEXT,
    tech_stack VARCHAR(300) DEFAULT '',
    category VARCHAR(80) DEFAULT 'Web',
    image VARCHAR(255) DEFAULT '',
    video VARCHAR(255) DEFAULT '',
    github_link VARCHAR(255) DEFAULT '',
    live_link VARCHAR(255) DEFAULT '',
    featured BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------- certificates
CREATE TABLE IF NOT EXISTS certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    issuer VARCHAR(160) DEFAULT '',
    issue_date VARCHAR(40) DEFAULT '',
    credential_link VARCHAR(255) DEFAULT '',
    file VARCHAR(255) DEFAULT '',
    display_order INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------- achievements
CREATE TABLE IF NOT EXISTS achievements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    date VARCHAR(40) DEFAULT '',
    icon_class VARCHAR(120) DEFAULT 'fa-solid fa-trophy',
    image VARCHAR(255) DEFAULT '',
    display_order INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------- services
CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(160) NOT NULL,
    description TEXT,
    icon_class VARCHAR(120) DEFAULT 'fa-solid fa-code',
    display_order INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------- gallery
CREATE TABLE IF NOT EXISTS gallery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image VARCHAR(255) NOT NULL,
    caption VARCHAR(200) DEFAULT '',
    display_order INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------- social_links
CREATE TABLE IF NOT EXISTS social_links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    platform VARCHAR(60) NOT NULL,
    url VARCHAR(255) NOT NULL,
    icon_class VARCHAR(120) DEFAULT 'fa-brands fa-github',
    display_order INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------- contact_messages
CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL,
    subject VARCHAR(200) DEFAULT '',
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Note: running the Flask app (app.py) will also auto-create
-- these tables via SQLAlchemy if they don't already exist, and
-- will seed a first admin account + starter profile/skills/
-- services/social links. Importing this file manually is only
-- needed if you prefer to set up the schema before first run.
-- ============================================================
