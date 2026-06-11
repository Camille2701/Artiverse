from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import User
from app.schemas import UserResponse, UserUpdate, UserProfileResponse, ReviewResponse, ListResponse
from app.services import UserService, ReviewService, RatingService, ListService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def list_users(
    search: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """List users, optionally filtered by a username/email search term."""
    from sqlalchemy import select, or_

    query = select(User)
    if search:
        like = f"%{search}%"
        query = query.where(
            or_(User.username.ilike(like), User.email.ilike(like))
        )
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user info."""
    return current_user


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get user profile by ID."""
    user = await UserService.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user profile."""
    await db.refresh(current_user)
    
    if user_update.username:
        # Check if username is taken
        existing = await UserService.get_user_by_username(db, user_update.username)
        if existing and existing.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        current_user.username = user_update.username

    if user_update.email:
        # Check if email is taken
        existing = await UserService.get_user_by_email(db, user_update.email)
        if existing and existing.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = user_update.email
    
    if user_update.bio is not None:
        current_user.bio = user_update.bio
    
    if user_update.avatar_url is not None:
        current_user.avatar_url = user_update.avatar_url

    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.get("/{user_id}/reviews", tags=["reviews"])
async def get_user_reviews(
    user_id: str,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get reviews by a user."""
    user = await UserService.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    reviews, total = await ReviewService.get_reviews_by_user(db, user_id, skip, limit)

    return {
        "items": [ReviewResponse.model_validate(r).model_dump(mode="json") for r in reviews],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/{user_id}/lists", response_model=dict)
async def get_user_lists(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get all lists for a user."""
    user = await UserService.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    lists = await ListService.get_user_lists(db, user_id)

    return {
        "lists": [ListResponse.model_validate(lst).model_dump(mode="json") for lst in lists]
    }
