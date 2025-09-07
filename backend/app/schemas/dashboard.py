"""
Dashboard-related Pydantic schemas for data validation and serialization.

These schemas define the structure of dashboard data that flows through our API.
"""

from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class CategoryDashboard(BaseModel):
    """Schema for category data in dashboard with budget and spending information."""
    id: int = Field(..., description="Category's unique identifier")
    name: str = Field(..., description="Category name")
    totalSpent: Decimal = Field(..., description="Total amount spent in the current month")
    budget: Optional[Decimal] = Field(None, description="Allocated budget for the current month")

    @field_validator('name')
    @classmethod
    def format_name(cls, v: str) -> str:
        """Format name with title case for frontend display."""
        return v.title() if v else v

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Alimentação",
                "totalSpent": 450.75,
                "budget": 800.00
            }
        }
    )


class TotalSpentDashboard(BaseModel):
    """Schema for total spending and budget information in dashboard."""
    budget: Decimal = Field(..., description="Total allocated budget for all categories")
    spent: Decimal = Field(..., description="Total amount spent across all categories")
    month: str = Field(..., description="Month in MM/YY format")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "budget": 1500.12,
                "spent": 2000.99,
                "month": "08/25"
            }
        }
    )