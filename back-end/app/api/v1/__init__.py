from fastapi import APIRouter

from app.api.v1 import auth, users, media, ratings, reviews, lists

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(media.router)
router.include_router(ratings.router)
router.include_router(reviews.router)
router.include_router(lists.router)
