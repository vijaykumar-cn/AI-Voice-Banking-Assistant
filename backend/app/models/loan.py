from datetime import date
from sqlalchemy import Date, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)

    loan_id: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id")
    )

    loan_type: Mapped[str] = mapped_column(String(50))

    loan_amount: Mapped[float] = mapped_column(Float)

    remaining_amount: Mapped[float] = mapped_column(Float)

    interest_rate: Mapped[float] = mapped_column(Float)

    emi_amount: Mapped[float] = mapped_column(Float)

    next_due_date: Mapped[date] = mapped_column(Date)

    status: Mapped[str] = mapped_column(String(20))

    customer = relationship("Customer", back_populates="loans")

    payments = relationship(
        "Payment",
        back_populates="loan",
        cascade="all, delete-orphan"
    )