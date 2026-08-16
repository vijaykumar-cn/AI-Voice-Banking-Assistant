from langchain_core.tools import tool

from app.database.session import SessionLocal
from app.services.loan_service import LoanService


LOAN_TYPES = [
    {
        "loan_type": "Home Loan",
        "description": "For purchasing or renovating residential property.",
    },
    {
        "loan_type": "Personal Loan",
        "description": "Unsecured loan for personal expenses such as wedding, medical, or travel.",
    },
    {
        "loan_type": "Car Loan",
        "description": "For purchasing a new or used vehicle.",
    },
    {
        "loan_type": "Education Loan",
        "description": "For tuition fees and other education-related expenses.",
    },
    {
        "loan_type": "Business Loan",
        "description": "For business expansion, working capital, or startup needs.",
    },
]


@tool
def get_loan_types():
    """
    Return the loan products offered by ABC Bank.
    Use this tool when the user asks about available loan types or loan offerings.
    """

    return {
        "loan_types": LOAN_TYPES
    }


@tool
def get_customer_loan(customer_id: int):
    """
    Get loan information for a customer.
    """

    db = SessionLocal()

    try:
        service = LoanService(db)

        loan = service.get_customer_loan(customer_id)

        if loan is None:
            return {
                "error": "Loan not found"
            }

        return {
            "loan_type": loan.loan_type,
            "loan_amount": loan.loan_amount,
            "remaining_amount": loan.remaining_amount,
            "emi": loan.emi_amount,
            "interest": loan.interest_rate,
            "due_date": str(loan.next_due_date),
        }

    finally:
        db.close()