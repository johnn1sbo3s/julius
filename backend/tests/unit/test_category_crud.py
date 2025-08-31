"""
Unit tests for Category CRUD operations.
"""

import pytest
from sqlalchemy.orm import Session

from app.crud.category import (
    create_category,
    get_category,
    get_categories,
    get_category_by_name,
    update_category,
    delete_category,
)
from app.schemas.category import CategoryCreate, CategoryUpdate


class TestCategoryCRUD:
    """Test cases for Category CRUD operations."""
    
    def test_create_category(self, db_session: Session, test_user):
        """Test creating a new category."""
        category_data = CategoryCreate(name="Food & Dining")
        
        category = create_category(db_session, category_data, test_user.id)
        
        assert category.name == "Food & Dining"
        assert category.user_id == test_user.id
        assert category.id is not None
        assert category.created_at is not None
    
    def test_create_category_duplicate_name(self, db_session: Session, test_user):
        """Test creating a category with duplicate name for same user raises error."""
        category_data = CategoryCreate(name="Food & Dining")
        
        # Create first category
        create_category(db_session, category_data, test_user.id)
        
        # Try to create second category with same name for same user
        with pytest.raises(ValueError, match="already exists"):
            create_category(db_session, category_data, test_user.id)
    
    def test_create_category_same_name_different_users(self, db_session: Session, test_user):
        """Test creating categories with same name for different users is allowed."""
        from app.crud.user import create_user
        from app.schemas.user import UserCreate
        
        # Create another user
        user2_data = UserCreate(
            name="User 2",
            email="user2@example.com",
            password="password123"
        )
        user2 = create_user(db_session, user2_data)
        
        category_data = CategoryCreate(name="Food & Dining")
        
        # Create category for first user
        category1 = create_category(db_session, category_data, test_user.id)
        
        # Create category with same name for second user (should work)
        category2 = create_category(db_session, category_data, user2.id)
        
        assert category1.name == category2.name
        assert category1.user_id != category2.user_id
        assert category1.id != category2.id
    
    def test_get_category(self, db_session: Session, test_user):
        """Test getting a category by ID."""
        category_data = CategoryCreate(name="Transportation")
        created_category = create_category(db_session, category_data, test_user.id)
        
        retrieved_category = get_category(db_session, created_category.id, test_user.id)
        
        assert retrieved_category is not None
        assert retrieved_category.id == created_category.id
        assert retrieved_category.name == "Transportation"
        assert retrieved_category.user_id == test_user.id
    
    def test_get_category_wrong_user(self, db_session: Session, test_user):
        """Test getting a category with wrong user ID returns None."""
        from app.crud.user import create_user
        from app.schemas.user import UserCreate
        
        # Create another user
        user2_data = UserCreate(
            name="User 2",
            email="user2@example.com",
            password="password123"
        )
        user2 = create_user(db_session, user2_data)
        
        # Create category for user2
        category_data = CategoryCreate(name="Transportation")
        created_category = create_category(db_session, category_data, user2.id)
        
        # Try to get category as test_user (should return None)
        retrieved_category = get_category(db_session, created_category.id, test_user.id)
        assert retrieved_category is None
    
    def test_get_category_not_found(self, db_session: Session, test_user):
        """Test getting non-existent category returns None."""
        category = get_category(db_session, 999, test_user.id)
        assert category is None
    
    def test_get_categories(self, db_session: Session, test_user):
        """Test getting multiple categories for a user."""
        # User already has 5 default categories created automatically
        initial_categories = get_categories(db_session, test_user.id)
        assert len(initial_categories) == 5  # Default categories
        
        # Create additional categories
        additional_categories = ["Food", "Transportation", "Entertainment", "Healthcare", "Shopping"]
        
        for cat_name in additional_categories:
            category_data = CategoryCreate(name=cat_name)
            create_category(db_session, category_data, test_user.id)
        
        # Get all categories (5 default + 5 additional = 10)
        user_categories = get_categories(db_session, test_user.id, skip=0, limit=15)
        assert len(user_categories) == 10
        
        # Test pagination
        page1 = get_categories(db_session, test_user.id, skip=0, limit=2)
        assert len(page1) == 2
        
        page2 = get_categories(db_session, test_user.id, skip=2, limit=2)
        assert len(page2) == 2
        
        # Ensure different categories in different pages
        assert page1[0].id != page2[0].id
    
    def test_get_categories_empty(self, db_session: Session, test_user):
        """Test getting categories when user has default categories."""
        # User now has 5 default categories created automatically
        categories = get_categories(db_session, test_user.id)
        assert len(categories) == 5  # Default categories: Alimentação, Transporte, Gastos Fixos, Compras, Lazer
        
        # Verify the default categories exist
        category_names = [cat.name for cat in categories]
        expected_default_categories = ["Alimentação", "Transporte", "Gastos Fixos", "Compras", "Lazer"]
        
        for expected_name in expected_default_categories:
            assert expected_name in category_names
    
    def test_get_category_by_name(self, db_session: Session, test_user):
        """Test getting category by name."""
        category_data = CategoryCreate(name="Unique Category")
        created_category = create_category(db_session, category_data, test_user.id)
        
        retrieved_category = get_category_by_name(db_session, "Unique Category", test_user.id)
        
        assert retrieved_category is not None
        assert retrieved_category.id == created_category.id
        assert retrieved_category.name == "Unique Category"
    
    def test_get_category_by_name_not_found(self, db_session: Session, test_user):
        """Test getting non-existent category by name returns None."""
        category = get_category_by_name(db_session, "Non-existent", test_user.id)
        assert category is None
    
    def test_update_category(self, db_session: Session, test_user):
        """Test updating category information."""
        category_data = CategoryCreate(name="Old Name")
        category = create_category(db_session, category_data, test_user.id)
        
        # Update category name
        update_data = CategoryUpdate(name="New Name")
        updated_category = update_category(db_session, category.id, update_data, test_user.id)
        
        assert updated_category is not None
        assert updated_category.name == "New Name"
        assert updated_category.id == category.id
    
    def test_update_category_duplicate_name(self, db_session: Session, test_user):
        """Test updating category to duplicate name raises error."""
        # Create two categories
        cat1_data = CategoryCreate(name="Category 1")
        cat2_data = CategoryCreate(name="Category 2")
        
        cat1 = create_category(db_session, cat1_data, test_user.id)
        cat2 = create_category(db_session, cat2_data, test_user.id)
        
        # Try to update cat2's name to cat1's name
        update_data = CategoryUpdate(name="Category 1")
        
        with pytest.raises(ValueError, match="already exists"):
            update_category(db_session, cat2.id, update_data, test_user.id)
    
    def test_update_category_wrong_user(self, db_session: Session, test_user):
        """Test updating category with wrong user ID returns None."""
        from app.crud.user import create_user
        from app.schemas.user import UserCreate
        
        # Create another user and category
        user2_data = UserCreate(
            name="User 2",
            email="user2@example.com",
            password="password123"
        )
        user2 = create_user(db_session, user2_data)
        
        category_data = CategoryCreate(name="User 2 Category")
        category = create_category(db_session, category_data, user2.id)
        
        # Try to update as test_user
        update_data = CategoryUpdate(name="Hacked Name")
        result = update_category(db_session, category.id, update_data, test_user.id)
        
        assert result is None
    
    def test_update_category_not_found(self, db_session: Session, test_user):
        """Test updating non-existent category returns None."""
        update_data = CategoryUpdate(name="New Name")
        result = update_category(db_session, 999, update_data, test_user.id)
        assert result is None
    
    def test_delete_category(self, db_session: Session, test_user):
        """Test deleting a category."""
        category_data = CategoryCreate(name="To Delete")
        category = create_category(db_session, category_data, test_user.id)
        category_id = category.id
        
        # Delete the category
        result = delete_category(db_session, category_id, test_user.id)
        assert result is True
        
        # Verify category is deleted
        deleted_category = get_category(db_session, category_id, test_user.id)
        assert deleted_category is None
    
    def test_delete_category_wrong_user(self, db_session: Session, test_user):
        """Test deleting category with wrong user ID returns False."""
        from app.crud.user import create_user
        from app.schemas.user import UserCreate
        
        # Create another user and category
        user2_data = UserCreate(
            name="User 2",
            email="user2@example.com",
            password="password123"
        )
        user2 = create_user(db_session, user2_data)
        
        category_data = CategoryCreate(name="User 2 Category")
        category = create_category(db_session, category_data, user2.id)
        
        # Try to delete as test_user
        result = delete_category(db_session, category.id, test_user.id)
        assert result is False
        
        # Verify category still exists
        existing_category = get_category(db_session, category.id, user2.id)
        assert existing_category is not None
    
    def test_delete_category_not_found(self, db_session: Session, test_user):
        """Test deleting non-existent category returns False."""
        result = delete_category(db_session, 999, test_user.id)
        assert result is False