import pytest
from fastapi import status
from io import BytesIO
from PIL import Image


class TestMedia:
    """Test media management endpoints."""

    def test_create_media(self, client, test_user, auth_headers):
        """Test creating new media."""
        media_data = {
            "media_type": "movie",
            "title": "Test Movie",
            "original_title": "Test Movie Original",
            "synopsis": "A test movie",
            "release_date": "2024-01-01"
        }
        response = client.post(
            "/api/v1/media",
            data=media_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert data["media"]["title"] == "Test Movie"
        assert data["media"]["media_type"] == "movie"

    def test_create_media_unauthorized(self, client):
        """Test creating media without authentication."""
        media_data = {
            "media_type": "movie",
            "title": "Test Movie"
        }
        response = client.post("/api/v1/media", data=media_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_media_by_id(self, client, test_user, auth_headers):
        """Test getting media by ID."""
        # First create media
        media_data = {
            "media_type": "movie",
            "title": "Test Movie"
        }
        create_response = client.post(
            "/api/v1/media",
            data=media_data,
            headers=auth_headers
        )
        media_id = create_response.json()["media"]["id"]
        
        # Then get it
        response = client.get(f"/api/v1/media/{media_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == media_id

    def test_get_media_not_found(self, client, auth_headers):
        """Test getting non-existent media."""
        response = client.get("/api/v1/media/99999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_media(self, client, test_user, auth_headers):
        """Test updating media."""
        # First create media
        media_data = {
            "media_type": "movie",
            "title": "Test Movie"
        }
        create_response = client.post(
            "/api/v1/media",
            data=media_data,
            headers=auth_headers
        )
        media_id = create_response.json()["media"]["id"]
        
        # Then update it
        update_data = {
            "title": "Updated Movie",
            "synopsis": "Updated synopsis"
        }
        response = client.put(
            f"/api/v1/media/{media_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Movie"

    def test_delete_media(self, client, test_user, auth_headers):
        """Test deleting media."""
        # First create media
        media_data = {
            "media_type": "movie",
            "title": "Test Movie"
        }
        create_response = client.post(
            "/api/v1/media",
            data=media_data,
            headers=auth_headers
        )
        media_id = create_response.json()["media"]["id"]
        
        # Then delete it
        response = client.delete(
            f"/api/v1/media/{media_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK

    def test_list_media(self, client, test_user, auth_headers):
        """Test listing media."""
        response = client.get("/api/v1/media", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_search_media(self, client, test_user, auth_headers):
        """Test searching media."""
        # Create some media first
        media_data = {
            "media_type": "movie",
            "title": "Searchable Movie"
        }
        client.post("/api/v1/media", data=media_data, headers=auth_headers)
        
        # Search for it
        response = client.get(
            "/api/v1/media?search=Searchable",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert any("Searchable" in m.get("title", "") for m in data)
