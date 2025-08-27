"""
Expense API routes for managing user expenses within categories.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import expense as expense_schemas
from ..crud import expense as expense_crud


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=expense_schemas.ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: expense_schemas.ExpenseCreate,
    user_id: int = Query(..., description="ID of the user creating the expense"),  # TODO: Extract from JWT in Phase 5
    db: Session = Depends(get_db)
):
    """
    Create a new expense for a user.
    
    - **name**: Expense name (must be unique per user within category)
    - **category_id**: ID of the category this expense belongs to
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    """
    try:
        db_expense = expense_crud.create_expense(db=db, expense=expense, user_id=user_id)
        return db_expense
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[expense_schemas.ExpenseResponse])
def list_expenses(
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    skip: int = Query(0, ge=0, description="Number of expenses to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of expenses to return"),
    db: Session = Depends(get_db)
):
    """
    Get all expenses for a specific user with optional filtering.
    
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    - **category_id**: Optional filter by category ID
    - **skip**: Number of expenses to skip (for pagination)
    - **limit**: Maximum number of expenses to return
    """
    expenses = expense_crud.get_expenses(
        db=db, 
        user_id=user_id, 
        category_id=category_id, 
        skip=skip, 
        limit=limit
    )
    return expenses


@router.get("/{expense_id}", response_model=expense_schemas.ExpenseResponse)
def get_expense(
    expense_id: int,
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    db: Session = Depends(get_db)
):
    """
    Get a specific expense by ID.
    
    - **expense_id**: ID of the expense
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    """
    expense = expense_crud.get_expense(db=db, expense_id=expense_id, user_id=user_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense


@router.put("/{expense_id}", response_model=expense_schemas.ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_update: expense_schemas.ExpenseUpdate,
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    db: Session = Depends(get_db)
):
    """
    Update an expense.
    
    - **expense_id**: ID of the expense to update
    - **name**: New expense name (optional, must be unique per user within category)
    - **category_id**: New category ID (optional, must belong to user)
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    """
    try:
        expense = expense_crud.update_expense(
            db=db, 
            expense_id=expense_id, 
            user_id=user_id, 
            expense=expense_update
        )
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        return expense
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    db: Session = Depends(get_db)
):
    """
    Delete an expense.
    
    - **expense_id**: ID of the expense to delete
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    """
    success = expense_crud.delete_expense(db=db, expense_id=expense_id, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )