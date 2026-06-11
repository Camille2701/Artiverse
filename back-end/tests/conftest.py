import pytest
import os
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings
from app.models import User
from app.schemas import UserCreate
from app.services import UserService
from app.utils.security import create_access_token
from datetime import timedelta

# Configure pytest-asyncio
pytest_plugins = ("pytest_asyncio",)


# Create async in-memory SQLite database for testing
@pytest.fixture(scope="function")
async def test_db():
    """Create a test database for each test function."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_sessionmaker(engine)() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def client(test_db):
    """Create a test client with dependency overrides."""
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_db) -> User:
    """Create a test user."""
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    user = await UserService.create_user(test_db, user_data)
    await test_db.refresh(user)
    return user


@pytest.fixture
async def test_user_token(test_user) -> str:
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
async def test_user_2(test_db) -> User:
    """Create a second test user."""
    user_data = UserCreate(
        username="testuser2",
        email="test2@example.com",
        password="testpass123"
    )
    user = await UserService.create_user(test_db, user_data)
    await test_db.refresh(user)
    return user
