"""
CRUD package for database operations.

This package contains all database operations organized by domain.
"""

# User CRUD operations
from .user import (
    get_password_hash,
    verify_password,
    get_user,
    get_user_by_email,
    get_users,
    create_user,
    update_user,
    delete_user,
    authenticate_user,
)

# Category CRUD operations
from .category import (
    get_category,
    get_categories,
    get_category_by_name,
    create_category,
    update_category,
    delete_category,
)

# Expense CRUD operations
from .expense import (
    get_expense,
    get_expenses,
    get_expense_by_name,
    create_expense,
    update_expense,
    delete_expense,
)

# Expense Budget CRUD operations
from .expense_budget import (
    get_expense_budget,
    get_expense_budgets,
    get_expense_budget_by_month,
    create_expense_budget,
    update_expense_budget,
    delete_expense_budget,
)

# Transaction CRUD operations
from .transaction import (
    get_transaction,
    get_transactions,
    create_transaction,
    update_transaction,
    delete_transaction,
    get_monthly_summary,
)

__all__ = [
    # User operations
    "get_password_hash",
    "verify_password",
    "get_user",
    "get_user_by_email",
    "get_users",
    "create_user",
    "update_user",
    "delete_user",
    "authenticate_user",
    # Category operations
    "get_category",
    "get_categories",
    "get_category_by_name",
    "create_category",
    "update_category",
    "delete_category",
    # Expense operations
    "get_expense",
    "get_expenses",
    "get_expense_by_name",
    "create_expense",
    "update_expense",
    "delete_expense",
    # Expense Budget operations
    "get_expense_budget",
    "get_expense_budgets",
    "get_expense_budget_by_month",
    "create_expense_budget",
    "update_expense_budget",
    "delete_expense_budget",
    # Transaction operations
    "get_transaction",
    "get_transactions",
    "create_transaction",
    "update_transaction",
    "delete_transaction",
    "get_monthly_summary",
]