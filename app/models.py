from . import db
from flask import json
from sqlalchemy import Numeric
from datetime import datetime, timedelta


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    admn_no = db.Column(db.String(20), unique=True, nullable=False)
    loans = db.relationship("Loan", backref="user", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    copy_numbers = db.Column(db.Integer, nullable=False)
    book_location = db.Column(db.String(120), nullable=False)
    loans = db.relationship("Loan", backref="book", lazy=True)

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}')"


class Loan(db.Model):
    __tablename__ = "loan"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    checkout_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True, default=None)
    fines = db.Column(db.Float, default=0.00, nullable=False)

    def __repr__(self):
        return f"Loan('{self.book_id}', '{self.user_id}')"

    def calculate_fines(self):
        if self.return_date and self.return_date > self.due_date:
            days_late = (self.return_date - self.due_date).days
            return days_late * 20.00
        elif datetime.utcnow() > self.due_date:
            days_late = (datetime.utcnow() - self.due_date).days
            return days_late * 20.00
        return 0.00

    def update_fines(self):
        self.fines = self.calculate_fines()
        db.session.commit()
