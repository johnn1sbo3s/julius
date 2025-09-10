"""
Category Budget API routes for managing monthly budget allocations.
"""

from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.category_budget import (
    CategoryBudgetCreate,
    CategoryBudgetUpdate,
    CategoryBudgetResponse,
    MonthlyBudgetAllocation,
    MonthlyBudgetSummary,
)
from app.crud.category_budget import (
    create_category_budget,
    get_category_budget,
    get_category_budgets_by_month,
    get_category_budgets_by_category,
    update_category_budget,
    delete_category_budget,
    delete_category_budgets_by_month,
    create_or_update_monthly_budget,
    get_monthly_budget_summary,
    get_active_month,
    has_active_month,
    open_new_month,
    reopen_month,
    close_active_month,
)
from app.security import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/category-budgets", tags=["category-budgets"])


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=CategoryBudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget_allocation(
    category_budget: CategoryBudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new category budget allocation.

    Args:
        category_budget: Category budget creation data
        db: Database session
        current_user: Current authenticated user

    Returns:
        CategoryBudgetResponse: Created category budget

    Raises:
        HTTPException: If category not found or budget already exists
    """
    try:
        db_budget = create_category_budget(db, category_budget, current_user.id)
        return db_budget
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{budget_id}", response_model=CategoryBudgetResponse)
def get_budget_allocation(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get a specific category budget allocation.

    Args:
        budget_id: ID of the category budget
        db: Database session
        current_user: Current authenticated user

    Returns:
        CategoryBudgetResponse: Category budget data

    Raises:
        HTTPException: If budget not found
    """
    db_budget = get_category_budget(db, budget_id, current_user.id)
    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category budget not found"
        )
    return db_budget


@router.get("/current-month", response_model=MonthlyBudgetSummary)
def get_current_monthly_budget(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all category budget allocations for the currently active month.

    Args:
        db: Database session
        current_user: Current authenticated user

    Returns:
        MonthlyBudgetSummary: Monthly budget summary with all categories

    Raises:
        HTTPException: If no active month found
    """
    # Get the active month for the user
    month = get_active_month(db, current_user.id)
    if not month:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active month found. Please open a month first."
        )

    summary = get_monthly_budget_summary(db, current_user.id, month)
    return summary


@router.get("/category/{category_id}", response_model=List[CategoryBudgetResponse])
def get_category_budget_history(
    category_id: int,
    limit: int = 12,  # Default to last 12 months
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get budget allocation history for a specific category.

    Args:
        category_id: ID of the category
        limit: Maximum number of results (default: 12)
        db: Database session
        current_user: Current authenticated user

    Returns:
        List[CategoryBudgetResponse]: List of category budgets
    """
    budgets = get_category_budgets_by_category(db, current_user.id, category_id, limit)
    return budgets


@router.put("/{budget_id}", response_model=CategoryBudgetResponse)
def update_budget_allocation(
    budget_id: int,
    budget_update: CategoryBudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a category budget allocation.

    Args:
        budget_id: ID of the category budget to update
        budget_update: Update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        CategoryBudgetResponse: Updated category budget

    Raises:
        HTTPException: If budget not found
    """
    db_budget = update_category_budget(db, budget_id, budget_update, current_user.id)
    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category budget not found"
        )
    return db_budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget_allocation(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a category budget allocation.

    Args:
        budget_id: ID of the category budget to delete
        db: Database session
        current_user: Current authenticated user

    Raises:
        HTTPException: If budget not found
    """
    success = delete_category_budget(db, budget_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category budget not found"
        )


@router.post("/allocate-current-month", response_model=MonthlyBudgetSummary, status_code=status.HTTP_201_CREATED)
def allocate_current_monthly_budget(
    allocation: MonthlyBudgetAllocation,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create or update all category budget allocations for the currently active month.
    This will replace any existing allocations for the active month.

    Args:
        allocation: Monthly budget allocation data
        db: Database session
        current_user: Current authenticated user

    Returns:
        MonthlyBudgetSummary: Updated monthly budget summary

    Raises:
        HTTPException: If no active month found, categories not found or validation errors
    """
    # Get the active month for the user
    month = get_active_month(db, current_user.id)
    if not month:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active month found. Please open a month first."
        )

    try:
        # Convert allocation format from list of dicts to single dict
        allocations_dict = {}
        for allocation_item in allocation.allocations:
            for category_id_str, amount in allocation_item.items():
                category_id = int(category_id_str)
                allocations_dict[category_id] = Decimal(str(amount))

        # Create or update budgets
        create_or_update_monthly_budget(db, current_user.id, month, allocations_dict)

        # Return updated summary
        summary = get_monthly_budget_summary(db, current_user.id, month)
        return summary

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/month/{month}", status_code=status.HTTP_204_NO_CONTENT)
def delete_monthly_budget(
    month: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete all category budget allocations for a specific month.

    Args:
        month: Month in YYYY-MM format
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Number of deleted records
    """
    deleted_count = delete_category_budgets_by_month(db, current_user.id, month)
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No budget allocations found for {month}"
        )

    return {"deleted_count": deleted_count}


@router.get("/active-month", response_model=dict)
def get_active_month_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get the currently active month for the user.

    Args:
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Active month information or None if no active month
    """
    active_month = get_active_month(db, current_user.id)
    return {
        "active_month": active_month,
        "has_active_month": active_month is not None
    }


@router.post("/open-month/{month}", response_model=dict, status_code=status.HTTP_201_CREATED)
def open_month_endpoint(
    month: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Open a new month for budget planning.
    This will fail if there's already an active month.

    Args:
        month: Month to open in YYYY-MM format
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Success message with opened month

    Raises:
        HTTPException: If month format is invalid, there's already an active month, or month already exists
    """
    # Validate month format
    try:
        from datetime import datetime
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be in YYYY-MM format"
        )

    # Check if there's already an active month
    if has_active_month(db, current_user.id):
        active_month = get_active_month(db, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot open month {month}. There's already an active month: {active_month}. Close it first."
        )

    try:
        success = open_new_month(db, current_user.id, month)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to open month. There might be an active month already."
            )

        return {
            "message": f"Month {month} opened successfully",
            "active_month": month
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/reopen-month/{month}", response_model=dict)
def reopen_month_endpoint(
    month: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reopen an existing month as the active month.
    This will fail if there's already an active month or if the month doesn't exist.

    Args:
        month: Month to reopen in YYYY-MM format
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Success message with reopened month

    Raises:
        HTTPException: If month format is invalid, there's already an active month, or month doesn't exist
    """
    # Validate month format
    try:
        from datetime import datetime
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be in YYYY-MM format"
        )

    # Check if there's already an active month
    if has_active_month(db, current_user.id):
        active_month = get_active_month(db, current_user.id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot reopen month {month}. There's already an active month: {active_month}. Close it first."
        )

    success = reopen_month(db, current_user.id, month)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Month {month} not found or failed to reopen"
        )

    return {
        "message": f"Month {month} reopened successfully",
        "active_month": month
    }


@router.post("/close-month", response_model=dict)
def close_month_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Close the currently active month.

    Args:
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Success message

    Raises:
        HTTPException: If no active month found
    """
    # Get the active month before closing
    active_month = get_active_month(db, current_user.id)
    if not active_month:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active month found to close"
        )

    success = close_active_month(db, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active month found to close"
        )

    return {
        "message": f"Month {active_month} closed successfully",
        "closed_month": active_month
    }