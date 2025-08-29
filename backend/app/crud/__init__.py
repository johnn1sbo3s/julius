"""
CRUD package for database operations.

This package contains all database operations organized by domain.
"""

# User CRUD operations
from .user import (
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

# Category Budget CRUD operations
from .category_budget import (
    get_category_budget,
    get_category_budgets_by_month,
    get_category_budgets_by_category,
    create_category_budget,
    update_category_budget,
    delete_category_budget,
    delete_category_budgets_by_month,
    create_or_update_monthly_budget,
    get_monthly_budget_summary,
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
    # Category Budget operations
    "get_category_budget",
    "get_category_budgets_by_month",
    "get_category_budgets_by_category",
    "create_category_budget",
    "update_category_budget",
    "delete_category_budget",
    "delete_category_budgets_by_month",
    "create_or_update_monthly_budget",
    "get_monthly_budget_summary",
    # Transaction operations
    "get_transaction",
    "get_transactions",
    "create_transaction",
    "update_transaction",
    "delete_transaction",
    "get_monthly_summary",
]