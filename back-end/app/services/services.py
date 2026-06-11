from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.models import User, Media, Rating, Review, List, ListItem, ActivityType
from app.schemas import (
    UserCreate, MediaCreate, RatingCreate, ReviewCreate, ListCreate
)
from app.utils.security import get_password_hash
from app.services.xp_service import XPService
from app.services.social_service import SocialService


class UserService:
    """Service for user-related operations."""

    @staticmethod
    async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
        """Create a new user."""
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=get_password_hash(user_create.password),
            bio=user_create.bio,
            avatar_url=user_create.avatar_url
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
        """Get user by username."""
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        """Get user by email."""
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
        """Get user by ID."""
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()


class MediaService:
    """Service for media-related operations."""

    @staticmethod
    async def create_media(db: AsyncSession, media_create: MediaCreate, cover_image: str = None, banner_image: str = None) -> Media:
        """Create a new media."""
        db_media = Media(
            media_type=media_create.media_type,
            title=media_create.title,
            original_title=media_create.original_title,
            synopsis=media_create.synopsis,
            release_date=media_create.release_date,
            cover_image=cover_image,
            banner_image=banner_image,
            franchise=media_create.franchise,
            genres=media_create.genres,
            creators=media_create.creators,
        )
        db.add(db_media)
        await db.commit()
        await db.refresh(db_media)
        return db_media

    @staticmethod
    async def get_media_by_id(db: AsyncSession, media_id: str) -> Media | None:
        """Get media by ID."""
        result = await db.execute(
            select(Media).where(Media.id == media_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def search_media(db: AsyncSession, query: str, media_type: str | None = None, skip: int = 0, limit: int = 10,
                          min_rating: float | None = None, max_rating: float | None = None,
                          year_from: int | None = None, year_to: int | None = None,
                          sort_by: str = "relevance") -> tuple[list[Media], int]:
        """Enhanced search media with multiple filters."""
        # Build base query
        if query:
            stmt = select(Media).where(
                (Media.title.ilike(f"%{query}%")) |
                (Media.original_title.ilike(f"%{query}%")) |
                (Media.synopsis.ilike(f"%{query}%"))
            )
        else:
            stmt = select(Media)

        # Apply filters
        if media_type:
            stmt = stmt.where(Media.media_type == media_type)

        if min_rating is not None:
            stmt = stmt.where(Media.average_rating >= min_rating)

        if max_rating is not None:
            stmt = stmt.where(Media.average_rating <= max_rating)

        if year_from is not None:
            stmt = stmt.where(Media.release_date >= f"{year_from}-01-01")

        if year_to is not None:
            stmt = stmt.where(Media.release_date <= f"{year_to}-12-31")

        # Apply sorting
        if sort_by == "rating":
            stmt = stmt.order_by(desc(Media.average_rating))
        elif sort_by == "popularity":
            stmt = stmt.order_by(desc(Media.popularity_score))
        elif sort_by == "newest":
            stmt = stmt.order_by(desc(Media.release_date))
        elif sort_by == "oldest":
            stmt = stmt.order_by(Media.release_date)
        else:  # relevance (default)
            # For relevance, prioritize exact title matches
            if query:
                stmt = stmt.order_by(
                    Media.title.ilike(query).desc(),
                    Media.popularity_score.desc()
                )
            else:
                stmt = stmt.order_by(desc(Media.popularity_score))

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await db.execute(count_stmt)
        total = total_result.scalar()

        # Get paginated results
        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        items = result.scalars().all()

        return items, total

    @staticmethod
    async def get_trending_media(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[Media]:
        """Get trending media sorted by popularity."""
        result = await db.execute(
            select(Media)
            .order_by(desc(Media.popularity_score))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def delete_media(db: AsyncSession, media_id: str) -> bool:
        """Delete a media by ID. Returns True if a row was removed."""
        stmt = select(Media).where(Media.id == media_id)
        result = await db.execute(stmt)
        media = result.scalar_one_or_none()

        if media:
            await db.delete(media)
            await db.commit()
            return True
        return False

    @staticmethod
    def _suggestion_score(source: Media, candidate: Media) -> float:
        """Rank candidates: franchise > shared creators > shared genres > popularity."""
        score = float(candidate.popularity_score or 0) * 0.01

        if source.franchise and candidate.franchise and source.franchise == candidate.franchise:
            score += 100

        source_creators = set(source.creators or [])
        candidate_creators = set(candidate.creators or [])
        shared_creators = source_creators & candidate_creators
        score += len(shared_creators) * 25

        source_genres = set(source.genres or [])
        candidate_genres = set(candidate.genres or [])
        shared_genres = source_genres & candidate_genres
        score += len(shared_genres) * 10

        if source.media_type == candidate.media_type:
            score += 2

        return score

    @staticmethod
    async def get_suggestions(
        db: AsyncSession,
        media_id: str,
        limit: int = 8,
    ) -> list[Media]:
        """Return ranked media suggestions for a given media item."""
        source = await MediaService.get_media_by_id(db, media_id)
        if not source:
            return []

        result = await db.execute(select(Media).where(Media.id != media_id))
        candidates = result.scalars().all()

        ranked = sorted(
            candidates,
            key=lambda candidate: MediaService._suggestion_score(source, candidate),
            reverse=True,
        )

        return ranked[:limit]


class RatingService:
    """Service for rating-related operations."""

    @staticmethod
    async def create_or_update_rating(db: AsyncSession, rating_create: RatingCreate, user_id: str) -> Rating:
        """Create or update a rating."""
        # Get user
        user_result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()

        # Check for existing rating
        existing_result = await db.execute(
            select(Rating).where(
                Rating.user_id == user_id,
                Rating.media_id == rating_create.media_id
            )
        )
        existing_rating = existing_result.scalar_one_or_none()

        if existing_rating:
            existing_rating.score = rating_create.score
            db.add(existing_rating)
            updated_rating = existing_rating
        else:
            db_rating = Rating(
                user_id=user_id,
                media_id=rating_create.media_id,
                score=rating_create.score
            )
            db.add(db_rating)
            updated_rating = db_rating

            # Award XP for rating (only for new ratings)
            if user:
                await XPService.award_rating_xp(db, user)

        await db.commit()
        await db.refresh(updated_rating)
        return updated_rating

    @staticmethod
    async def get_rating(db: AsyncSession, user_id: str, media_id: str) -> Rating | None:
        """Get a specific rating."""
        result = await db.execute(
            select(Rating).where(
                Rating.user_id == user_id,
                Rating.media_id == media_id
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_rating(db: AsyncSession, rating_id: str):
        """Delete a rating."""
        result = await db.execute(
            select(Rating).where(Rating.id == rating_id)
        )
        rating = result.scalar_one_or_none()

        if rating:
            await db.delete(rating)
            await db.commit()


class ReviewService:
    """Service for review-related operations."""

    @staticmethod
    async def create_review(db: AsyncSession, review_create: ReviewCreate, user_id: str) -> Review:
        """Create a new review."""
        user_result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()

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
            await XPService.award_review_xp(db, user)

            # Log activity
            await SocialService.log_activity(
                db, user_id, ActivityType.REVIEW_CREATED,
                entity_type="media", entity_id=review_create.media_id,
                metadata={"review_title": review_create.title}
            )

        await db.commit()
        await db.refresh(db_review)
        return db_review

    @staticmethod
    async def get_review_by_id(db: AsyncSession, review_id: str) -> Review | None:
        """Get review by ID."""
        result = await db.execute(
            select(Review).where(Review.id == review_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_reviews_by_media(db: AsyncSession, media_id: str, skip: int = 0, limit: int = 10) -> tuple[list[Review], int]:
        """Get reviews for a media."""
        # Get total count
        count_stmt = select(func.count()).select_from(
            select(Review).where(Review.media_id == media_id).subquery()
        )
        total_result = await db.execute(count_stmt)
        total = total_result.scalar()

        # Get paginated results
        stmt = (
            select(Review)
            .where(Review.media_id == media_id)
            .order_by(desc(Review.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        items = result.scalars().all()

        return items, total

    @staticmethod
    async def get_reviews_by_user(db: AsyncSession, user_id: str, skip: int = 0, limit: int = 10) -> tuple[list[Review], int]:
        """Get reviews by a user."""
        # Get total count
        count_stmt = select(func.count()).select_from(
            select(Review).where(Review.user_id == user_id).subquery()
        )
        total_result = await db.execute(count_stmt)
        total = total_result.scalar()

        # Get paginated results
        stmt = (
            select(Review)
            .where(Review.user_id == user_id)
            .order_by(desc(Review.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        items = result.scalars().all()

        return items, total

    @staticmethod
    async def delete_review(db: AsyncSession, review_id: str):
        """Delete a review."""
        result = await db.execute(
            select(Review).where(Review.id == review_id)
        )
        review = result.scalar_one_or_none()

        if review:
            await db.delete(review)
            await db.commit()


class ListService:
    """Service for list-related operations."""

    @staticmethod
    async def create_list(db: AsyncSession, list_create: ListCreate, user_id: str) -> List:
        """Create a new list."""
        user_result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()

        db_list = List(
            user_id=user_id,
            name=list_create.name,
            visibility=list_create.visibility
        )
        db.add(db_list)

        # Award XP for creating a list
        if user:
            await XPService.award_list_creation_xp(db, user)

        await db.commit()
        await db.refresh(db_list)
        return db_list

    @staticmethod
    async def get_list_by_id(db: AsyncSession, list_id: str) -> List | None:
        """Get list by ID."""
        result = await db.execute(
            select(List).where(List.id == list_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_lists(db: AsyncSession, user_id: str) -> list[List]:
        """Get all lists for a user."""
        result = await db.execute(
            select(List).where(List.user_id == user_id)
        )
        return result.scalars().all()

    @staticmethod
    async def add_to_list(db: AsyncSession, list_id: str, media_id: str) -> ListItem:
        """Add media to a list."""
        list_result = await db.execute(
            select(List).where(List.id == list_id)
        )
        list_obj = list_result.scalar_one_or_none()

        user = None
        if list_obj:
            user_result = await db.execute(
                select(User).where(User.id == list_obj.user_id)
            )
            user = user_result.scalar_one_or_none()

        list_item = ListItem(
            list_id=list_id,
            media_id=media_id
        )
        db.add(list_item)

        # Award XP for adding media to list
        if user:
            await XPService.award_media_added_to_list_xp(db, user)

        await db.commit()
        await db.refresh(list_item)
        return list_item

    @staticmethod
    async def remove_from_list(db: AsyncSession, list_id: str, media_id: str):
        """Remove media from a list."""
        result = await db.execute(
            select(ListItem).where(
                ListItem.list_id == list_id,
                ListItem.media_id == media_id
            )
        )
        list_item = result.scalar_one_or_none()

        if list_item:
            await db.delete(list_item)
            await db.commit()

    @staticmethod
    async def delete_list(db: AsyncSession, list_id: str):
        """Delete a list."""
        result = await db.execute(
            select(List).where(List.id == list_id)
        )
        list_obj = result.scalar_one_or_none()

        if list_obj:
            await db.delete(list_obj)
            await db.commit()
