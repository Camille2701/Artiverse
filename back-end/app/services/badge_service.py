from sqlalchemy.orm import Session
from app.models import User, Badge, UserBadge, BadgeTier, BadgeCategory, MediaType, Media, Rating, Review
from sqlalchemy import func, and_
from typing import List, Dict, Optional
import json


class BadgeService:
    """Service for badge management and unlocking."""

    # Badge definitions
    BADGE_DEFINITIONS = [
        # Genre Expert Badges
        {
            "name": "Horror Master",
            "description": "Reviewed 50+ horror movies",
            "tier": BadgeTier.HOLOGRAPHIC,
            "category": BadgeCategory.GENRE_EXPERT,
            "icon": "🎬👻",
            "requirements": {"type": "reviews_in_genre", "media_type": MediaType.MOVIE, "count": 50},
            "xp_reward": 200
        },
        {
            "name": "Sci-Fi Collector",
            "description": "Rated 25+ science fiction video games",
            "tier": BadgeTier.GRADIENT,
            "category": BadgeCategory.GENRE_EXPERT,
            "icon": "🎮🚀",
            "requirements": {"type": "ratings_in_genre", "media_type": MediaType.VIDEO_GAME, "count": 25},
            "xp_reward": 150
        },
        {
            "name": "Bookworm",
            "description": "Reviewed 30+ books",
            "tier": BadgeTier.GRADIENT,
            "category": BadgeCategory.GENRE_EXPERT,
            "icon": "📚🐛",
            "requirements": {"type": "reviews_in_genre", "media_type": MediaType.BOOK, "count": 30},
            "xp_reward": 150
        },
        {
            "name": "Binge Watcher",
            "description": "Reviewed 20+ TV series",
            "tier": BadgeTier.FLAT,
            "category": BadgeCategory.GENRE_EXPERT,
            "icon": "📺🎉",
            "requirements": {"type": "reviews_in_genre", "media_type": MediaType.TV_SERIES, "count": 20},
            "xp_reward": 100
        },

        # Achievement Badges
        {
            "name": "First Review",
            "description": "Wrote your first review",
            "tier": BadgeTier.FLAT,
            "category": BadgeCategory.ACHIEVEMENT,
            "icon": "✍️🌟",
            "requirements": {"type": "total_reviews", "count": 1},
            "xp_reward": 50
        },
        {
            "name": "Century Club",
            "description": "Rated 100+ media items",
            "tier": BadgeTier.HOLOGRAPHIC,
            "category": BadgeCategory.ACHIEVEMENT,
            "icon": "💯🎯",
            "requirements": {"type": "total_ratings", "count": 100},
            "xp_reward": 300
        },
        {
            "name": "List Master",
            "description": "Created 10+ lists",
            "tier": BadgeTier.GRADIENT,
            "category": BadgeCategory.ACHIEVEMENT,
            "icon": "📋👑",
            "requirements": {"type": "total_lists", "count": 10},
            "xp_reward": 150
        },
        {
            "name": "Rising Star",
            "description": "Reached level 5",
            "tier": BadgeTier.FLAT,
            "category": BadgeCategory.ACHIEVEMENT,
            "icon": "⭐🚀",
            "requirements": {"type": "level_reached", "count": 5},
            "xp_reward": 100
        },
        {
            "name": "Elite Critic",
            "description": "Reached level 20",
            "tier": BadgeTier.HOLOGRAPHIC,
            "category": BadgeCategory.ACHIEVEMENT,
            "icon": "🏆👑",
            "requirements": {"type": "level_reached", "count": 20},
            "xp_reward": 500
        },

        # Social Badges
        {
            "name": "Helpful Reviewer",
            "description": "Received 50+ helpful votes on reviews",
            "tier": BadgeTier.GRADIENT,
            "category": BadgeCategory.SOCIAL,
            "icon": "👍💬",
            "requirements": {"type": "total_likes", "count": 50},
            "xp_reward": 150
        },
        {
            "name": "Curator",
            "description": "Created 5+ public lists",
            "tier": BadgeTier.GRADIENT,
            "category": BadgeCategory.SOCIAL,
            "icon": "🎨📚",
            "requirements": {"type": "public_lists", "count": 5},
            "xp_reward": 100
        },
        {
            "name": "Community Leader",
            "description": "100+ total helpful votes received",
            "tier": BadgeTier.HOLOGRAPHIC,
            "category": BadgeCategory.SOCIAL,
            "icon": "🌟👥",
            "requirements": {"type": "total_likes", "count": 100},
            "xp_reward": 300
        },

        # Rare Badges
        {
            "name": "Early Adopter",
            "description": "Joined in the first month of platform launch",
            "tier": BadgeTier.HOLOGRAPHIC,
            "category": BadgeCategory.RARE,
            "icon": "🎮🌟",
            "requirements": {"type": "early_adopter"},
            "xp_reward": 500
        },
        {
            "name": "Perfect 10",
            "description": "Gave a perfect 10/10 rating",
            "tier": BadgeTier.FLAT,
            "category": BadgeCategory.RARE,
            "icon": "🌟🔥",
            "requirements": {"type": "perfect_rating"},
            "xp_reward": 75
        },
        {
            "name": "Streak Master",
            "description": "Maintained a 7-day login streak",
            "tier": BadgeTier.GRADIENT,
            "category": BadgeCategory.RARE,
            "icon": "🔥📅",
            "requirements": {"type": "streak", "count": 7},
            "xp_reward": 100
        },
        {
            "name": "Monthly Champion",
            "description": "Maintained a 30-day login streak",
            "tier": BadgeTier.HOLOGRAPHIC,
            "category": BadgeCategory.RARE,
            "icon": "🏆📅",
            "requirements": {"type": "streak", "count": 30},
            "xp_reward": 300
        }
    ]

    @staticmethod
    def initialize_badges(db: Session):
        """Initialize all badges in the database."""
        for badge_def in BadgeService.BADGE_DEFINITIONS:
            existing = db.query(Badge).filter(Badge.name == badge_def["name"]).first()
            if not existing:
                badge = Badge(
                    name=badge_def["name"],
                    description=badge_def["description"],
                    icon=badge_def["icon"],
                    tier=badge_def["tier"],
                    category=badge_def["category"],
                    requirements=badge_def["requirements"],
                    xp_reward=badge_def["xp_reward"]
                )
                db.add(badge)
        db.commit()

    @staticmethod
    def get_user_badges(db: Session, user_id: str) -> List[Dict]:
        """Get all badges earned by a user."""
        user_badges = db.query(UserBadge).filter(UserBadge.user_id == user_id).all()

        badges = []
        for user_badge in user_badges:
            badge = user_badge.badge
            badges.append({
                "id": badge.id,
                "name": badge.name,
                "description": badge.description,
                "icon": badge.icon,
                "tier": badge.tier.value,
                "category": badge.category.value,
                "earned_at": user_badge.earned_at.isoformat() if user_badge.earned_at else None,
                "is_equipped": user_badge.is_equipped,
                "progress": user_badge.progress,
                "xp_reward": badge.xp_reward
            })

        return badges

    @staticmethod
    def get_available_badges(db: Session) -> List[Dict]:
        """Get all available badges."""
        badges = db.query(Badge).order_by(Badge.tier, Badge.category).all()

        return [
            {
                "id": badge.id,
                "name": badge.name,
                "description": badge.description,
                "icon": badge.icon,
                "tier": badge.tier.value,
                "category": badge.category.value,
                "requirements": badge.requirements,
                "xp_reward": badge.xp_reward
            }
            for badge in badges
        ]

    @staticmethod
    def check_badge_eligibility(db: Session, user: User) -> List[Badge]:
        """Check which badges the user is eligible for but hasn't earned yet."""
        # Get user's current badge IDs
        earned_badge_ids = {ub.badge_id for ub in user.badges}

        # Get all badges
        all_badges = db.query(Badge).filter(~Badge.id.in_(earned_badge_ids)).all()

        eligible_badges = []

        for badge in all_badges:
            if BadgeService._check_single_badge(db, user, badge):
                eligible_badges.append(badge)

        return eligible_badges

    @staticmethod
    def _check_single_badge(db: Session, user: User, badge: Badge) -> bool:
        """Check if a user meets the requirements for a single badge."""
        requirements = badge.requirements
        req_type = requirements.get("type")

        if req_type == "total_reviews":
            count = db.query(Review).filter(Review.user_id == user.id).count()
            return count >= requirements.get("count", 0)

        elif req_type == "total_ratings":
            count = db.query(Rating).filter(Rating.user_id == user.id).count()
            return count >= requirements.get("count", 0)

        elif req_type == "total_lists":
            count = db.query(func.count()).select_from(func.text("lists")).where(
                func.text("lists.user_id") == user.id
            ).scalar()
            return count >= requirements.get("count", 0)

        elif req_type == "level_reached":
            return user.level >= requirements.get("count", 0)

        elif req_type == "reviews_in_genre":
            media_type = requirements.get("media_type")
            count = db.query(Review).join(Media).filter(
                and_(
                    Review.user_id == user.id,
                    Media.media_type == media_type
                )
            ).count()
            return count >= requirements.get("count", 0)

        elif req_type == "ratings_in_genre":
            media_type = requirements.get("media_type")
            count = db.query(Rating).join(Media).filter(
                and_(
                    Rating.user_id == user.id,
                    Media.media_type == media_type
                )
            ).count()
            return count >= requirements.get("count", 0)

        elif req_type == "total_likes":
            total = db.query(func.sum(Review.like_count)).join(User).filter(
                User.id == user.id
            ).scalar() or 0
            return total >= requirements.get("count", 0)

        elif req_type == "public_lists":
            from app.models import List
            count = db.query(List).filter(
                and_(
                    List.user_id == user.id,
                    List.visibility == "public"
                )
            ).count()
            return count >= requirements.get("count", 0)

        elif req_type == "perfect_rating":
            has_perfect = db.query(Rating).filter(
                and_(
                    Rating.user_id == user.id,
                    Rating.score == 10
                )
            ).first()
            return has_perfect is not None

        elif req_type == "streak":
            return user.streak_days >= requirements.get("count", 0)

        elif req_type == "early_adopter":
            # Check if user joined in first 30 days
            from datetime import datetime, timedelta
            if user.created_at:
                thirty_days_after_launch = datetime(2025, 1, 1) + timedelta(days=30)  # Assuming launch date
                return user.created_at < thirty_days_after_launch
            return False

        return False

    @staticmethod
    def award_badge(db: Session, user: User, badge: Badge) -> UserBadge:
        """Award a badge to a user."""
        # Check if user already has this badge
        existing = db.query(UserBadge).filter(
            and_(
                UserBadge.user_id == user.id,
                UserBadge.badge_id == badge.id
            )
        ).first()

        if existing:
            return existing

        # Create new user badge
        user_badge = UserBadge(
            user_id=user.id,
            badge_id=badge.id,
            progress={"awarded_at": datetime.now().isoformat()}
        )

        db.add(user_badge)
        db.commit()
        db.refresh(user_badge)

        return user_badge

    @staticmethod
    def check_and_award_badges(db: Session, user: User) -> List[Dict]:
        """Check eligibility and award any new badges."""
        eligible_badges = BadgeService.check_badge_eligibility(db, user)

        awarded_badges = []
        for badge in eligible_badges:
            user_badge = BadgeService.award_badge(db, user, badge)
            awarded_badges.append({
                "badge_name": badge.name,
                "badge_icon": badge.icon,
                "tier": badge.tier.value,
                "xp_reward": badge.xp_reward,
                "earned_at": user_badge.earned_at.isoformat()
            })

        return awarded_badges

    @staticmethod
    def get_badge_progress(db: Session, user: User, badge: Badge) -> Dict:
        """Get user's progress toward a specific badge."""
        requirements = badge.requirements
        req_type = requirements.get("type")
        target = requirements.get("count", 1)

        current = 0

        if req_type == "total_reviews":
            current = db.query(Review).filter(Review.user_id == user.id).count()

        elif req_type == "total_ratings":
            current = db.query(Rating).filter(Rating.user_id == user.id).count()

        elif req_type == "total_lists":
            current = db.query(func.count()).select_from(func.text("lists")).where(
                func.text("lists.user_id") == user.id
            ).scalar()

        elif req_type == "level_reached":
            current = user.level

        elif req_type == "reviews_in_genre":
            media_type = requirements.get("media_type")
            current = db.query(Review).join(Media).filter(
                and_(
                    Review.user_id == user.id,
                    Media.media_type == media_type
                )
            ).count()

        elif req_type == "ratings_in_genre":
            media_type = requirements.get("media_type")
            current = db.query(Rating).join(Media).filter(
                and_(
                    Rating.user_id == user.id,
                    Media.media_type == media_type
                )
            ).count()

        elif req_type == "total_likes":
            current = db.query(func.sum(Review.like_count)).join(User).filter(
                User.id == user.id
            ).scalar() or 0

        elif req_type == "public_lists":
            from app.models import List
            current = db.query(List).filter(
                and_(
                    List.user_id == user.id,
                    List.visibility == "public"
                )
            ).count()

        elif req_type == "streak":
            current = user.streak_days

        # For boolean requirements, progress is either 0 or 100%
        if req_type in ["perfect_rating", "early_adopter"]:
            is_complete = BadgeService._check_single_badge(db, user, badge)
            current = 1 if is_complete else 0
            target = 1

        percentage = min(100, (current / target) * 100) if target > 0 else 0

        return {
            "badge_name": badge.name,
            "current": current,
            "target": target,
            "percentage": round(percentage, 1),
            "is_complete": current >= target
        }

    @staticmethod
    def equip_badge(db: Session, user: User, badge_id: str) -> bool:
        """Equip a badge for display."""
        # Unequip all badges first
        db.query(UserBadge).filter(UserBadge.user_id == user.id).update(
            {"is_equipped": False}
        )

        # Equip the specified badge
        user_badge = db.query(UserBadge).filter(
            and_(
                UserBadge.user_id == user.id,
                UserBadge.badge_id == badge_id
            )
        ).first()

        if user_badge:
            user_badge.is_equipped = True
            db.commit()
            return True

        return False