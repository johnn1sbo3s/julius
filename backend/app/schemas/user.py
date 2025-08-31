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

from ..models.enums import UserRole


class UserBase(BaseModel):
    """Base user schema with common fields."""
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=6, max_length=100, description="User's password")
    role: Optional[UserRole] = Field(UserRole.USER, description="User's role in the system")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "password": "securePassword123",
                "role": "user"
            }
        }
    )


class UserAdminUpdate(BaseModel):
    """Schema for admin updating user information including role and active status."""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's full name")
    email: Optional[EmailStr] = Field(None, description="User's email address")
    password: Optional[str] = Field(None, min_length=6, max_length=100, description="New password")
    role: Optional[UserRole] = Field(None, description="User's role in the system")
    is_active: Optional[bool] = Field(None, description="Whether the user account is active")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "João Carlos Silva",
                "email": "joao.carlos@newemail.com",
                "role": "moderator",
                "is_active": True
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
    role: UserRole = Field(..., description="User's role in the system")
    is_active: bool = Field(..., description="Whether the user account is active")
    created_at: datetime = Field(..., description="When the user was created")
    
    model_config = ConfigDict(
        from_attributes=True,  # This allows conversion from SQLAlchemy models
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "role": "user",
                "is_active": True,
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