"""
User model for authentication and user management.
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import UserRole

if TYPE_CHECKING:
    from .category import Category
    from .category_budget import CategoryBudget


class User(Base):
    """User model for storing user information."""
    
    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[UserRole] = mapped_column(String(20), nullable=False, default=UserRole.USER, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    categories: Mapped[list["Category"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    category_budgets: Mapped[list["CategoryBudget"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == UserRole.ADMIN
    
    def is_moderator(self) -> bool:
        """Check if user has moderator role or higher."""
        return self.role in (UserRole.ADMIN, UserRole.MODERATOR)
    
    def has_permission(self, required_role: UserRole) -> bool:
        """Check if user has the required role or higher permission level."""
        role_hierarchy = {
            UserRole.USER: 0,
            UserRole.MODERATOR: 1,
            UserRole.ADMIN: 2
        }
        return role_hierarchy.get(self.role, 0) >= role_hierarchy.get(required_role, 0)