from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum


class MediaTypeEnum(str, Enum):
    MOVIE = "movie"
    TV_SERIES = "tv_series"
    BOOK = "book"
    VIDEO_GAME = "video_game"


# ==================== USER SCHEMAS ====================

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    id: str
    level: int
    experience_points: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProfileResponse(UserResponse):
    pass


# ==================== MEDIA SCHEMAS ====================

def _normalize_release_date(value):
    """Accept a plain date string (YYYY-MM-DD) and promote it to a datetime."""
    if isinstance(value, str) and len(value) == 10:
        return f"{value}T00:00:00"
    return value


class MediaBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    original_title: Optional[str] = None
    synopsis: Optional[str] = None
    release_date: Optional[datetime] = None
    cover_image: Optional[str] = None
    banner_image: Optional[str] = None
    franchise: Optional[str] = None
    genres: Optional[List[str]] = None
    creators: Optional[List[str]] = None

    @field_validator("release_date", mode="before")
    @classmethod
    def _parse_release_date(cls, value):
        return _normalize_release_date(value)


class MediaCreate(MediaBase):
    media_type: MediaTypeEnum


class MediaUpdate(BaseModel):
    title: Optional[str] = None
    original_title: Optional[str] = None
    synopsis: Optional[str] = None
    release_date: Optional[datetime] = None
    cover_image: Optional[str] = None
    banner_image: Optional[str] = None
    franchise: Optional[str] = None
    genres: Optional[List[str]] = None
    creators: Optional[List[str]] = None

    @field_validator("release_date", mode="before")
    @classmethod
    def _parse_release_date(cls, value):
        return _normalize_release_date(value)


class MediaResponse(MediaBase):
    id: str
    media_type: MediaTypeEnum
    average_rating: float
    popularity_score: float
    created_at: datetime
    updated_at: datetime

    # Additional fields for frontend compatibility
    type: MediaTypeEnum = Field(alias="media_type")
    description: Optional[str] = Field(alias="synopsis")
    rating: float = Field(alias="average_rating")
    image: Optional[str] = Field(alias="cover_image")
    releaseDate: Optional[datetime] = Field(alias="release_date")

    class Config:
        from_attributes = True
        populate_by_name = True


# ==================== RATING SCHEMAS ====================

class RatingBase(BaseModel):
    score: int = Field(..., ge=1, le=10)


class RatingCreate(RatingBase):
    media_id: str


class RatingUpdate(BaseModel):
    score: int = Field(..., ge=1, le=10)


class RatingResponse(RatingBase):
    id: str
    user_id: str
    media_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== REVIEW SCHEMAS ====================

class ReviewBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    spoiler: bool = False


class ReviewCreate(ReviewBase):
    media_id: str


class ReviewUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    spoiler: Optional[bool] = None


class ReviewResponse(ReviewBase):
    id: str
    user_id: str
    media_id: str
    like_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== LIST SCHEMAS ====================

class ListBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    visibility: str = Field(default="private")


class ListCreate(ListBase):
    pass


class ListUpdate(BaseModel):
    name: Optional[str] = None
    visibility: Optional[str] = None


class ListItemResponse(BaseModel):
    id: str
    media_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ListResponse(ListBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    items: list[ListItemResponse] = []

    class Config:
        from_attributes = True


# ==================== AUTH SCHEMAS ====================

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[datetime] = None
