"""
Dashboard CRUD operations for database entities.

This module contains all dashboard-related database operations for aggregating
data from multiple domains (categories, expenses, transactions, etc.).
"""

from datetime import datetime, timezone
from typing import List
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from ..models.category import Category
from ..models.category_budget import CategoryBudget
from ..models.expense import Expense
from ..models.transaction import Transaction


def get_categories_dashboard(db: Session, user_id: int, month: str) -> List[dict]:
    """
    Get categories with budget and total spent for dashboard display.
    
    Args:
        db: Database session
        user_id: ID of the user
        month: Month in YYYY-MM format
        
    Returns:
        List of dictionaries with category id, name, totalSpent, and budget
    """
    # Get all categories for the user
    categories = db.query(Category).filter(Category.user_id == user_id).all()
    
    result = []
    
    for category in categories:
        # Get budget allocation for this category and month
        budget_query = db.query(CategoryBudget).filter(
            and_(
                CategoryBudget.user_id == user_id,
                CategoryBudget.category_id == category.id,
                CategoryBudget.month == month
            )
        ).first()
        
        budget_amount = budget_query.allocated_amount if budget_query else None
        
        # Get total spent for this category in the given month
        # Join: Category -> Expense -> Transaction
        total_spent = db.query(func.sum(Transaction.amount)).join(
            Expense, Transaction.expense_id == Expense.id
        ).filter(
            and_(
                Expense.category_id == category.id,
                Expense.user_id == user_id,
                func.to_char(Transaction.transaction_date, 'YYYY-MM') == month
            )
        ).scalar() or Decimal('0.00')
        
        result.append({
            'id': category.id,
            'name': category.name,
            'totalSpent': total_spent,
            'budget': budget_amount
        })
    
    return result