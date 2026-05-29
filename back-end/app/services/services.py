from sqlalchemy.orm import Session
from app.models import User, Media, Rating, Review, List, ListItem, ActivityType
from app.schemas import (
    UserCreate, MediaCreate, RatingCreate, ReviewCreate, ListCreate
)
from app.utils.security import get_password_hash
from sqlalchemy import func, desc
from app.services.xp_service import XPService
from app.services.social_service import SocialService


class UserService:
    """Service for user-related operations."""
    
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user."""
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=get_password_hash(user_create.password),
            bio=user_create.bio,
            avatar_url=user_create.avatar_url
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User | None:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()


class MediaService:
    """Service for media-related operations."""
    
    @staticmethod
    def create_media(db: Session, media_create: MediaCreate, cover_image: str = None, banner_image: str = None) -> Media:
        """Create a new media."""
        db_media = Media(
            media_type=media_create.media_type,
            title=media_create.title,
            original_title=media_create.original_title,
            synopsis=media_create.synopsis,
            release_date=media_create.release_date,
            cover_image=cover_image,
            banner_image=banner_image
        )
        db.add(db_media)
        db.commit()
        db.refresh(db_media)
        return db_media
    
    @staticmethod
    def get_media_by_id(db: Session, media_id: str) -> Media | None:
        """Get media by ID."""
        return db.query(Media).filter(Media.id == media_id).first()
    
    @staticmethod
    def search_media(db: Session, query: str, media_type: str | None = None, skip: int = 0, limit: int = 10,
                    min_rating: float | None = None, max_rating: float | None = None,
                    year_from: int | None = None, year_to: int | None = None,
                    sort_by: str = "relevance") -> tuple[list[Media], int]:
        """Enhanced search media with multiple filters."""
        # Build base query
        if query:
            q = db.query(Media).filter(
                (Media.title.ilike(f"%{query}%")) |
                (Media.original_title.ilike(f"%{query}%")) |
                (Media.synopsis.ilike(f"%{query}%"))
            )
        else:
            q = db.query(Media)

        # Apply filters
        if media_type:
            q = q.filter(Media.media_type == media_type)

        if min_rating is not None:
            q = q.filter(Media.average_rating >= min_rating)

        if max_rating is not None:
            q = q.filter(Media.average_rating <= max_rating)

        if year_from is not None:
            q = q.filter(Media.release_date >= f"{year_from}-01-01")

        if year_to is not None:
            q = q.filter(Media.release_date <= f"{year_to}-12-31")

        # Apply sorting
        if sort_by == "rating":
            q = q.order_by(desc(Media.average_rating))
        elif sort_by == "popularity":
            q = q.order_by(desc(Media.popularity_score))
        elif sort_by == "newest":
            q = q.order_by(desc(Media.release_date))
        elif sort_by == "oldest":
            q = q.order_by(Media.release_date)
        else:  # relevance (default)
            # For relevance, prioritize exact title matches
            if query:
                q = q.order_by(
                    Media.title.ilike(query).desc(),
                    Media.popularity_score.desc()
                )
            else:
                q = q.order_by(desc(Media.popularity_score))

        total = q.count()
        items = q.offset(skip).limit(limit).all()
        return items, total
    
    @staticmethod
    def get_trending_media(db: Session, skip: int = 0, limit: int = 10) -> list[Media]:
        """Get trending media sorted by popularity."""
        return db.query(Media).order_by(desc(Media.popularity_score)).offset(skip).limit(limit).all()

    @staticmethod
    def delete_media(db: Session, media_id: str) -> bool:
        """Delete a media by ID. Returns True if a row was removed."""
        deleted = db.query(Media).filter(Media.id == media_id).delete()
        db.commit()
        return bool(deleted)


class RatingService:
    """Service for rating-related operations."""
    
    @staticmethod
    def create_or_update_rating(db: Session, rating_create: RatingCreate, user_id: str) -> Rating:
        """Create or update a rating."""
        user = db.query(User).filter(User.id == user_id).first()
        existing_rating = db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.media_id == rating_create.media_id
        ).first()

        if existing_rating:
            existing_rating.score = rating_create.score
            db.add(existing_rating)
        else:
            db_rating = Rating(
                user_id=user_id,
                media_id=rating_create.media_id,
                score=rating_create.score
            )
            db.add(db_rating)

            # Award XP for rating (only for new ratings)
            if user:
                XPService.award_rating_xp(db, user)

        db.commit()
        db.refresh(db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.media_id == rating_create.media_id
        ).first())
        return db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.media_id == rating_create.media_id
        ).first()
    
    @staticmethod
    def get_rating(db: Session, user_id: str, media_id: str) -> Rating | None:
        """Get a specific rating."""
        return db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.media_id == media_id
        ).first()
    
    @staticmethod
    def delete_rating(db: Session, rating_id: str):
        """Delete a rating."""
        db.query(Rating).filter(Rating.id == rating_id).delete()
        db.commit()


class ReviewService:
    """Service for review-related operations."""
    
    @staticmethod
    def create_review(db: Session, review_create: ReviewCreate, user_id: str) -> Review:
        """Create a new review."""
        user = db.query(User).filter(User.id == user_id).first()
        db_review = Review(
            user_id=user_id,
            media_id=review_create.media_id,
            title=review_create.title,
            content=review_create.content,
            spoiler=review_create.spoiler
        )
        db.add(db_review)

        # Award XP for creating a review
        if user:
            XPService.award_review_xp(db, user)

            # Log activity
            SocialService.log_activity(
                db, user_id, ActivityType.REVIEW_CREATED,
                entity_type="media", entity_id=review_create.media_id,
                metadata={"review_title": review_create.title}
            )

        db.commit()
        db.refresh(db_review)
        return db_review
    
    @staticmethod
    def get_review_by_id(db: Session, review_id: str) -> Review | None:
        """Get review by ID."""
        return db.query(Review).filter(Review.id == review_id).first()
    
    @staticmethod
    def get_reviews_by_media(db: Session, media_id: str, skip: int = 0, limit: int = 10) -> tuple[list[Review], int]:
        """Get reviews for a media."""
        q = db.query(Review).filter(Review.media_id == media_id).order_by(desc(Review.created_at))
        total = q.count()
        items = q.offset(skip).limit(limit).all()
        return items, total
    
    @staticmethod
    def get_reviews_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 10) -> tuple[list[Review], int]:
        """Get reviews by a user."""
        q = db.query(Review).filter(Review.user_id == user_id).order_by(desc(Review.created_at))
        total = q.count()
        items = q.offset(skip).limit(limit).all()
        return items, total
    
    @staticmethod
    def delete_review(db: Session, review_id: str):
        """Delete a review."""
        db.query(Review).filter(Review.id == review_id).delete()
        db.commit()


class ListService:
    """Service for list-related operations."""
    
    @staticmethod
    def create_list(db: Session, list_create: ListCreate, user_id: str) -> List:
        """Create a new list."""
        user = db.query(User).filter(User.id == user_id).first()
        db_list = List(
            user_id=user_id,
            name=list_create.name,
            visibility=list_create.visibility
        )
        db.add(db_list)

        # Award XP for creating a list
        if user:
            XPService.award_list_creation_xp(db, user)

        db.commit()
        db.refresh(db_list)
        return db_list
    
    @staticmethod
    def get_list_by_id(db: Session, list_id: str) -> List | None:
        """Get list by ID."""
        return db.query(List).filter(List.id == list_id).first()
    
    @staticmethod
    def get_user_lists(db: Session, user_id: str) -> list[List]:
        """Get all lists for a user."""
        return db.query(List).filter(List.user_id == user_id).all()
    
    @staticmethod
    def add_to_list(db: Session, list_id: str, media_id: str) -> ListItem:
        """Add media to a list."""
        list_obj = db.query(List).filter(List.id == list_id).first()
        user = db.query(User).filter(User.id == list_obj.user_id).first() if list_obj else None

        list_item = ListItem(
            list_id=list_id,
            media_id=media_id
        )
        db.add(list_item)

        # Award XP for adding media to list
        if user:
            XPService.award_media_added_to_list_xp(db, user)

        db.commit()
        db.refresh(list_item)
        return list_item
    
    @staticmethod
    def remove_from_list(db: Session, list_id: str, media_id: str):
        """Remove media from a list."""
        db.query(ListItem).filter(
            ListItem.list_id == list_id,
            ListItem.media_id == media_id
        ).delete()
        db.commit()
    
    @staticmethod
    def delete_list(db: Session, list_id: str):
        """Delete a list."""
        db.query(List).filter(List.id == list_id).delete()
        db.commit()
