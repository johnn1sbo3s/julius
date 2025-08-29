"""
Authentication routes for JWT login and token management.
"""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.auth import Token, LoginRequest
from app.schemas.user import UserResponse
from app.security import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    
    Use OAuth2PasswordRequestForm which requires:
    - username (we use email)
    - password
    
    Returns:
        Token: JWT access token
        
    Raises:
        HTTPException: If authentication fails
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login-json", response_model=Token)
async def login_with_json(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Alternative login endpoint that accepts JSON instead of form data.
    
    Args:
        login_data: Login credentials in JSON format
        db: Database session
        
    Returns:
        Token: JWT access token
        
    Raises:
        HTTPException: If authentication fails
    """
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's information from JWT token.
    
    Args:
        current_user: Current authenticated user from JWT token
        
    Returns:
        UserResponse: Current user's profile data
    """
    return current_user


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_active_user)
):
    """
    Refresh the current access token.
    
    Args:
        current_user: Current authenticated user from JWT token
        
    Returns:
        Token: New JWT access token
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(current_user.id)}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}