"""
Transaction CRUD operations for database entities.

This module contains all transaction-related database operations (Create, Read, Update, Delete)
separated from the API routes for better organization and testability.
"""

from datetime import datetime, timezone, date
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from ..models import Transaction, Expense, Category
from ..schemas.transaction import TransactionCreate, TransactionUpdate
from .expense import get_expense


def get_transaction(db: Session, transaction_id: int, user_id: int) -> Optional[Transaction]:
    """Get a transaction by ID, ensuring it belongs to the specified user."""
    return db.query(Transaction).filter(
        and_(Transaction.id == transaction_id, Transaction.user_id == user_id)
    ).first()


def get_transactions(
    db: Session, 
    user_id: int, 
    expense_id: Optional[int] = None,
    category_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[Transaction]:
    """Get transactions for a specific user with advanced filtering."""
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    
    # Filter by expense
    if expense_id:
        query = query.filter(Transaction.expense_id == expense_id)
    
    # Filter by category (through expense)
    if category_id:
        query = query.join(Expense).filter(Expense.category_id == category_id)
    
    # Filter by date range
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    
    # Filter by amount range
    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)
    
    # Order by date (most recent first)
    query = query.order_by(Transaction.transaction_date.desc())
    
    return query.offset(skip).limit(limit).all()


def create_transaction(db: Session, transaction: TransactionCreate, user_id: int) -> Transaction:
    """
    Create a new transaction.
    
    Args:
        db: Database session
        transaction: Transaction data from API request
        user_id: ID of the user creating the transaction
        
    Returns:
        Created transaction model
        
    Raises:
        ValueError: If expense doesn't belong to the user
    """
    # Verify that the expense belongs to the user
    expense = get_expense(db, transaction.expense_id, user_id)
    if not expense:
        raise ValueError(f"Expense with ID {transaction.expense_id} not found for this user")
    
    # Set transaction date to current date if not provided
    transaction_date = transaction.transaction_date or date.today()
    
    # Create transaction model
    db_transaction = Transaction(
        expense_id=transaction.expense_id,
        user_id=user_id,
        amount=transaction.amount,
        description=transaction.description,
        transaction_date=transaction_date,
        created_at=datetime.now(timezone.utc)
    )
    
    # Save to database
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction


def update_transaction(db: Session, transaction_id: int, user_id: int, transaction: TransactionUpdate) -> Optional[Transaction]:
    """
    Update transaction information.
    
    Args:
        db: Database session
        transaction_id: ID of transaction to update
        user_id: ID of the user who owns the transaction
        transaction: Updated transaction data
        
    Returns:
        Updated transaction model or None if transaction not found
    """
    db_transaction = get_transaction(db, transaction_id, user_id)
    if not db_transaction:
        return None
    
    # Update only provided fields
    update_data = transaction.model_dump(exclude_unset=True)
    
    # Apply updates
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction


def delete_transaction(db: Session, transaction_id: int, user_id: int) -> bool:
    """
    Delete a transaction.
    
    Args:
        db: Database session
        transaction_id: ID of transaction to delete
        user_id: ID of the user who owns the transaction
        
    Returns:
        True if transaction was deleted, False if transaction not found
    """
    db_transaction = get_transaction(db, transaction_id, user_id)
    if not db_transaction:
        return False
    
    db.delete(db_transaction)
    db.commit()
    
    return True


def get_monthly_summary(db: Session, user_id: int, month: str) -> dict:
    """
    Get monthly spending summary for a user.
    
    Args:
        db: Database session
        user_id: ID of the user
        month: Month in YYYY-MM format
        
    Returns:
        Dictionary with spending summary
    """
    start_date = datetime.strptime(f"{month}-01", "%Y-%m-%d").date()
    if month.endswith("-12"):
        year = int(month[:4]) + 1
        end_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d").date()
    else:
        month_num = int(month[-2:]) + 1
        year = month[:4]
        end_date = datetime.strptime(f"{year}-{month_num:02d}-01", "%Y-%m-%d").date()
    
    # Get total spending by category
    category_totals = db.query(
        Category.name,
        func.sum(Transaction.amount).label('total')
    ).join(Expense).join(Transaction).filter(
        and_(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date < end_date
        )
    ).group_by(Category.id, Category.name).all()
    
    # Get total spending
    total_spending = db.query(func.sum(Transaction.amount)).filter(
        and_(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date < end_date
        )
    ).scalar() or 0
    
    return {
        "month": month,
        "total_spending": float(total_spending),
        "categories": [{
            "name": name,
            "total": float(total)
        } for name, total in category_totals]
    }