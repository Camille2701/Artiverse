from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db import get_db
from app.schemas import UserCreate, Token, UserResponse
from app.services import UserService, XPService
from app.utils.security import verify_password, create_access_token
from app.core.config import settings
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """Register a new user - Frontend compatible format."""
    # Check if user already exists
    if UserService.get_user_by_email(db, user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if UserService.get_user_by_username(db, user_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    user = UserService.create_user(db, user_create)

    # Auto-login after registration
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )

    # Award daily login XP
    xp_result = XPService.award_daily_login_xp(db, user)

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
            "avatar_url": user.avatar_url,
            "level": user.level,
            "experience_points": user.experience_points
        },
        "token": access_token,
        "xp_awarded": xp_result
    }


@router.post("/login")
def login(
    login_data: dict,
    db: Session = Depends(get_db)
):
    """Login and get access token - Frontend compatible format."""
    username = login_data.get("username")
    email = login_data.get("email")
    password = login_data.get("password")

    user = None

    if username:
        user = UserService.get_user_by_username(db, username)
    elif email:
        user = UserService.get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )

    # Award daily login XP
    xp_result = XPService.award_daily_login_xp(db, user)

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
            "avatar_url": user.avatar_url,
            "level": user.level,
            "experience_points": user.experience_points
        },
        "token": access_token,
        "xp_awarded": xp_result
    }


@router.post("/login-form", response_model=Token)
def login_form(
    username: str = None,
    password: str = None,
    email: str = None,
    db: Session = Depends(get_db)
):
    """Login with form data (username or email)."""
    user = None
    
    if username:
        user = UserService.get_user_by_username(db, username)
    elif email:
        user = UserService.get_user_by_email(db, email)
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
