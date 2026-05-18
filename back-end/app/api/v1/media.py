from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas import MediaResponse, MediaCreate, MediaUpdate
from app.services import MediaService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/media", tags=["media"])


@router.post("", response_model=MediaResponse)
def create_media(
    media_create: MediaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new media (admin only for MVP)."""
    media = MediaService.create_media(db, media_create)
    return media


@router.get("", response_model=dict)
def list_media(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all media with pagination."""
    from app.models import Media
    media_list = db.query(Media).offset(skip).limit(limit).all()
    total = db.query(Media).count()
    
    return {
        "items": media_list,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/search", response_model=dict)
def search_media(
    q: str,
    media_type: str | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Search media by title."""
    items, total = MediaService.search_media(db, q, media_type, skip, limit)
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "query": q
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
        "items": media_list,
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
