"""
CRUD operations for database entities.

This module contains all the database operations (Create, Read, Update, Delete)
separated from the API routes for better organization and testability.
"""

from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from . import models, schemas


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

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Get a user by ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get a user by email address."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Get multiple users with pagination."""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
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
    db_user = models.User(
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


def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Optional[models.User]:
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


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
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


# =============================================================================
# CATEGORY CRUD OPERATIONS
# =============================================================================

def get_category(db: Session, category_id: int, user_id: int) -> Optional[models.Category]:
    """Get a category by ID, ensuring it belongs to the specified user."""
    return db.query(models.Category).filter(
        and_(models.Category.id == category_id, models.Category.user_id == user_id)
    ).first()


def get_categories(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Category]:
    """Get categories for a specific user with pagination."""
    return db.query(models.Category).filter(
        models.Category.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_category_by_name(db: Session, user_id: int, name: str) -> Optional[models.Category]:
    """Get a category by name for a specific user."""
    return db.query(models.Category).filter(
        and_(models.Category.user_id == user_id, models.Category.name == name)
    ).first()


def create_category(db: Session, category: schemas.CategoryCreate, user_id: int) -> models.Category:
    """
    Create a new category for a user.
    
    Args:
        db: Database session
        category: Category data from API request
        user_id: ID of the user creating the category
        
    Returns:
        Created category model
        
    Raises:
        ValueError: If category with name already exists for this user
    """
    # Check if category already exists for this user
    if get_category_by_name(db, user_id, category.name):
        raise ValueError(f"Category '{category.name}' already exists for this user")
    
    # Create category model
    db_category = models.Category(
        name=category.name,
        user_id=user_id,
        created_at=datetime.now(timezone.utc)
    )
    
    # Save to database
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


def update_category(db: Session, category_id: int, user_id: int, category: schemas.CategoryUpdate) -> Optional[models.Category]:
    """
    Update category information.
    
    Args:
        db: Database session
        category_id: ID of category to update
        user_id: ID of the user who owns the category
        category: Updated category data
        
    Returns:
        Updated category model or None if category not found
        
    Raises:
        ValueError: If trying to update to a name that already exists for this user
    """
    db_category = get_category(db, category_id, user_id)
    if not db_category:
        return None
    
    # Check if name is being updated and if it already exists
    if category.name and category.name != db_category.name:
        existing_category = get_category_by_name(db, user_id, category.name)
        if existing_category:
            raise ValueError(f"Category '{category.name}' already exists for this user")
    
    # Update only provided fields
    update_data = category.model_dump(exclude_unset=True)
    
    # Apply updates
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    
    return db_category


def delete_category(db: Session, category_id: int, user_id: int) -> bool:
    """
    Delete a category.
    
    Args:
        db: Database session
        category_id: ID of category to delete
        user_id: ID of the user who owns the category
        
    Returns:
        True if category was deleted, False if category not found
    """
    db_category = get_category(db, category_id, user_id)
    if not db_category:
        return False
    
    db.delete(db_category)
    db.commit()
    
    return True