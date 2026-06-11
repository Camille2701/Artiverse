from fastapi import APIRouter

from app.api.v1 import auth, users, media, ratings, reviews, lists, xp, statistics, badges, social, admin

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(media.router)
router.include_router(ratings.router)
router.include_router(reviews.router)
router.include_router(lists.router)
router.include_router(xp.router)
router.include_router(statistics.router)
router.include_router(badges.router)
router.include_router(social.router)
router.include_router(admin.router)
