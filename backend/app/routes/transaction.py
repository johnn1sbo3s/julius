"""
Transaction API routes with advanced filtering and analytics.
"""

from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import transaction as transaction_schemas
from ..crud import transaction as transaction_crud


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=transaction_schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: transaction_schemas.TransactionCreate,
    user_id: int = Query(..., description="ID of the user creating the transaction"),  # TODO: Extract from JWT in Phase 5
    db: Session = Depends(get_db)
):
    """
    Create a new transaction.
    
    - **expense_id**: ID of the expense this transaction belongs to
    - **amount**: Transaction amount (must be positive)
    - **description**: Optional transaction description
    - **transaction_date**: Date when the transaction occurred
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    """
    try:
        db_transaction = transaction_crud.create_transaction(db=db, transaction=transaction, user_id=user_id)
        return db_transaction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[transaction_schemas.TransactionResponse])
def list_transactions(
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    expense_id: Optional[int] = Query(None, description="Filter by expense ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    start_date: Optional[date] = Query(None, description="Filter transactions from this date"),
    end_date: Optional[date] = Query(None, description="Filter transactions until this date"),
    min_amount: Optional[float] = Query(None, ge=0, description="Minimum transaction amount"),
    max_amount: Optional[float] = Query(None, ge=0, description="Maximum transaction amount"),
    skip: int = Query(0, ge=0, description="Number of transactions to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of transactions to return"),
    db: Session = Depends(get_db)
):
    """
    Get transactions for a user with advanced filtering.
    
    **Advanced Filtering Options:**
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    - **expense_id**: Filter by specific expense
    - **category_id**: Filter by category (through expense)
    - **start_date**: Filter transactions from this date onwards
    - **end_date**: Filter transactions up to this date
    - **min_amount**: Minimum transaction amount
    - **max_amount**: Maximum transaction amount
    - **skip**: Number of transactions to skip (for pagination)
    - **limit**: Maximum number of transactions to return
    
    **Results are ordered by date (most recent first)**
    """
    transactions = transaction_crud.get_transactions(
        db=db,
        user_id=user_id,
        expense_id=expense_id,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount,
        skip=skip,
        limit=limit
    )
    return transactions


@router.get("/{transaction_id}", response_model=transaction_schemas.TransactionResponse)
def get_transaction(
    transaction_id: int,
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    db: Session = Depends(get_db)
):
    """
    Get a specific transaction by ID.
    
    - **transaction_id**: ID of the transaction
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    """
    transaction = transaction_crud.get_transaction(db=db, transaction_id=transaction_id, user_id=user_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction


@router.put("/{transaction_id}", response_model=transaction_schemas.TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction_update: transaction_schemas.TransactionUpdate,
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    db: Session = Depends(get_db)
):
    """
    Update a transaction.
    
    - **transaction_id**: ID of the transaction to update
    - **amount**: New transaction amount (optional, must be positive)
    - **description**: New transaction description (optional)
    - **transaction_date**: New transaction date (optional)
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    """
    transaction = transaction_crud.update_transaction(
        db=db, 
        transaction_id=transaction_id, 
        user_id=user_id, 
        transaction=transaction_update
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    db: Session = Depends(get_db)
):
    """
    Delete a transaction.
    
    - **transaction_id**: ID of the transaction to delete
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    """
    success = transaction_crud.delete_transaction(db=db, transaction_id=transaction_id, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )


@router.get("/analytics/monthly-summary")
def get_monthly_summary(
    user_id: int = Query(..., description="ID of the user"),  # TODO: Extract from JWT in Phase 5
    month: str = Query(..., pattern=r"^\d{4}-\d{2}$", description="Month in YYYY-MM format"),
    db: Session = Depends(get_db)
):
    """
    Get monthly spending summary for a user.
    
    **Analytics Endpoint**
    - **user_id**: ID of the user (will be extracted from JWT token in Phase 5)
    - **month**: Month in YYYY-MM format (e.g., "2024-08")
    
    **Returns:**
    - Total spending for the month
    - Spending breakdown by category
    """
    try:
        summary = transaction_crud.get_monthly_summary(db=db, user_id=user_id, month=month)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error generating monthly summary: {str(e)}"
        )