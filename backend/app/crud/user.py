"""
User CRUD operations for database entities.

This module contains all user-related database operations (Create, Read, Update, Delete)
separated from the API routes for better organization and testability.
"""

from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session

from ..models import User, Category, Expense
from ..schemas.user import UserCreate, UserUpdate
from ..security import get_password_hash, verify_password


# =============================================================================
# DEFAULT DATA INITIALIZATION
# =============================================================================

def _create_default_categories_and_expenses(db: Session, user_id: int) -> None:
    """
    Create default categories and expenses for a new user.
    
    This function creates predefined categories with their associated expenses:
    - Alimentação: delivery, janta, almoço
    - Transporte: uber, gasolina, manutenção
    - Gastos Fixos: energia, internet, mercado, aluguel, celular
    - Compras: roupas, jogos
    - Lazer: (empty category for user to add their own expenses)
    
    Args:
        db: Database session
        user_id: ID of the newly created user
    """
    # Define default categories and their expenses
    default_data = {
        "Alimentação": ["delivery", "janta", "almoço"],
        "Transporte": ["uber", "gasolina", "manutenção"],
        "Gastos Fixos": ["energia", "internet", "mercado", "aluguel", "celular"],
        "Compras": ["roupas", "jogos"],
        "Lazer": []  # Empty category for user customization
    }
    
    for category_name, expense_names in default_data.items():
        # Create category
        category = Category(
            name=category_name,
            user_id=user_id,
            created_at=datetime.now(timezone.utc)
        )
        db.add(category)
        db.flush()  # Flush to get the category ID
        
        # Create expenses for this category
        for expense_name in expense_names:
            expense = Expense(
                name=expense_name,
                category_id=category.id,
                user_id=user_id,
                created_at=datetime.now(timezone.utc)
            )
            db.add(expense)
    
    # Commit all changes
    db.commit()


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
    Create a new user with default categories and expenses.
    
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
    
    # Save user to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create default categories and expenses for the new user
    _create_default_categories_and_expenses(db, db_user.id)
    
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