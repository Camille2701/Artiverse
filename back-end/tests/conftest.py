import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings
from app.models import User
from app.schemas import UserCreate
from app.services import UserService
from app.utils.security import create_access_token
from datetime import timedelta


# Create in-memory SQLite database for testing
@pytest.fixture(scope="function")
def test_db():
    """Create a test database for each test function."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal()
    
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Create a test client with dependency overrides."""
    def override_get_db():
        # Do NOT close the shared session here: the test_db fixture owns its
        # lifecycle. Closing per-request detaches ORM instances held by other
        # fixtures (test_user, test_user_2) and breaks subsequent attribute access.
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(test_db) -> User:
    """Create a test user."""
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    user = UserService.create_user(test_db, user_data)
    test_db.refresh(user)
    return user


@pytest.fixture
def test_user_token(test_user) -> str:
    """Create an access token for test user."""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": test_user.id},
        expires_delta=access_token_expires
    )
    return access_token


@pytest.fixture
def auth_headers(test_user_token) -> dict:
    """Get authorization headers with token."""
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture
def test_user_2(test_db) -> User:
    """Create a second test user."""
    user_data = UserCreate(
        username="testuser2",
        email="test2@example.com",
        password="testpass123"
    )
    user = UserService.create_user(test_db, user_data)
    test_db.refresh(user)
    return user
