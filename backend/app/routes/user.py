"""
User API routes for registration, authentication and profile management.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import user as user_schemas
from ..crud import user as user_crud


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=user_schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user: user_schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    - **name**: User's full name
    - **email**: User's email address (must be unique)
    - **password**: User's password (minimum 6 characters)
    """
    try:
        db_user = user_crud.create_user(db=db, user=user)
        return db_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )



@router.get("/me", response_model=user_schemas.UserResponse)
def get_current_user_profile(
    user_id: int,  # TODO: This will be replaced with JWT token in Phase 5
    db: Session = Depends(get_db)
):
    """
    Get current user's profile.
    
    Note: In Phase 5, user_id will be extracted from JWT token.
    """
    user = user_crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/{user_id}", response_model=user_schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific user by ID.
    """
    user = user_crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/", response_model=List[user_schemas.UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get a list of users with pagination.
    
    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of users to return
    """
    users = user_crud.get_users(db=db, skip=skip, limit=limit)
    return users


@router.put("/{user_id}", response_model=user_schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: user_schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user information.
    
    - **name**: User's full name (optional)
    - **email**: User's email address (optional, must be unique)
    - **password**: New password (optional, minimum 6 characters)
    """
    try:
        user = user_crud.update_user(db=db, user_id=user_id, user=user_update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a user.
    """
    success = user_crud.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )