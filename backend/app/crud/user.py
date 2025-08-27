"""
User CRUD operations for database entities.

This module contains all user-related database operations (Create, Read, Update, Delete)
separated from the API routes for better organization and testability.
"""

from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session

from ..models import User
from ..schemas.user import UserCreate, UserUpdate


# =============================================================================
# PASSWORD UTILITIES
# =============================================================================

def get_password_hash(password: str) -> str:
    """Hash a password for storing in the database."""
    # For now, we'll use a simple approach. In Phase 5, we'll implement proper hashing
    # TODO: Replace with proper bcrypt hashing in Phase 5
    return f"hashed_{password}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    # For now, simple verification. Will be replaced with bcrypt in Phase 5
    # TODO: Replace with proper bcrypt verification in Phase 5
    return hashed_password == f"hashed_{plain_password}"


# =============================================================================
# USER CRUD OPERATIONS
# =============================================================================

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email address."""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get multiple users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        db: Database session
        user: User data from API request
        
    Returns:
        Created user model
        
    Raises:
        ValueError: If user with email already exists
    """
    # Check if user already exists
    if get_user_by_email(db, user.email):
        raise ValueError(f"User with email {user.email} already exists")
    
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Create user model
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        created_at=datetime.now(timezone.utc)
    )
    
    # Save to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
    """
    Update user information.
    
    Args:
        db: Database session
        user_id: ID of user to update
        user: Updated user data
        
    Returns:
        Updated user model or None if user not found
        
    Raises:
        ValueError: If trying to update to an email that already exists
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    # Check if email is being updated and if it already exists
    if user.email and user.email != db_user.email:
        existing_user = get_user_by_email(db, user.email)
        if existing_user:
            raise ValueError(f"User with email {user.email} already exists")
    
    # Update only provided fields
    update_data = user.model_dump(exclude_unset=True)
    
    # Hash password if being updated
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    # Apply updates
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user.
    
    Args:
        db: Database session
        user_id: ID of user to delete
        
    Returns:
        True if user was deleted, False if user not found
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    
    return True


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user with email and password.
    
    Args:
        db: Database session
        email: User's email
        password: User's password
        
    Returns:
        User model if authentication successful, None otherwise
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user