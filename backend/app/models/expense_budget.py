"""
ExpenseBudget model for tracking budget allocations.
"""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .expense import Expense


class ExpenseBudget(Base):
    """ExpenseBudget model for tracking budget allocations."""
    
    __tablename__: str = "expense_budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    expense_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("expenses.id"), nullable=False
    )
    month: Mapped[str] = mapped_column(String(7), nullable=False)
    budget: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Relationships
    expense: Mapped["Expense"] = relationship(back_populates="budgets")