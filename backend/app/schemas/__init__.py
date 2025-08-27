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
from .expense_budget import (
    ExpenseBudgetBase,
    ExpenseBudgetCreate,
    ExpenseBudgetUpdate,
    ExpenseBudgetResponse,
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
    # Expense Budget schemas
    "ExpenseBudgetBase",
    "ExpenseBudgetCreate",
    "ExpenseBudgetUpdate",
    "ExpenseBudgetResponse",
    # Transaction schemas
    "TransactionBase",
    "TransactionCreate",
    "TransactionUpdate",
    "TransactionResponse",
]