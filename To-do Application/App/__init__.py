import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create database connection object globally
db = SQLAlchemy()

BASE_DIR = Path(__file__).resolve().parent.parent


def load_env_file(env_path):
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        os.environ[key] = value


load_env_file(BASE_DIR / ".env")
load_env_file(Path(__file__).resolve().parent / ".env")


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-me-in-your-env-file")

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        database_path = BASE_DIR / "instance" / "tasks.db"
        database_url = f"sqlite:///{database_path}"

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app