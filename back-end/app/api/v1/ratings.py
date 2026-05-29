from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.db import get_db
from app.models import User
from app.schemas import RatingResponse, RatingCreate, RatingUpdate
from app.services import RatingService, MediaService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.post("", response_model=RatingResponse)
def create_or_update_rating(
    rating_create: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update a rating for media."""
    # Verify media exists
    media = MediaService.get_media_by_id(db, rating_create.media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    
    rating = RatingService.create_or_update_rating(db, rating_create, current_user.id)
    return rating


@router.get("/media/{media_id}", response_model=dict)
def get_media_ratings(
    media_id: str,
    db: Session = Depends(get_db)
):
    """Get all ratings for a media."""
    from app.models import Media, Rating
    media = MediaService.get_media_by_id(db, media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    
    from sqlalchemy import func
    ratings = db.query(Rating).filter(Rating.media_id == media_id).all()
    avg_score = db.query(func.avg(Rating.score)).filter(
        Rating.media_id == media_id
    ).scalar()

    return {
        "media_id": media_id,
        "ratings": [RatingResponse.model_validate(r).model_dump(mode="json") for r in ratings],
        "average_score": float(avg_score) if avg_score is not None else 0.0,
        "count": len(ratings)
    }


@router.get("/media/{media_id}/me", response_model=Optional[RatingResponse])
def get_my_rating_for_media(
    media_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the current user's rating for a media (null if not rated)."""
    return RatingService.get_rating(db, current_user.id, media_id)


@router.get("/{rating_id}", response_model=RatingResponse)
def get_rating(
    rating_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific rating."""
    from app.models import Rating
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    return rating


@router.patch("/{rating_id}", response_model=RatingResponse)
def update_rating(
    rating_id: str,
    rating_update: RatingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a rating."""
    from app.models import Rating
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    if rating.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this rating"
        )
    
    rating.score = rating_update.score
    db.commit()
    db.refresh(rating)
    return rating


@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(
    rating_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a rating."""
    from app.models import Rating
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    if rating.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this rating"
        )
    
    RatingService.delete_rating(db, rating_id)
