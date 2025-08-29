"""
CategoryBudget Pydantic schemas for API validation and serialization.
"""

from decimal import Decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class CategoryBudgetBase(BaseModel):
    """Base schema for CategoryBudget with common fields."""
    
    category_id: int = Field(..., description="ID of the category")
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$", description="Month in YYYY-MM format")
    allocated_amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Allocated budget amount")


class CategoryBudgetCreate(CategoryBudgetBase):
    """Schema for creating a new category budget allocation."""
    
    @field_validator('month')
    @classmethod
    def validate_month_format(cls, v: str) -> str:
        """Validate month format is YYYY-MM."""
        try:
            year, month = v.split('-')
            year_int = int(year)
            month_int = int(month)
            
            if year_int < 2000 or year_int > 2100:
                raise ValueError("Year must be between 2000 and 2100")
            if month_int < 1 or month_int > 12:
                raise ValueError("Month must be between 01 and 12")
                
            return v
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("Month must be in YYYY-MM format")
            raise e


class CategoryBudgetUpdate(BaseModel):
    """Schema for updating an existing category budget allocation."""
    
    allocated_amount: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2, description="New allocated budget amount")


class CategoryBudgetResponse(CategoryBudgetBase):
    """Schema for CategoryBudget API responses."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    created_at: datetime


class CategoryBudgetWithCategory(CategoryBudgetResponse):
    """Schema for CategoryBudget with category information included."""
    
    category_name: str = Field(..., description="Name of the category")


class MonthlyBudgetAllocation(BaseModel):
    """Schema for creating/updating all category budgets for a month."""
    
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$", description="Month in YYYY-MM format")
    allocations: list[dict[str, Decimal]] = Field(..., description="List of category_id -> allocated_amount mappings")
    
    @field_validator('month')
    @classmethod
    def validate_month_format(cls, v: str) -> str:
        """Validate month format is YYYY-MM."""
        try:
            year, month = v.split('-')
            year_int = int(year)
            month_int = int(month)
            
            if year_int < 2000 or year_int > 2100:
                raise ValueError("Year must be between 2000 and 2100")
            if month_int < 1 or month_int > 12:
                raise ValueError("Month must be between 01 and 12")
                
            return v
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("Month must be in YYYY-MM format")
            raise e
    
    @field_validator('allocations')
    @classmethod
    def validate_allocations(cls, v: list[dict]) -> list[dict]:
        """Validate that all allocations have positive amounts."""
        for allocation in v:
            for category_id, amount in allocation.items():
                if not isinstance(category_id, str) or not category_id.isdigit():
                    raise ValueError("Category ID must be a string representing an integer")
                if not isinstance(amount, (int, float, Decimal)) or amount <= 0:
                    raise ValueError("Allocated amount must be positive")
        return v


class MonthlyBudgetSummary(BaseModel):
    """Schema for monthly budget summary with all category allocations."""
    
    month: str
    total_allocated: Decimal
    categories: list[CategoryBudgetWithCategory]
    
    model_config = ConfigDict(from_attributes=True)