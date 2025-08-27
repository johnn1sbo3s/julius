"""
Expense CRUD operations for database entities.

This module contains all expense-related database operations (Create, Read, Update, Delete)
separated from the API routes for better organization and testability.
"""

from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models import Expense
from ..schemas.expense import ExpenseCreate, ExpenseUpdate
from .category import get_category


def get_expense(db: Session, expense_id: int, user_id: int) -> Optional[Expense]:
    """Get an expense by ID, ensuring it belongs to the specified user."""
    return db.query(Expense).filter(
        and_(Expense.id == expense_id, Expense.user_id == user_id)
    ).first()


def get_expenses(db: Session, user_id: int, category_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Expense]:
    """Get expenses for a specific user with optional category filtering."""
    query = db.query(Expense).filter(Expense.user_id == user_id)
    
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    
    return query.offset(skip).limit(limit).all()


def get_expense_by_name(db: Session, user_id: int, name: str, category_id: Optional[int] = None) -> Optional[Expense]:
    """Get an expense by name for a specific user and optionally category."""
    query = db.query(Expense).filter(
        and_(Expense.user_id == user_id, Expense.name == name)
    )
    
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    
    return query.first()


def create_expense(db: Session, expense: ExpenseCreate, user_id: int) -> Expense:
    """
    Create a new expense for a user.
    
    Args:
        db: Database session
        expense: Expense data from API request
        user_id: ID of the user creating the expense
        
    Returns:
        Created expense model
        
    Raises:
        ValueError: If expense with name already exists for this user in the same category
    """
    # Check if expense already exists for this user in the same category
    if get_expense_by_name(db, user_id, expense.name, expense.category_id):
        raise ValueError(f"Expense '{expense.name}' already exists in this category for this user")
    
    # Verify that the category belongs to the user
    category = get_category(db, expense.category_id, user_id)
    if not category:
        raise ValueError(f"Category with ID {expense.category_id} not found for this user")
    
    # Create expense model
    db_expense = Expense(
        name=expense.name,
        category_id=expense.category_id,
        user_id=user_id,
        created_at=datetime.now(timezone.utc)
    )
    
    # Save to database
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    return db_expense


def update_expense(db: Session, expense_id: int, user_id: int, expense: ExpenseUpdate) -> Optional[Expense]:
    """
    Update expense information.
    
    Args:
        db: Database session
        expense_id: ID of expense to update
        user_id: ID of the user who owns the expense
        expense: Updated expense data
        
    Returns:
        Updated expense model or None if expense not found
        
    Raises:
        ValueError: If trying to update to a name that already exists
    """
    db_expense = get_expense(db, expense_id, user_id)
    if not db_expense:
        return None
    
    # Check if name is being updated and if it already exists
    if expense.name and expense.name != db_expense.name:
        existing_expense = get_expense_by_name(db, user_id, expense.name, expense.category_id or db_expense.category_id)
        if existing_expense:
            raise ValueError(f"Expense '{expense.name}' already exists in this category for this user")
    
    # Verify category belongs to user if being updated
    if expense.category_id and expense.category_id != db_expense.category_id:
        category = get_category(db, expense.category_id, user_id)
        if not category:
            raise ValueError(f"Category with ID {expense.category_id} not found for this user")
    
    # Update only provided fields
    update_data = expense.model_dump(exclude_unset=True)
    
    # Apply updates
    for field, value in update_data.items():
        setattr(db_expense, field, value)
    
    db.commit()
    db.refresh(db_expense)
    
    return db_expense


def delete_expense(db: Session, expense_id: int, user_id: int) -> bool:
    """
    Delete an expense.
    
    Args:
        db: Database session
        expense_id: ID of expense to delete
        user_id: ID of the user who owns the expense
        
    Returns:
        True if expense was deleted, False if expense not found
    """
    db_expense = get_expense(db, expense_id, user_id)
    if not db_expense:
        return False
    
    db.delete(db_expense)
    db.commit()
    
    return True