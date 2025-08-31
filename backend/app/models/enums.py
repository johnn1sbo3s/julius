"""
Enums used across the application models.
"""

import enum


class UserRole(str, enum.Enum):
    """User role enumeration for role-based access control."""
    
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    
    def __str__(self) -> str:
        return self.value