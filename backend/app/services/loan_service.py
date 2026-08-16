from sqlalchemy.orm import Session

from app.repositories.loan_repository import LoanRepository


class LoanService:

    def __init__(self, db: Session):
        self.repository = LoanRepository(db)

    def get_customer_loan(self, customer_id: int):
        return self.repository.get_by_customer_id(customer_id)