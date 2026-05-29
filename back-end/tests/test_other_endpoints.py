import pytest
from fastapi import status


class TestXP:
    """Test XP system endpoints."""

    def test_get_user_xp(self, client, test_user, auth_headers):
        """Test getting user XP."""
        response = client.get(
            f"/api/v1/xp/{test_user.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "experience_points" in data
        assert "level" in data

    def test_award_xp(self, client, test_user, auth_headers):
        """Test awarding XP to user."""
        response = client.post(
            f"/api/v1/xp/award?user_id={test_user.id}&xp_amount=100",
            headers=auth_headers
        )
        # This may be admin-only or may fail gracefully
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN]


class TestBadges:
    """Test badge endpoints."""

    def test_get_user_badges(self, client, test_user, auth_headers):
        """Test getting user badges."""
        response = client.get(
            f"/api/v1/badges/user/{test_user.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_list_all_badges(self, client, auth_headers):
        """Test listing all available badges."""
        response = client.get(
            "/api/v1/badges",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestStatistics:
    """Test statistics endpoints."""

    def test_get_user_statistics(self, client, test_user, auth_headers):
        """Test getting user statistics."""
        response = client.get(
            f"/api/v1/statistics/user/{test_user.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "reviews_count" in data or "media_watched" in data

    def test_get_global_statistics(self, client, auth_headers):
        """Test getting global statistics."""
        response = client.get(
            "/api/v1/statistics/global",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK


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
        # First follow
        client.post(
            f"/api/v1/social/follow/{test_user_2.id}",
            headers=auth_headers
        )
        
        # Then unfollow
        response = client.delete(
            f"/api/v1/social/follow/{test_user_2.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_followers(self, client, test_user, auth_headers):
        """Test getting followers list."""
        response = client.get(
            f"/api/v1/social/followers/{test_user.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_get_following(self, client, test_user, auth_headers):
        """Test getting following list."""
        response = client.get(
            f"/api/v1/social/following/{test_user.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
