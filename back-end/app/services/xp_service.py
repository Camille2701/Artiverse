from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models import User
from datetime import datetime, timedelta
from typing import Optional


class XPService:
    """Service for XP calculation and level progression."""

    # XP values for different actions
    XP_VALUES = {
        "review_created": 50,
        "rating_given": 10,
        "list_created": 25,
        "media_added_to_list": 5,
        "daily_login": 5,
        "first_media_of_type": 15,
        "completionist": 100,  # Rated all media of a type
        "review_liked": 5,
        "helpful_review": 10,
    }

    # Streak bonuses (multipliers)
    STREAK_BONUSES = {
        1: 1.0,   # No streak bonus
        2: 1.1,   # 2 day streak
        3: 1.2,   # 3 day streak
        7: 1.5,   # 7 day streak
        14: 2.0,  # 14 day streak
        30: 3.0,  # 30 day streak
    }

    @staticmethod
    def calculate_xp_for_level(level: int) -> int:
        """Calculate total XP needed for a given level."""
        # Using a quadratic progression: XP = 100 * level^2
        return 100 * (level ** 2)

    @staticmethod
    def calculate_level_from_xp(total_xp: int) -> int:
        """Calculate current level based on total XP."""
        # Inverse of the level calculation: level = sqrt(XP / 100)
        import math
        return max(1, int(math.sqrt(total_xp / 100)) + 1)

    @staticmethod
    def get_xp_progress(user: User) -> dict:
        """Get XP progress information for a user."""
        current_level_xp = XPService.calculate_xp_for_level(user.level)
        next_level_xp = XPService.calculate_xp_for_level(user.level + 1)
        xp_in_current_level = user.experience_points - current_level_xp
        xp_needed_for_next_level = next_level_xp - current_level_xp
        progress_percentage = (xp_in_current_level / xp_needed_for_next_level) * 100

        return {
            "current_level": user.level,
            "current_xp": user.experience_points,
            "xp_in_current_level": xp_in_current_level,
            "xp_needed_for_next_level": xp_needed_for_next_level,
            "progress_percentage": round(progress_percentage, 2),
            "next_level": user.level + 1,
        }

    @staticmethod
    async def add_xp(db: AsyncSession, user: User, action: str, streak_days: int = 0) -> tuple[int, int]:
        """
        Add XP to a user for a specific action with optional streak bonus.

        Returns:
            tuple: (xp_gained, new_level)
        """
        base_xp = XPService.XP_VALUES.get(action, 0)

        # Apply streak bonus if applicable
        streak_multiplier = XPService.STREAK_BONUSES.get(streak_days, 1.0)
        xp_gained = int(base_xp * streak_multiplier)

        # Add XP to user
        user.experience_points += xp_gained

        # Check for level up
        old_level = user.level
        new_level = XPService.calculate_level_from_xp(user.experience_points)

        if new_level > old_level:
            user.level = new_level
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return xp_gained, new_level

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return xp_gained, old_level

    @staticmethod
    async def award_daily_login_xp(db: AsyncSession, user: User) -> dict:
        """
        Award XP for daily login and calculate streak bonus.

        Returns:
            dict: Contains xp_gained, new_level, and streak information
        """
        today = datetime.now().date()
        last_login = user.last_login_date.date() if user.last_login_date else None

        streak_days = user.streak_days

        if last_login:
            if last_login == today:
                # Already logged in today, no XP
                return {
                    "xp_gained": 0,
                    "new_level": user.level,
                    "streak_days": streak_days,
                    "message": "Already received daily login XP today"
                }
            elif last_login == today - timedelta(days=1):
                # Consecutive day, increment streak
                streak_days += 1
                user.streak_days = streak_days
            elif last_login < today - timedelta(days=1):
                # Streak broken
                streak_days = 1
                user.streak_days = streak_days
        else:
            # First login ever
            streak_days = 1
            user.streak_days = streak_days

        # Update last login date
        user.last_login_date = datetime.now()

        xp_gained, new_level = await XPService.add_xp(db, user, "daily_login", streak_days)

        return {
            "xp_gained": xp_gained,
            "new_level": new_level,
            "streak_days": streak_days,
            "message": f"Received {xp_gained} XP for daily login! {streak_days} day streak!"
        }

    @staticmethod
    async def award_review_xp(db: AsyncSession, user: User) -> dict:
        """Award XP for creating a review."""
        xp_gained, new_level = await XPService.add_xp(db, user, "review_created")
        return {
            "xp_gained": xp_gained,
            "new_level": new_level,
            "message": f"Received {xp_gained} XP for your review!"
        }

    @staticmethod
    async def award_rating_xp(db: AsyncSession, user: User) -> dict:
        """Award XP for giving a rating."""
        xp_gained, new_level = await XPService.add_xp(db, user, "rating_given")
        return {
            "xp_gained": xp_gained,
            "new_level": new_level,
            "message": f"Received {xp_gained} XP for rating!"
        }

    @staticmethod
    async def award_list_creation_xp(db: AsyncSession, user: User) -> dict:
        """Award XP for creating a list."""
        xp_gained, new_level = await XPService.add_xp(db, user, "list_created")
        return {
            "xp_gained": xp_gained,
            "new_level": new_level,
            "message": f"Received {xp_gained} XP for creating a list!"
        }

    @staticmethod
    async def award_media_added_to_list_xp(db: AsyncSession, user: User) -> dict:
        """Award XP for adding media to a list."""
        xp_gained, new_level = await XPService.add_xp(db, user, "media_added_to_list")
        return {
            "xp_gained": xp_gained,
            "new_level": new_level,
            "message": f"Received {xp_gained} XP for adding media to list!"
        }

    @staticmethod
    async def get_leaderboard(db: AsyncSession, limit: int = 10) -> list[dict]:
        """Get top users by XP."""
        result = await db.execute(
            select(User)
            .order_by(desc(User.experience_points))
            .limit(limit)
        )
        top_users = result.scalars().all()

        return [
            {
                "username": user.username,
                "avatar_url": user.avatar_url,
                "level": user.level,
                "experience_points": user.experience_points,
                "rank": idx + 1
            }
            for idx, user in enumerate(top_users)
        ]