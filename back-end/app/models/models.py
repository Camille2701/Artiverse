from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey, Enum, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
import uuid

from app.db.base import Base


class MediaType(str, enum.Enum):
    """Enum for media types."""
    MOVIE = "movie"
    TV_SERIES = "tv_series"
    BOOK = "book"
    VIDEO_GAME = "video_game"


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    avatar_url = Column(String(512), nullable=True)
    bio = Column(Text, nullable=True)
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    lists = relationship("List", back_populates="user", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_user_username", "username"),
        Index("idx_user_email", "email"),
    )


class Media(Base):
    """Media model for movies, TV series, books, and video games."""
    __tablename__ = "media"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    media_type = Column(Enum(MediaType), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    original_title = Column(String(255), nullable=True)
    synopsis = Column(Text, nullable=True)
    release_date = Column(DateTime(timezone=True), nullable=True)
    cover_image = Column(String(512), nullable=True)
    banner_image = Column(String(512), nullable=True)
    average_rating = Column(Float, default=0.0)
    popularity_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    reviews = relationship("Review", back_populates="media", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="media", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_media_title", "title"),
        Index("idx_media_type", "media_type"),
    )


class Rating(Base):
    """Rating model - one rating per user per media."""
    __tablename__ = "ratings"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    media_id = Column(String, ForeignKey("media.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)  # 1-10 scale
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    media = relationship("Media", back_populates="ratings")
    
    __table_args__ = (
        UniqueConstraint("user_id", "media_id", name="unique_user_media_rating"),
        Index("idx_rating_user_id", "user_id"),
        Index("idx_rating_media_id", "media_id"),
    )


class Review(Base):
    """Review model."""
    __tablename__ = "reviews"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    media_id = Column(String, ForeignKey("media.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    spoiler = Column(Boolean, default=False)
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    media = relationship("Media", back_populates="reviews")
    
    __table_args__ = (
        Index("idx_review_user_id", "user_id"),
        Index("idx_review_media_id", "media_id"),
        Index("idx_review_created_at", "created_at"),
    )


class List(Base):
    """User list model (e.g., Watched, Wishlist, Currently Watching)."""
    __tablename__ = "lists"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    visibility = Column(String(50), default="private")  # private, friends, public
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="lists")
    items = relationship("ListItem", back_populates="list", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_list_user_id", "user_id"),
        UniqueConstraint("user_id", "name", name="unique_user_list_name"),
    )


class ListItem(Base):
    """Items in a user list."""
    __tablename__ = "list_items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    list_id = Column(String, ForeignKey("lists.id", ondelete="CASCADE"), nullable=False)
    media_id = Column(String, ForeignKey("media.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    list = relationship("List", back_populates="items")
    media = relationship("Media")
    
    __table_args__ = (
        UniqueConstraint("list_id", "media_id", name="unique_list_media"),
        Index("idx_list_item_list_id", "list_id"),
        Index("idx_list_item_media_id", "media_id"),
    )
