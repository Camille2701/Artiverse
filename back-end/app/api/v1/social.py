from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db import get_db
from app.models import User
from app.services.social_service import SocialService
from app.dependencies.auth import get_current_user
from pydantic import BaseModel


router = APIRouter(prefix="/social", tags=["social"])


@router.post("/follow/{user_id}")
async def follow_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Follow a user."""
    try:
        success = await SocialService.follow_user(db, current_user, user_id)
        if success:
            return {"message": "Successfully followed user"}
        else:
            return {"message": "Already following this user"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/follow/{user_id}")
async def unfollow_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Unfollow a user."""
    success = await SocialService.unfollow_user(db, current_user, user_id)
    if success:
        return {"message": "Successfully unfollowed user"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not following this user"
        )


@router.get("/following")
async def get_following(
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get users that the current user is following."""
    following = await SocialService.get_following(db, current_user.id, limit)
    return {"following": following}


@router.get("/followers")
async def get_followers(
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get users that follow the current user."""
    followers = await SocialService.get_followers(db, current_user.id, limit)
    return {"followers": followers}


@router.get("/following/{user_id}")
async def get_user_following(
    user_id: str,
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get users that a specific user is following."""
    following = await SocialService.get_following(db, user_id, limit)
    return {"following": following}


@router.get("/followers/{user_id}")
async def get_user_followers(
    user_id: str,
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get users that follow a specific user."""
    followers = await SocialService.get_followers(db, user_id, limit)
    return {"followers": followers}


@router.get("/stats/{user_id}")
async def get_follow_stats(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get follow statistics for a user."""
    # Check if user exists
    from sqlalchemy import select

    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    stats = await SocialService.get_follow_stats(db, user_id)
    return stats


@router.get("/is-following/{user_id}")
async def check_is_following(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Check if current user is following a specific user."""
    is_following = await SocialService.is_following(db, current_user.id, user_id)
    return {"is_following": is_following}


@router.get("/feed")
async def get_activity_feed(
    limit: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get activity feed from followed users."""
    feed = await SocialService.get_feed(db, current_user.id, limit)
    return {"feed": feed}


@router.get("/activity/{user_id}")
async def get_user_activity(
    user_id: str,
    limit: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get recent activity for a user."""
    # Check if user exists
    from sqlalchemy import select

    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    activity = await SocialService.get_user_activity(db, user_id, limit)
    return {"activity": activity}


@router.get("/similar")
async def get_similar_users(
    limit: int = Query(10, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get users with similar taste based on ratings."""
    similar_users = await SocialService.get_similar_users(db, current_user.id, limit)
    return {"similar_users": similar_users}