from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, desc, and_, select
from app.models import User, Media, Rating, Review, List, ListItem, MediaType
from typing import Dict
from datetime import datetime, timedelta


class StatisticsService:
    """Service for user statistics and analytics."""

    @staticmethod
    async def get_user_statistics(db: AsyncSession, user_id: str) -> Dict:
        """Get comprehensive statistics for a user."""
        # Basic counts
        result = await db.execute(
            select(func.count()).select_from(Review).where(Review.user_id == user_id)
        )
        total_reviews = result.scalar()

        result = await db.execute(
            select(func.count()).select_from(Rating).where(Rating.user_id == user_id)
        )
        total_ratings = result.scalar()

        result = await db.execute(
            select(func.count()).select_from(List).where(List.user_id == user_id)
        )
        total_lists = result.scalar()

        # Total media in lists
        result = await db.execute(
            select(List).where(List.user_id == user_id)
        )
        user_lists = result.scalars().all()
        list_ids = [lst.id for lst in user_lists]

        if list_ids:
            result = await db.execute(
                select(func.count()).select_from(ListItem).where(ListItem.list_id.in_(list_ids))
            )
            total_media_in_lists = result.scalar()
        else:
            total_media_in_lists = 0

        # Reviews by media type
        reviews_by_type_result = await db.execute(
            select(Media.media_type, func.count(Review.id).label('count'))
            .join(Review, Media.id == Review.media_id)
            .where(Review.user_id == user_id)
            .group_by(Media.media_type)
        )
        reviews_by_type = reviews_by_type_result.all()

        reviews_by_type_dict = {media_type.value: count for media_type, count in reviews_by_type}

        # Ratings by media type
        ratings_by_type_result = await db.execute(
            select(Media.media_type,
                   func.count(Rating.id).label('count'),
                   func.avg(Rating.score).label('avg_score'))
            .join(Rating, Media.id == Rating.media_id)
            .where(Rating.user_id == user_id)
            .group_by(Media.media_type)
        )
        ratings_by_type = ratings_by_type_result.all()

        ratings_by_type_dict = {
            media_type.value: {
                'count': count,
                'average_score': float(avg_score) if avg_score else 0
            }
            for media_type, count, avg_score in ratings_by_type
        }

        # Activity timeline (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)

        # Reviews per day
        daily_reviews_result = await db.execute(
            select(func.date(Review.created_at).label('date'),
                   func.count(Review.id).label('count'))
            .where(and_(
                Review.user_id == user_id,
                Review.created_at >= thirty_days_ago
            ))
            .group_by(func.date(Review.created_at))
        )
        daily_reviews = daily_reviews_result.all()

        # Ratings per day
        daily_ratings_result = await db.execute(
            select(func.date(Rating.created_at).label('date'),
                   func.count(Rating.id).label('count'))
            .where(and_(
                Rating.user_id == user_id,
                Rating.created_at >= thirty_days_ago
            ))
            .group_by(func.date(Rating.created_at))
        )
        daily_ratings = daily_ratings_result.all()

        # Combine activity data
        activity_timeline = {}
        for date_str, count in daily_reviews:
            activity_timeline[str(date_str)] = activity_timeline.get(str(date_str), 0) + count

        for date_str, count in daily_ratings:
            activity_timeline[str(date_str)] = activity_timeline.get(str(date_str), 0) + count

        # Top rated media by user
        top_rated_result = await db.execute(
            select(Media, Rating.score)
            .join(Rating, Media.id == Rating.media_id)
            .where(and_(
                Rating.user_id == user_id,
                Rating.score >= 8
            ))
            .order_by(desc(Rating.score))
            .limit(5)
        )
        top_rated = top_rated_result.all()

        top_rated_list = [
            {
                'media_id': media.id,
                'title': media.title,
                'media_type': media.media_type.value,
                'cover_image': media.cover_image,
                'rating': score
            }
            for media, score in top_rated
        ]

        # Taste distribution — based on ratings only (one rating = one media consumed)
        taste_distribution = {}
        total_rated = sum(
            ratings_by_type_dict.get(mt.value, {}).get('count', 0)
            for mt in MediaType
        )

        for media_type in MediaType:
            count = ratings_by_type_dict.get(media_type.value, {}).get('count', 0)
            taste_distribution[media_type.value] = {
                'total': count,
                'percentage': round((count / total_rated) * 100, 1) if total_rated > 0 else 0
            }

        return {
            'user_id': user_id,
            'total_reviews': total_reviews,
            'total_ratings': total_ratings,
            'total_lists': total_lists,
            'total_media_in_lists': total_media_in_lists,
            'total_interactions': total_reviews + total_ratings,
            'reviews_by_type': reviews_by_type_dict,
            'ratings_by_type': ratings_by_type_dict,
            'activity_timeline': activity_timeline,
            'top_rated': top_rated_list,
            'taste_distribution': taste_distribution,
            'generated_at': datetime.now().isoformat()
        }

    @staticmethod
    async def get_platform_statistics(db: AsyncSession) -> Dict:
        """Get platform-wide statistics."""
        result = await db.execute(select(func.count()).select_from(User))
        total_users = result.scalar()

        result = await db.execute(select(func.count()).select_from(Media))
        total_media = result.scalar()

        result = await db.execute(select(func.count()).select_from(Review))
        total_reviews = result.scalar()

        result = await db.execute(select(func.count()).select_from(Rating))
        total_ratings = result.scalar()

        result = await db.execute(select(func.count()).select_from(List))
        total_lists = result.scalar()

        # Media by type
        media_by_type_result = await db.execute(
            select(Media.media_type, func.count(Media.id).label('count'))
            .group_by(Media.media_type)
        )
        media_by_type = media_by_type_result.all()

        media_by_type_dict = {media_type.value: count for media_type, count in media_by_type}

        # Most active users (by total interactions)
        user_activity_result = await db.execute(
            select(User.id, User.username,
                   func.count(Review.id).label('review_count'),
                   func.count(Rating.id).label('rating_count'))
            .outerjoin(Review, User.id == Review.user_id)
            .outerjoin(Rating, User.id == Rating.user_id)
            .group_by(User.id)
            .order_by(desc(func.count(Review.id) + func.count(Rating.id)))
            .limit(10)
        )
        user_activity = user_activity_result.all()

        most_active_users = [
            {
                'user_id': user_id,
                'username': username,
                'total_activity': review_count + rating_count,
                'reviews': review_count,
                'ratings': rating_count
            }
            for user_id, username, review_count, rating_count in user_activity
        ]

        return {
            'total_users': total_users,
            'total_media': total_media,
            'total_reviews': total_reviews,
            'total_ratings': total_ratings,
            'total_lists': total_lists,
            'media_by_type': media_by_type_dict,
            'most_active_users': most_active_users,
            'generated_at': datetime.now().isoformat()
        }

    @staticmethod
    async def get_user_comparison(db: AsyncSession, user_id: str, compare_user_id: str) -> Dict:
        """Compare statistics between two users."""
        user1_stats = await StatisticsService.get_user_statistics(db, user_id)
        user2_stats = await StatisticsService.get_user_statistics(db, compare_user_id)

        # Calculate compatibility based on common rated media
        # First, get media IDs rated by compare_user_id
        compare_media_result = await db.execute(
            select(Rating.media_id).where(Rating.user_id == compare_user_id)
        )
        compare_media_ids = [row[0] for row in compare_media_result.all()]

        if compare_media_ids:
            # Get common ratings
            common_ratings_result = await db.execute(
                select(Rating, Media)
                .join(Media, Rating.media_id == Media.id)
                .where(and_(
                    Rating.user_id == user_id,
                    Rating.media_id.in_(compare_media_ids)
                ))
            )
            common_ratings = common_ratings_result.all()
        else:
            common_ratings = []

        # Simple compatibility calculation
        compatibility_score = 0
        if common_ratings:
            # Find matching ratings from compare user
            media_ids = [rating.media_id for rating, _ in common_ratings]

            compare_ratings_result = await db.execute(
                select(Rating).where(and_(
                    Rating.user_id == compare_user_id,
                    Rating.media_id.in_(media_ids)
                ))
            )
            compare_ratings = compare_ratings_result.scalars().all()

            # Calculate similarity
            total_diff = 0
            for rating, _ in common_ratings:
                for compare_rating in compare_ratings:
                    if rating.media_id == compare_rating.media_id:
                        total_diff += abs(rating.score - compare_rating.score)
                        break

            avg_diff = total_diff / len(common_ratings) if common_ratings else 0
            compatibility_score = max(0, 100 - (avg_diff * 10))  # Convert to percentage

        return {
            'user1': user1_stats,
            'user2': user2_stats,
            'compatibility_score': round(compatibility_score, 1),
            'common_media_count': len(common_ratings),
            'generated_at': datetime.now().isoformat()
        }