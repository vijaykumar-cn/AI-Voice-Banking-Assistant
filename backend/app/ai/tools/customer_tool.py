from langchain_core.tools import tool

from app.database.session import SessionLocal
from app.services.customer_service import CustomerService


@tool
def verify_customer(customer_id: str):
    """
    Verify customer by customer ID.
    """

    db = SessionLocal()

    try:

        service = CustomerService(db)

        customer = service.get_customer(customer_id)

        if customer is None:
            return {
                "authenticated": False
            }

        return {
            "authenticated": True,
            "id": customer.id,
            "customer_id": customer.customer_id,
            "customer_name": customer.name,
        }

    finally:
        db.close()