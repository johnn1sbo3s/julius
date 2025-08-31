"""
User API routes for registration, authentication and profile management.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import user as user_schemas
from ..crud import user as user_crud
from ..security import get_current_active_user, get_current_admin_user, get_current_moderator_user
from ..models.user import User
from ..models.enums import UserRole


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
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's profile.
    
    Requires JWT authentication.
    """
    return current_user


# Admin-only endpoints for user management

@router.get("/admin/users", response_model=List[user_schemas.UserResponse])
def admin_list_users(
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get a list of users with pagination. (Admin only)
    
    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of users to return
    - **include_inactive**: Include deactivated users in results
    """
    users = user_crud.get_users(db=db, skip=skip, limit=limit, include_inactive=include_inactive)
    return users


@router.get("/admin/users/{user_id}", response_model=user_schemas.UserResponse)
def admin_get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific user by ID. (Admin only)
    """
    user = user_crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/admin/users", response_model=user_schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def admin_create_user(
    user: user_schemas.UserCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Create a new user with specified role. (Admin only)
    
    - **name**: User's full name
    - **email**: User's email address (must be unique)
    - **password**: User's password (minimum 6 characters)
    - **role**: User's role (user, moderator, admin)
    """
    try:
        db_user = user_crud.create_user(db=db, user=user)
        return db_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/admin/users/{user_id}", response_model=user_schemas.UserResponse)
def admin_update_user(
    user_id: int,
    user_update: user_schemas.UserAdminUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update user information including role and status. (Admin only)
    
    - **name**: User's full name (optional)
    - **email**: User's email address (optional, must be unique)
    - **password**: New password (optional, minimum 6 characters)
    - **role**: User's role (optional)
    - **is_active**: User's active status (optional)
    """
    try:
        user = user_crud.admin_update_user(db=db, user_id=user_id, user=user_update)
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


@router.delete("/admin/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Permanently delete a user. (Admin only)
    
    This action is irreversible. Consider using deactivate instead.
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    success = user_crud.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


@router.patch("/admin/users/{user_id}/deactivate", response_model=user_schemas.UserResponse)
def admin_deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Deactivate a user account. (Admin only)
    
    This is a soft delete - the user data remains but the account is disabled.
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    user = user_crud.deactivate_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.patch("/admin/users/{user_id}/activate", response_model=user_schemas.UserResponse)
def admin_activate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Activate a user account. (Admin only)
    
    This reactivates a previously deactivated account.
    """
    user = user_crud.activate_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/me", response_model=user_schemas.UserResponse)
def update_current_user(
    user_update: user_schemas.UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's information.
    
    Users can only update their own profile.
    
    - **name**: User's full name (optional)
    - **email**: User's email address (optional, must be unique)
    - **password**: New password (optional, minimum 6 characters)
    """
    try:
        user = user_crud.update_user(db=db, user_id=current_user.id, user=user_update)
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


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete current user's account.
    
    Users can only delete their own account.
    This action is irreversible.
    """
    success = user_crud.delete_user(db=db, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )