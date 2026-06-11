from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc
from app.models import User, Follow, ActivityLog, ActivityType, Media, Rating, Review
from typing import List, Dict, Optional
from datetime import datetime


class SocialService:
    """Service for social features like follows and activity feeds."""

    @staticmethod
    async def follow_user(db: AsyncSession, follower: User, followed_id: str) -> bool:
        """Follow a user."""
        # Can't follow yourself
        if follower.id == followed_id:
            raise ValueError("Cannot follow yourself")

        # Check if user exists
        followed_result = await db.execute(
            select(User).where(User.id == followed_id)
        )
        followed = followed_result.scalar_one_or_none()
        if not followed:
            raise ValueError("User not found")

        # Check if already following
        existing_result = await db.execute(
            select(Follow).where(
                and_(
                    Follow.follower_id == follower.id,
                    Follow.followed_id == followed_id
                )
            )
        )
        existing = existing_result.scalar_one_or_none()

        if existing:
            return False  # Already following

        # Create follow relationship
        follow = Follow(
            follower_id=follower.id,
            followed_id=followed_id
        )
        db.add(follow)

        # Log activity
        activity = ActivityLog(
            user_id=follower.id,
            activity_type=ActivityType.RATING_GIVEN,  # Reusing enum for social activities
            entity_type="user",
            entity_id=followed_id,
            activity_metadata={"action": "follow", "followed_username": followed.username}
        )
        db.add(activity)

        await db.commit()
        return True

    @staticmethod
    async def unfollow_user(db: AsyncSession, follower: User, followed_id: str) -> bool:
        """Unfollow a user."""
        result = await db.execute(
            select(Follow).where(
                and_(
                    Follow.follower_id == follower.id,
                    Follow.followed_id == followed_id
                )
            )
        )
        follow = result.scalar_one_or_none()

        if not follow:
            return False  # Not following

        await db.delete(follow)
        await db.commit()
        return True

    @staticmethod
    async def get_following(db: AsyncSession, user_id: str, limit: int = 50) -> List[Dict]:
        """Get users that the given user is following."""
        result = await db.execute(
            select(Follow)
            .where(Follow.follower_id == user_id)
            .order_by(desc(Follow.created_at))
            .limit(limit)
        )
        follows = result.scalars().all()

        following_users = []
        for follow in follows:
            user_result = await db.execute(
                select(User).where(User.id == follow.followed_id)
            )
            user = user_result.scalar_one_or_none()
            if user:
                following_users.append({
                    "id": user.id,
                    "username": user.username,
                    "avatar_url": user.avatar_url,
                    "level": user.level,
                    "followed_at": follow.created_at.isoformat()
                })

        return following_users

    @staticmethod
    async def get_followers(db: AsyncSession, user_id: str, limit: int = 50) -> List[Dict]:
        """Get users that follow the given user."""
        result = await db.execute(
            select(Follow)
            .where(Follow.followed_id == user_id)
            .order_by(desc(Follow.created_at))
            .limit(limit)
        )
        follows = result.scalars().all()

        follower_users = []
        for follow in follows:
            user_result = await db.execute(
                select(User).where(User.id == follow.follower_id)
            )
            user = user_result.scalar_one_or_none()
            if user:
                follower_users.append({
                    "id": user.id,
                    "username": user.username,
                    "avatar_url": user.avatar_url,
                    "level": user.level,
                    "followed_at": follow.created_at.isoformat()
                })

        return follower_users

    @staticmethod
    async def is_following(db: AsyncSession, follower_id: str, followed_id: str) -> bool:
        """Check if follower is following followed."""
        result = await db.execute(
            select(Follow).where(
                and_(
                    Follow.follower_id == follower_id,
                    Follow.followed_id == followed_id
                )
            )
        )
        follow = result.scalar_one_or_none()
        return follow is not None

    @staticmethod
    async def get_follow_stats(db: AsyncSession, user_id: str) -> Dict:
        """Get follow statistics for a user."""
        following_count_result = await db.execute(
            select(func.count(Follow.id)).where(Follow.follower_id == user_id)
        )
        following_count = following_count_result.scalar() or 0

        followers_count_result = await db.execute(
            select(func.count(Follow.id)).where(Follow.followed_id == user_id)
        )
        followers_count = followers_count_result.scalar() or 0

        return {
            "following_count": following_count,
            "followers_count": followers_count
        }

    @staticmethod
    async def log_activity(db: AsyncSession, user_id: str, activity_type: ActivityType,
                          entity_type: Optional[str] = None, entity_id: Optional[str] = None,
                          metadata: Optional[Dict] = None) -> ActivityLog:
        """Log a user activity."""
        activity = ActivityLog(
            user_id=user_id,
            activity_type=activity_type,
            entity_type=entity_type,
            entity_id=entity_id,
            activity_metadata=metadata
        )
        db.add(activity)
        await db.commit()
        await db.refresh(activity)
        return activity

    @staticmethod
    async def get_user_activity(db: AsyncSession, user_id: str, limit: int = 20) -> List[Dict]:
        """Get recent activity for a user."""
        result = await db.execute(
            select(ActivityLog)
            .where(ActivityLog.user_id == user_id)
            .order_by(desc(ActivityLog.created_at))
            .limit(limit)
        )
        activities = result.scalars().all()

        activity_list = []
        for activity in activities:
            user_result = await db.execute(
                select(User).where(User.id == activity.user_id)
            )
            user = user_result.scalar_one_or_none()

            activity_data = {
                "id": activity.id,
                "activity_type": activity.activity_type.value,
                "entity_type": activity.entity_type,
                "entity_id": activity.entity_id,
                "metadata": activity.activity_metadata,
                "created_at": activity.created_at.isoformat(),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "avatar_url": user.avatar_url
                } if user else None
            }

            # Add additional data based on entity type
            if activity.entity_type == "media" and activity.entity_id:
                media_result = await db.execute(
                    select(Media).where(Media.id == activity.entity_id)
                )
                media = media_result.scalar_one_or_none()
                if media:
                    activity_data["media"] = {
                        "id": media.id,
                        "title": media.title,
                        "media_type": media.media_type.value,
                        "cover_image": media.cover_image
                    }

            activity_list.append(activity_data)

        return activity_list

    @staticmethod
    async def get_feed(db: AsyncSession, user_id: str, limit: int = 20) -> List[Dict]:
        """Get activity feed from followed users."""
        # Get IDs of users that the current user follows
        followed_result = await db.execute(
            select(Follow.followed_id).where(Follow.follower_id == user_id)
        )
        followed_ids = [row[0] for row in followed_result.all()]

        if not followed_ids:
            return []

        # Get recent activities from followed users
        result = await db.execute(
            select(ActivityLog)
            .where(ActivityLog.user_id.in_(followed_ids))
            .order_by(desc(ActivityLog.created_at))
            .limit(limit)
        )
        activities = result.scalars().all()

        feed_items = []
        for activity in activities:
            user_result = await db.execute(
                select(User).where(User.id == activity.user_id)
            )
            user = user_result.scalar_one_or_none()

            activity_data = {
                "id": activity.id,
                "activity_type": activity.activity_type.value,
                "entity_type": activity.entity_type,
                "entity_id": activity.entity_id,
                "metadata": activity.activity_metadata,
                "created_at": activity.created_at.isoformat(),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "avatar_url": user.avatar_url
                } if user else None
            }

            # Add additional data based on entity type
            if activity.entity_type == "media" and activity.entity_id:
                media_result = await db.execute(
                    select(Media).where(Media.id == activity.entity_id)
                )
                media = media_result.scalar_one_or_none()
                if media:
                    activity_data["media"] = {
                        "id": media.id,
                        "title": media.title,
                        "media_type": media.media_type.value,
                        "cover_image": media.cover_image
                    }

            feed_items.append(activity_data)

        return feed_items

    @staticmethod
    async def get_similar_users(db: AsyncSession, user_id: str, limit: int = 10) -> List[Dict]:
        """Get users with similar taste based on ratings."""
        # Get current user's ratings
        user_ratings_result = await db.execute(
            select(Rating).where(Rating.user_id == user_id)
        )
        user_ratings = user_ratings_result.scalars().all()

        if len(user_ratings) < 3:
            # Not enough data for similarity calculation
            return []

        # Get media IDs rated by current user
        rated_media_ids = [r.media_id for r in user_ratings]

        # Find other users who have rated the same media
        similar_candidates_result = await db.execute(
            select(Rating.user_id, func.count(Rating.id).label('common_ratings'))
            .where(
                and_(
                    Rating.media_id.in_(rated_media_ids),
                    Rating.user_id != user_id
                )
            )
            .group_by(Rating.user_id)
            .having(func.count(Rating.id) >= 3)
            .order_by(desc('common_ratings'))
            .limit(limit * 2)
        )
        similar_candidates = similar_candidates_result.all()

        similar_users = []
        for candidate_id, common_count in similar_candidates:
            candidate_result = await db.execute(
                select(User).where(User.id == candidate_id)
            )
            candidate = candidate_result.scalar_one_or_none()
            if candidate:
                # Calculate simple compatibility score
                compatibility = min(100, (common_count / len(rated_media_ids)) * 100)

                similar_users.append({
                    "id": candidate.id,
                    "username": candidate.username,
                    "avatar_url": candidate.avatar_url,
                    "level": candidate.level,
                    "compatibility_score": round(compatibility, 1),
                    "common_ratings": common_count
                })

        # Sort by compatibility and limit
        similar_users.sort(key=lambda x: x['compatibility_score'], reverse=True)
        return similar_users[:limit]