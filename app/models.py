from . import db
from flask import json
from sqlalchemy import Numeric

class User(db.Model):
    __tablename__='user'

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    admn_no = db.Column(db.String(20), unique=True, nullable=False)
    loans = db.relationship('Loan', backref='user', lazy=True)#user can have multiple loans 

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Book(db.Model):
    __tablename__='book'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    copy_numbers = db.Column(db.Integer, nullable=False)
    book_location = db.Column(db.String(120), nullable=False)
    loans = db.relationship('Loan', backref='book', lazy=True)#book can have multiple loans 

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}')"


class Loan(db.Model):
    __tablename__='loan'
    id = db.Column(db.BigInteger, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)#many to one each loan is linked
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)#to a specific user and book
    checkout_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(80), nullable=False)
    fines = db.Column(Numeric(10, 2), default=0.00, nullable=False)

    def __repr__(self):
        return f"Loan('{self.book_id}', '{self.user_id}')"