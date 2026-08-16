from datetime import date
from pydantic import BaseModel


class LoanCreate(BaseModel):
    loan_id: str
    customer_id: int
    loan_type: str
    loan_amount: float
    remaining_amount: float
    interest_rate: float
    emi_amount: float
    next_due_date: date
    status: str


class LoanResponse(LoanCreate):
    id: int

    class Config:
        from_attributes = True