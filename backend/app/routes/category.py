"""
Category API routes for user-specific expense categorization.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import category as category_schemas
from ..crud import category as category_crud
from ..security import get_current_active_user
from ..models.user import User


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=category_schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: category_schemas.CategoryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new category for a user.

    - **name**: Category name (must be unique per user)

    The user ID is automatically extracted from the JWT token.
    """
    try:
        db_category = category_crud.create_category(db=db, category=category, user_id=current_user.id)
        return db_category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[category_schemas.CategoryResponse])
def list_categories(
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0, description="Number of categories to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of categories to return"),
    db: Session = Depends(get_db)
):
    """
    Get all categories for the authenticated user with pagination.

    - **skip**: Number of categories to skip (for pagination)
    - **limit**: Maximum number of categories to return

    The user ID is automatically extracted from the JWT token.
    """
    categories = category_crud.get_categories(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=category_schemas.CategoryResponse)
def get_category(
    category_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific category by ID for the authenticated user.

    - **category_id**: ID of the category

    The user ID is automatically extracted from the JWT token.
    """
    category = category_crud.get_category(db=db, category_id=category_id, user_id=current_user.id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.put("/{category_id}", response_model=category_schemas.CategoryResponse)
def update_category(
    category_id: int,
    category_update: category_schemas.CategoryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a category for the authenticated user.

    - **category_id**: ID of the category to update
    - **name**: New category name (optional, must be unique per user)

    The user ID is automatically extracted from the JWT token.
    """
    try:
        category = category_crud.update_category(
            db=db,
            category_id=category_id,
            user_id=current_user.id,
            category=category_update
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a category for the authenticated user.

    - **category_id**: ID of the category to delete

    The user ID is automatically extracted from the JWT token.
    """
    success = category_crud.delete_category(db=db, category_id=category_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )