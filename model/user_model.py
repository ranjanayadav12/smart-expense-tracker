from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    expenses = db.relationship(
        'Expense',
        backref='user',
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Set Password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Check Password
    def check_password(self, password):
        return check_password_hash(self.password, password)