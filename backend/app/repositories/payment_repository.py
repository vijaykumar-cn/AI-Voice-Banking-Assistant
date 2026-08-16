from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_payments(self, loan_id: int):
        return (
            self.db.query(Payment)
            .filter(Payment.loan_id == loan_id)
            .all()
        )