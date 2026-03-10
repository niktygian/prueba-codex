from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db


def ensure_default_admin():
    db = get_db()
    existing = db.execute("SELECT id FROM usuarios WHERE username = ?", ("admin",)).fetchone()
    if not existing:
        db.execute(
            "INSERT INTO usuarios (nombre, username, password_hash, rol) VALUES (?, ?, ?, ?)",
            ("Administrador", "admin", generate_password_hash("admin123"), "admin"),
        )
        db.commit()


def login(username, password):
    user = get_db().execute("SELECT * FROM usuarios WHERE username = ?", (username,)).fetchone()
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None
