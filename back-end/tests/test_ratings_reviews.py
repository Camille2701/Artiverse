import pytest
from fastapi import status


class TestRatings:
    """Test rating endpoints."""

    def test_rate_media(self, client, test_user, auth_headers):
        """Test rating media."""
        # First create media
        media_data = {
            "media_type": "movie",
            "title": "Test Movie"
        }
        media_response = client.post(
            "/api/v1/media",
            data=media_data,
            headers=auth_headers
        )
        media_id = media_response.json()["media"]["id"]
        
        # Then rate it
        rating_data = {"rating": 4.5}
        response = client.post(
            f"/api/v1/ratings?media_id={media_id}&rating=4.5",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_media_ratings(self, client, test_user, test_user_2, auth_headers):
        """Test getting ratings for media."""
        # Create media
        media_data = {
            "media_type": "movie",
            "title": "Test Movie"
        }
        media_response = client.post(
            "/api/v1/media",
            data=media_data,
            headers=auth_headers
        )
        media_id = media_response.json()["media"]["id"]
        
        # Rate it
        client.post(
            f"/api/v1/ratings?media_id={media_id}&rating=4.5",
            headers=auth_headers
        )
        
        # Get ratings
        response = client.get(
            f"/api/v1/ratings/media/{media_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_rating(self, client, test_user, auth_headers):
        """Test updating a rating."""
        # Create media
        media_data = {
            "media_type": "movie",
            "title": "Test Movie"
        }
        media_response = client.post(
            "/api/v1/media",
            data=media_data,
            headers=auth_headers
        )
        media_id = media_response.json()["media"]["id"]
        
        # Rate it
        client.post(
            f"/api/v1/ratings?media_id={media_id}&rating=3.5",
            headers=auth_headers
        )
        
        # Update rating
        response = client.put(
            f"/api/v1/ratings/{media_id}?rating=4.5",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK


class TestReviews:
    """Test review endpoints."""

    def test_create_review(self, client, test_user, auth_headers):
        """Test creating a review."""
        # Create media
        media_data = {
            "media_type": "movie",
            "title": "Test Movie"
        }
        media_response = client.post(
            "/api/v1/media",
            data=media_data,
            headers=auth_headers
        )
        media_id = media_response.json()["media"]["id"]
        
        # Create review
        review_data = {
            "title": "Great movie!",
            "content": "This is a great movie, highly recommended.",
            "rating": 4.5
        }
        response = client.post(
            f"/api/v1/reviews?media_id={media_id}",
            json=review_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_media_reviews(self, client, test_user, auth_headers):
        """Test getting reviews for media."""
        # Create media
        media_data = {
            "media_type": "movie",
            "title": "Test Movie"
        }
        media_response = client.post(
            "/api/v1/media",
            data=media_data,
            headers=auth_headers
        )
        media_id = media_response.json()["media"]["id"]
        
        # Create review
        review_data = {
            "title": "Great movie!",
            "content": "This is a great movie.",
            "rating": 4.5
        }
        client.post(
            f"/api/v1/reviews?media_id={media_id}",
            json=review_data,
            headers=auth_headers
        )
        
        # Get reviews
        response = client.get(
            f"/api/v1/reviews?media_id={media_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_review(self, client, test_user, auth_headers):
        """Test updating a review."""
        # Create media
        media_data = {
            "media_type": "movie",
            "title": "Test Movie"
        }
        media_response = client.post(
            "/api/v1/media",
            data=media_data,
            headers=auth_headers
        )
        media_id = media_response.json()["media"]["id"]
        
        # Create review
        review_data = {
            "title": "Good movie",
            "content": "It was good.",
            "rating": 3.5
        }
        create_response = client.post(
            f"/api/v1/reviews?media_id={media_id}",
            json=review_data,
            headers=auth_headers
        )
        
        if create_response.status_code == status.HTTP_200_OK:
            review_id = create_response.json().get("id")
            
            # Update review
            update_data = {
                "title": "Great movie",
                "content": "Actually it was great!",
                "rating": 4.5
            }
            response = client.put(
                f"/api/v1/reviews/{review_id}",
                json=update_data,
                headers=auth_headers
            )
            assert response.status_code == status.HTTP_200_OK

    def test_delete_review(self, client, test_user, auth_headers):
        """Test deleting a review."""
        # Create media
        media_data = {
            "media_type": "movie",
            "title": "Test Movie"
        }
        media_response = client.post(
            "/api/v1/media",
            data=media_data,
            headers=auth_headers
        )
        media_id = media_response.json()["media"]["id"]
        
        # Create review
        review_data = {
            "title": "Test review",
            "content": "Test content.",
            "rating": 3.0
        }
        create_response = client.post(
            f"/api/v1/reviews?media_id={media_id}",
            json=review_data,
            headers=auth_headers
        )
        
        if create_response.status_code == status.HTTP_200_OK:
            review_id = create_response.json().get("id")
            
            # Delete review
            response = client.delete(
                f"/api/v1/reviews/{review_id}",
                headers=auth_headers
            )
            assert response.status_code == status.HTTP_200_OK
