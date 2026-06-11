from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import User
from app.schemas import ReviewResponse, ReviewCreate, ReviewUpdate
from app.services import ReviewService, MediaService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("", response_model=ReviewResponse)
async def create_review(
    review_create: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new review."""
    # Verify media exists
    media = await MediaService.get_media_by_id(db, review_create.media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )

    review = await ReviewService.create_review(db, review_create, current_user.id)
    return review


@router.get("/media/{media_id}", response_model=dict)
async def get_media_reviews(
    media_id: str,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get reviews for a media."""
    media = await MediaService.get_media_by_id(db, media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )

    reviews, total = await ReviewService.get_reviews_by_media(db, media_id, skip, limit)

    # Bulk-fetch usernames
    user_ids = list({r.user_id for r in reviews})
    usernames: dict[str, str] = {}
    if user_ids:
        from sqlalchemy import select as sa_select
        res = await db.execute(sa_select(User).where(User.id.in_(user_ids)))
        usernames = {u.id: u.username for u in res.scalars().all()}

    items = []
    for r in reviews:
        data = ReviewResponse.model_validate(r).model_dump(mode="json")
        data["username"] = usernames.get(r.user_id)
        items.append(data)

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "media_id": media_id
    }


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific review."""
    review = await ReviewService.get_review_by_id(db, review_id)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    return review


@router.patch("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: str,
    review_update: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a review."""
    review = await ReviewService.get_review_by_id(db, review_id)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this review"
        )
    
    update_data = review_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(review, field, value)

    await db.commit()
    await db.refresh(review)
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a review."""
    review = await ReviewService.get_review_by_id(db, review_id)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this review"
        )

    await ReviewService.delete_review(db, review_id)
