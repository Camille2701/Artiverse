import pytest
from fastapi import status


class TestXP:
    """Test XP system endpoints."""

    def test_get_xp_progress(self, client, test_user, auth_headers):
        """Test getting the current user's XP progress."""
        response = client.get(
            "/api/v1/xp/progress",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "current_xp" in data
        assert "current_level" in data

    def test_award_xp(self, client, test_user, auth_headers):
        """Test awarding XP for an action."""
        response = client.post(
            "/api/v1/xp/award",
            json={"action": "review_created"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["xp_gained"] == 50


class TestBadges:
    """Test badge endpoints."""

    def test_get_user_badges(self, client, test_user, auth_headers):
        """Test getting badges for a specific user."""
        response = client.get(
            f"/api/v1/badges/users/{test_user.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_list_all_badges(self, client, test_user, auth_headers):
        """Test listing all available badges."""
        response = client.get(
            "/api/v1/badges/available",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestStatistics:
    """Test statistics endpoints."""

    def test_get_user_statistics(self, client, test_user, auth_headers):
        """Test getting statistics for a specific user."""
        response = client.get(
            f"/api/v1/statistics/users/{test_user.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_reviews" in data

    def test_get_platform_statistics(self, client, test_user, auth_headers):
        """Test getting platform-wide statistics."""
        response = client.get(
            "/api/v1/statistics/platform",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_users" in data


class TestSocial:
    """Test social/follow endpoints."""

    def test_follow_user(self, client, test_user, test_user_2, auth_headers):
        """Test following a user."""
        response = client.post(
            f"/api/v1/social/follow/{test_user_2.id}",
            headers=auth_headers
        )
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]

    def test_unfollow_user(self, client, test_user, test_user_2, auth_headers):
        """Test unfollowing a user."""
        client.post(
            f"/api/v1/social/follow/{test_user_2.id}",
            headers=auth_headers
        )

        response = client.delete(
            f"/api/v1/social/follow/{test_user_2.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_followers(self, client, test_user, auth_headers):
        """Test getting a user's followers list."""
        response = client.get(
            f"/api/v1/social/followers/{test_user.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data["followers"], list)

    def test_get_following(self, client, test_user, auth_headers):
        """Test getting a user's following list."""
        response = client.get(
            f"/api/v1/social/following/{test_user.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data["following"], list)
