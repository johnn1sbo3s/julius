"""
Expense Budget-related Pydantic schemas for data validation and serialization.

These schemas define the structure of expense budget data that flows through our API:
- Input validation (what users send to us)
- Output serialization (what we send back to users)
- Update operations (partial data modifications)
"""

from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict, field_validator

if TYPE_CHECKING:
    from .expense import ExpenseResponse


class ExpenseBudgetBase(BaseModel):
    """Base expense budget schema with common fields."""
    expense_id: int = Field(..., gt=0, description="ID of the expense this budget belongs to")
    month: str = Field(..., pattern=r'^\d{4}-\d{2}$', description="Month in YYYY-MM format")
    budget: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Budget amount")
    
    @field_validator('budget')
    def validate_budget(cls, v):
        if v <= 0:
            raise ValueError('Budget must be greater than 0')
        return v


class ExpenseBudgetCreate(ExpenseBudgetBase):
    """Schema for creating a new expense budget."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "expense_id": 1,
                "month": "2024-08",
                "budget": "500.00"
            }
        }
    )


class ExpenseBudgetUpdate(BaseModel):
    """Schema for updating expense budget information."""
    month: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}$', description="Month in YYYY-MM format")
    budget: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2, description="Budget amount")
    
    @field_validator('budget')
    def validate_budget(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Budget must be greater than 0')
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "budget": "600.00"
            }
        }
    )


class ExpenseBudgetResponse(ExpenseBudgetBase):
    """Schema for expense budget data returned by the API."""
    id: int = Field(..., description="Expense budget's unique identifier")
    
    # Include expense information in response
    expense: Optional["ExpenseResponse"] = Field(None, description="Expense details")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "expense_id": 1,
                "month": "2024-08",
                "budget": "500.00",
                "expense": {
                    "id": 1,
                    "name": "Supermercado",
                    "category_id": 1,
                    "user_id": 1,
                    "created_at": "2024-08-26T10:30:00"
                }
            }
        }
    )