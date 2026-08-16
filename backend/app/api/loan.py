from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.loan import LoanCreate, LoanResponse
from app.services.loan_service import LoanService

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/", response_model=LoanResponse)
def create_loan(
    loan: LoanCreate,
    db: Session = Depends(get_db),
):
    service = LoanService(db)
    return service.create_loan(loan)


@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(
    loan_id: str,
    db: Session = Depends(get_db),
):
    service = LoanService(db)

    loan = service.get_loan(loan_id)

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )

    return loan


@router.get("/customer/{customer_id}", response_model=list[LoanResponse])
def get_customer_loans(
    customer_id: int,
    db: Session = Depends(get_db),
):
    service = LoanService(db)
    return service.get_customer_loans(customer_id)