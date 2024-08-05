from app import create_app
from app.models import Loan, db


app = create_app()


with app.app_context():
    Loan.query.delete()
    db.session.commit()
