"""
Category-related Pydantic schemas for data validation and serialization.

These schemas define the structure of category data that flows through our API:
- Input validation (what users send to us)
- Output serialization (what we send back to users)
- Update operations (partial data modifications)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    """Base category schema with common fields."""
    name: str = Field(..., min_length=2, max_length=100, description="Category name")


class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Alimentação"
            }
        }
    )


class CategoryUpdate(BaseModel):
    """Schema for updating category information."""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Category name")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Alimentação e Bebidas"
            }
        }
    )


class CategoryResponse(CategoryBase):
    """Schema for category data returned by the API."""
    id: int = Field(..., description="Category's unique identifier")
    user_id: int = Field(..., description="ID of the user who owns this category")
    created_at: datetime = Field(..., description="When the category was created")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Alimentação",
                "user_id": 1,
                "created_at": "2024-08-26T10:30:00"
            }
        }
    )