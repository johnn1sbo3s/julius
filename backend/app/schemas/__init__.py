"""
Schemas package for Pydantic data validation and serialization.

This package contains all Pydantic schemas organized by domain.
"""

from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
)
from .auth import (
    Token,
    TokenData,
    LoginRequest,
)
from .category import (
    CategoryBase,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)
from .expense import (
    ExpenseBase,
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
)
from .category_budget import (
    CategoryBudgetBase,
    CategoryBudgetCreate,
    CategoryBudgetUpdate,
    CategoryBudgetResponse,
    CategoryBudgetWithCategory,
    MonthlyBudgetAllocation,
    MonthlyBudgetSummary,
)
from .transaction import (
    TransactionBase,
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    # Authentication schemas
    "Token",
    "TokenData",
    "LoginRequest",
    # Category schemas
    "CategoryBase",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryResponse",
    # Expense schemas
    "ExpenseBase",
    "ExpenseCreate",
    "ExpenseUpdate",
    "ExpenseResponse",
    # Category Budget schemas
    "CategoryBudgetBase",
    "CategoryBudgetCreate",
    "CategoryBudgetUpdate",
    "CategoryBudgetResponse",
    "CategoryBudgetWithCategory",
    "MonthlyBudgetAllocation",
    "MonthlyBudgetSummary",
    # Transaction schemas
    "TransactionBase",
    "TransactionCreate",
    "TransactionUpdate",
    "TransactionResponse",
]