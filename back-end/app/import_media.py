"""
Media Import Script for Artiverse

This script imports media data from various sources:
1. TMDb (The Movie Database) - Movies & TV Shows
2. GoodReads - Books
3. RAWG - Video Games

Requirements:
- pip install requests pandas
- TMDB API key (free): https://www.themoviedb.org/settings/api
- GoodReads datasets (optional): https://cseweb.ucsd.edu/~jmcauley/datasets/goodreads.html
- RAWG API (free): https://api.rawg.io/docs/

Usage:
    # Import from TMDb (recommended - real-time data with images)
    docker compose exec backend python -m app.import_media --source tmdb --api-key YOUR_TMDB_KEY

    # Import from GoodReads dataset (requires downloaded CSV)
    docker compose exec backend python -m app.import_media --source goodreads --file goodreads_books.json

    # Import from RAWG (video games)
    docker compose exec backend python -m app.import_media --source rawg --api-key YOUR_RAWG_KEY

    # Import sample data from all sources
    docker compose exec backend python -m app.import_media --sample
"""

import asyncio
import argparse
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional
import json

import requests
import pandas as pd
from sqlalchemy import select

from app.db import AsyncSessionLocal
from app.models import Media, MediaType
from app.utils.security import get_password_hash


# Constants
TMDB_BASE_URL = "https://api.themoviedb.org/3"
RAWG_BASE_URL = "https://api.rawg.io/api"


class TMDBImporter:
    """Import media from TMDb API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """Make a GET request to TMDb API."""
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        response = self.session.get(f"{TMDB_BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def get_popular_movies(self, limit: int = 50) -> List[dict]:
        """Get popular movies from TMDb."""
        movies = []
        page = 1

        while len(movies) < limit:
            data = self._get('/movie/popular', {'page': page})
            for movie in data.get('results', []):
                if len(movies) >= limit:
                    break
                movies.append(movie)
            page += 1
            if page > data.get('total_pages', 1):
                break

        return movies

    def get_popular_tv_shows(self, limit: int = 50) -> List[dict]:
        """Get popular TV shows from TMDb."""
        shows = []
        page = 1

        while len(shows) < limit:
            data = self._get('/tv/popular', {'page': page})
            for show in data.get('results', []):
                if len(shows) >= limit:
                    break
                shows.append(show)
            page += 1
            if page > data.get('total_pages', 1):
                break

        return shows

    def get_movie_details(self, movie_id: int) -> dict:
        """Get detailed information about a movie."""
        return self._get(f'/movie/{movie_id}', {
            'append_to_response': 'credits,videos,external_ids'
        })

    def get_tv_details(self, tv_id: int) -> dict:
        """Get detailed information about a TV show."""
        return self._get(f'/tv/{tv_id}', {
            'append_to_response': 'credits,videos,external_ids'
        })

    def format_movie(self, movie: dict) -> dict:
        """Format TMDb movie data for Artiverse."""
        return {
            'media_type': MediaType.MOVIE,
            'title': movie.get('title', ''),
            'original_title': movie.get('original_title'),
            'synopsis': movie.get('overview', ''),
            'release_date': self._parse_date(movie.get('release_date')),
            'cover_image': self._get_image_url(movie.get('poster_path')),
            'banner_image': self._get_image_url(movie.get('backdrop_path'), is_banner=True),
            'average_rating': movie.get('vote_average', 0),
            'popularity_score': movie.get('popularity', 0),
            'genres': [g.get('name') for g in movie.get('genres', [])],
            'creators': self._get_creators(movie),
            'franchise': movie.get('belongsToCollection', {}).get('name') if movie.get('belongsToCollection') else None,
            'external_ids': {
                'tmdb': str(movie.get('id')),
                'imdb': movie.get('imdb_id')
            }
        }

    def format_tv_show(self, show: dict) -> dict:
        """Format TMDb TV show data for Artiverse."""
        return {
            'media_type': MediaType.SERIE,
            'title': show.get('name', ''),
            'original_title': show.get('original_name'),
            'synopsis': show.get('overview', ''),
            'release_date': self._parse_date(show.get('first_air_date')),
            'cover_image': self._get_image_url(show.get('poster_path')),
            'banner_image': self._get_image_url(show.get('backdrop_path'), is_banner=True),
            'average_rating': show.get('vote_average', 0),
            'popularity_score': show.get('popularity', 0),
            'genres': [g.get('name') for g in show.get('genres', [])],
            'creators': [c.get('name') for c in show.get('created_by', [])],
            'franchise': None,
            'external_ids': {
                'tmdb': str(show.get('id'))
            }
        }

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime object."""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            return None

    def _get_image_url(self, path: Optional[str], is_banner: bool = False) -> Optional[str]:
        """Get full image URL from TMDb path."""
        if not path:
            return None
        size = 'w1280' if is_banner else 'w500'
        return f"https://image.tmdb.org/t/p/{size}{path}"

    def _get_creators(self, movie: dict) -> List[str]:
        """Extract creators (directors, writers) from movie data."""
        creators = []
        crew = movie.get('credits', {}).get('crew', [])

        for person in crew:
            job = person.get('job', '').lower()
            if job in ['director', 'writer', 'screenplay']:
                name = person.get('name', '')
                if name and name not in creators:
                    creators.append(name)

        return creators


class RAWGImporter:
    """Import video games from RAWG API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """Make a GET request to RAWG API."""
        if params is None:
            params = {}
        params['key'] = self.api_key
        response = self.session.get(f"{RAWG_BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def get_popular_games(self, limit: int = 50) -> List[dict]:
        """Get popular games from RAWG."""
        games = []
        page = 1

        while len(games) < limit:
            data = self._get('/games', {
                'page': page,
                'page_size': 40,
                'ordering': '-rating'
            })
            for game in data.get('results', []):
                if len(games) >= limit:
                    break
                games.append(game)
            page += 1
            if not data.get('next'):
                break

        return games

    def format_game(self, game: dict) -> dict:
        """Format RAWG game data for Artiverse."""
        return {
            'media_type': MediaType.GAME,
            'title': game.get('name', ''),
            'original_title': None,
            'synopsis': game.get('description_raw', '')[:1000],  # Limit description length
            'release_date': self._parse_date(game.get('released')),
            'cover_image': game.get('background_image'),
            'banner_image': game.get('background_image_additional'),
            'average_rating': game.get('rating', 0) * 2,  # Convert 0-5 scale to 0-10
            'popularity_score': game.get('metacritic', 0) if game.get('metacritic') else 0,
            'genres': [g.get('name') for g in game.get('genres', [])],
            'creators': [p.get('name') for p in game.get('publishers', [])],
            'franchise': None,
            'external_ids': {
                'rawg': str(game.get('id'))
            }
        }

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime object."""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            return None


class GoodReadsImporter:
    """Import books from GoodReads dataset."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_books(self, limit: int = 100) -> List[dict]:
        """Load books from GoodReads JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data[:limit]
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.file_path}")
            return []

    def format_book(self, book: dict) -> dict:
        """Format GoodReads book data for Artiverse."""
        # Try different field names as GoodReads datasets vary
        title = book.get('Title') or book.get('title') or book.get('book_title') or ''
        authors = book.get('Authors') or book.get('authors') or book.get('author') or []
        description = book.get('Description') or book.get('description') or book.get('book_description') or ''
        isbn = book.get('ISBN') or book.get('isbn') or book.get('isbn13') or ''
        year = book.get('Year') or book.get('year') or book.get('publication_year') or None

        # Handle authors as list
        if isinstance(authors, str):
            authors = [authors]
        elif isinstance(authors, dict):
            authors = list(authors.values())

        return {
            'media_type': MediaType.BOOK,
            'title': title,
            'original_title': None,
            'synopsis': str(description)[:1000] if description else '',
            'release_date': self._parse_year(year),
            'cover_image': self._get_cover_image(book, isbn),
            'banner_image': None,
            'average_rating: 0,
            'popularity_score': 0,
            'genres': [],
            'creators': authors if isinstance(authors, list) else [str(authors)],
            'franchise': None,
            'external_ids': {
                'isbn': str(isbn) if isbn else None
            }
        }

    def _parse_year(self, year: Optional[Any]) -> Optional[datetime]:
        """Parse year to datetime object."""
        if not year:
            return None
        try:
            year_int = int(str(year)[:4])  # Handle various formats
            if 1800 <= year_int <= datetime.now().year + 1:
                return datetime(year_int, 1, 1)
        except (ValueError, TypeError):
            pass
        return None

    def _get_cover_image(self, book: dict, isbn: str) -> Optional[str]:
        """Get cover image URL from book data."""
        # Try different field names
        image = book.get('Image') or book.get('image') or book.get('cover_url') or book.get('cover')

        if image:
            return str(image)

        # Fallback to Open Library Covers API
        if isbn:
            return f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

        return None


async def import_media_to_db(media_data: List[dict]) -> dict:
    """Import formatted media data into database."""
    results = {
        'success': 0,
        'skipped': 0,
        'error': 0,
        'total': len(media_data)
    }

    async with AsyncSessionLocal() as db:
        for media_item in media_data:
            try:
                # Check if media already exists by title and media_type
                existing = await db.execute(
                    select(Media).where(
                        Media.title == media_item['title'],
                        Media.media_type == media_item['media_type']
                    )
                )
                if existing.scalar_one_or_none():
                    results['skipped'] += 1
                    continue

                # Create new media
                media = Media(
                    media_type=media_item['media_type'],
                    title=media_item['title'],
                    original_title=media_item.get('original_title'),
                    synopsis=media_item.get('synopsis'),
                    release_date=media_item.get('release_date'),
                    cover_image=media_item.get('cover_image'),
                    banner_image=media_item.get('banner_image'),
                    franchise=media_item.get('franchise'),
                    genres=media_item.get('genres', []),
                    creators=media_item.get('creators', []),
                    average_rating=media_item.get('average_rating', 0),
                    popularity_score=media_item.get('popularity_score', 0)
                )

                db.add(media)
                await db.commit()
                results['success'] += 1

                print(f"✓ Imported: {media_item['title']} ({media_item['media_type']})")

            except Exception as e:
                print(f"✗ Error importing {media_item.get('title', 'Unknown')}: {e}")
                results['error'] += 1
                await db.rollback()

    return results


async def import_sample_data():
    """Import sample data from TMDb (no API key needed for sample)."""
    print("📥 Importing sample media data...")

    # Use some popular, public domain data
    sample_media = [
        {
            'media_type': MediaType.MOVIE,
            'title': 'The Shawshank Redemption',
            'synopsis': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
            'release_date': datetime(1994, 9, 23),
            'cover_image': 'https://image.tmdb.org/t/p/w500/9O7gLzmreU3uos5qsbLBJcmMz9.jpg',
            'banner_image': 'https://image.tmdb.org/t/p/w1280/xmTa5UkJfumRhAgqDZRwb7Miq2.jpg',
            'franchise': None,
            'genres': ['Drama'],
            'creators': ['Frank Darabont'],
            'average_rating': 8.7,
            'popularity_score': 95.0
        },
        {
            'media_type': MediaType.MOVIE,
            'title': 'The Godfather',
            'synopsis': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
            'release_date': datetime(1972, 3, 24),
            'cover_image': 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
            'banner_image': 'https://image.tmdb.org/t/p/w1280/t5UuVscLm7PCByMwRc7iFqTOwv.jpg',
            'franchise': 'The Godfather',
            'genres': ['Drama', 'Crime'],
            'creators': ['Francis Ford Coppola'],
            'average_rating': 8.7,
            'popularity_score': 92.0
        },
        {
            'media_type': MediaType.SERIE,
            'title': 'Breaking Bad',
            'synopsis': 'A chemistry teacher diagnosed with lung cancer turns to manufacturing and selling methamphetamine.',
            'release_date': datetime(2008, 1, 20),
            'cover_image': 'https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg',
            'banner_image': 'https://image.tmdb.org/t/p/w1280/tsRy63Mu5cu8etL1X7ZLyf7UP1M.jpg',
            'franchise': None,
            'genres': ['Drama', 'Crime', 'Thriller'],
            'creators': ['Vince Gilligan'],
            'average_rating': 9.5,
            'popularity_score': 97.0
        },
        {
            'media_type': MediaType.GAME,
            'title': 'The Legend of Zelda: Breath of the Wild',
            'synopsis': 'Link awakens from a deep sleep and must explore the wilds of Hyrule to stop Calamity Ganon.',
            'release_date': datetime(2017, 3, 3),
            'cover_image': 'https://image.tmdb.org/t/p/w500/zjTxDJTTMfjVyLJB5vukk2FFseM.jpg',
            'banner_image': 'https://image.tmdb.org/t/p/w1280/a7ZGXQvnVhHfJNPWq1eL4SBZyk9.jpg',
            'franchise': 'The Legend of Zelda',
            'genres': ['Adventure', 'Action', 'RPG'],
            'creators': ['Nintendo'],
            'average_rating': 9.4,
            'popularity_score': 95.0
        },
        {
            'media_type': MediaType.BOOK,
            'title': '1984',
            'synopsis': 'Among the seminal texts of the 20th century, Nineteen Eighty-Four is a rare work that grows more haunting as its futuristic purgatory becomes more real.',
            'release_date': datetime(1949, 6, 8),
            'cover_image': 'https://covers.openlibrary.org/b/id/8428146-L.jpg',
            'banner_image': None,
            'franchise': None,
            'genres': ['Dystopian', 'Science Fiction', 'Classic'],
            'creators': ['George Orwell'],
            'average_rating': 8.4,
            'popularity_score': 76.0
        }
    ]

    results = await import_media_to_db(sample_media)

    print(f"\n{'='*50}")
    print(f"Sample data import completed!")
    print(f"✓ Success: {results['success']}")
    print(f"⊝ Skipped: {results['skipped']}")
    print(f"✗ Errors: {results['error']}")
    print(f"{'='*50}")


async def main():
    parser = argparse.ArgumentParser(description='Import media data to Artiverse')
    parser.add_argument('--source', choices=['tmdb', 'rawg', 'goodreads', 'sample'],
                        help='Data source to import from')
    parser.add_argument('--api-key', help='API key for the service')
    parser.add_argument('--file', help='Path to data file (for GoodReads)')
    parser.add_argument('--limit', type=int, default=50, help='Number of items to import')

    args = parser.parse_args()

    if not args.source:
        print("Error: Please specify --source (tmdb, rawg, goodreads, sample)")
        parser.print_help()
        sys.exit(1)

    if args.source == 'sample':
        await import_sample_data()
        return

    if args.source == 'tmdb' and not args.api_key:
        print("Error: TMDb requires --api-key")
        print("Get your free API key at: https://www.themoviedb.org/settings/api")
        sys.exit(1)

    if args.source == 'rawg' and not args.api_key:
        print("Error: RAWG requires --api-key")
        print("Get your free API key at: https://api.rawg.io/docs/")
        sys.exit(1)

    if args.source == 'goodreads' and not args.file:
        print("Error: GoodReads requires --file path to JSON dataset")
        print("Download datasets from: https://cseweb.ucsd.edu/~jmcauley/datasets/goodreads.html")
        sys.exit(1)

    media_data = []

    try:
        if args.source == 'tmdb':
            print(f"🎬 Importing from TMDb...")
            importer = TMDBImporter(args.api_key)

            print(f"Fetching {args.limit} popular movies...")
            movies = importer.get_popular_movies(args.limit // 2 + 1)
            for movie in movies[:args.limit // 2]:
                try:
                    details = importer.get_movie_details(movie['id'])
                    media_data.append(importer.format_movie(details))
                except Exception as e:
                    print(f"Error fetching movie details: {e}")

            print(f"Fetching {args.limit // 2} popular TV shows...")
            shows = importer.get_popular_tv_shows(args.limit // 2)
            for show in shows[:args.limit // 2]:
                try:
                    details = importer.get_tv_details(show['id'])
                    media_data.append(importer.format_tv_show(details))
                except Exception as e:
                    print(f"Error fetching TV show details: {e}")

        elif args.source == 'rawg':
            print(f"🎮 Importing from RAWG...")
            importer = RAWGImporter(args.api_key)

            print(f"Fetching {args.limit} popular games...")
            games = importer.get_popular_games(args.limit)
            for game in games:
                media_data.append(importer.format_game(game))

        elif args.source == 'goodreads':
            print(f"📚 Importing from GoodReads dataset...")
            importer = GoodReadsImporter(args.file)

            print(f"Loading {args.limit} books from {args.file}...")
            books = importer.load_books(args.limit)
            for book in books:
                media_data.append(importer.format_book(book))

        # Import to database
        if media_data:
            print(f"\n📥 Importing {len(media_data)} items to database...")
            results = await import_media_to_db(media_data)

            print(f"\n{'='*50}")
            print(f"Import completed!")
            print(f"✓ Success: {results['success']}")
            print(f"⊝ Skipped: {results['skipped']}")
            print(f"✗ Errors: {results['error']}")
            print(f"{'='*50}")
        else:
            print("No media data to import")

    except Exception as e:
        print(f"Error during import: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
