from flask import Blueprint, request, jsonify, json
from . import db
from .models import Book

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

@book_blueprint.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    if not books:
        return jsonify({'message': 'No books found!'}), 404
    return jsonify({'books': [{'id': book.id, 'title': book.title, 
                               'author': book.author, 'copy_numbers': book.copy_numbers, 
                               'book_location': book.book_location} for book in books]})
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
#getting a specific book 
@book_blueprint.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'message': 'Book not found!'}), 404
    return jsonify({'book': {'id': book.id, 'title': book.title, 
                             'author': book.author, 'copy_numbers': book.copy_numbers, 
                             'book_location': book.book_location}})