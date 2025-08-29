"""
CRUD operations for CategoryBudget model.
"""

from decimal import Decimal
from typing import Optional

from sqlalchemy import and_, delete
from sqlalchemy.orm import Session, joinedload

from app.models.category_budget import CategoryBudget
from app.models.category import Category
from app.schemas.category_budget import CategoryBudgetCreate, CategoryBudgetUpdate


def create_category_budget(
    db: Session, 
    category_budget: CategoryBudgetCreate, 
    user_id: int
) -> CategoryBudget:
    """
    Create a new category budget allocation.
    
    Args:
        db: Database session
        category_budget: CategoryBudget creation data
        user_id: ID of the user creating the budget
        
    Returns:
        CategoryBudget: Created category budget
        
    Raises:
        ValueError: If category doesn't exist or doesn't belong to user
    """
    # Verify that category exists and belongs to user
    category = db.query(Category).filter(
        Category.id == category_budget.category_id,
        Category.user_id == user_id
    ).first()
    
    if not category:
        raise ValueError("Category not found or doesn't belong to user")
    
    # Check if budget already exists for this category and month
    existing_budget = db.query(CategoryBudget).filter(
        CategoryBudget.user_id == user_id,
        CategoryBudget.category_id == category_budget.category_id,
        CategoryBudget.month == category_budget.month
    ).first()
    
    if existing_budget:
        raise ValueError(f"Budget already exists for category {category.name} in {category_budget.month}")
    
    db_category_budget = CategoryBudget(
        user_id=user_id,
        category_id=category_budget.category_id,
        month=category_budget.month,
        allocated_amount=category_budget.allocated_amount
    )
    
    db.add(db_category_budget)
    db.commit()
    db.refresh(db_category_budget)
    
    return db_category_budget


def get_category_budget(
    db: Session, 
    budget_id: int, 
    user_id: int
) -> Optional[CategoryBudget]:
    """
    Get a category budget by ID for a specific user.
    
    Args:
        db: Database session
        budget_id: ID of the category budget
        user_id: ID of the user
        
    Returns:
        CategoryBudget or None: Found category budget or None if not found
    """
    return db.query(CategoryBudget).filter(
        CategoryBudget.id == budget_id,
        CategoryBudget.user_id == user_id
    ).first()


def get_category_budgets_by_month(
    db: Session, 
    user_id: int, 
    month: str
) -> list[CategoryBudget]:
    """
    Get all category budgets for a user in a specific month.
    
    Args:
        db: Database session
        user_id: ID of the user
        month: Month in YYYY-MM format
        
    Returns:
        list[CategoryBudget]: List of category budgets
    """
    return db.query(CategoryBudget).options(
        joinedload(CategoryBudget.category)
    ).filter(
        CategoryBudget.user_id == user_id,
        CategoryBudget.month == month
    ).all()


def get_category_budgets_by_category(
    db: Session, 
    user_id: int, 
    category_id: int,
    limit: Optional[int] = None
) -> list[CategoryBudget]:
    """
    Get category budgets for a specific category.
    
    Args:
        db: Database session
        user_id: ID of the user
        category_id: ID of the category
        limit: Maximum number of results to return
        
    Returns:
        list[CategoryBudget]: List of category budgets
    """
    query = db.query(CategoryBudget).filter(
        CategoryBudget.user_id == user_id,
        CategoryBudget.category_id == category_id
    ).order_by(CategoryBudget.month.desc())
    
    if limit:
        query = query.limit(limit)
    
    return query.all()


def update_category_budget(
    db: Session, 
    budget_id: int, 
    budget_update: CategoryBudgetUpdate, 
    user_id: int
) -> Optional[CategoryBudget]:
    """
    Update a category budget.
    
    Args:
        db: Database session
        budget_id: ID of the category budget to update
        budget_update: Update data
        user_id: ID of the user
        
    Returns:
        CategoryBudget or None: Updated category budget or None if not found
    """
    db_budget = get_category_budget(db, budget_id, user_id)
    if not db_budget:
        return None
    
    update_data = budget_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_budget, field, value)
    
    db.commit()
    db.refresh(db_budget)
    
    return db_budget


def delete_category_budget(
    db: Session, 
    budget_id: int, 
    user_id: int
) -> bool:
    """
    Delete a category budget.
    
    Args:
        db: Database session
        budget_id: ID of the category budget to delete
        user_id: ID of the user
        
    Returns:
        bool: True if deleted successfully, False if not found
    """
    db_budget = get_category_budget(db, budget_id, user_id)
    if not db_budget:
        return False
    
    db.delete(db_budget)
    db.commit()
    
    return True


def delete_category_budgets_by_month(
    db: Session, 
    user_id: int, 
    month: str
) -> int:
    """
    Delete all category budgets for a user in a specific month.
    
    Args:
        db: Database session
        user_id: ID of the user
        month: Month in YYYY-MM format
        
    Returns:
        int: Number of deleted records
    """
    result = db.execute(
        delete(CategoryBudget).where(
            and_(
                CategoryBudget.user_id == user_id,
                CategoryBudget.month == month
            )
        )
    )
    db.commit()
    
    return result.rowcount


def create_or_update_monthly_budget(
    db: Session,
    user_id: int,
    month: str,
    allocations: dict[int, Decimal]
) -> list[CategoryBudget]:
    """
    Create or update all category budgets for a specific month.
    This will replace any existing budgets for the month.
    
    Args:
        db: Database session
        user_id: ID of the user
        month: Month in YYYY-MM format
        allocations: Dict mapping category_id to allocated_amount
        
    Returns:
        list[CategoryBudget]: List of created/updated category budgets
        
    Raises:
        ValueError: If any category doesn't exist or doesn't belong to user
    """
    # Verify all categories exist and belong to user
    category_ids = list(allocations.keys())
    categories = db.query(Category).filter(
        Category.id.in_(category_ids),
        Category.user_id == user_id
    ).all()
    
    if len(categories) != len(category_ids):
        found_ids = {cat.id for cat in categories}
        missing_ids = set(category_ids) - found_ids
        raise ValueError(f"Categories not found or don't belong to user: {missing_ids}")
    
    # Delete existing budgets for this month
    delete_category_budgets_by_month(db, user_id, month)
    
    # Create new budgets
    created_budgets = []
    for category_id, amount in allocations.items():
        db_budget = CategoryBudget(
            user_id=user_id,
            category_id=category_id,
            month=month,
            allocated_amount=amount
        )
        db.add(db_budget)
        created_budgets.append(db_budget)
    
    db.commit()
    
    # Refresh all objects to get IDs and other computed fields
    for budget in created_budgets:
        db.refresh(budget)
    
    return created_budgets


def get_monthly_budget_summary(
    db: Session,
    user_id: int,
    month: str
) -> dict:
    """
    Get a summary of monthly budget allocation.
    
    Args:
        db: Database session
        user_id: ID of the user
        month: Month in YYYY-MM format
        
    Returns:
        dict: Monthly budget summary with total and per-category breakdown
    """
    budgets = get_category_budgets_by_month(db, user_id, month)
    
    total_allocated = sum(budget.allocated_amount for budget in budgets)
    
    return {
        "month": month,
        "total_allocated": total_allocated,
        "categories": [
            {
                "id": budget.id,
                "user_id": budget.user_id,
                "category_id": budget.category_id,
                "category_name": budget.category.name,
                "month": budget.month,
                "allocated_amount": budget.allocated_amount,
                "created_at": budget.created_at
            }
            for budget in budgets
        ]
    }