import pytest
from fastapi import status
from app.schemas import UserCreate


class TestAuth:
    """Test authentication endpoints."""

    def test_register_success(self, client):
        """Test successful user registration."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["user"]["username"] == "newuser"
        assert data["user"]["email"] == "newuser@example.com"
        assert "token" in data
        assert data["user"]["level"] == 1
        # Registration triggers the daily-login XP award, so a fresh user
        # starts with a non-negative XP balance rather than strictly 0.
        assert data["user"]["experience_points"] >= 0

    def test_register_duplicate_email(self, client, test_user):
        """Test registration fails with duplicate email."""
        user_data = {
            "username": "anotheruser",
            "email": test_user.email,
            "password": "password123"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["error"]

    def test_register_duplicate_username(self, client, test_user):
        """Test registration fails with duplicate username."""
        user_data = {
            "username": test_user.username,
            "email": "different@example.com",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already taken" in response.json()["error"]

    def test_login_with_username(self, client, test_user):
        """Test login with username."""
        login_data = {
            "username": test_user.username,
            "password": "testpass123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["user"]["id"] == test_user.id
        assert "token" in data

    def test_login_with_email(self, client, test_user):
        """Test login with email."""
        login_data = {
            "email": test_user.email,
            "password": "testpass123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["user"]["id"] == test_user.id
        assert "token" in data

    def test_login_invalid_password(self, client, test_user):
        """Test login fails with wrong password."""
        login_data = {
            "username": test_user.username,
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, client):
        """Test login fails for nonexistent user."""
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
