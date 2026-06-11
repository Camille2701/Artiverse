import pytest
from fastapi import status


async def _create_media(client, auth_headers, title="Test Movie"):
    """Helper to create a media and return its id."""
    response = await client.post(
        "/api/v1/media",
        data={"media_type": "movie", "title": title},
        headers=auth_headers
    )
    return response.json()["media"]["id"]


class TestRatings:
    """Test rating endpoints."""

    async def test_rate_media(self, client, test_user, auth_headers):
        """Test rating media."""
        media_id = await _create_media(client, auth_headers)

        response = await client.post(
            "/api/v1/ratings",
            json={"media_id": media_id, "score": 8},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["score"] == 8

    async def test_get_media_ratings(self, client, test_user, test_user_2, auth_headers):
        """Test getting ratings for media."""
        media_id = await _create_media(client, auth_headers)

        await client.post(
            "/api/v1/ratings",
            json={"media_id": media_id, "score": 9},
            headers=auth_headers
        )

        response = await client.get(
            f"/api/v1/ratings/media/{media_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1

    async def test_update_rating(self, client, test_user, auth_headers):
        """Test updating a rating."""
        media_id = await _create_media(client, auth_headers)

        create_response = await client.post(
            "/api/v1/ratings",
            json={"media_id": media_id, "score": 7},
            headers=auth_headers
        )
        rating_id = create_response.json()["id"]

        response = await client.patch(
            f"/api/v1/ratings/{rating_id}",
            json={"score": 9},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["score"] == 9


class TestReviews:
    """Test review endpoints."""

    async def test_create_review(self, client, test_user, auth_headers):
        """Test creating a review."""
        media_id = await _create_media(client, auth_headers)

        review_data = {
            "media_id": media_id,
            "title": "Great movie!",
            "content": "This is a great movie, highly recommended.",
            "spoiler": False
        }
        response = await client.post(
            "/api/v1/reviews",
            json=review_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Great movie!"

    async def test_get_media_reviews(self, client, test_user, auth_headers):
        """Test getting reviews for media."""
        media_id = await _create_media(client, auth_headers)

        await client.post(
            "/api/v1/reviews",
            json={
                "media_id": media_id,
                "title": "Great movie!",
                "content": "This is a great movie.",
                "spoiler": False
            },
            headers=auth_headers
        )

        response = await client.get(
            f"/api/v1/reviews/media/{media_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1

    async def test_update_review(self, client, test_user, auth_headers):
        """Test updating a review."""
        media_id = await _create_media(client, auth_headers)

        create_response = await client.post(
            "/api/v1/reviews",
            json={
                "media_id": media_id,
                "title": "Good movie",
                "content": "It was good.",
                "spoiler": False
            },
            headers=auth_headers
        )
        review_id = create_response.json()["id"]

        response = await client.patch(
            f"/api/v1/reviews/{review_id}",
            json={"title": "Great movie", "content": "Actually it was great!"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Great movie"

    async def test_delete_review(self, client, test_user, auth_headers):
        """Test deleting a review."""
        media_id = await _create_media(client, auth_headers)

        create_response = await client.post(
            "/api/v1/reviews",
            json={
                "media_id": media_id,
                "title": "Test review",
                "content": "Test content.",
                "spoiler": False
            },
            headers=auth_headers
        )
        review_id = create_response.json()["id"]

        response = await client.delete(
            f"/api/v1/reviews/{review_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
