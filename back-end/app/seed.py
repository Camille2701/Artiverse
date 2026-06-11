"""Seed the database with sample media, users, ratings and reviews.

Run it (with the stack up) via:

    docker-compose exec backend python -m app.seed

The script is idempotent: existing rows (matched by username / media title)
are skipped, so it can be run multiple times safely.
"""

import asyncio
from datetime import datetime

from sqlalchemy import select

from app.db import AsyncSessionLocal
from app.models import User, Media, MediaType, Rating, Review
from app.utils.security import get_password_hash


def _cover(slug: str) -> str:
    return f"https://picsum.photos/seed/{slug}/400/600"


def _banner(slug: str) -> str:
    return f"https://picsum.photos/seed/{slug}-banner/1280/420"


USERS = [
    {
        "username": "cinephile",
        "email": "cinephile@artiverse.dev",
        "password": "password123",
        "bio": "I watch everything twice.",
        "level": 5,
        "experience_points": 2500,
    },
    {
        "username": "bookworm",
        "email": "bookworm@artiverse.dev",
        "password": "password123",
        "bio": "Currently buried in a 900-page fantasy novel.",
        "level": 3,
        "experience_points": 900,
    },
    {
        "username": "gamer_gwen",
        "email": "gwen@artiverse.dev",
        "password": "password123",
        "bio": "RPG enjoyer. 100% completionist.",
        "level": 7,
        "experience_points": 4900,
    },
]

# media_type, title, original_title, y, mo, d, synopsis, avg, pop, franchise, genres, creators
MEDIA = [
    # Star Wars franchise
    ("movie", "Star Wars: A New Hope", None, 1977, 5, 25,
     "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy.",
     8.6, 98.0, "Star Wars", ["Sci-Fi", "Adventure"], ["Mark Hamill", "Harrison Ford", "Carrie Fisher"]),
    ("movie", "Star Wars: The Empire Strikes Back", None, 1980, 5, 21,
     "After the Rebels are brutally overpowered by the Empire, Luke begins Jedi training with Yoda.",
     8.7, 97.0, "Star Wars", ["Sci-Fi", "Adventure"], ["Mark Hamill", "Harrison Ford", "Carrie Fisher"]),
    ("movie", "Star Wars: Return of the Jedi", None, 1983, 5, 25,
     "After rescuing Han Solo, the Rebels look to destroy the second Death Star.",
     8.3, 94.0, "Star Wars", ["Sci-Fi", "Adventure"], ["Mark Hamill", "Harrison Ford", "Carrie Fisher"]),
    ("video_game", "Star Wars Jedi: Fallen Order", None, 2019, 11, 15,
     "A young Jedi padawan must complete his training while being hunted by the Empire.",
     8.5, 88.0, "Star Wars", ["Action", "Adventure"], ["Respawn Entertainment"]),
    ("book", "Star Wars: Heir to the Empire", None, 1991, 5, 1,
     "Grand Admiral Thrawn mounts a final campaign to destroy the New Republic.",
     8.2, 72.0, "Star Wars", ["Sci-Fi"], ["Timothy Zahn"]),

    # Dune franchise
    ("movie", "Dune: Part Two", None, 2024, 3, 1,
     "Paul Atreides unites with the Fremen to wage war against House Harkonnen.",
     8.6, 99.0, "Dune", ["Sci-Fi", "Adventure"], ["Timothée Chalamet", "Zendaya", "Denis Villeneuve"]),
    ("movie", "Dune", None, 2021, 10, 22,
     "Feature adaptation of Frank Herbert's science fiction novel about the son of a noble family.",
     8.0, 92.0, "Dune", ["Sci-Fi", "Adventure"], ["Timothée Chalamet", "Zendaya", "Denis Villeneuve"]),
    ("book", "Dune", None, 1965, 8, 1,
     "On Arrakis, young Paul Atreides becomes embroiled in a struggle for spice.",
     8.2, 85.0, "Dune", ["Sci-Fi"], ["Frank Herbert"]),
    ("video_game", "Dune: Spice Wars", None, 2022, 5, 10,
     "A 4X strategy game set on the desert planet Arrakis.",
     7.2, 65.0, "Dune", ["Strategy", "Sci-Fi"], ["Shiro Games"]),

    # The Witcher franchise
    ("video_game", "The Witcher 3: Wild Hunt", None, 2015, 5, 19,
     "Monster hunter Geralt searches for his adopted daughter while a spectral army hunts her.",
     9.3, 96.0, "The Witcher", ["RPG", "Fantasy"], ["CD Projekt Red"]),
    ("tv_series", "The Witcher", None, 2019, 12, 20,
     "Geralt of Rivia, a solitary monster hunter, struggles to find his place in a world of people.",
     8.0, 90.0, "The Witcher", ["Fantasy", "Drama"], ["Henry Cavill", "Anya Chalotra"]),
    ("book", "The Last Wish", None, 1993, 1, 1,
     "A collection of short stories introducing Geralt of Rivia.",
     8.4, 70.0, "The Witcher", ["Fantasy"], ["Andrzej Sapkowski"]),

    # Zelda franchise
    ("video_game", "The Legend of Zelda: Breath of the Wild", None, 2017, 3, 3,
     "Link awakens to defeat Calamity Ganon in a vast open world.",
     9.4, 95.0, "The Legend of Zelda", ["Adventure", "Action"], ["Nintendo"]),
    ("video_game", "The Legend of Zelda: Tears of the Kingdom", None, 2023, 5, 12,
     "Link explores the skies and depths of Hyrule to rescue Princess Zelda.",
     9.5, 94.0, "The Legend of Zelda", ["Adventure", "Action"], ["Nintendo"]),
    ("book", "The Legend of Zelda: Hyrule Historia", None, 2011, 12, 21,
     "An encyclopedia of the Zelda universe with artwork and lore.",
     8.0, 60.0, "The Legend of Zelda", ["Fantasy"], ["Nintendo"]),

    # Marvel franchise
    ("movie", "Avengers: Endgame", None, 2019, 4, 26,
     "The Avengers assemble once more to reverse Thanos's snap.",
     8.4, 99.0, "Marvel Cinematic Universe", ["Action", "Sci-Fi"], ["Robert Downey Jr.", "Chris Evans", "Scarlett Johansson"]),
    ("movie", "Iron Man", None, 2008, 5, 2,
     "Tony Stark builds a high-tech suit of armor to escape captivity.",
     7.9, 88.0, "Marvel Cinematic Universe", ["Action", "Sci-Fi"], ["Robert Downey Jr.", "Gwyneth Paltrow"]),
    ("video_game", "Marvel's Spider-Man", None, 2018, 9, 7,
     "Peter Parker protects New York as Spider-Man.",
     9.0, 91.0, "Marvel Cinematic Universe", ["Action", "Adventure"], ["Insomniac Games"]),

    # LOTR franchise
    ("movie", "The Lord of the Rings: The Fellowship of the Ring", None, 2001, 12, 19,
     "A hobbit and eight companions set out to destroy the One Ring.",
     8.8, 96.0, "The Lord of the Rings", ["Fantasy", "Adventure"], ["Elijah Wood", "Ian McKellen", "Viggo Mortensen"]),
    ("movie", "The Lord of the Rings: The Two Towers", None, 2002, 12, 18,
     "The fellowship is broken but the quest to destroy the Ring continues.",
     8.7, 95.0, "The Lord of the Rings", ["Fantasy", "Adventure"], ["Elijah Wood", "Ian McKellen", "Viggo Mortensen"]),
    ("book", "The Fellowship of the Ring", None, 1954, 7, 29,
     "The first volume of Tolkien's epic fantasy trilogy.",
     8.8, 80.0, "The Lord of the Rings", ["Fantasy"], ["J.R.R. Tolkien"]),
    ("video_game", "Middle-earth: Shadow of Mordor", None, 2014, 9, 30,
     "Talion, a ranger, seeks revenge in Mordor with a wraith's help.",
     8.2, 78.0, "The Lord of the Rings", ["Action", "Fantasy"], ["Monolith Productions"]),

    # Standalone / other
    ("movie", "Inception", None, 2010, 7, 16,
     "A thief who steals secrets through dream-sharing is given the inverse task of planting an idea.",
     8.8, 93.0, None, ["Sci-Fi", "Thriller"], ["Leonardo DiCaprio", "Christopher Nolan"]),
    ("movie", "Parasite", "기생충", 2019, 5, 30,
     "Greed and class discrimination threaten a symbiotic relationship between two families.",
     8.5, 90.0, None, ["Drama", "Thriller"], ["Song Kang-ho", "Bong Joon-ho"]),
    ("tv_series", "Breaking Bad", None, 2008, 1, 20,
     "A chemistry teacher turns to manufacturing methamphetamine to secure his family's future.",
     9.5, 97.0, None, ["Drama", "Crime"], ["Bryan Cranston", "Aaron Paul"]),
    ("tv_series", "Arcane", None, 2021, 11, 6,
     "The origins of two League of Legends champions and the power that will tear them apart.",
     9.0, 91.0, "League of Legends", ["Animation", "Fantasy"], ["Hailee Steinfeld", "Fortiche Productions"]),
    ("book", "1984", None, 1949, 6, 8,
     "In a totalitarian superstate, a man rebels against Big Brother.",
     8.4, 76.0, None, ["Dystopian"], ["George Orwell"]),
    ("book", "Project Hail Mary", None, 2021, 5, 4,
     "A lone astronaut wakes up with no memory and must save humanity.",
     8.7, 82.0, None, ["Sci-Fi"], ["Andy Weir"]),
    ("video_game", "Elden Ring", None, 2022, 2, 25,
     "Rise, Tarnished, and explore the Lands Between to become the Elden Lord.",
     9.5, 98.0, None, ["RPG", "Action"], ["FromSoftware"]),
    ("video_game", "Hades", None, 2020, 9, 17,
     "Defy the god of the dead as you hack and slash out of the Underworld.",
     8.8, 83.0, None, ["Roguelike", "Action"], ["Supergiant Games"]),
]

REVIEWS = [
    ("Star Wars: A New Hope", "cinephile", "A galaxy far, far away",
     "The film that started it all. Still magical decades later.", False),
    ("Dune: Part Two", "bookworm", "Epic and faithful",
     "Herbert fans will appreciate the scale and world-building.", False),
    ("The Witcher 3: Wild Hunt", "gamer_gwen", "Masterpiece",
     "Side quests alone are worth the price of admission.", False),
    ("Breaking Bad", "cinephile", "Peak television",
     "Every season raises the stakes. Perfect ending.", False),
    ("Elden Ring", "gamer_gwen", "Open world perfection",
     "Exploration and boss fights are endlessly rewarding.", False),
    ("The Lord of the Rings: The Fellowship of the Ring", "bookworm", "Faithful adaptation",
     "Tolkien's world brought to life with care and grandeur.", False),
    ("Avengers: Endgame", "gamer_gwen", "Emotional payoff",
     "A decade of storytelling culminating in an epic finale.", False),
    ("Inception", "cinephile", "Mind-bending",
     "Nolan at his most ambitious. The score is iconic.", False),
]

RATINGS = [
    ("Star Wars: A New Hope", "cinephile", 9),
    ("Star Wars: A New Hope", "gamer_gwen", 8),
    ("Dune: Part Two", "bookworm", 9),
    ("Dune: Part Two", "cinephile", 9),
    ("The Witcher 3: Wild Hunt", "gamer_gwen", 10),
    ("Breaking Bad", "cinephile", 10),
    ("Elden Ring", "gamer_gwen", 10),
    ("The Lord of the Rings: The Fellowship of the Ring", "bookworm", 9),
    ("Avengers: Endgame", "gamer_gwen", 9),
    ("Inception", "cinephile", 9),
    ("Arcane", "cinephile", 9),
    ("Project Hail Mary", "bookworm", 9),
]


async def run():
    created = {"users": 0, "media": 0, "reviews": 0, "ratings": 0}
    async with AsyncSessionLocal() as db:
        users: dict[str, User] = {}
        for u in USERS:
            result = await db.execute(select(User).where(User.username == u["username"]))
            user = result.scalar_one_or_none()
            if not user:
                user = User(
                    username=u["username"],
                    email=u["email"],
                    hashed_password=get_password_hash(u["password"]),
                    bio=u["bio"],
                    level=u["level"],
                    experience_points=u["experience_points"],
                )
                db.add(user)
                await db.flush()
                created["users"] += 1
            users[u["username"]] = user
        await db.commit()

        media_by_title: dict[str, Media] = {}
        for mtype, title, original, y, mo, d, synopsis, avg, pop, franchise, genres, creators in MEDIA:
            result = await db.execute(select(Media).where(Media.title == title))
            media = result.scalar_one_or_none()
            slug = title.lower().replace(" ", "-").replace(":", "")
            if not media:
                media = Media(
                    media_type=MediaType(mtype),
                    title=title,
                    original_title=original,
                    synopsis=synopsis,
                    release_date=datetime(y, mo, d),
                    cover_image=_cover(slug),
                    banner_image=_banner(slug),
                    franchise=franchise,
                    genres=genres,
                    creators=creators,
                    average_rating=avg,
                    popularity_score=pop,
                )
                db.add(media)
                await db.flush()
                created["media"] += 1
            else:
                media.franchise = franchise
                media.genres = genres
                media.creators = creators
                if not media.cover_image:
                    media.cover_image = _cover(slug)
            media_by_title[title] = media
        await db.commit()

        for title, username, rtitle, content, spoiler in REVIEWS:
            media = media_by_title.get(title)
            user = users.get(username)
            if not media or not user:
                continue
            result = await db.execute(
                select(Review).where(
                    Review.media_id == media.id,
                    Review.user_id == user.id,
                )
            )
            if result.scalar_one_or_none():
                continue
            db.add(Review(
                user_id=user.id,
                media_id=media.id,
                title=rtitle,
                content=content,
                spoiler=spoiler,
            ))
            created["reviews"] += 1
        await db.commit()

        for title, username, score in RATINGS:
            media = media_by_title.get(title)
            user = users.get(username)
            if not media or not user:
                continue
            result = await db.execute(
                select(Rating).where(
                    Rating.media_id == media.id,
                    Rating.user_id == user.id,
                )
            )
            if result.scalar_one_or_none():
                continue
            db.add(Rating(user_id=user.id, media_id=media.id, score=score))
            created["ratings"] += 1
        await db.commit()

    print(
        "Seed complete. Created "
        f"{created['users']} users, {created['media']} media, "
        f"{created['reviews']} reviews, {created['ratings']} ratings."
    )
    print("\nSample logins (email / password):")
    print("- cinephile@artiverse.dev / password123")
    print("- bookworm@artiverse.dev / password123")
    print("- gamer_gwen@artiverse.dev / password123")


if __name__ == "__main__":
    asyncio.run(run())
