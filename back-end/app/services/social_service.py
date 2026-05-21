from sqlalchemy.orm import Session
from app.models import User, Follow, ActivityLog, ActivityType, Media, Rating, Review
from sqlalchemy import func, and_, desc
from typing import List, Dict, Optional
from datetime import datetime


class SocialService:
    """Service for social features like follows and activity feeds."""

    @staticmethod
    def follow_user(db: Session, follower: User, followed_id: str) -> bool:
        """Follow a user."""
        # Can't follow yourself
        if follower.id == followed_id:
            raise ValueError("Cannot follow yourself")

        # Check if user exists
        followed = db.query(User).filter(User.id == followed_id).first()
        if not followed:
            raise ValueError("User not found")

        # Check if already following
        existing = db.query(Follow).filter(
            and_(
                Follow.follower_id == follower.id,
                Follow.followed_id == followed_id
            )
        ).first()

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

        db.commit()
        return True

    @staticmethod
    def unfollow_user(db: Session, follower: User, followed_id: str) -> bool:
        """Unfollow a user."""
        follow = db.query(Follow).filter(
            and_(
                Follow.follower_id == follower.id,
                Follow.followed_id == followed_id
            )
        ).first()

        if not follow:
            return False  # Not following

        db.delete(follow)
        db.commit()
        return True

    @staticmethod
    def get_following(db: Session, user_id: str, limit: int = 50) -> List[Dict]:
        """Get users that the given user is following."""
        follows = db.query(Follow).filter(
            Follow.follower_id == user_id
        ).order_by(desc(Follow.created_at)).limit(limit).all()

        following_users = []
        for follow in follows:
            user = db.query(User).filter(User.id == follow.followed_id).first()
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
    def get_followers(db: Session, user_id: str, limit: int = 50) -> List[Dict]:
        """Get users that follow the given user."""
        follows = db.query(Follow).filter(
            Follow.followed_id == user_id
        ).order_by(desc(Follow.created_at)).limit(limit).all()

        follower_users = []
        for follow in follows:
            user = db.query(User).filter(User.id == follow.follower_id).first()
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
    def is_following(db: Session, follower_id: str, followed_id: str) -> bool:
        """Check if follower is following followed."""
        follow = db.query(Follow).filter(
            and_(
                Follow.follower_id == follower_id,
                Follow.followed_id == followed_id
            )
        ).first()
        return follow is not None

    @staticmethod
    def get_follow_stats(db: Session, user_id: str) -> Dict:
        """Get follow statistics for a user."""
        following_count = db.query(func.count(Follow.id)).filter(
            Follow.follower_id == user_id
        ).scalar() or 0

        followers_count = db.query(func.count(Follow.id)).filter(
            Follow.followed_id == user_id
        ).scalar() or 0

        return {
            "following_count": following_count,
            "followers_count": followers_count
        }

    @staticmethod
    def log_activity(db: Session, user_id: str, activity_type: ActivityType,
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
        db.commit()
        db.refresh(activity)
        return activity

    @staticmethod
    def get_user_activity(db: Session, user_id: str, limit: int = 20) -> List[Dict]:
        """Get recent activity for a user."""
        activities = db.query(ActivityLog).filter(
            ActivityLog.user_id == user_id
        ).order_by(desc(ActivityLog.created_at)).limit(limit).all()

        activity_list = []
        for activity in activities:
            user = db.query(User).filter(User.id == activity.user_id).first()
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
                media = db.query(Media).filter(Media.id == activity.entity_id).first()
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
    def get_feed(db: Session, user_id: str, limit: int = 20) -> List[Dict]:
        """Get activity feed from followed users."""
        # Get IDs of users that the current user follows
        followed_ids = [f.followed_id for f in db.query(Follow).filter(
            Follow.follower_id == user_id
        ).all()]

        if not followed_ids:
            return []

        # Get recent activities from followed users
        activities = db.query(ActivityLog).filter(
            ActivityLog.user_id.in_(followed_ids)
        ).order_by(desc(ActivityLog.created_at)).limit(limit).all()

        feed_items = []
        for activity in activities:
            user = db.query(User).filter(User.id == activity.user_id).first()
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
                media = db.query(Media).filter(Media.id == activity.entity_id).first()
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
    def get_similar_users(db: Session, user_id: str, limit: int = 10) -> List[Dict]:
        """Get users with similar taste based on ratings."""
        # Get current user's ratings
        user_ratings = db.query(Rating).filter(Rating.user_id == user_id).all()

        if len(user_ratings) < 3:
            # Not enough data for similarity calculation
            return []

        # Get media IDs rated by current user
        rated_media_ids = [r.media_id for r in user_ratings]

        # Find other users who have rated the same media
        similar_candidates = db.query(
            Rating.user_id,
            func.count(Rating.id).label('common_ratings')
        ).filter(
            and_(
                Rating.media_id.in_(rated_media_ids),
                Rating.user_id != user_id
            )
        ).group_by(Rating.user_id).having(
            func.count(Rating.id) >= 3  # At least 3 common ratings
        ).order_by(desc('common_ratings')).limit(limit * 2).all()

        similar_users = []
        for candidate_id, common_count in similar_candidates:
            candidate = db.query(User).filter(User.id == candidate_id).first()
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