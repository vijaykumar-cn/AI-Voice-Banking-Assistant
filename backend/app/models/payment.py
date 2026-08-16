from datetime import date
from sqlalchemy import Date, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)

    payment_id: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        index=True
    )

    loan_id: Mapped[int] = mapped_column(
        ForeignKey("loans.id")
    )

    amount: Mapped[float] = mapped_column(Float)

    payment_date: Mapped[date] = mapped_column(Date)

    payment_method: Mapped[str] = mapped_column(String(30))

    payment_status: Mapped[str] = mapped_column(String(20))

    loan = relationship(
        "Loan",
        back_populates="payments"
    )