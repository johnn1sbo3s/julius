"""
Pydantic schemas for data validation and serialization.

These schemas define the structure of data that flows through our API:
- Input validation (what users send to us)
- Output serialization (what we send back to users)
- Update operations (partial data modifications)
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


# =============================================================================
# USER SCHEMAS
# =============================================================================

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


# =============================================================================
# CATEGORY SCHEMAS
# =============================================================================

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


# =============================================================================
# EXPENSE SCHEMAS
# =============================================================================

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
    
    # Include category information in response
    category: Optional[CategoryResponse] = Field(None, description="Category details")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Supermercado",
                "category_id": 1,
                "user_id": 1,
                "created_at": "2024-08-26T10:30:00",
                "category": {
                    "id": 1,
                    "name": "Alimentação",
                    "user_id": 1,
                    "created_at": "2024-08-26T10:30:00"
                }
            }
        }
    )


# =============================================================================
# EXPENSE BUDGET SCHEMAS
# =============================================================================

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
    expense: Optional[ExpenseResponse] = Field(None, description="Expense details")
    
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


# =============================================================================
# TRANSACTION SCHEMAS
# =============================================================================

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
    
    # Include expense information in response
    expense: Optional[ExpenseResponse] = Field(None, description="Expense details")
    
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
                "created_at": "2024-08-26T10:30:00",
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