from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.db import get_db
from app.models import User, Media
from app.schemas import MediaResponse, MediaCreate, MediaUpdate
from app.services import MediaService
from app.services.storage_service import StorageService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/media", tags=["media"])


def _media_to_frontend(media: Media) -> dict:
    """Serialize a Media ORM object into the frontend-compatible shape."""
    return {
        "id": media.id,
        "title": media.title,
        "type": media.media_type.value,
        "description": media.synopsis,
        "rating": float(media.average_rating),
        "releaseDate": media.release_date.isoformat() if media.release_date else None,
        "image": media.cover_image,
    }


@router.post("")
async def create_media(
    media_type: str = Form(...),
    title: str = Form(...),
    original_title: Optional[str] = Form(None),
    synopsis: Optional[str] = Form(None),
    release_date: Optional[str] = Form(None),
    cover_image: Optional[UploadFile] = File(None),
    banner_image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new media with image uploads."""
    try:
        # Upload cover image if provided
        cover_filename = None
        if cover_image:
            cover_filename = await StorageService.upload_image(cover_image, "covers")
        
        # Upload banner image if provided
        banner_filename = None
        if banner_image:
            banner_filename = await StorageService.upload_image(banner_image, "banners")
        
        # Create media
        media_create = MediaCreate(
            media_type=media_type,
            title=title,
            original_title=original_title,
            synopsis=synopsis,
            release_date=release_date
        )
        
        media = MediaService.create_media(
            db, 
            media_create,
            cover_image=cover_filename,
            banner_image=banner_filename
        )
        
        return {
            "success": True,
            "media": {
                "id": media.id,
                "title": media.title,
                "media_type": media.media_type.value,
                "description": media.synopsis,
                "rating": float(media.average_rating),
                "releaseDate": media.release_date.isoformat() if media.release_date else None,
                "cover_image": media.cover_image
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create media: {str(e)}"
        )


@router.get("")
def list_media(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all media with pagination - Frontend compatible format."""
    from app.models import Media
    media_list = db.query(Media).offset(skip).limit(limit).all()

    # Transform to frontend compatible format
    return [_media_to_frontend(media) for media in media_list]


@router.get("/search", response_model=dict)
def search_media(
    q: str = "",
    media_type: str | None = None,
    min_rating: float | None = None,
    max_rating: float | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    sort_by: str = "relevance",
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Enhanced search media with multiple filters.

    Parameters:
    - q: Search query (searches title, original title, and synopsis)
    - media_type: Filter by media type (movie, tv_series, book, video_game)
    - min_rating: Minimum average rating (1-10)
    - max_rating: Maximum average rating (1-10)
    - year_from: Minimum release year
    - year_to: Maximum release year
    - sort_by: Sort order (relevance, rating, popularity, newest, oldest)
    - skip: Pagination offset
    - limit: Results per page (max 100)
    """
    # Validate parameters
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit cannot exceed 100"
        )

    if min_rating is not None and (min_rating < 1 or min_rating > 10):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum rating must be between 1 and 10"
        )

    if max_rating is not None and (max_rating < 1 or max_rating > 10):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum rating must be between 1 and 10"
        )

    if min_rating is not None and max_rating is not None and min_rating > max_rating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum rating cannot be greater than maximum rating"
        )

    valid_sort_options = ["relevance", "rating", "popularity", "newest", "oldest"]
    if sort_by not in valid_sort_options:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort_by option. Valid options: {', '.join(valid_sort_options)}"
        )

    items, total = MediaService.search_media(
        db, q, media_type, skip, limit,
        min_rating, max_rating, year_from, year_to, sort_by
    )

    return {
        "items": [_media_to_frontend(m) for m in items],
        "total": total,
        "skip": skip,
        "limit": limit,
        "query": q,
        "filters": {
            "media_type": media_type,
            "min_rating": min_rating,
            "max_rating": max_rating,
            "year_from": year_from,
            "year_to": year_to
        },
        "sort_by": sort_by
    }


@router.get("/trending", response_model=dict)
def get_trending(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get trending media."""
    from app.models import Media
    media_list = MediaService.get_trending_media(db, skip, limit)
    total = db.query(Media).count()

    return {
        "items": [_media_to_frontend(m) for m in media_list],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/{media_id}", response_model=MediaResponse)
def get_media(media_id: str, db: Session = Depends(get_db)):
    """Get media by ID."""
    media = MediaService.get_media_by_id(db, media_id)
    
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    
    return media


@router.patch("/{media_id}", response_model=MediaResponse)
def update_media(
    media_id: str,
    media_update: MediaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update media (admin only for MVP)."""
    media = MediaService.get_media_by_id(db, media_id)
    
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    
    update_data = media_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(media, field, value)

    db.commit()
    db.refresh(media)
    return media


@router.delete("/{media_id}")
def delete_media(
    media_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete media (admin only for MVP)."""
    deleted = MediaService.delete_media(db, media_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )

    return {"success": True}
