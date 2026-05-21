from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.db import get_db
from app.models import User
from app.services import XPService
from app.dependencies.auth import get_current_user
from app.schemas import UserResponse
from pydantic import BaseModel


router = APIRouter(prefix="/xp", tags=["xp"])


class XPProgressResponse(BaseModel):
    current_level: int
    current_xp: int
    xp_in_current_level: int
    xp_needed_for_next_level: int
    progress_percentage: float
    next_level: int


class XPActionResponse(BaseModel):
    xp_gained: int
    new_level: int
    message: str


@router.get("/progress", response_model=XPProgressResponse)
def get_xp_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's XP progress."""
    progress = XPService.get_xp_progress(current_user)
    return progress


@router.post("/daily-login", response_model=XPActionResponse)
def award_daily_login_xp(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Award XP for daily login."""
    result = XPService.award_daily_login_xp(db, current_user)
    return result


@router.get("/leaderboard")
def get_leaderboard(
    limit: Optional[int] = 10,
    db: Session = Depends(get_db)
):
    """Get top users by XP."""
    if limit > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit cannot exceed 50"
        )
    leaderboard = XPService.get_leaderboard(db, limit)
    return {"leaderboard": leaderboard}


class XPActionRequest(BaseModel):
    action: str  # review_created, rating_given, list_created, media_added_to_list


@router.post("/award", response_model=XPActionResponse)
def award_xp(
    action_request: XPActionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Award XP for a specific action (internal use)."""
    valid_actions = list(XPService.XP_VALUES.keys())

    if action_request.action not in valid_actions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid action. Valid actions: {', '.join(valid_actions)}"
        )

    # Route to appropriate award method
    if action_request.action == "review_created":
        result = XPService.award_review_xp(db, current_user)
    elif action_request.action == "rating_given":
        result = XPService.award_rating_xp(db, current_user)
    elif action_request.action == "list_created":
        result = XPService.award_list_creation_xp(db, current_user)
    elif action_request.action == "media_added_to_list":
        result = XPService.award_media_added_to_list_xp(db, current_user)
    else:
        result = XPService.add_xp(db, current_user, action_request.action)

    return result