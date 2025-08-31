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


router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)


@router.get("/categories", response_model=List[dashboard_schemas.CategoryDashboard])
def get_categories_dashboard(
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    month: str = Query(None, description="Month in YYYY-MM format (default: current month)"),
    db: Session = Depends(get_db)
):
    """
    Get categories with budget and spending information for dashboard.
    
    Returns all categories for the user with:
    - Category ID and name
    - Total amount spent in the specified month
    - Allocated budget for the specified month (if any)
    
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    - **month**: Month in YYYY-MM format (defaults to current month)
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
    
    categories_data = dashboard_crud.get_categories_dashboard(db=db, user_id=user_id, month=month)
    return categories_data