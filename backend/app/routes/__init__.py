# Routes package - organized by domain

# Import all routers
from .user import router as user_router
from .category import router as category_router
from .expense import router as expense_router
from .category_budget import router as category_budget_router
from .transaction import router as transaction_router
from .auth import router as auth_router
from .dashboard import router as dashboard_router

# Export all routers for easy access
__all__ = [
    "user_router",
    "category_router",
    "expense_router",
    "category_budget_router",
    "transaction_router",
    "auth_router",
    "dashboard_router",
]