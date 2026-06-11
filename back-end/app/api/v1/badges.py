from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db import get_db
from app.models import User, Badge
from app.services import BadgeService, XPService
from app.dependencies.auth import get_current_user
from pydantic import BaseModel


router = APIRouter(prefix="/badges", tags=["badges"])


class BadgeResponse(BaseModel):
    id: str
    name: str
    description: str
    icon: Optional[str]
    tier: str
    category: str
    requirements: Optional[dict]
    xp_reward: int


class UserBadgeResponse(BaseModel):
    id: str
    name: str
    description: str
    icon: Optional[str]
    tier: str
    category: str
    earned_at: Optional[str]
    is_equipped: bool
    progress: Optional[dict]
    xp_reward: int


class BadgeProgressResponse(BaseModel):
    badge_name: str
    current: int
    target: int
    percentage: float
    is_complete: bool


@router.get("/available", response_model=list[BadgeResponse])
async def get_available_badges(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all available badges."""
    badges = await BadgeService.get_available_badges(db)
    return badges


@router.get("/my-badges", response_model=list[UserBadgeResponse])
async def get_my_badges(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get badges earned by the current user."""
    badges = await BadgeService.get_user_badges(db, current_user.id)
    return badges


@router.get("/users/{user_id}", response_model=list[UserBadgeResponse])
async def get_user_badges(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get badges earned by a specific user."""
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

    badges = await BadgeService.get_user_badges(db, user_id)
    return badges


@router.get("/check-eligibility")
async def check_badge_eligibility(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Check which badges the user is eligible for but hasn't earned."""
    eligible_badges = await BadgeService.check_badge_eligibility(db, current_user)

    return {
        "eligible_badges": [
            {
                "id": badge.id,
                "name": badge.name,
                "description": badge.description,
                "icon": badge.icon,
                "tier": badge.tier.value,
                "category": badge.category.value,
                "xp_reward": badge.xp_reward
            }
            for badge in eligible_badges
        ]
    }


@router.post("/award-new")
async def award_new_badges(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Check eligibility and award any new badges."""
    awarded_badges = await BadgeService.check_and_award_badges(db, current_user)

    return {
        "awarded_badges": awarded_badges,
        "total_awarded": len(awarded_badges)
    }


@router.get("/progress/{badge_id}", response_model=BadgeProgressResponse)
async def get_badge_progress(
    badge_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's progress toward a specific badge."""
    from sqlalchemy import select

    query = select(Badge).filter(Badge.id == badge_id)
    result = await db.execute(query)
    badge = result.scalar_one_or_none()
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found"
        )

    progress = await BadgeService.get_badge_progress(db, current_user, badge)
    return progress


@router.post("/equip/{badge_id}")
async def equip_badge(
    badge_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Equip a badge for display."""
    success = await BadgeService.equip_badge(db, current_user, badge_id)

    if success:
        return {"message": "Badge equipped successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not equip badge. You may not have earned this badge."
        )


@router.post("/initialize")
async def initialize_badges(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Initialize all badges in the database (admin operation)."""
    try:
        await BadgeService.initialize_badges(db)
        return {"message": "Badges initialized successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize badges: {str(e)}"
        )