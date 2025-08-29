"""
Transaction-related Pydantic schemas for data validation and serialization.

These schemas define the structure of transaction data that flows through our API:
- Input validation (what users send to us)
- Output serialization (what we send back to users)
- Update operations (partial data modifications)
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class TransactionBase(BaseModel):
    """Base transaction schema with common fields."""
    expense_id: int = Field(..., gt=0, description="ID of the expense this transaction belongs to")
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Transaction amount")
    description: Optional[str] = Field(None, max_length=500, description="Transaction description")
    transaction_date: date = Field(..., description="Date when the transaction occurred")
    
    @field_validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "expense_id": 1,
                "amount": "45.80",
                "description": "Compras no supermercado",
                "transaction_date": "2024-08-26"
            }
        }
    )


class TransactionUpdate(BaseModel):
    """Schema for updating transaction information."""
    amount: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2, description="Transaction amount")
    description: Optional[str] = Field(None, max_length=500, description="Transaction description")
    transaction_date: Optional[date] = Field(None, description="Date when the transaction occurred")
    
    @field_validator('amount')
    def validate_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "amount": "50.00",
                "description": "Compras mensais no supermercado"
            }
        }
    )


class TransactionResponse(TransactionBase):
    """Schema for transaction data returned by the API."""
    id: int = Field(..., description="Transaction's unique identifier")
    user_id: int = Field(..., description="ID of the user who owns this transaction")
    created_at: datetime = Field(..., description="When the transaction was created")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "expense_id": 1,
                "amount": "45.80",
                "description": "Compras no supermercado",
                "transaction_date": "2024-08-26",
                "user_id": 1,
                "created_at": "2024-08-26T10:30:00"
            }
        }
    )