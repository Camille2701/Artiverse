from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db import get_db
from app.models import User
from app.schemas import RatingResponse, RatingCreate, RatingUpdate
from app.services import RatingService, MediaService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.get("", response_model=dict)
async def get_my_ratings(
    skip: int = 0,
    limit: int = 200,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all ratings for the current user."""
    from app.models import Rating
    from sqlalchemy import select, func

    count_result = await db.execute(
        select(func.count()).select_from(Rating).where(Rating.user_id == current_user.id)
    )
    total = count_result.scalar_one()

    result = await db.execute(
        select(Rating)
        .where(Rating.user_id == current_user.id)
        .order_by(Rating.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    ratings = result.scalars().all()

    return {
        "items": [RatingResponse.model_validate(r).model_dump(mode="json") for r in ratings],
        "total": total
    }


@router.post("", response_model=RatingResponse)
async def create_or_update_rating(
    rating_create: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create or update a rating for media."""
    # Verify media exists
    media = await MediaService.get_media_by_id(db, rating_create.media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )

    rating = await RatingService.create_or_update_rating(db, rating_create, current_user.id)
    return rating


@router.get("/media/{media_id}", response_model=dict)
async def get_media_ratings(
    media_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get all ratings for a media."""
    from app.models import Media, Rating
    from sqlalchemy import select, func

    media = await MediaService.get_media_by_id(db, media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )

    ratings_query = select(Rating).filter(Rating.media_id == media_id)
    ratings_result = await db.execute(ratings_query)
    ratings = ratings_result.scalars().all()

    avg_query = select(func.avg(Rating.score)).filter(Rating.media_id == media_id)
    avg_result = await db.execute(avg_query)
    avg_score = avg_result.scalar()

    return {
        "media_id": media_id,
        "ratings": [RatingResponse.model_validate(r).model_dump(mode="json") for r in ratings],
        "average_score": float(avg_score) if avg_score is not None else 0.0,
        "count": len(ratings)
    }


@router.get("/media/{media_id}/me", response_model=Optional[RatingResponse])
async def get_my_rating_for_media(
    media_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get the current user's rating for a media (null if not rated)."""
    return await RatingService.get_rating(db, current_user.id, media_id)


@router.get("/{rating_id}", response_model=RatingResponse)
async def get_rating(
    rating_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific rating."""
    from app.models import Rating
    from sqlalchemy import select

    query = select(Rating).filter(Rating.id == rating_id)
    result = await db.execute(query)
    rating = result.scalar_one_or_none()
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    return rating


@router.patch("/{rating_id}", response_model=RatingResponse)
async def update_rating(
    rating_id: str,
    rating_update: RatingUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a rating."""
    from app.models import Rating
    from sqlalchemy import select

    query = select(Rating).filter(Rating.id == rating_id)
    result = await db.execute(query)
    rating = result.scalar_one_or_none()
    
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
    await db.commit()
    await db.refresh(rating)
    return rating


@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rating(
    rating_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a rating."""
    from app.models import Rating
    from sqlalchemy import select

    query = select(Rating).filter(Rating.id == rating_id)
    result = await db.execute(query)
    rating = result.scalar_one_or_none()
    
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

    await RatingService.delete_rating(db, rating_id)
