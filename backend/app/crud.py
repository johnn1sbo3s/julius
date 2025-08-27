"""
CRUD operations for database entities.

This module contains all the database operations (Create, Read, Update, Delete)
separated from the API routes for better organization and testability.
"""

from datetime import datetime, timezone, date
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

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


# =============================================================================
# EXPENSE CRUD OPERATIONS
# =============================================================================

def get_expense(db: Session, expense_id: int, user_id: int) -> Optional[models.Expense]:
    """Get an expense by ID, ensuring it belongs to the specified user."""
    return db.query(models.Expense).filter(
        and_(models.Expense.id == expense_id, models.Expense.user_id == user_id)
    ).first()


def get_expenses(db: Session, user_id: int, category_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[models.Expense]:
    """Get expenses for a specific user with optional category filtering."""
    query = db.query(models.Expense).filter(models.Expense.user_id == user_id)
    
    if category_id:
        query = query.filter(models.Expense.category_id == category_id)
    
    return query.offset(skip).limit(limit).all()


def get_expense_by_name(db: Session, user_id: int, name: str, category_id: Optional[int] = None) -> Optional[models.Expense]:
    """Get an expense by name for a specific user and optionally category."""
    query = db.query(models.Expense).filter(
        and_(models.Expense.user_id == user_id, models.Expense.name == name)
    )
    
    if category_id:
        query = query.filter(models.Expense.category_id == category_id)
    
    return query.first()


def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int) -> models.Expense:
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
    db_expense = models.Expense(
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


def update_expense(db: Session, expense_id: int, user_id: int, expense: schemas.ExpenseUpdate) -> Optional[models.Expense]:
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


# =============================================================================
# EXPENSE BUDGET CRUD OPERATIONS
# =============================================================================

def get_expense_budget(db: Session, budget_id: int, user_id: int) -> Optional[models.ExpenseBudget]:
    """Get an expense budget by ID, ensuring it belongs to the specified user."""
    return db.query(models.ExpenseBudget).join(models.Expense).filter(
        and_(models.ExpenseBudget.id == budget_id, models.Expense.user_id == user_id)
    ).first()


def get_expense_budgets(db: Session, user_id: int, expense_id: Optional[int] = None, month: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[models.ExpenseBudget]:
    """Get expense budgets for a specific user with optional filtering."""
    query = db.query(models.ExpenseBudget).join(models.Expense).filter(models.Expense.user_id == user_id)
    
    if expense_id:
        query = query.filter(models.ExpenseBudget.expense_id == expense_id)
    
    if month:
        query = query.filter(models.ExpenseBudget.month == month)
    
    return query.offset(skip).limit(limit).all()


def get_expense_budget_by_month(db: Session, expense_id: int, month: str, user_id: int) -> Optional[models.ExpenseBudget]:
    """Get an expense budget by expense and month."""
    return db.query(models.ExpenseBudget).join(models.Expense).filter(
        and_(
            models.ExpenseBudget.expense_id == expense_id,
            models.ExpenseBudget.month == month,
            models.Expense.user_id == user_id
        )
    ).first()


def create_expense_budget(db: Session, budget: schemas.ExpenseBudgetCreate, user_id: int) -> models.ExpenseBudget:
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
    db_budget = models.ExpenseBudget(
        expense_id=budget.expense_id,
        month=budget.month,
        budget=budget.budget
    )
    
    # Save to database
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    
    return db_budget


def update_expense_budget(db: Session, budget_id: int, user_id: int, budget: schemas.ExpenseBudgetUpdate) -> Optional[models.ExpenseBudget]:
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


# =============================================================================
# TRANSACTION CRUD OPERATIONS
# =============================================================================

def get_transaction(db: Session, transaction_id: int, user_id: int) -> Optional[models.Transaction]:
    """Get a transaction by ID, ensuring it belongs to the specified user."""
    return db.query(models.Transaction).filter(
        and_(models.Transaction.id == transaction_id, models.Transaction.user_id == user_id)
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
) -> List[models.Transaction]:
    """Get transactions for a specific user with advanced filtering."""
    query = db.query(models.Transaction).filter(models.Transaction.user_id == user_id)
    
    # Filter by expense
    if expense_id:
        query = query.filter(models.Transaction.expense_id == expense_id)
    
    # Filter by category (through expense)
    if category_id:
        query = query.join(models.Expense).filter(models.Expense.category_id == category_id)
    
    # Filter by date range
    if start_date:
        query = query.filter(models.Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.transaction_date <= end_date)
    
    # Filter by amount range
    if min_amount is not None:
        query = query.filter(models.Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(models.Transaction.amount <= max_amount)
    
    # Order by date (most recent first)
    query = query.order_by(models.Transaction.transaction_date.desc())
    
    return query.offset(skip).limit(limit).all()


def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int) -> models.Transaction:
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
    
    # Create transaction model
    db_transaction = models.Transaction(
        expense_id=transaction.expense_id,
        user_id=user_id,
        amount=transaction.amount,
        description=transaction.description,
        transaction_date=transaction.transaction_date,
        created_at=datetime.now(timezone.utc)
    )
    
    # Save to database
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction


def update_transaction(db: Session, transaction_id: int, user_id: int, transaction: schemas.TransactionUpdate) -> Optional[models.Transaction]:
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


# =============================================================================
# REPORTING AND ANALYTICS FUNCTIONS
# =============================================================================

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
    from sqlalchemy import func
    
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
        models.Category.name,
        func.sum(models.Transaction.amount).label('total')
    ).join(models.Expense).join(models.Transaction).filter(
        and_(
            models.Transaction.user_id == user_id,
            models.Transaction.transaction_date >= start_date,
            models.Transaction.transaction_date < end_date
        )
    ).group_by(models.Category.id, models.Category.name).all()
    
    # Get total spending
    total_spending = db.query(func.sum(models.Transaction.amount)).filter(
        and_(
            models.Transaction.user_id == user_id,
            models.Transaction.transaction_date >= start_date,
            models.Transaction.transaction_date < end_date
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