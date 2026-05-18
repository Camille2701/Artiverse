from sqlalchemy.orm import Session
from app.models import User, Media, Rating, Review, List, ListItem
from app.schemas import (
    UserCreate, MediaCreate, RatingCreate, ReviewCreate, ListCreate
)
from app.utils.security import get_password_hash
from sqlalchemy import func, desc


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
    def create_media(db: Session, media_create: MediaCreate) -> Media:
        """Create a new media."""
        db_media = Media(
            media_type=media_create.media_type,
            title=media_create.title,
            original_title=media_create.original_title,
            synopsis=media_create.synopsis,
            release_date=media_create.release_date,
            cover_image=media_create.cover_image,
            banner_image=media_create.banner_image
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
    def search_media(db: Session, query: str, media_type: str | None = None, skip: int = 0, limit: int = 10) -> tuple[list[Media], int]:
        """Search media by title."""
        q = db.query(Media).filter(Media.title.ilike(f"%{query}%"))
        
        if media_type:
            q = q.filter(Media.media_type == media_type)
        
        total = q.count()
        items = q.offset(skip).limit(limit).all()
        return items, total
    
    @staticmethod
    def get_trending_media(db: Session, skip: int = 0, limit: int = 10) -> list[Media]:
        """Get trending media sorted by popularity."""
        return db.query(Media).order_by(desc(Media.popularity_score)).offset(skip).limit(limit).all()


class RatingService:
    """Service for rating-related operations."""
    
    @staticmethod
    def create_or_update_rating(db: Session, rating_create: RatingCreate, user_id: str) -> Rating:
        """Create or update a rating."""
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
        db_review = Review(
            user_id=user_id,
            media_id=review_create.media_id,
            title=review_create.title,
            content=review_create.content,
            spoiler=review_create.spoiler
        )
        db.add(db_review)
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
        db_list = List(
            user_id=user_id,
            name=list_create.name,
            visibility=list_create.visibility
        )
        db.add(db_list)
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
        list_item = ListItem(
            list_id=list_id,
            media_id=media_id
        )
        db.add(list_item)
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
