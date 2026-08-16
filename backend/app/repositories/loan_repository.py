from sqlalchemy.orm import Session

from app.models.loan import Loan


class LoanRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_customer_id(self, customer_id: int):
        return (
            self.db.query(Loan)
            .filter(Loan.customer_id == customer_id)
            .first()
        )

    def get_by_loan_id(self, loan_id: str):
        return (
            self.db.query(Loan)
            .filter(Loan.loan_id == loan_id)
            .first()
        )