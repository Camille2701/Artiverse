import pytest
from fastapi import status


class TestXP:
    """Test XP system endpoints."""

    async def test_get_xp_progress(self, client, test_user, auth_headers):
        """Test getting the current user's XP progress."""
        response = await client.get(
            "/api/v1/xp/progress",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "current_xp" in data
        assert "current_level" in data

    async def test_award_xp(self, client, test_user, auth_headers):
        """Test awarding XP for an action."""
        response = await client.post(
            "/api/v1/xp/award",
            json={"action": "review_created"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["xp_gained"] == 50


class TestBadges:
    """Test badge endpoints."""

    async def test_get_user_badges(self, client, test_user, auth_headers):
        """Test getting badges for a specific user."""
        user_id = test_user.id
        response = await client.get(
            f"/api/v1/badges/users/{user_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    async def test_list_all_badges(self, client, test_user, auth_headers):
        """Test listing all available badges."""
        response = await client.get(
            "/api/v1/badges/available",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestStatistics:
    """Test statistics endpoints."""

    async def test_get_user_statistics(self, client, test_user, auth_headers):
        """Test getting statistics for a specific user."""
        user_id = test_user.id
        response = await client.get(
            f"/api/v1/statistics/users/{user_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_reviews" in data

    async def test_get_platform_statistics(self, client, test_user, auth_headers):
        """Test getting platform-wide statistics."""
        response = await client.get(
            "/api/v1/statistics/platform",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_users" in data


class TestSocial:
    """Test social/follow endpoints."""

    async def test_follow_user(self, client, test_user, test_user_2, auth_headers):
        """Test following a user."""
        user_2_id = test_user_2.id
        response = await client.post(
            f"/api/v1/social/follow/{user_2_id}",
            headers=auth_headers
        )
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]

    async def test_unfollow_user(self, client, test_user, test_user_2, auth_headers):
        """Test unfollowing a user."""
        user_2_id = test_user_2.id
        await client.post(
            f"/api/v1/social/follow/{user_2_id}",
            headers=auth_headers
        )

        response = await client.delete(
            f"/api/v1/social/follow/{user_2_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK

    async def test_get_followers(self, client, test_user, auth_headers):
        """Test getting a user's followers list."""
        user_id = test_user.id
        response = await client.get(
            f"/api/v1/social/followers/{user_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data["followers"], list)

    async def test_get_following(self, client, test_user, auth_headers):
        """Test getting a user's following list."""
        user_id = test_user.id
        response = await client.get(
            f"/api/v1/social/following/{user_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data["following"], list)
