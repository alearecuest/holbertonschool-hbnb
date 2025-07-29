#!/usr/bin/python3
"""
User model for HBnB
"""
from datetime import datetime
from app.extensions import db, bcrypt
from app.models.review import Review
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column("password", db.String(128), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviews = db.relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )

    def set_password(self, password: str) -> None:
        """Hashea y almacena la contraseña."""
        self._password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """Verifica la contraseña contra el hash."""
        return bcrypt.check_password_hash(self._password, password)

    def to_dict(self) -> dict:
        """Serializa el usuario (omitiendo la contraseña)."""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat()
        }
