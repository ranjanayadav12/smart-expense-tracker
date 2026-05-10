from database.db import db
from datetime import datetime


class Expense(db.Model):

    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    amount = db.Column(db.Float, nullable=False)

    category = db.Column(db.String(100), nullable=False)

    payment_method = db.Column(db.String(50), nullable=False)

    description = db.Column(db.Text, nullable=True)

    date = db.Column(db.Date, default=datetime.now().date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Expense {self.title}>"
