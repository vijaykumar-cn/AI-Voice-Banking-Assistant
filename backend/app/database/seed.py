from datetime import date

from app.database.session import SessionLocal
from app.models.customer import Customer
from app.models.loan import Loan

db = SessionLocal()

try:
    # Check if customer already exists
    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == "CUST1001")
        .first()
    )

    if customer is None:
        customer = Customer(
            customer_id="CUST1001",
            name="Vijay Kumar",
            phone="9876543210",
            email="vijay@example.com",
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        print("✅ Customer created")

    else:
        print("✅ Customer already exists")

    # Check if loan already exists
    loan = (
        db.query(Loan)
        .filter(Loan.loan_id == "LN1001")
        .first()
    )

    if loan is None:
        loan = Loan(
            loan_id="LN1001",
            customer_id=customer.id,
            loan_type="Home Loan",
            loan_amount=1000000,
            remaining_amount=750000,
            interest_rate=8.5,
            emi_amount=18500,
            next_due_date=date(2026, 9, 5),
            status="ACTIVE",
        )

        db.add(loan)
        db.commit()

        print("✅ Loan created")

    else:
        print("✅ Loan already exists")

finally:
    db.close()

print("✅ Seed completed")