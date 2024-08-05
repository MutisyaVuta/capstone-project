from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from . import db
from .models import Book, Loan

library_blueprint = Blueprint('library', __name__)
##

@library_blueprint.route("/delete_book/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book():
    book_id = request.get_json().get('book_id')
    if not book_id:
        return jsonify({'message': "Book ID is required"}), 400
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': "Book not found"}), 404 
    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': "Failed to delete book", 'error': str(e)}), 500

    return jsonify({'message': "Book deleted successfully"}), 200

@library_blueprint.route("/delete_loan/<int:loan_id>", methods=["DELETE"])
@jwt_required()
def delete_loan():
    loan_id = request.get_json().get('loan_id')
    if not loan_id:
        return jsonify({'message': "Loan ID is required"}), 400
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({'message': "Loan not found"}), 404
    try:
        db.session.delete(loan)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': "Failed to delete loan", 'error': str(e)}), 500

    return jsonify({'message': "Loan deleted successfully"}), 200

@library_blueprint.route("/search_book", methods=["POST"])
def search_book():
    title = request.get_json().get('title')
    if not title:
        return jsonify({'message': "Book title is required"}), 400
    books = Book.query.filter(Book.title.like(f"%{title}%")).all()
    if not books:
        return jsonify({'message': "No books found"}), 404
    return jsonify({'books': [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]}), 200