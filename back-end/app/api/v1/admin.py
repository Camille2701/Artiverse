from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional

from app.dependencies.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/admin", tags=["admin"])


def _require_admin(current_user: User = Depends(get_current_user)) -> User:
    if "admin" not in (current_user.email or ""):
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


class ImportRequest(BaseModel):
    source: str  # "sample", "tmdb", "rawg"
    api_key: Optional[str] = None
    limit: int = 50


class ImportResult(BaseModel):
    success: int
    skipped: int
    error: int
    total: int
    message: str


@router.post("/import", response_model=ImportResult)
async def import_media(
    request: ImportRequest,
    current_user: User = Depends(_require_admin),
):
    """
    Trigger media import from external sources.
    Supported sources: sample, tmdb, rawg
    """
    from app.import_media import (
        import_sample_data,
        import_media_to_db,
        TMDBImporter,
        RAWGImporter,
    )
    import asyncio

    if request.source == "sample":
        try:
            # Run the sample import directly
            from app.models import MediaType
            from datetime import datetime

            sample_media = [
                {
                    "media_type": MediaType.MOVIE,
                    "title": "The Shawshank Redemption",
                    "synopsis": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                    "release_date": datetime(1994, 9, 23),
                    "cover_image": "https://image.tmdb.org/t/p/w500/9O7gLzmreU3uos5qsbLBJcmMz9.jpg",
                    "banner_image": "https://image.tmdb.org/t/p/w1280/xmTa5UkJfumRhAgqDZRwb7Miq2.jpg",
                    "franchise": None,
                    "genres": ["Drama"],
                    "creators": ["Frank Darabont"],
                    "average_rating": 8.7,
                    "popularity_score": 95.0,
                },
                {
                    "media_type": MediaType.MOVIE,
                    "title": "The Godfather",
                    "synopsis": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                    "release_date": datetime(1972, 3, 24),
                    "cover_image": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
                    "banner_image": None,
                    "franchise": "The Godfather",
                    "genres": ["Drama", "Crime"],
                    "creators": ["Francis Ford Coppola"],
                    "average_rating": 8.7,
                    "popularity_score": 92.0,
                },
                {
                    "media_type": MediaType.TV_SERIES,
                    "title": "Breaking Bad",
                    "synopsis": "A chemistry teacher diagnosed with lung cancer turns to manufacturing and selling methamphetamine.",
                    "release_date": datetime(2008, 1, 20),
                    "cover_image": "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg",
                    "banner_image": None,
                    "franchise": None,
                    "genres": ["Drama", "Crime", "Thriller"],
                    "creators": ["Vince Gilligan"],
                    "average_rating": 9.5,
                    "popularity_score": 97.0,
                },
                {
                    "media_type": MediaType.VIDEO_GAME,
                    "title": "The Legend of Zelda: Breath of the Wild",
                    "synopsis": "Link awakens from a deep sleep and must explore the wilds of Hyrule to stop Calamity Ganon.",
                    "release_date": datetime(2017, 3, 3),
                    "cover_image": "https://upload.wikimedia.org/wikipedia/en/c/c6/The_Legend_of_Zelda_Breath_of_the_Wild.jpg",
                    "banner_image": None,
                    "franchise": "The Legend of Zelda",
                    "genres": ["Adventure", "Action", "RPG"],
                    "creators": ["Nintendo"],
                    "average_rating": 9.4,
                    "popularity_score": 95.0,
                },
                {
                    "media_type": MediaType.BOOK,
                    "title": "1984",
                    "synopsis": "Among the seminal texts of the 20th century, a haunting depiction of a totalitarian society.",
                    "release_date": datetime(1949, 6, 8),
                    "cover_image": "https://covers.openlibrary.org/b/id/8428146-L.jpg",
                    "banner_image": None,
                    "franchise": None,
                    "genres": ["Dystopian", "Science Fiction"],
                    "creators": ["George Orwell"],
                    "average_rating": 8.4,
                    "popularity_score": 76.0,
                },
                {
                    "media_type": MediaType.MOVIE,
                    "title": "Inception",
                    "synopsis": "A thief who steals corporate secrets through the use of dream-sharing technology.",
                    "release_date": datetime(2010, 7, 16),
                    "cover_image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
                    "banner_image": None,
                    "franchise": None,
                    "genres": ["Action", "Science Fiction", "Thriller"],
                    "creators": ["Christopher Nolan"],
                    "average_rating": 8.8,
                    "popularity_score": 91.0,
                },
                {
                    "media_type": MediaType.TV_SERIES,
                    "title": "Game of Thrones",
                    "synopsis": "Nine noble families fight for control of the mythical land of Westeros.",
                    "release_date": datetime(2011, 4, 17),
                    "cover_image": "https://image.tmdb.org/t/p/w500/u3bZgnGQ9T01sWNhyveQz0wH0Hl.jpg",
                    "banner_image": None,
                    "franchise": "A Song of Ice and Fire",
                    "genres": ["Drama", "Fantasy"],
                    "creators": ["David Benioff", "D. B. Weiss"],
                    "average_rating": 9.2,
                    "popularity_score": 99.0,
                },
                {
                    "media_type": MediaType.VIDEO_GAME,
                    "title": "The Witcher 3: Wild Hunt",
                    "synopsis": "As war rages on throughout the Northern Realms, you take on the greatest contract of your life.",
                    "release_date": datetime(2015, 5, 19),
                    "cover_image": "https://upload.wikimedia.org/wikipedia/en/0/0c/Witcher_3_cover_art.jpg",
                    "banner_image": None,
                    "franchise": "The Witcher",
                    "genres": ["RPG", "Adventure"],
                    "creators": ["CD Projekt Red"],
                    "average_rating": 9.6,
                    "popularity_score": 98.0,
                },
                {
                    "media_type": MediaType.BOOK,
                    "title": "The Lord of the Rings",
                    "synopsis": "A meek hobbit of the Shire and eight companions set out on a journey to Mount Doom to destroy the One Ring.",
                    "release_date": datetime(1954, 7, 29),
                    "cover_image": "https://covers.openlibrary.org/b/id/8406786-L.jpg",
                    "banner_image": None,
                    "franchise": "Middle-earth",
                    "genres": ["Fantasy", "Adventure"],
                    "creators": ["J.R.R. Tolkien"],
                    "average_rating": 9.0,
                    "popularity_score": 92.0,
                },
            ]

            results = await import_media_to_db(sample_media)
            return ImportResult(
                success=results["success"],
                skipped=results["skipped"],
                error=results["error"],
                total=results["total"],
                message=f"Importation terminée : {results['success']} ajoutés, {results['skipped']} ignorés.",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    elif request.source == "tmdb":
        if not request.api_key:
            raise HTTPException(status_code=400, detail="api_key is required for TMDb source")
        try:
            importer = TMDBImporter(request.api_key)
            media_data = []

            movies = importer.get_popular_movies(request.limit // 2)
            for movie in movies:
                try:
                    details = importer.get_movie_details(movie["id"])
                    media_data.append(importer.format_movie(details))
                except Exception:
                    pass

            shows = importer.get_popular_tv_shows(request.limit // 2)
            for show in shows:
                try:
                    details = importer.get_tv_details(show["id"])
                    media_data.append(importer.format_tv_show(details))
                except Exception:
                    pass

            results = await import_media_to_db(media_data)
            return ImportResult(
                success=results["success"],
                skipped=results["skipped"],
                error=results["error"],
                total=results["total"],
                message=f"TMDb import terminé : {results['success']} ajoutés.",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    elif request.source == "rawg":
        if not request.api_key:
            raise HTTPException(status_code=400, detail="api_key is required for RAWG source")
        try:
            importer = RAWGImporter(request.api_key)
            games = importer.get_popular_games(request.limit)
            media_data = [importer.format_game(g) for g in games]
            results = await import_media_to_db(media_data)
            return ImportResult(
                success=results["success"],
                skipped=results["skipped"],
                error=results["error"],
                total=results["total"],
                message=f"RAWG import terminé : {results['success']} ajoutés.",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    else:
        raise HTTPException(status_code=400, detail=f"Unknown source: {request.source}")
