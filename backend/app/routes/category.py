"""
Category API routes for user-specific expense categorization.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import category as category_schemas
from ..crud import category as category_crud


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=category_schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: category_schemas.CategoryCreate,
    user_id: int = Query(..., description="ID of the user creating the category"),  # TODO: Extract from JWT in Phase 5
    db: Session = Depends(get_db)
):
    """
    Create a new category for a user.
    
    - **name**: Category name (must be unique per user)
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    """
    try:
        db_category = category_crud.create_category(db=db, category=category, user_id=user_id)
        return db_category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[category_schemas.CategoryResponse])
def list_categories(
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    skip: int = Query(0, ge=0, description="Number of categories to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of categories to return"),
    db: Session = Depends(get_db)
):
    """
    Get all categories for a specific user with pagination.
    
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    - **skip**: Number of categories to skip (for pagination)
    - **limit**: Maximum number of categories to return
    """
    categories = category_crud.get_categories(db=db, user_id=user_id, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=category_schemas.CategoryResponse)
def get_category(
    category_id: int,
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    db: Session = Depends(get_db)
):
    """
    Get a specific category by ID.
    
    - **category_id**: ID of the category
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    """
    category = category_crud.get_category(db=db, category_id=category_id, user_id=user_id)
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
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    db: Session = Depends(get_db)
):
    """
    Update a category.
    
    - **category_id**: ID of the category to update
    - **name**: New category name (optional, must be unique per user)
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    """
    try:
        category = category_crud.update_category(
            db=db, 
            category_id=category_id, 
            user_id=user_id, 
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
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    db: Session = Depends(get_db)
):
    """
    Delete a category.
    
    - **category_id**: ID of the category to delete
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    """
    success = category_crud.delete_category(db=db, category_id=category_id, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )