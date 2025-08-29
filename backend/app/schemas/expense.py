"""
Expense-related Pydantic schemas for data validation and serialization.

These schemas define the structure of expense data that flows through our API:
- Input validation (what users send to us)
- Output serialization (what we send back to users)
- Update operations (partial data modifications)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ExpenseBase(BaseModel):
    """Base expense schema with common fields."""
    name: str = Field(..., min_length=2, max_length=100, description="Expense name")
    category_id: int = Field(..., gt=0, description="ID of the category this expense belongs to")


class ExpenseCreate(ExpenseBase):
    """Schema for creating a new expense."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Supermercado",
                "category_id": 1
            }
        }
    )


class ExpenseUpdate(BaseModel):
    """Schema for updating expense information."""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Expense name")
    category_id: Optional[int] = Field(None, gt=0, description="ID of the category this expense belongs to")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Supermercado e Mercearia"
            }
        }
    )


class ExpenseResponse(ExpenseBase):
    """Schema for expense data returned by the API."""
    id: int = Field(..., description="Expense's unique identifier")
    user_id: int = Field(..., description="ID of the user who owns this expense")
    created_at: datetime = Field(..., description="When the expense was created")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Supermercado",
                "category_id": 1,
                "user_id": 1,
                "created_at": "2024-08-26T10:30:00"
            }
        }
    )