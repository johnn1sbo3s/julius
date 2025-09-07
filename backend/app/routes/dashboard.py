"""
Dashboard API routes for aggregated data display.

This module contains endpoints that aggregate data from multiple domains
to provide comprehensive dashboard views for users.
"""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import dashboard as dashboard_schemas
from ..crud import dashboard as dashboard_crud
from ..security import get_current_active_user
from ..models.user import User


router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)


@router.get("/categories", response_model=List[dashboard_schemas.CategoryDashboard])
def get_categories_dashboard(
    month: str = Query(None, description="Month in YYYY-MM format (default: current month)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get categories with budget and spending information for dashboard.

    Returns all categories for the authenticated user with:
    - Category ID and name
    - Total amount spent in the specified month
    - Allocated budget for the specified month (if any)

    - **month**: Month in YYYY-MM format (defaults to current month)
    - **Authentication**: Requires valid JWT token
    """
    # If no month specified, use current month
    if not month:
        month = datetime.now().strftime("%Y-%m")

    # Validate month format
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be in YYYY-MM format"
        )

    # Extract user_id from authenticated user
    user_id = current_user.id

    categories_data = dashboard_crud.get_categories_dashboard(db=db, user_id=user_id, month=month)
    return categories_data


@router.get("/total-spent", response_model=dashboard_schemas.TotalSpentDashboard)
def get_total_spent_dashboard(
    month: str = Query(None, description="Month in YYYY-MM format (default: current month)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get total spending and budget information for dashboard.

    Returns aggregated data for the authenticated user:
    - Total allocated budget across all categories
    - Total amount spent across all categories
    - Formatted month (MM/YY)

    - **month**: Month in YYYY-MM format (defaults to current month)
    - **Authentication**: Requires valid JWT token
    """
    # If no month specified, use current month
    if not month:
        month = datetime.now().strftime("%Y-%m")

    # Validate month format
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be in YYYY-MM format"
        )

    # Extract user_id from authenticated user
    user_id = current_user.id

    total_data = dashboard_crud.get_total_spent_dashboard(db=db, user_id=user_id, month=month)
    return total_data