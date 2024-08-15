from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Loan
from datetime import datetime, timedelta
from . import db 

loan = Blueprint("loan", __name__)

#create a loan 
@loan.route("/loans", methods=["POST"])
def create_loan():
    data = request.get_json()

    if "book_id" not in data or "user_id" not in data:
        return jsonify({"error": "Missing required fields: book_id or user_id"}), 400

    new_loan = Loan(
        book_id=data["book_id"],
        user_id=data["user_id"],
        checkout_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=7),
        return_date=None,
        fines=float(data.get("fines", 0.00)),
    )

    db.session.add(new_loan)
    db.session.commit()

    return jsonify({"message": "Loan created successfully"}), 201

#get all loans
@loan.route("/loans", methods=["GET"])
def get_loan():
    loans = Loan.query.all()
    list_loan = []

    for loan in loans:
        loan_data = {
            "id": loan.id,
            "book_id": loan.book_id,
            "user_id": loan.user_id,
            "checkout_date": (
                loan.checkout_date.isoformat() if loan.checkout_date else None
            ),
            "due_date": loan.due_date.isoformat() if loan.due_date else None,
            "return_date": loan.return_date.isoformat() if loan.return_date else None,
            "fines": float(loan.fines),
        }
        list_loan.append(loan_data)

    return jsonify(list_loan)

#retrieve specific loan by id 
@loan.route("/loan/<int:loan_id>/", methods=["GET"])
def get_loan_by_id(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    return jsonify(
        {
            "id": loan.id,
            "book_id": loan.book_id,
            "user_id": loan.user_id,
            "checkout_date": (
                loan.checkout_date.isoformat() if loan.checkout_date else None
            ),
            "due_date": loan.due_date.isoformat() if loan.due_date else None,
            "return_date": loan.return_date.isoformat() if loan.return_date else None,
            "fines": float(loan.fines),
        }
    )

#return and calculate fines
@loan.route("/loans/<int:loan_id>/return", methods=["POST"])
def return_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)

    loan.return_date = datetime.utcnow()
    
    # Update the fines based on the return date
    loan.update_fines()

    fines_amount = loan.fines if loan.fines is not None else 0.00
    return jsonify({"message": "Book returned successfully", "fines": fines_amount}), 200


#checks if the a loan exists for that specific book
@loan.route("/loans/book/<int:book_id>", methods=["GET"])
def get_loan_id_for_book(book_id):
    loan = Loan.query.filter_by(book_id=book_id).first()
    if loan:
        return jsonify({"loan_id": loan.id})
    else:
        return jsonify({"error": "Loan not found"}), 404