"""
User-related Pydantic schemas for data validation and serialization.

These schemas define the structure of user data that flows through our API:
- Input validation (what users send to us)
- Output serialization (what we send back to users)
- Update operations (partial data modifications)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user schema with common fields."""
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=6, max_length=100, description="User's password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "password": "securePassword123"
            }
        }
    )


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's full name")
    email: Optional[EmailStr] = Field(None, description="User's email address")
    password: Optional[str] = Field(None, min_length=6, max_length=100, description="New password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "João Carlos Silva",
                "email": "joao.carlos@newemail.com"
            }
        }
    )


class UserResponse(UserBase):
    """Schema for user data returned by the API."""
    id: int = Field(..., description="User's unique identifier")
    created_at: datetime = Field(..., description="When the user was created")
    
    model_config = ConfigDict(
        from_attributes=True,  # This allows conversion from SQLAlchemy models
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "created_at": "2024-08-26T10:30:00"
            }
        }
    )


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "joao.silva@email.com",
                "password": "securePassword123"
            }
        }
    )