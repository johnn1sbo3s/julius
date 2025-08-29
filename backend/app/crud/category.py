"""
Category CRUD operations for database entities.

This module contains all category-related database operations (Create, Read, Update, Delete)
separated from the API routes for better organization and testability.
"""

from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models import Category
from ..schemas.category import CategoryCreate, CategoryUpdate


def get_category(db: Session, category_id: int, user_id: int) -> Optional[Category]:
    """Get a category by ID, ensuring it belongs to the specified user."""
    return db.query(Category).filter(
        and_(Category.id == category_id, Category.user_id == user_id)
    ).first()


def get_categories(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Category]:
    """Get categories for a specific user with pagination."""
    return db.query(Category).filter(
        Category.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_category_by_name(db: Session, name: str, user_id: int) -> Optional[Category]:
    """Get a category by name for a specific user."""
    return db.query(Category).filter(
        and_(Category.user_id == user_id, Category.name == name)
    ).first()


def create_category(db: Session, category: CategoryCreate, user_id: int) -> Category:
    """
    Create a new category for a user.
    
    Args:
        db: Database session
        category: Category data from API request
        user_id: ID of the user creating the category
        
    Returns:
        Created category model
        
    Raises:
        ValueError: If category with name already exists for this user
    """
    # Check if category already exists for this user
    if get_category_by_name(db, category.name, user_id):
        raise ValueError(f"Category '{category.name}' already exists for this user")
    
    # Create category model
    db_category = Category(
        name=category.name,
        user_id=user_id,
        created_at=datetime.now(timezone.utc)
    )
    
    # Save to database
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


def update_category(db: Session, category_id: int, category: CategoryUpdate, user_id: int) -> Optional[Category]:
    """
    Update category information.
    
    Args:
        db: Database session
        category_id: ID of category to update
        user_id: ID of the user who owns the category
        category: Updated category data
        
    Returns:
        Updated category model or None if category not found
        
    Raises:
        ValueError: If trying to update to a name that already exists for this user
    """
    db_category = get_category(db, category_id, user_id)
    if not db_category:
        return None
    
    # Check if name is being updated and if it already exists
    if category.name and category.name != db_category.name:
        existing_category = get_category_by_name(db, category.name, user_id)
        if existing_category:
            raise ValueError(f"Category '{category.name}' already exists for this user")
    
    # Update only provided fields
    update_data = category.model_dump(exclude_unset=True)
    
    # Apply updates
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    
    return db_category


def delete_category(db: Session, category_id: int, user_id: int) -> bool:
    """
    Delete a category.
    
    Args:
        db: Database session
        category_id: ID of category to delete
        user_id: ID of the user who owns the category
        
    Returns:
        True if category was deleted, False if category not found
    """
    db_category = get_category(db, category_id, user_id)
    if not db_category:
        return False
    
    db.delete(db_category)
    db.commit()
    
    return True