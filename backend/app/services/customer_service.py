from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate


class CustomerService:

    def __init__(self, db: Session):
        self.repository = CustomerRepository(db)

    def create_customer(self, customer: CustomerCreate):

        db_customer = Customer(
            customer_id=customer.customer_id,
            name=customer.name,
            phone=customer.phone,
            email=customer.email,
        )

        return self.repository.create(db_customer)

    def get_customer(self, customer_id: str):
        return self.repository.get_by_customer_id(customer_id)