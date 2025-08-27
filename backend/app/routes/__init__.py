# Routes package - organized by domain

# Import all routers
from .user import router as user_router

# Export all routers for easy access
__all__ = [
    "user_router",
]