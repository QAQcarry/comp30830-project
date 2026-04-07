"""User model for Flask-Login authentication."""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text


class User(UserMixin):
    def __init__(self, id, email, password_hash):
        self.id = id
        self.email = email
        self.password_hash = password_hash

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_id(engine, user_id):
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT id, email, password_hash FROM users WHERE id = :id"),
                {"id": user_id}
            ).fetchone()
        if row is None:
            return None
        return User(row.id, row.email, row.password_hash)

    @staticmethod
    def get_by_email(engine, email):
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT id, email, password_hash FROM users WHERE email = :email"),
                {"email": email.strip().lower()}
            ).fetchone()
        if row is None:
            return None
        return User(row.id, row.email, row.password_hash)

    @staticmethod
    def create_user(engine, email, password):
        password_hash = generate_password_hash(password)
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO users (email, password_hash) VALUES (:email, :password_hash)"),
                {"email": email.strip().lower(), "password_hash": password_hash}
            )
            conn.commit()
