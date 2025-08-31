"""
Dashboard-related Pydantic schemas for data validation and serialization.

These schemas define the structure of dashboard data that flows through our API.
"""

from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CategoryDashboard(BaseModel):
    """Schema for category data in dashboard with budget and spending information."""
    id: int = Field(..., description="Category's unique identifier")
    name: str = Field(..., description="Category name")
    totalSpent: Decimal = Field(..., description="Total amount spent in the current month")
    budget: Optional[Decimal] = Field(None, description="Allocated budget for the current month")

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