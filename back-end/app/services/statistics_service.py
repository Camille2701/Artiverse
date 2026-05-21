from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from app.models import User, Media, Rating, Review, List, ListItem, MediaType
from typing import Dict, List
from datetime import datetime, timedelta


class StatisticsService:
    """Service for user statistics and analytics."""

    @staticmethod
    def get_user_statistics(db: Session, user_id: str) -> Dict:
        """Get comprehensive statistics for a user."""
        # Basic counts
        total_reviews = db.query(Review).filter(Review.user_id == user_id).count()
        total_ratings = db.query(Rating).filter(Rating.user_id == user_id).count()
        total_lists = db.query(List).filter(List.user_id == user_id).count()

        # Total media in lists
        user_lists = db.query(List).filter(List.user_id == user_id).all()
        list_ids = [lst.id for lst in user_lists]
        total_media_in_lists = db.query(ListItem).filter(ListItem.list_id.in_(list_ids)).count()

        # Reviews by media type
        reviews_by_type = db.query(
            Media.media_type,
            func.count(Review.id).label('count')
        ).join(
            Review, Media.id == Review.media_id
        ).filter(
            Review.user_id == user_id
        ).group_by(Media.media_type).all()

        reviews_by_type_dict = {media_type.value: count for media_type, count in reviews_by_type}

        # Ratings by media type
        ratings_by_type = db.query(
            Media.media_type,
            func.count(Rating.id).label('count'),
            func.avg(Rating.score).label('avg_score')
        ).join(
            Rating, Media.id == Rating.media_id
        ).filter(
            Rating.user_id == user_id
        ).group_by(Media.media_type).all()

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
        daily_reviews = db.query(
            func.date(Review.created_at).label('date'),
            func.count(Review.id).label('count')
        ).filter(
            and_(
                Review.user_id == user_id,
                Review.created_at >= thirty_days_ago
            )
        ).group_by(func.date(Review.created_at)).all()

        # Ratings per day
        daily_ratings = db.query(
            func.date(Rating.created_at).label('date'),
            func.count(Rating.id).label('count')
        ).filter(
            and_(
                Rating.user_id == user_id,
                Rating.created_at >= thirty_days_ago
            )
        ).group_by(func.date(Rating.created_at)).all()

        # Combine activity data
        activity_timeline = {}
        for date_str, count in daily_reviews:
            activity_timeline[str(date_str)] = activity_timeline.get(str(date_str), 0) + count

        for date_str, count in daily_ratings:
            activity_timeline[str(date_str)] = activity_timeline.get(str(date_str), 0) + count

        # Top rated media by user
        top_rated = db.query(
            Media,
            Rating.score
        ).join(
            Rating, Media.id == Rating.media_id
        ).filter(
            and_(
                Rating.user_id == user_id,
                Rating.score >= 8
            )
        ).order_by(desc(Rating.score)).limit(5).all()

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

        # Most reviewed media types
        total_interactions = total_reviews + total_ratings
        taste_distribution = {}

        for media_type in MediaType:
            type_reviews = reviews_by_type_dict.get(media_type.value, 0)
            type_ratings = ratings_by_type_dict.get(media_type.value, {}).get('count', 0)
            type_total = type_reviews + type_ratings

            if total_interactions > 0:
                taste_distribution[media_type.value] = {
                    'total': type_total,
                    'percentage': round((type_total / total_interactions) * 100, 1)
                }
            else:
                taste_distribution[media_type.value] = {
                    'total': type_total,
                    'percentage': 0
                }

        return {
            'user_id': user_id,
            'total_reviews': total_reviews,
            'total_ratings': total_ratings,
            'total_lists': total_lists,
            'total_media_in_lists': total_media_in_lists,
            'total_interactions': total_interactions,
            'reviews_by_type': reviews_by_type_dict,
            'ratings_by_type': ratings_by_type_dict,
            'activity_timeline': activity_timeline,
            'top_rated': top_rated_list,
            'taste_distribution': taste_distribution,
            'generated_at': datetime.now().isoformat()
        }

    @staticmethod
    def get_platform_statistics(db: Session) -> Dict:
        """Get platform-wide statistics."""
        total_users = db.query(User).count()
        total_media = db.query(Media).count()
        total_reviews = db.query(Review).count()
        total_ratings = db.query(Rating).count()
        total_lists = db.query(List).count()

        # Media by type
        media_by_type = db.query(
            Media.media_type,
            func.count(Media.id).label('count')
        ).group_by(Media.media_type).all()

        media_by_type_dict = {media_type.value: count for media_type, count in media_by_type}

        # Most active users (by total interactions)
        user_activity = db.query(
            User.id,
            User.username,
            func.count(Review.id).label('review_count'),
            func.count(Rating.id).label('rating_count')
        ).outerjoin(
            Review, User.id == Review.user_id
        ).outerjoin(
            Rating, User.id == Rating.user_id
        ).group_by(User.id).order_by(
            desc(func.count(Review.id) + func.count(Rating.id))
        ).limit(10).all()

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
    def get_user_comparison(db: Session, user_id: str, compare_user_id: str) -> Dict:
        """Compare statistics between two users."""
        user1_stats = StatisticsService.get_user_statistics(db, user_id)
        user2_stats = StatisticsService.get_user_statistics(db, compare_user_id)

        # Calculate compatibility based on common rated media
        common_ratings = db.query(
            Rating,
            Media
        ).join(
            Media, Rating.media_id == Media.id
        ).filter(
            Rating.user_id == user_id
        ).filter(
            Rating.media_id.in_(
                db.query(Rating.media_id).filter(Rating.user_id == compare_user_id)
            )
        ).all()

        # Simple compatibility calculation
        compatibility_score = 0
        if common_ratings:
            # Find matching ratings from compare user
            media_ids = [rating.media_id for rating, _ in common_ratings]
            compare_ratings = db.query(Rating).filter(
                and_(
                    Rating.user_id == compare_user_id,
                    Rating.media_id.in_(media_ids)
                )
            ).all()

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