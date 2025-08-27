"""
Expense Budget CRUD operations for database entities.

This module contains all expense budget-related database operations (Create, Read, Update, Delete)
separated from the API routes for better organization and testability.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models import ExpenseBudget, Expense
from ..schemas.expense_budget import ExpenseBudgetCreate, ExpenseBudgetUpdate
from .expense import get_expense


def get_expense_budget(db: Session, budget_id: int, user_id: int) -> Optional[ExpenseBudget]:
    """Get an expense budget by ID, ensuring it belongs to the specified user."""
    return db.query(ExpenseBudget).join(Expense).filter(
        and_(ExpenseBudget.id == budget_id, Expense.user_id == user_id)
    ).first()


def get_expense_budgets(db: Session, user_id: int, expense_id: Optional[int] = None, month: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[ExpenseBudget]:
    """Get expense budgets for a specific user with optional filtering."""
    query = db.query(ExpenseBudget).join(Expense).filter(Expense.user_id == user_id)
    
    if expense_id:
        query = query.filter(ExpenseBudget.expense_id == expense_id)
    
    if month:
        query = query.filter(ExpenseBudget.month == month)
    
    return query.offset(skip).limit(limit).all()


def get_expense_budget_by_month(db: Session, expense_id: int, month: str, user_id: int) -> Optional[ExpenseBudget]:
    """Get an expense budget by expense and month."""
    return db.query(ExpenseBudget).join(Expense).filter(
        and_(
            ExpenseBudget.expense_id == expense_id,
            ExpenseBudget.month == month,
            Expense.user_id == user_id
        )
    ).first()


def create_expense_budget(db: Session, budget: ExpenseBudgetCreate, user_id: int) -> ExpenseBudget:
    """
    Create a new expense budget.
    
    Args:
        db: Database session
        budget: Budget data from API request
        user_id: ID of the user creating the budget
        
    Returns:
        Created budget model
        
    Raises:
        ValueError: If budget already exists for this expense and month
    """
    # Verify that the expense belongs to the user
    expense = get_expense(db, budget.expense_id, user_id)
    if not expense:
        raise ValueError(f"Expense with ID {budget.expense_id} not found for this user")
    
    # Check if budget already exists for this expense and month
    if get_expense_budget_by_month(db, budget.expense_id, budget.month, user_id):
        raise ValueError(f"Budget for expense '{expense.name}' already exists for month {budget.month}")
    
    # Create budget model
    db_budget = ExpenseBudget(
        expense_id=budget.expense_id,
        month=budget.month,
        budget=budget.budget
    )
    
    # Save to database
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    
    return db_budget


def update_expense_budget(db: Session, budget_id: int, user_id: int, budget: ExpenseBudgetUpdate) -> Optional[ExpenseBudget]:
    """
    Update expense budget information.
    
    Args:
        db: Database session
        budget_id: ID of budget to update
        user_id: ID of the user who owns the budget
        budget: Updated budget data
        
    Returns:
        Updated budget model or None if budget not found
    """
    db_budget = get_expense_budget(db, budget_id, user_id)
    if not db_budget:
        return None
    
    # Update only provided fields
    update_data = budget.model_dump(exclude_unset=True)
    
    # Apply updates
    for field, value in update_data.items():
        setattr(db_budget, field, value)
    
    db.commit()
    db.refresh(db_budget)
    
    return db_budget


def delete_expense_budget(db: Session, budget_id: int, user_id: int) -> bool:
    """
    Delete an expense budget.
    
    Args:
        db: Database session
        budget_id: ID of budget to delete
        user_id: ID of the user who owns the budget
        
    Returns:
        True if budget was deleted, False if budget not found
    """
    db_budget = get_expense_budget(db, budget_id, user_id)
    if not db_budget:
        return False
    
    db.delete(db_budget)
    db.commit()
    
    return True