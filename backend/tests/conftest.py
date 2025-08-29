"""
Pytest configuration and fixtures for testing.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models.base import Base
from app.security import get_current_active_user
from app.models.user import User


# Test database URL - using SQLite in memory for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override the get_db dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI application."""
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    # Clean up
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create all tables before each test
    Base.metadata.create_all(bind=engine)
    
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
    
    # Drop all tables after each test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db_session):
    """Create a test user for authenticated tests."""
    from app.crud.user import create_user
    from app.schemas.user import UserCreate
    
    user_data = UserCreate(
        name="Test User",
        email="test@example.com",
        password="testpassword123"
    )
    
    user = create_user(db_session, user_data)
    db_session.commit()
    return user


@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers for testing protected endpoints."""
    from app.security import create_access_token
    
    access_token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def mock_current_user(test_user):
    """Mock the current user dependency for testing."""
    def _get_current_user():
        return test_user
    
    app.dependency_overrides[get_current_active_user] = _get_current_user
    yield test_user
    
    # Clean up
    if get_current_active_user in app.dependency_overrides:
        del app.dependency_overrides[get_current_active_user]


@pytest.fixture
def test_category(db_session, test_user):
    """Create a test category for testing."""
    from app.crud.category import create_category
    from app.schemas.category import CategoryCreate
    
    category_data = CategoryCreate(name="Test Category")
    category = create_category(db_session, category_data, test_user.id)
    db_session.commit()
    return category


@pytest.fixture
def test_expense(db_session, test_user, test_category):
    """Create a test expense for testing."""
    from app.crud.expense import create_expense
    from app.schemas.expense import ExpenseCreate
    
    expense_data = ExpenseCreate(
        name="Test Expense",
        category_id=test_category.id
    )
    expense = create_expense(db_session, expense_data, test_user.id)
    db_session.commit()
    return expense