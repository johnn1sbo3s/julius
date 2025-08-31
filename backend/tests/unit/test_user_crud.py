"""
Unit tests for User CRUD operations.
"""

import pytest
from sqlalchemy.orm import Session

from app.crud.user import (
    create_user,
    get_user,
    get_user_by_email,
    get_users,
    update_user,
    delete_user,
    authenticate_user,
)
from app.schemas.user import UserCreate, UserUpdate
from app.crud.category import get_categories
from app.crud.expense import get_expenses


class TestUserCRUD:
    """Test cases for User CRUD operations."""
    
    def test_create_user(self, db_session: Session):
        """Test creating a new user."""
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            password="securepassword123"
        )
        
        user = create_user(db_session, user_data)
        
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.id is not None
        assert user.created_at is not None
        # Password should be hashed, not plain text
        assert user.password_hash != "securepassword123"
        assert user.password_hash.startswith("$2b$")  # bcrypt hash prefix
    
    def test_create_user_duplicate_email(self, db_session: Session):
        """Test creating a user with duplicate email raises error."""
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            password="securepassword123"
        )
        
        # Create first user
        create_user(db_session, user_data)
        
        # Try to create second user with same email
        user_data2 = UserCreate(
            name="Jane Doe",
            email="john@example.com",  # Same email
            password="anotherpassword"
        )
        
        with pytest.raises(ValueError, match="already exists"):
            create_user(db_session, user_data2)
    
    def test_get_user(self, db_session: Session):
        """Test getting a user by ID."""
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            password="securepassword123"
        )
        
        created_user = create_user(db_session, user_data)
        retrieved_user = get_user(db_session, created_user.id)
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == "john@example.com"
    
    def test_get_user_not_found(self, db_session: Session):
        """Test getting a non-existent user returns None."""
        user = get_user(db_session, 999)
        assert user is None
    
    def test_get_user_by_email(self, db_session: Session):
        """Test getting a user by email."""
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            password="securepassword123"
        )
        
        created_user = create_user(db_session, user_data)
        retrieved_user = get_user_by_email(db_session, "john@example.com")
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == "john@example.com"
    
    def test_get_user_by_email_not_found(self, db_session: Session):
        """Test getting a non-existent user by email returns None."""
        user = get_user_by_email(db_session, "nonexistent@example.com")
        assert user is None
    
    def test_get_users(self, db_session: Session):
        """Test getting multiple users with pagination."""
        # Create multiple users
        for i in range(5):
            user_data = UserCreate(
                name=f"User {i}",
                email=f"user{i}@example.com",
                password="password123"
            )
            create_user(db_session, user_data)
        
        # Test getting all users
        users = get_users(db_session, skip=0, limit=10)
        assert len(users) == 5
        
        # Test pagination
        users_page1 = get_users(db_session, skip=0, limit=2)
        assert len(users_page1) == 2
        
        users_page2 = get_users(db_session, skip=2, limit=2)
        assert len(users_page2) == 2
        
        # Ensure different users in different pages
        assert users_page1[0].id != users_page2[0].id
    
    def test_update_user(self, db_session: Session):
        """Test updating user information."""
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            password="securepassword123"
        )
        
        user = create_user(db_session, user_data)
        original_password_hash = user.password_hash
        
        # Update user name and email
        update_data = UserUpdate(
            name="John Smith",
            email="johnsmith@example.com"
        )
        
        updated_user = update_user(db_session, user.id, update_data)
        
        assert updated_user is not None
        assert updated_user.name == "John Smith"
        assert updated_user.email == "johnsmith@example.com"
        # Password should remain unchanged
        assert updated_user.password_hash == original_password_hash
    
    def test_update_user_password(self, db_session: Session):
        """Test updating user password."""
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            password="securepassword123"
        )
        
        user = create_user(db_session, user_data)
        original_password_hash = user.password_hash
        
        # Update password
        update_data = UserUpdate(password="newsecurepassword456")
        updated_user = update_user(db_session, user.id, update_data)
        
        assert updated_user is not None
        assert updated_user.password_hash != original_password_hash
        assert updated_user.password_hash.startswith("$2b$")
    
    def test_update_user_duplicate_email(self, db_session: Session):
        """Test updating user to duplicate email raises error."""
        # Create two users
        user1_data = UserCreate(name="User 1", email="user1@example.com", password="password1")
        user2_data = UserCreate(name="User 2", email="user2@example.com", password="password2")
        
        user1 = create_user(db_session, user1_data)
        user2 = create_user(db_session, user2_data)
        
        # Try to update user2's email to user1's email
        update_data = UserUpdate(email="user1@example.com")
        
        with pytest.raises(ValueError, match="already exists"):
            update_user(db_session, user2.id, update_data)
    
    def test_update_user_not_found(self, db_session: Session):
        """Test updating non-existent user returns None."""
        update_data = UserUpdate(name="New Name")
        result = update_user(db_session, 999, update_data)
        assert result is None
    
    def test_delete_user(self, db_session: Session):
        """Test deleting a user."""
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            password="securepassword123"
        )
        
        user = create_user(db_session, user_data)
        user_id = user.id
        
        # Delete the user
        result = delete_user(db_session, user_id)
        assert result is True
        
        # Verify user is deleted
        deleted_user = get_user(db_session, user_id)
        assert deleted_user is None
    
    def test_delete_user_not_found(self, db_session: Session):
        """Test deleting non-existent user returns False."""
        result = delete_user(db_session, 999)
        assert result is False
    
    def test_authenticate_user_success(self, db_session: Session):
        """Test successful user authentication."""
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            password="securepassword123"
        )
        
        created_user = create_user(db_session, user_data)
        
        # Test authentication with correct credentials
        authenticated_user = authenticate_user(
            db_session, "john@example.com", "securepassword123"
        )
        
        assert authenticated_user is not None
        assert authenticated_user.id == created_user.id
        assert authenticated_user.email == "john@example.com"
    
    def test_authenticate_user_wrong_password(self, db_session: Session):
        """Test authentication with wrong password."""
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            password="securepassword123"
        )
        
        create_user(db_session, user_data)
        
        # Test authentication with wrong password
        authenticated_user = authenticate_user(
            db_session, "john@example.com", "wrongpassword"
        )
        
        assert authenticated_user is None
    
    def test_authenticate_user_not_found(self, db_session: Session):
        """Test authentication with non-existent email."""
        authenticated_user = authenticate_user(
            db_session, "nonexistent@example.com", "anypassword"
        )
        
        assert authenticated_user is None
    
    def test_create_user_with_default_categories_and_expenses(self, db_session: Session):
        """Test that creating a user automatically creates default categories and expenses."""
        user_data = UserCreate(
            name="Test User",
            email="testuser@example.com",
            password="testpassword123"
        )
        
        # Create user
        user = create_user(db_session, user_data)
        
        # Verify user was created
        assert user.id is not None
        assert user.email == "testuser@example.com"
        
        # Get all categories for the user
        categories = get_categories(db_session, user.id)
        
        # Should have 5 default categories
        assert len(categories) == 5
        
        # Check category names
        category_names = {cat.name for cat in categories}
        expected_categories = {"Alimentação", "Transporte", "Gastos Fixos", "Compras", "Lazer"}
        assert category_names == expected_categories
        
        # Check expenses for each category
        expected_expenses = {
            "Alimentação": {"delivery", "janta", "almoço"},
            "Transporte": {"uber", "gasolina", "manutenção"},
            "Gastos Fixos": {"energia", "internet", "mercado", "aluguel", "celular"},
            "Compras": {"roupas", "jogos"},
            "Lazer": set()  # Empty category
        }
        
        for category in categories:
            expenses = get_expenses(db_session, user.id, category_id=category.id)
            expense_names = {exp.name for exp in expenses}
            
            expected_expense_names = expected_expenses[category.name]
            assert expense_names == expected_expense_names, f"Category '{category.name}' has incorrect expenses. Expected: {expected_expense_names}, Got: {expense_names}"
            
            # Verify each expense belongs to the correct category and user
            for expense in expenses:
                assert expense.category_id == category.id
                assert expense.user_id == user.id