from flask import Blueprint, request, jsonify, json, send_from_directory
from . import db
from .models import Book
import os
from flask import url_for
from .config import *
from werkzeug.utils import secure_filename

book_blueprint = Blueprint('book_blueprint', __name__)

# Add a book
@book_blueprint.route('/book', methods=['POST'])
#@jwt_required()
def add_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        copy_numbers=data['copy_numbers'],
        book_location=data['book_location']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully!'}), 201


# Get all book details
@book_blueprint.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    book_data = []
    for book in books:
        book_data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'copy_numbers': book.copy_numbers,
            'book_location': book.book_location,
            'image_url': book.image_url
        })
    return jsonify({'books': book_data})

# Update a book
@book_blueprint.route('/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'message': 'Book not found!'}), 404
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.copy_numbers = data.get('copy_numbers', book.copy_numbers)
    book.book_location = data.get('book_location', book.book_location)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully!'})