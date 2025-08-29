"""
CategoryBudget model for monthly budget allocation per category.
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .category import Category


class CategoryBudget(Base):
    """
    Model for monthly budget allocation per category.
    
    This represents how much of the total monthly budget
    is allocated to each category.
    """
    __tablename__: str = "category_budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    month: Mapped[str] = mapped_column(String(7), nullable=False)  # YYYY-MM format
    allocated_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="category_budgets")
    category: Mapped["Category"] = relationship(back_populates="budgets")
    
    def __repr__(self) -> str:
        return f"<CategoryBudget(id={self.id}, category_id={self.category_id}, month='{self.month}', amount={self.allocated_amount})>"