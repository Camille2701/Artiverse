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
from sqlalchemy import select, func

from app.db import AsyncSessionLocal
from app.models import Media, MediaType, User, Rating, Review as ReviewModel
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
        movies: List[dict] = []
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
        shows: List[dict] = []
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
            'media_type': MediaType.TV_SERIES,
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
        games: List[dict] = []
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
            'media_type': MediaType.VIDEO_GAME,
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
            'average_rating': 0,
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


SAMPLE_BOOKS = [
    # Classiques
    {"title": "1984", "authors": ["George Orwell"], "year": 1949, "isbn": "9780451524935", "genres": ["Dystopian", "Science Fiction"], "synopsis": "Dans un futur totalitaire, Winston Smith travaille pour le Parti qui réécrits l'histoire. Il se rebelle secrètement contre Big Brother.", "rating": 8.5},
    {"title": "Le Meilleur des mondes", "authors": ["Aldous Huxley"], "year": 1932, "isbn": "9782070360024", "genres": ["Dystopian", "Science Fiction"], "synopsis": "Dans un monde parfaitement conditionné où le bonheur est obligatoire, Bernard Marx commence à douter du système.", "rating": 8.1},
    {"title": "Fahrenheit 451", "authors": ["Ray Bradbury"], "year": 1953, "isbn": "9780743247153", "genres": ["Dystopian", "Science Fiction"], "synopsis": "Dans une société future où les livres sont interdits et brûlés, un pompier commence à remettre en question son rôle.", "rating": 8.0},
    {"title": "Le Seigneur des anneaux : La Communauté de l'Anneau", "authors": ["J.R.R. Tolkien"], "year": 1954, "isbn": "9782070612888", "genres": ["Fantasy", "Adventure"], "synopsis": "Le hobbit Frodon Sacquet hérite d'un anneau magique et doit partir en quête pour le détruire avant que Sauron ne l'utilise.", "rating": 9.0},
    {"title": "Harry Potter et la Philosophie de la Pierre", "authors": ["J.K. Rowling"], "year": 1997, "isbn": "9782070541270", "genres": ["Fantasy", "Young Adult"], "synopsis": "Un jeune orphelin découvre à ses 11 ans qu'il est un sorcier et intègre l'école de magie Poudlard.", "rating": 8.9},
    {"title": "Le Petit Prince", "authors": ["Antoine de Saint-Exupéry"], "year": 1943, "isbn": "9780156012195", "genres": ["Classic", "Fable"], "synopsis": "Un aviateur rencontre un petit prince venu d'une autre planète et apprend des leçons sur l'amour et la vie.", "rating": 8.7},
    {"title": "Crime et Châtiment", "authors": ["Fiodor Dostoïevski"], "year": 1866, "isbn": "9782070360277", "genres": ["Classic", "Psychological Fiction"], "synopsis": "Raskolnikov, un étudiant pauvre, commet un meurtre et doit affronter la culpabilité qui ronge sa conscience.", "rating": 8.5},
    {"title": "L'Étranger", "authors": ["Albert Camus"], "year": 1942, "isbn": "9782070360024", "genres": ["Classic", "Philosophical Fiction"], "synopsis": "Meursault, un homme indifférent, tue un Arabe sur une plage et est jugé autant pour son manque d'émotion que pour son crime.", "rating": 8.2},
    {"title": "Don Quichotte", "authors": ["Miguel de Cervantes"], "year": 1605, "isbn": "9782070413324", "genres": ["Classic", "Adventure"], "synopsis": "Un noble espagnol, la tête remplie de romans de chevalerie, se prend pour un chevalier errant et part en quête d'aventures.", "rating": 8.0},
    {"title": "Les Misérables", "authors": ["Victor Hugo"], "year": 1862, "isbn": "9782070409228", "genres": ["Classic", "Historical Fiction"], "synopsis": "Jean Valjean, un ancien forçat, tente de se racheter dans la France du XIXe siècle, poursuivi par l'inspecteur Javert.", "rating": 8.6},
    # Fantasy & SF moderne
    {"title": "Dune", "authors": ["Frank Herbert"], "year": 1965, "isbn": "9780441013593", "genres": ["Science Fiction", "Epic"], "synopsis": "Sur la planète désertique Arrakis, Paul Atréides affronte trahison et destin parmi les Fremen pour contrôler l'épice.", "rating": 8.8},
    {"title": "Fondation", "authors": ["Isaac Asimov"], "year": 1951, "isbn": "9780553293357", "genres": ["Science Fiction"], "synopsis": "Hari Seldon crée la psychohistoire pour préserver la civilisation à travers un futur de chaos galactique.", "rating": 8.6},
    {"title": "Ender's Game", "authors": ["Orson Scott Card"], "year": 1985, "isbn": "9780812550702", "genres": ["Science Fiction", "Young Adult"], "synopsis": "Andrew Ender Wiggin est formé dès l'enfance pour devenir le commandant qui sauvera l'humanité d'une invasion extraterrestre.", "rating": 8.4},
    {"title": "Le Nom du Vent", "authors": ["Patrick Rothfuss"], "year": 2007, "isbn": "9782352942689", "genres": ["Fantasy"], "synopsis": "Kvothe, légendaire magicien et musicien, raconte l'histoire de sa vie à un chroniqueur dans une auberge isolée.", "rating": 8.7},
    {"title": "La Roue du Temps : L'Œil du Monde", "authors": ["Robert Jordan"], "year": 1990, "isbn": "9780765342997", "genres": ["Fantasy", "Epic"], "synopsis": "Rand al'Thor et ses amis quittent leur village natal et découvrent que le destin du monde repose sur leurs épaules.", "rating": 8.3},
    {"title": "Le Trône de Fer", "authors": ["George R.R. Martin"], "year": 1996, "isbn": "9782070468959", "genres": ["Fantasy", "Epic"], "synopsis": "Dans les Sept Couronnes de Westeros, les grandes familles se disputent le pouvoir dans une guerre sans merci.", "rating": 9.0},
    {"title": "Neuromancer", "authors": ["William Gibson"], "year": 1984, "isbn": "9780441569595", "genres": ["Science Fiction", "Cyberpunk"], "synopsis": "Case, un hacker au rabais, est recruté pour une mission mystérieuse dans un monde de cyberespace et d'intelligence artificielle.", "rating": 8.0},
    {"title": "Hyperion", "authors": ["Dan Simmons"], "year": 1989, "isbn": "9780553283686", "genres": ["Science Fiction", "Epic"], "synopsis": "Sept pèlerins se rendent sur la planète Hyperion et partagent leurs histoires avant d'affronter le mystérieux Gréement.", "rating": 8.6},
    # Littérature générale
    {"title": "To Kill a Mockingbird", "authors": ["Harper Lee"], "year": 1960, "isbn": "9780061935466", "genres": ["Classic", "Social Commentary"], "synopsis": "Scout Finch grandit dans l'Alabama des années 30 tandis que son père, avocat, défend un homme noir accusé injustement.", "rating": 8.7},
    {"title": "The Great Gatsby", "authors": ["F. Scott Fitzgerald"], "year": 1925, "isbn": "9780743273565", "genres": ["Classic", "Drama"], "synopsis": "Nick Carraway observe l'obsession de son voisin Jay Gatsby pour Daisy Buchanan dans l'Amérique dorée des années 20.", "rating": 8.0},
    {"title": "Orgueil et Préjugés", "authors": ["Jane Austen"], "year": 1813, "isbn": "9780141439518", "genres": ["Classic", "Romance"], "synopsis": "Elizabeth Bennet doit naviguer entre attentes sociales et sentiments personnels face au fier Mr. Darcy.", "rating": 8.6},
    {"title": "Cent Ans de Solitude", "authors": ["Gabriel García Márquez"], "year": 1967, "isbn": "9780060883287", "genres": ["Magic Realism", "Classic"], "synopsis": "La saga de la famille Buendía sur sept générations dans le village imaginaire de Macondo, fondateur du réalisme magique.", "rating": 8.7},
    {"title": "L'Alchimiste", "authors": ["Paulo Coelho"], "year": 1988, "isbn": "9780062315007", "genres": ["Philosophical Fiction", "Fable"], "synopsis": "Santiago, un berger andalou, voyage jusqu'en Égypte à la recherche d'un trésor et découvre le sens de sa Légende Personnelle.", "rating": 7.9},
    {"title": "Le Portrait de Dorian Gray", "authors": ["Oscar Wilde"], "year": 1890, "isbn": "9780141439570", "genres": ["Classic", "Gothic"], "synopsis": "Dorian Gray reste éternellement jeune tandis que son portrait vieillit et révèle la corruption de son âme.", "rating": 8.3},
    {"title": "Moby Dick", "authors": ["Herman Melville"], "year": 1851, "isbn": "9781503280786", "genres": ["Classic", "Adventure"], "synopsis": "Le capitaine Achab mène son équipage dans une quête obsessionnelle pour tuer la baleine blanche qui lui a arraché la jambe.", "rating": 7.8},
    {"title": "Ulysse", "authors": ["James Joyce"], "year": 1922, "isbn": "9780679722762", "genres": ["Classic", "Modernist"], "synopsis": "Un seul jour à Dublin, le 16 juin 1904, suivi par Leopold Bloom et Stephen Dedalus dans un chef-d'œuvre du modernisme.", "rating": 7.6},
    # Thriller & policier
    {"title": "Le Da Vinci Code", "authors": ["Dan Brown"], "year": 2003, "isbn": "9782709626088", "genres": ["Thriller", "Mystery"], "synopsis": "Robert Langdon enquête sur un meurtre au Louvre qui l'entraîne dans une conspiration millénaire liée au christianisme.", "rating": 7.5},
    {"title": "Gone Girl", "authors": ["Gillian Flynn"], "year": 2012, "isbn": "9780307588371", "genres": ["Thriller", "Mystery"], "synopsis": "Le jour de leur 5e anniversaire de mariage, Amy Dunne disparaît. Son mari Nick devient rapidement le principal suspect.", "rating": 8.0},
    {"title": "Millennium : Les Hommes qui n'aimaient pas les femmes", "authors": ["Stieg Larsson"], "year": 2005, "isbn": "9782020873048", "genres": ["Thriller", "Mystery"], "synopsis": "Le journaliste Mikael Blomkvist et la hackeuse Lisbeth Salander enquêtent sur une disparition vieille de 40 ans.", "rating": 8.2},
    {"title": "The Silence of the Lambs", "authors": ["Thomas Harris"], "year": 1988, "isbn": "9780312924584", "genres": ["Thriller", "Horror"], "synopsis": "L'agent Clarice Starling doit obtenir l'aide du Dr Hannibal Lecter pour attraper un tueur en série.", "rating": 8.4},
    # Développement personnel & non-fiction
    {"title": "Sapiens : Une brève histoire de l'humanité", "authors": ["Yuval Noah Harari"], "year": 2011, "isbn": "9782226257017", "genres": ["Non-fiction", "History"], "synopsis": "Une exploration fascinante de l'histoire de l'espèce humaine, de la préhistoire à l'ère moderne.", "rating": 8.5},
    {"title": "Le Monde de Sophie", "authors": ["Jostein Gaarder"], "year": 1991, "isbn": "9782020241113", "genres": ["Philosophical Fiction", "Young Adult"], "synopsis": "Sophie reçoit des lettres mystérieuses d'un philosophe inconnu et découvre l'histoire de la philosophie occidentale.", "rating": 8.0},
    {"title": "L'Art de la guerre", "authors": ["Sun Tzu"], "year": -500, "isbn": "9782070414994", "genres": ["Classic", "Philosophy"], "synopsis": "Traité militaire chinois antique dont les principes stratégiques s'appliquent encore aujourd'hui dans de nombreux domaines.", "rating": 8.1},
    # Young Adult & contemporain
    {"title": "Hunger Games", "authors": ["Suzanne Collins"], "year": 2008, "isbn": "9780439023481", "genres": ["Young Adult", "Dystopian", "Science Fiction"], "synopsis": "Dans un futur dystopique, Katniss Everdeen se porte volontaire pour remplacer sa jeune sœur dans un jeu télévisé mortel.", "rating": 8.4},
    {"title": "Divergente", "authors": ["Veronica Roth"], "year": 2011, "isbn": "9782092535226", "genres": ["Young Adult", "Dystopian", "Science Fiction"], "synopsis": "Dans une société divisée en factions, Tris Prior découvre qu'elle est Divergente, une anomalie qui menace l'ordre établi.", "rating": 7.8},
    {"title": "Le Labyrinthe", "authors": ["James Dashner"], "year": 2009, "isbn": "9782092530726", "genres": ["Young Adult", "Dystopian", "Science Fiction"], "synopsis": "Thomas se réveille dans un labyrinthe géant sans aucun souvenir de son passé, entouré d'autres adolescents dans la même situation.", "rating": 7.9},
    {"title": "Twilight", "authors": ["Stephenie Meyer"], "year": 2005, "isbn": "9780316160179", "genres": ["Young Adult", "Romance", "Fantasy"], "synopsis": "Bella Swan emménage à Forks et tombe amoureuse d'Edward Cullen, un vampire centenaire qui lutte contre ses instincts.", "rating": 7.3},
    {"title": "The Fault in Our Stars", "authors": ["John Green"], "year": 2012, "isbn": "9780525478812", "genres": ["Young Adult", "Romance", "Drama"], "synopsis": "Hazel et Gus se rencontrent dans un groupe de soutien pour adolescents atteints de cancer et tombent amoureux.", "rating": 8.0},
    # Littérature française
    {"title": "L'Écume des jours", "authors": ["Boris Vian"], "year": 1947, "isbn": "9782070368228", "genres": ["Surrealism", "Romance", "Classic"], "synopsis": "Colin et Chloé vivent un amour dans un monde poétique et surréaliste jusqu'à ce qu'un nénuphar grandisse dans le poumon de Chloé.", "rating": 8.0},
    {"title": "Le Grand Meaulnes", "authors": ["Alain-Fournier"], "year": 1913, "isbn": "9782070360697", "genres": ["Classic", "Coming-of-age"], "synopsis": "Augustin Meaulnes découvre un domaine mystérieux et tombe amoureux d'une jeune fille. Une quête de l'idéal perdu.", "rating": 7.8},
    {"title": "Voyage au bout de la nuit", "authors": ["Louis-Ferdinand Céline"], "year": 1932, "isbn": "9782070313044", "genres": ["Classic", "Modernist"], "synopsis": "Ferdinand Bardamu traverse les horreurs de la guerre, de la colonisation et de la misère dans un roman désespéré et novateur.", "rating": 8.2},
    {"title": "La Peste", "authors": ["Albert Camus"], "year": 1947, "isbn": "9782070360253", "genres": ["Classic", "Allegorical Fiction"], "synopsis": "Une épidémie de peste s'abat sur Oran, en Algérie. Le Dr Rieux et ses compagnons luttent contre l'absurde et la mort.", "rating": 8.3},
    # Romans graphiques & manga (livres)
    {"title": "Persepolis", "authors": ["Marjane Satrapi"], "year": 2000, "isbn": "9782844140128", "genres": ["Graphic Novel", "Autobiography"], "synopsis": "L'auteure retrace son enfance en Iran pendant la révolution islamique et son adolescence en exil à Vienne.", "rating": 8.6},
    {"title": "Maus", "authors": ["Art Spiegelman"], "year": 1980, "isbn": "9780679748403", "genres": ["Graphic Novel", "History"], "synopsis": "L'histoire de la survie du père de l'auteur pendant l'Holocauste, racontée avec des souris pour les Juifs et des chats pour les nazis.", "rating": 8.8},
    # Biographies & mémoires
    {"title": "Journal d'Anne Frank", "authors": ["Anne Frank"], "year": 1947, "isbn": "9782070400089", "genres": ["Autobiography", "History", "War"], "synopsis": "Le journal intime d'une jeune fille juive se cachant avec sa famille à Amsterdam pendant l'occupation nazie.", "rating": 8.6},
    {"title": "Educated", "authors": ["Tara Westover"], "year": 2018, "isbn": "9780399590504", "genres": ["Autobiography", "Non-fiction"], "synopsis": "Tara Westover grandit dans une famille survivaliste sans aller à l'école et parvient à décrocher un doctorat à Cambridge.", "rating": 8.4},
    # Horreur
    {"title": "It", "authors": ["Stephen King"], "year": 1986, "isbn": "9780450411434", "genres": ["Horror", "Coming-of-age"], "synopsis": "Dans la ville de Derry, un groupe d'enfants affronte une entité terrifiante qui se manifeste sous la forme d'un clown.", "rating": 8.5},
    {"title": "Shining", "authors": ["Stephen King"], "year": 1977, "isbn": "9780385121675", "genres": ["Horror", "Psychological Fiction"], "synopsis": "Jack Torrance s'installe avec sa famille dans un hôtel isolé pour en être le gardien d'hiver. L'hôtel a d'autres plans.", "rating": 8.4},
    {"title": "Frankenstein", "authors": ["Mary Shelley"], "year": 1818, "isbn": "9780141439471", "genres": ["Classic", "Horror", "Science Fiction"], "synopsis": "Victor Frankenstein crée un être vivant à partir de parties de cadavres et en subit les terribles conséquences.", "rating": 8.1},
    {"title": "Dracula", "authors": ["Bram Stoker"], "year": 1897, "isbn": "9780141439846", "genres": ["Classic", "Horror", "Gothic"], "synopsis": "Jonathan Harker visite le château du comte Dracula en Transylvanie et découvre l'existence terrifiante des vampires.", "rating": 8.0},
    # Romans récents
    {"title": "L'Ombre du vent", "authors": ["Carlos Ruiz Zafón"], "year": 2001, "isbn": "9782246641414", "genres": ["Mystery", "Historical Fiction"], "synopsis": "Daniel Sempere découvre un roman mystérieux dans le Cimetière des Livres Oubliés et cherche son auteur dans la Barcelone d'après-guerre.", "rating": 8.5},
    {"title": "La Vérité sur l'affaire Harry Quebert", "authors": ["Joël Dicker"], "year": 2012, "isbn": "9782877068901", "genres": ["Thriller", "Mystery"], "synopsis": "Marcus Goldman, jeune écrivain, tente d'innocenter son mentor Harry Quebert accusé du meurtre d'une jeune fille 35 ans auparavant.", "rating": 8.0},
    {"title": "Americanah", "authors": ["Chimamanda Ngozi Adichie"], "year": 2013, "isbn": "9780307455925", "genres": ["Literary Fiction", "Social Commentary"], "synopsis": "Ifemelu quitte le Nigeria pour les États-Unis et observe les subtilités de la race en Amérique à travers son blog.", "rating": 8.2},
    {"title": "Le Problème à trois corps", "authors": ["Liu Cixin"], "year": 2006, "isbn": "9782330042073", "genres": ["Science Fiction", "Hard SF"], "synopsis": "Un signal radio envoyé dans l'espace pendant la Révolution culturelle chinoise provoque une invasion extraterrestre imminente.", "rating": 8.7},
    {"title": "Normal People", "authors": ["Sally Rooney"], "year": 2018, "isbn": "9780571334650", "genres": ["Literary Fiction", "Romance", "Coming-of-age"], "synopsis": "Marianne et Connell naviguent une relation complexe de l'école secondaire en Irlande jusqu'à l'université de Dublin.", "rating": 7.8},
    {"title": "Anxious People", "authors": ["Fredrik Backman"], "year": 2019, "isbn": "9781501160844", "genres": ["Literary Fiction", "Humor", "Drama"], "synopsis": "Un braquage raté dans une agence immobilière réunit des inconnus dans un appartement et révèle leurs vies secrètes.", "rating": 8.1},
    {"title": "Where the Crawdads Sing", "authors": ["Delia Owens"], "year": 2018, "isbn": "9780735224292", "genres": ["Literary Fiction", "Mystery"], "synopsis": "Kya Clark, la fille des marais abandonnée par sa famille, grandit seule dans les bayous de Caroline du Nord.", "rating": 8.3},
]


SAMPLE_STAR_WARS = [
    # Films
    {"media_type": MediaType.MOVIE, "title": "Star Wars : Un Nouvel Espoir", "original_title": "Star Wars: A New Hope", "authors": ["George Lucas"], "year": 1977, "cover": "https://image.tmdb.org/t/p/w500/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg", "banner": "https://image.tmdb.org/t/p/w1280/zqkmTXzjkAgXmEWLRsY4UpTWCeo.jpg", "genres": ["Science Fiction", "Adventure", "Action"], "synopsis": "Luke Skywalker, jeune fermier de Tatooine, rejoint la Rébellion contre l'Empire Galactique en compagnie d'un chevalier Jedi, d'un contrebandier et d'une princesse.", "rating": 8.6},
    {"media_type": MediaType.MOVIE, "title": "Star Wars : L'Empire contre-attaque", "original_title": "Star Wars: The Empire Strikes Back", "authors": ["Irvin Kershner"], "year": 1980, "cover": "https://image.tmdb.org/t/p/w500/2l05cFWJacyIsTpsqSgH0wQXe4V.jpg", "banner": "https://image.tmdb.org/t/p/w1280/ig0LASmASCIEBMfFGdyZjHEMoLM.jpg", "genres": ["Science Fiction", "Adventure", "Action"], "synopsis": "Après la destruction de l'Étoile de la Mort, l'Alliance Rebelle est traquée par l'Empire. Luke se forme auprès du maître Yoda tandis que Dark Vador le pourchasse.", "rating": 9.0},
    {"media_type": MediaType.MOVIE, "title": "Star Wars : Le Retour du Jedi", "original_title": "Star Wars: Return of the Jedi", "authors": ["Richard Marquand"], "year": 1983, "cover": "https://image.tmdb.org/t/p/w500/mDCBQNhR6R0PVFucJl3aHBgLdC.jpg", "banner": "https://image.tmdb.org/t/p/w1280/7GBFpbtyRqDFgEWWBGwfBluNRzF.jpg", "genres": ["Science Fiction", "Adventure", "Action"], "synopsis": "Luke Skywalker affronte Dark Vador et l'Empereur lors de la bataille décisive pour sauver la galaxie et ramener son père vers la lumière.", "rating": 8.3},
    {"media_type": MediaType.MOVIE, "title": "Star Wars : La Menace Fantôme", "original_title": "Star Wars: The Phantom Menace", "authors": ["George Lucas"], "year": 1999, "cover": "https://image.tmdb.org/t/p/w500/6wkfovpn7Eq8dYNKaG5PY3q2oq6.jpg", "banner": "https://image.tmdb.org/t/p/w1280/bOFaAXmWWXC3Rbv4u4uM9ZSzRXP.jpg", "genres": ["Science Fiction", "Adventure", "Action"], "synopsis": "Deux chevaliers Jedi découvrent un jeune garçon extraordinairement doué dans la Force : Anakin Skywalker, peut-être l'Élu de la prophétie.", "rating": 7.0},
    {"media_type": MediaType.MOVIE, "title": "Star Wars : L'Attaque des Clones", "original_title": "Star Wars: Attack of the Clones", "authors": ["George Lucas"], "year": 2002, "cover": "https://image.tmdb.org/t/p/w500/4of2CVe4LjFB7at84EQe3MKgkZH.jpg", "banner": "https://image.tmdb.org/t/p/w1280/8BPZO0Bf8TeAy8znF43z8soK3ys.jpg", "genres": ["Science Fiction", "Adventure", "Action"], "synopsis": "Anakin Skywalker et Padmé Amidala tombent amoureux tandis que la République est menacée par une armée séparatiste et les manœuvres de Palpatine.", "rating": 6.7},
    {"media_type": MediaType.MOVIE, "title": "Star Wars : La Revanche des Sith", "original_title": "Star Wars: Revenge of the Sith", "authors": ["George Lucas"], "year": 2005, "cover": "https://image.tmdb.org/t/p/w500/wXthtEN5kdWA1bHz03lkuCJS6hA.jpg", "banner": "https://image.tmdb.org/t/p/w1280/rkmSfQmSMNDOEYt7p5F5e0d2ZGH.jpg", "genres": ["Science Fiction", "Adventure", "Drama"], "synopsis": "Anakin Skywalker bascule du côté obscur et devient Dark Vador, marquant la chute de la République et l'avènement de l'Empire.", "rating": 7.5},
    {"media_type": MediaType.MOVIE, "title": "Star Wars : Le Réveil de la Force", "original_title": "Star Wars: The Force Awakens", "authors": ["J.J. Abrams"], "year": 2015, "cover": "https://image.tmdb.org/t/p/w500/x7UcKgq8tBXsuVCwcuNuMWDkxaP.jpg", "banner": "https://image.tmdb.org/t/p/w1280/hHuE1bMUFMHSXHDJE73WkxBTr6Z.jpg", "genres": ["Science Fiction", "Adventure", "Action"], "synopsis": "Trente ans après la chute de l'Empire, une nouvelle menace surgit. Rey, Finn et Poe Dameron rejoignent la Résistance contre le Premier Ordre.", "rating": 7.9},
    {"media_type": MediaType.MOVIE, "title": "Rogue One : A Star Wars Story", "original_title": "Rogue One: A Star Wars Story", "authors": ["Gareth Edwards"], "year": 2016, "cover": "https://image.tmdb.org/t/p/w500/i0yw1mFbB7sNGHCs7EXZPzFkdA1.jpg", "banner": "https://image.tmdb.org/t/p/w1280/tZjVVIYXACV4IIIhXeIM9XqGmOx.jpg", "genres": ["Science Fiction", "Adventure", "War"], "synopsis": "Un groupe de rebelles mène une mission suicide pour voler les plans de l'Étoile de la Mort avant les événements du premier film.", "rating": 8.1},
    # Séries
    {"media_type": MediaType.TV_SERIES, "title": "The Mandalorian", "original_title": "The Mandalorian", "authors": ["Jon Favreau"], "year": 2019, "cover": "https://image.tmdb.org/t/p/w500/eU1i6eHXlzMqZAB2HfijNZJWKdM.jpg", "banner": "https://image.tmdb.org/t/p/w1280/9ijMGlJKqcslswWUzTEwScm82Gs.jpg", "genres": ["Science Fiction", "Adventure", "Western"], "synopsis": "Un chasseur de primes mandalorien solitaire navigue dans les confins de la galaxie loin de l'autorité de la Nouvelle République, avec un mystérieux enfant.", "rating": 8.7},
    {"media_type": MediaType.TV_SERIES, "title": "Andor", "original_title": "Andor", "authors": ["Tony Gilroy"], "year": 2022, "cover": "https://image.tmdb.org/t/p/w500/59SVNwLfoMnZPPB6ukW6dlPxAdI.jpg", "banner": "https://image.tmdb.org/t/p/w1280/59SVNwLfoMnZPPB6ukW6dlPxAdI.jpg", "genres": ["Science Fiction", "Thriller", "Drama"], "synopsis": "La genèse du personnage de Cassian Andor et les origines de la Rébellion contre l'Empire Galactique, cinq ans avant Rogue One.", "rating": 8.4},
    {"media_type": MediaType.TV_SERIES, "title": "Obi-Wan Kenobi", "original_title": "Obi-Wan Kenobi", "authors": ["Deborah Chow"], "year": 2022, "cover": "https://image.tmdb.org/t/p/w500/bEk7gFtOH5azbxMJPMOTFHUToGW.jpg", "banner": "https://image.tmdb.org/t/p/w1280/4SgCNMHe0ciFBqUMoOPKPFDOy1P.jpg", "genres": ["Science Fiction", "Adventure", "Drama"], "synopsis": "Dix ans après la Revanche des Sith, Obi-Wan Kenobi est forcé de sortir de l'exil pour sauver le jeune Leia Organa.", "rating": 7.2},
    {"media_type": MediaType.TV_SERIES, "title": "The Book of Boba Fett", "original_title": "The Book of Boba Fett", "authors": ["Jon Favreau", "Dave Filoni"], "year": 2021, "cover": "https://image.tmdb.org/t/p/w500/gNbdjDi1HamTCrfvM9JeA94bNi2.jpg", "banner": "https://image.tmdb.org/t/p/w1280/aBEeAjpCkRhRNBKxgKnGCJTaTDE.jpg", "genres": ["Science Fiction", "Adventure", "Western"], "synopsis": "Boba Fett et Fennec Shand réclament le territoire qui était jadis sous le contrôle de Jabba le Hutt sur Tatooine.", "rating": 7.3},
    {"media_type": MediaType.TV_SERIES, "title": "Star Wars : The Clone Wars", "original_title": "Star Wars: The Clone Wars", "authors": ["Dave Filoni"], "year": 2008, "cover": "https://image.tmdb.org/t/p/w500/xWGqsLxSoHNL2GYXPKCE9nQoGzj.jpg", "banner": "https://image.tmdb.org/t/p/w1280/xWGqsLxSoHNL2GYXPKCE9nQoGzj.jpg", "genres": ["Science Fiction", "Animation", "Adventure"], "synopsis": "La série animée suit Anakin Skywalker, Obi-Wan Kenobi et leur padawan Ahsoka Tano durant les Guerres des Clones.", "rating": 8.5},
    {"media_type": MediaType.TV_SERIES, "title": "Ahsoka", "original_title": "Ahsoka", "authors": ["Dave Filoni"], "year": 2023, "cover": "https://image.tmdb.org/t/p/w500/aqLbNMNGEpLDR8TjGE8FkfKFQzQ.jpg", "banner": "https://image.tmdb.org/t/p/w1280/3yqzarPNzOuEV0GdUuKPpDHnS5b.jpg", "genres": ["Science Fiction", "Adventure", "Drama"], "synopsis": "L'ancienne padawan Ahsoka Tano enquête sur une menace émergente pour la galaxie après la chute de l'Empire.", "rating": 7.4},
    # Jeux vidéo
    {"media_type": MediaType.VIDEO_GAME, "title": "Star Wars Jedi: Fallen Order", "original_title": "Star Wars Jedi: Fallen Order", "authors": ["Respawn Entertainment"], "year": 2019, "cover": "https://image.tmdb.org/t/p/w500/yJgNGEGcBZf3nYWGnxzTKiXsJq2.jpg", "genres": ["Action", "Adventure", "RPG"], "synopsis": "Cal Kestis, padawan ayant survécu à l'Ordre 66, cherche à reconstruire l'Ordre Jedi en explorant des planètes inconnues.", "rating": 8.5},
    {"media_type": MediaType.VIDEO_GAME, "title": "Star Wars Jedi: Survivor", "original_title": "Star Wars Jedi: Survivor", "authors": ["Respawn Entertainment"], "year": 2023, "cover": "https://image.tmdb.org/t/p/w500/xJHokMbljvjADYdit5fK5VQsXEG.jpg", "genres": ["Action", "Adventure", "RPG"], "synopsis": "Cal Kestis continue sa quête dans une galaxie de plus en plus dominée par l'Empire, cherchant un refuge sûr pour les derniers Jedi.", "rating": 8.7},
    {"media_type": MediaType.VIDEO_GAME, "title": "Star Wars: Knights of the Old Republic", "original_title": "Star Wars: Knights of the Old Republic", "authors": ["BioWare"], "year": 2003, "cover": "https://covers.openlibrary.org/b/id/8228691-L.jpg", "genres": ["RPG", "Adventure"], "synopsis": "Quatre millénaires avant l'Étoile de la Mort, un héros découvre une connexion profonde à la Force et doit choisir son destin.", "rating": 9.5},
    {"media_type": MediaType.VIDEO_GAME, "title": "Star Wars Battlefront II", "original_title": "Star Wars Battlefront II", "authors": ["EA DICE", "Motive Studios"], "year": 2017, "cover": "https://image.tmdb.org/t/p/w500/kNAfmJHFNnDmvTG7HlYhIDJ6TSA.jpg", "genres": ["Action", "Shooter", "Multiplayer"], "synopsis": "Jouez en tant qu'Iden Versio, commandante de l'unité d'élite Inferno Squad, dans une histoire couvrant 30 ans de la saga.", "rating": 7.2},
    {"media_type": MediaType.VIDEO_GAME, "title": "Star Wars: The Old Republic", "original_title": "Star Wars: The Old Republic", "authors": ["BioWare"], "year": 2011, "cover": "https://image.tmdb.org/t/p/w500/eFMHCiLeTDNMEbSGNX17k8eFmhJ.jpg", "genres": ["RPG", "MMORPG", "Adventure"], "synopsis": "Un MMORPG se déroulant 300 ans après KOTOR, permettant aux joueurs de choisir leur voie parmi Jedi, Sith et de nombreuses autres classes.", "rating": 8.0},
    {"media_type": MediaType.VIDEO_GAME, "title": "LEGO Star Wars : La Saga Skywalker", "original_title": "LEGO Star Wars: The Skywalker Saga", "authors": ["TT Games"], "year": 2022, "cover": "https://image.tmdb.org/t/p/w500/lKfGnHBkNvC2xCUjdxFBFkL9uf0.jpg", "genres": ["Action", "Adventure", "Comedy"], "synopsis": "Revivez les 9 films de la saga Skywalker dans un monde en briques LEGO avec humour et centaines de personnages jouables.", "rating": 8.3},
    # Livres
    {"media_type": MediaType.BOOK, "title": "Star Wars : Héritier de l'Empire", "original_title": "Heir to the Empire", "authors": ["Timothy Zahn"], "year": 1991, "isbn": "9782265053267", "genres": ["Science Fiction", "Adventure"], "synopsis": "Cinq ans après Le Retour du Jedi, la Nouvelle République est menacée par le Grand Amiral Thrawn, stratège militaire de génie.", "rating": 8.8},
    {"media_type": MediaType.BOOK, "title": "Star Wars : Dark Force Rising", "original_title": "Dark Force Rising", "authors": ["Timothy Zahn"], "year": 1992, "isbn": "9782265055858", "genres": ["Science Fiction", "Adventure"], "synopsis": "Thrawn cherche la Flotte du Katana, une armada perdue, pour écraser définitivement la Nouvelle République. Luke découvre Mara Jade.", "rating": 8.7},
    {"media_type": MediaType.BOOK, "title": "Star Wars : La Dernière Commande", "original_title": "The Last Command", "authors": ["Timothy Zahn"], "year": 1993, "isbn": "9782265059061", "genres": ["Science Fiction", "Adventure"], "synopsis": "Le conflit contre Thrawn atteint son apogée alors que Luke affronte un clone de lui-même créé par l'Empereur.", "rating": 8.6},
    {"media_type": MediaType.BOOK, "title": "Star Wars : Ahsoka", "original_title": "Ahsoka", "authors": ["E.K. Johnston"], "year": 2016, "isbn": "9781368003018", "genres": ["Science Fiction", "Young Adult"], "synopsis": "L'histoire d'Ahsoka Tano après sa fuite de l'Ordre Jedi et la montée de l'Empire, avant sa réapparition dans Rebels.", "rating": 8.1},
    {"media_type": MediaType.BOOK, "title": "Star Wars : Tarkin", "original_title": "Tarkin", "authors": ["James Luceno"], "year": 2014, "isbn": "9782012045491", "genres": ["Science Fiction", "Political Fiction"], "synopsis": "L'ascension de Wilhuff Tarkin, depuis sa jeunesse jusqu'à son rôle de Grand Moff aux côtés de Dark Vador.", "rating": 7.9},
    {"media_type": MediaType.BOOK, "title": "Star Wars : Lost Stars", "original_title": "Lost Stars", "authors": ["Claudia Gray"], "year": 2015, "isbn": "9781368003025", "genres": ["Science Fiction", "Romance", "Young Adult"], "synopsis": "Deux amis d'enfance rejoignent l'Empire et se retrouvent sur des camps opposés lors de la guerre entre l'Empire et la Rébellion.", "rating": 8.6},
    {"media_type": MediaType.BOOK, "title": "Star Wars : Maître et Apprenti", "original_title": "Master & Apprentice", "authors": ["Claudia Gray"], "year": 2019, "isbn": "9782012045484", "genres": ["Science Fiction", "Adventure"], "synopsis": "Obi-Wan Kenobi et Qui-Gon Jinn, avant La Menace Fantôme, affrontent une crise politique qui teste leur relation.", "rating": 8.2},
]


async def import_star_wars():
    """Import Star Wars media (films, séries, jeux, livres) into the database."""
    print(f"⭐ Importing {len(SAMPLE_STAR_WARS)} Star Wars media...")

    media_data = []
    for item in SAMPLE_STAR_WARS:
        year = item.get("year")
        release_date = None
        if year:
            try:
                release_date = datetime(year, 1, 1)
            except ValueError:
                pass

        cover = item.get("cover")
        if not cover and item.get("isbn"):
            cover = f"https://covers.openlibrary.org/b/isbn/{item['isbn']}-L.jpg"

        media_data.append({
            "media_type": item["media_type"],
            "title": item["title"],
            "original_title": item.get("original_title"),
            "synopsis": item.get("synopsis", ""),
            "release_date": release_date,
            "cover_image": cover,
            "banner_image": item.get("banner"),
            "average_rating": item.get("rating", 0),
            "popularity_score": item.get("rating", 0) * 10,
            "genres": item.get("genres", []),
            "creators": item.get("authors", []),
            "franchise": "Star Wars",
        })

    results = await import_media_to_db(media_data)
    print(f"\n{'='*50}")
    print(f"Import completed!")
    print(f"✓ Success: {results['success']}")
    print(f"⊝ Skipped: {results['skipped']}")
    print(f"✗ Errors: {results['error']}")
    print(f"{'='*50}")


async def import_books_sample():
    """Import curated sample books into the database."""
    print(f"📚 Importing {len(SAMPLE_BOOKS)} books...")

    media_data = []
    for book in SAMPLE_BOOKS:
        year = book.get("year")
        release_date = None
        if year and year > 0:
            try:
                release_date = datetime(max(1, year), 1, 1)
            except ValueError:
                pass

        isbn = book.get("isbn", "")
        cover = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg" if isbn else None

        media_data.append({
            "media_type": MediaType.BOOK,
            "title": book["title"],
            "original_title": None,
            "synopsis": book.get("synopsis", ""),
            "release_date": release_date,
            "cover_image": cover,
            "banner_image": None,
            "average_rating": book.get("rating", 0),
            "popularity_score": book.get("rating", 0) * 10,
            "genres": book.get("genres", []),
            "creators": book.get("authors", []),
            "franchise": None,
        })

    results = await import_media_to_db(media_data)
    print(f"\n{'='*50}")
    print(f"Import completed!")
    print(f"✓ Success: {results['success']}")
    print(f"⊝ Skipped: {results['skipped']}")
    print(f"✗ Errors: {results['error']}")
    print(f"{'='*50}")


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
            'media_type': MediaType.TV_SERIES,
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
            'media_type': MediaType.VIDEO_GAME,
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


DEMO_USERS = [
    {"username": "cinephile_thomas", "email": "thomas@artiverse.demo", "password": "demo1234"},
    {"username": "marie_lit_tout",   "email": "marie@artiverse.demo",   "password": "demo1234"},
    {"username": "gamer_alex",        "email": "alex@artiverse.demo",    "password": "demo1234"},
    {"username": "sofia_series",      "email": "sofia@artiverse.demo",   "password": "demo1234"},
    {"username": "lucas_culture",     "email": "lucas@artiverse.demo",   "password": "demo1234"},
]

# (media_title, media_type_value, username, score, review_title, review_content, spoiler)
DEMO_REVIEWS = [
    # cinephile_thomas
    ("Star Wars : L'Empire contre-attaque", "movie", "cinephile_thomas", 10, "Le chef-d'œuvre absolu", "Difficile d'imaginer un film plus parfait. La révélation de Dark Vador reste l'un des plus grands moments du cinéma. Kershner signe ici une œuvre qui transcende le divertissement.", False),
    ("Star Wars : Un Nouvel Espoir", "movie", "cinephile_thomas", 9, "Le début d'une révolution", "George Lucas a changé le cinéma de blockbuster pour toujours. L'aventure est totale, les personnages immédiatement attachants, et la musique de Williams est inoubliable.", False),
    ("Rogue One : A Star Wars Story", "movie", "cinephile_thomas", 8, "Le meilleur spin-off", "Sombre, guerrier, sincère. Rogue One ose quelque chose que la saga principale ne fait jamais : montrer le vrai coût de la guerre. La scène finale du couloir reste la meilleure de la franchise.", True),
    ("Star Wars : La Revanche des Sith", "movie", "cinephile_thomas", 7, "La chute méritait mieux", "La transformation d'Anakin en Vador est visuellement spectaculaire mais émotionnellement précipitée. Ewan McGregor sauve l'ensemble avec une prestation très investie.", False),
    ("The Shawshank Redemption", "movie", "cinephile_thomas", 10, "L'espoir comme arme absolue", "Chaque visionnage révèle une nouvelle couche. Tim Robbins et Morgan Freeman livrent deux des meilleures performances de l'histoire du cinéma. Un film qui vous change.", False),
    ("The Godfather", "movie", "cinephile_thomas", 10, "La perfection formelle", "Coppola n'a jamais été aussi maître de son art. Chaque plan est une peinture, chaque réplique une leçon. Le film de gangsters définitif qui transcende le genre.", False),
    # marie_lit_tout
    ("1984", "book", "marie_lit_tout", 10, "Plus actuel que jamais", "Orwell avait tout compris. Ce roman n'a pas vieilli d'un jour — la novlangue, la réécriture de l'histoire, la surveillance permanente. À lire absolument, plusieurs fois si possible.", False),
    ("Le Petit Prince", "book", "marie_lit_tout", 9, "Un conte pour grands enfants", "Derrière sa simplicité apparente se cache une profondeur infinie. Chaque relecture à différents âges révèle un sens nouveau. Saint-Exupéry a écrit l'essentiel en quelques pages.", False),
    ("Star Wars : Héritier de l'Empire", "book", "marie_lit_tout", 9, "Thrawn, le meilleur antagoniste SW", "Timothy Zahn a créé le personnage le plus fascinant de l'univers étendu. Un roman qui respecte l'esprit de la saga tout en apportant quelque chose de nouveau et de mature.", False),
    ("Star Wars : Lost Stars", "book", "marie_lit_tout", 10, "La meilleure histoire d'amour Star Wars", "Claudia Gray réussit l'impossible : raconter toute la trilogie originale du point de vue de deux personnages ordinaires. Émouvant, intelligent, indispensable.", False),
    ("Dune", "book", "marie_lit_tout", 9, "SF politique au sommet", "Herbert a construit un univers d'une richesse inouïe. La première moitié est exigeante mais la récompense est totale. Paul Atréides est un héros tragique inoubliable.", False),
    ("Harry Potter et la Philosophie de la Pierre", "book", "marie_lit_tout", 8, "La magie de l'enfance capturée", "Rowling a créé un monde si cohérent et si vivant qu'on regrette de ne pas avoir reçu sa lettre de Poudlard. Une lecture qui reste gravée à vie.", False),
    # gamer_alex
    ("Star Wars Jedi: Fallen Order", "video_game", "gamer_alex", 9, "Enfin un bon jeu SW solo", "Respawn a réussi là où beaucoup avaient échoué : un jeu Star Wars avec une vraie narration, un combat technique et une exploration satisfaisante. Cal Kestis est attachant dès les premières heures.", False),
    ("Star Wars Jedi: Survivor", "video_game", "gamer_alex", 10, "La suite qui améliore tout", "Plus grand, plus profond, plus beau. Survivor prend tout ce qui fonctionnait dans Fallen Order et le pousse à son maximum. L'un des meilleurs jeux d'action-aventure de ces dernières années.", False),
    ("Star Wars: Knights of the Old Republic", "video_game", "gamer_alex", 10, "Le RPG Star Wars ultime", "Le twist de KOTOR reste l'un des plus grands moments narratifs du jeu vidéo. BioWare à son apogée : des choix qui comptent, des personnages profonds, un univers fascinant.", True),
    ("LEGO Star Wars : La Saga Skywalker", "video_game", "gamer_alex", 8, "La récré parfaite", "TT Games signe leur meilleur LEGO à ce jour. Humour, nostalgie et générosité de contenu au rendez-vous. Idéal pour jouer en famille ou décompresser après un jeu exigeant.", False),
    ("Star Wars: The Old Republic", "video_game", "gamer_alex", 7, "Un MMO ambitieux qui vieillit", "Les histoires de classe sont vraiment excellentes, surtout l'Inquisiteur Sith. Le jeu montre son âge dans ses mécaniques MMO mais reste une expérience Star Wars unique.", False),
    # sofia_series
    ("The Mandalorian", "tv_series", "sofia_series", 10, "Star Wars comme on l'aime", "Jon Favreau a compris quelque chose d'essentiel : le silence, la lenteur, les petits moments sont parfois plus puissants que les grandes batailles. Et Grogu est parfait.", False),
    ("Andor", "tv_series", "sofia_series", 10, "La série la plus adulte du MCU SW", "Tony Gilroy réalise un miracle : une série de politique-espionnage qui se passe dans l'univers Star Wars et qui n'a besoin d'aucun sabre laser pour captiver. Écriture au sommet.", False),
    ("Star Wars : The Clone Wars", "tv_series", "sofia_series", 9, "Le canon essentiel", "Dave Filoni a sauvé la prélogie avec cette série. Les arcs d'Ahsoka, de Maul et de la 501ème sont parmi les meilleures choses jamais produites dans la franchise.", False),
    ("Ahsoka", "tv_series", "sofia_series", 7, "Pour les fans de Rebels d'abord", "Magnifique visuellement et porté par Rosario Dawson, Ahsoka souffre d'un rythme irrégulier et demande une connaissance approfondie de Rebels pour être pleinement appréciée.", False),
    ("Breaking Bad", "tv_series", "sofia_series", 10, "La meilleure série de tous les temps", "Vince Gilligan a écrit la transformation la plus crédible et la plus dévastatrice de l'histoire de la télévision. Chaque saison monte d'un cran. Le final est parfait.", False),
    # lucas_culture
    ("Star Wars : La Menace Fantôme", "movie", "lucas_culture", 6, "Meilleur que sa réputation", "Oui, Jar Jar est agaçant. Oui, la politique est soporifique. Mais Darth Maul, le pod-racing et la double-lame électrisante compensent largement. Un film imparfait mais pas mauvais.", False),
    ("Star Wars : Ahsoka", "book", "lucas_culture", 8, "Pont essentiel entre Rebels et la suite", "E.K. Johnston capture parfaitement la voix d'Ahsoka. Un roman qui explore intelligemment la période post-Ordre 66 et ce que ça signifie d'être Jedi sans Ordre Jedi.", False),
    ("Star Wars : Maître et Apprenti", "book", "lucas_culture", 8, "Qui-Gon méritait mieux", "Ce roman répare une injustice en donnant enfin de la profondeur à Qui-Gon Jinn. La relation avec Obi-Wan est touchante et les thèmes philosophiques très bien explorés.", False),
    ("Obi-Wan Kenobi", "tv_series", "lucas_culture", 7, "Ewan McGregor au sommet", "La série est inégale et ses enjeux parfois discutables pour la continuité, mais Ewan McGregor est si convaincant qu'on pardonne tout. La confrontation finale est mémorable.", False),
    ("Dune", "book", "lucas_culture", 10, "La SF comme philosophie", "Herbert a écrit bien plus qu'un roman de science-fiction. C'est une méditation sur le pouvoir, la religion, l'écologie et le destin. Une œuvre totale qui résiste à toutes les adaptations.", False),
    ("Sapiens : Une brève histoire de l'humanité", "book", "lucas_culture", 9, "Vertigineux et indispensable", "Harari vous oblige à repenser tout ce que vous croyez savoir sur l'humanité. Certaines thèses sont discutables mais la stimulation intellectuelle est permanente.", False),
]


async def import_demo_users():
    """Create demo users with ratings and reviews."""
    print(f"👥 Creating {len(DEMO_USERS)} demo users and seeding reviews...")

    async with AsyncSessionLocal() as db:
        # 1. Create users
        user_map: dict[str, User] = {}
        for u in DEMO_USERS:
            existing = await db.execute(select(User).where(User.username == u["username"]))
            existing_user = existing.scalar_one_or_none()
            if existing_user:
                print(f"  ⊝ User already exists: {u['username']}")
                user_map[u["username"]] = existing_user
            else:
                new_user = User(
                    username=u["username"],
                    email=u["email"],
                    hashed_password=get_password_hash(u["password"]),
                )
                db.add(new_user)
                await db.flush()
                user_map[u["username"]] = new_user
                print(f"  ✓ Created user: {u['username']}")
        await db.commit()

        # Refresh to get IDs
        for username in user_map:
            await db.refresh(user_map[username])

        # 2. Seed ratings + reviews
        success = skipped = errors = 0
        for (media_title, media_type_val, username, score, rev_title, rev_content, spoiler) in DEMO_REVIEWS:
            try:
                user_obj = user_map.get(username)
                if not user_obj:
                    errors += 1
                    continue

                # Find media
                mt = MediaType(media_type_val)
                res = await db.execute(
                    select(Media).where(Media.title == media_title, Media.media_type == mt)
                )
                media_obj = res.scalar_one_or_none()
                if not media_obj:
                    print(f"  ✗ Media not found: {media_title}")
                    errors += 1
                    continue

                # Rating (upsert)
                res_r = await db.execute(
                    select(Rating).where(Rating.user_id == user_obj.id, Rating.media_id == media_obj.id)
                )
                rating_obj = res_r.scalar_one_or_none()
                if rating_obj:
                    rating_obj.score = score
                else:
                    db.add(Rating(user_id=user_obj.id, media_id=media_obj.id, score=score))

                # Review (upsert)
                res_rv = await db.execute(
                    select(ReviewModel).where(ReviewModel.user_id == user_obj.id, ReviewModel.media_id == media_obj.id)
                )
                review_obj = res_rv.scalar_one_or_none()
                if review_obj:
                    review_obj.title = rev_title
                    review_obj.content = rev_content
                    review_obj.spoiler = spoiler
                    skipped += 1
                else:
                    db.add(ReviewModel(
                        user_id=user_obj.id,
                        media_id=media_obj.id,
                        title=rev_title,
                        content=rev_content,
                        spoiler=spoiler,
                    ))
                    success += 1

                await db.commit()
                print(f"  ✓ {username} → {media_title} ({score}/10)")

            except Exception as e:
                print(f"  ✗ Error: {e}")
                await db.rollback()
                errors += 1

        print(f"\n{'='*50}")
        print(f"Demo data import completed!")
        print(f"✓ Created: {success}  ⊝ Updated: {skipped}  ✗ Errors: {errors}")
        print(f"{'='*50}")
        print("\nDemo accounts (password: demo1234):")
        for u in DEMO_USERS:
            print(f"  • {u['username']} — {u['email']}")


async def recalc_xp():
    """Recalculate XP for all users based on their existing ratings and reviews."""
    import math
    from app.services.xp_service import XPService

    print("🔄 Recalculating XP for all users...")

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()

        for user in users:
            rating_count_res = await db.execute(
                select(func.count()).select_from(Rating).where(Rating.user_id == user.id)
            )
            rating_count = rating_count_res.scalar()

            review_count_res = await db.execute(
                select(func.count()).select_from(ReviewModel).where(ReviewModel.user_id == user.id)
            )
            review_count = review_count_res.scalar()

            xp = rating_count * XPService.XP_VALUES["rating_given"] + review_count * XPService.XP_VALUES["review_created"]
            level = max(1, int(math.sqrt(xp / 100)) + 1) if xp > 0 else 1

            user.experience_points = xp
            user.level = level
            db.add(user)
            print(f"  ✓ {user.username}: {rating_count} notes + {review_count} avis = {xp} XP → Niv. {level}")

        await db.commit()
    print("\n✅ XP recalculated for all users.")


async def main():
    parser = argparse.ArgumentParser(description='Import media data to Artiverse')
    parser.add_argument('--source', choices=['tmdb', 'rawg', 'goodreads', 'books', 'starwars', 'demo', 'recalc-xp', 'sample'],
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

    if args.source == 'books':
        await import_books_sample()
        return

    if args.source == 'starwars':
        await import_star_wars()
        return

    if args.source == 'demo':
        await import_demo_users()
        return

    if args.source == 'recalc-xp':
        await recalc_xp()
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
