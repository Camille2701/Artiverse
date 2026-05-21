from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db import get_db
from app.models import User
from app.services.statistics_service import StatisticsService
from app.dependencies.auth import get_current_user


router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/me")
def get_my_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's statistics."""
    statistics = StatisticsService.get_user_statistics(db, current_user.id)
    return statistics


@router.get("/users/{user_id}")
def get_user_statistics(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get statistics for a specific user."""
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    statistics = StatisticsService.get_user_statistics(db, user_id)
    return statistics


@router.get("/platform")
def get_platform_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get platform-wide statistics."""
    statistics = StatisticsService.get_platform_statistics(db)
    return statistics


@router.get("/compare/{compare_user_id}")
def compare_users(
    compare_user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare current user's statistics with another user."""
    # Check if compare user exists
    compare_user = db.query(User).filter(User.id == compare_user_id).first()
    if not compare_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User to compare not found"
        )

    comparison = StatisticsService.get_user_comparison(db, current_user.id, compare_user_id)
    return comparison


@router.get("/leaderboard")
def get_activity_leaderboard(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user activity leaderboard."""
    platform_stats = StatisticsService.get_platform_statistics(db)
    return {
        "leaderboard": platform_stats["most_active_users"][:limit]
    }