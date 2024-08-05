from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Loan
from datetime import datetime, timedelta

loan = Blueprint("loan", __name__)


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


@loan.route("/loans/<int:loan_id>/return", methods=["POST"])
def return_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    loan.return_date = datetime.utcnow()
    loan.update_fines()

    return jsonify({"message": "Book returned successfully", "fines": loan.fines}), 200
