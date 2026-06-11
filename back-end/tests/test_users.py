import pytest
from fastapi import status


class TestUsers:
    """Test user management endpoints."""

    async def test_get_user_profile(self, client, test_user, auth_headers):
        """Test getting user profile."""
        response = await client.get(f"/api/v1/users/{test_user.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_user.id
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email

    async def test_get_user_profile_not_found(self, client, auth_headers):
        """Test getting non-existent user profile."""
        response = await client.get("/api/v1/users/99999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_current_user(self, client, test_user, auth_headers):
        """Test getting current user info."""
        response = await client.get("/api/v1/users/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_user.id

    async def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication."""
        response = await client.get("/api/v1/users/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_update_user_profile(self, client, test_user, auth_headers):
        """Test updating the current user's profile."""
        update_data = {
            "bio": "Updated bio",
            "avatar_url": "https://example.com/avatar.jpg"
        }
        response = await client.patch(
            "/api/v1/users/me",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["bio"] == "Updated bio"
        assert data["avatar_url"] == "https://example.com/avatar.jpg"

    async def test_list_users(self, client, test_user, test_user_2, auth_headers):
        """Test listing users."""
        response = await client.get("/api/v1/users", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    async def test_search_users(self, client, test_user, auth_headers):
        """Test searching users by username."""
        response = await client.get(
            f"/api/v1/users?search={test_user.username}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert any(u["username"] == test_user.username for u in data)
