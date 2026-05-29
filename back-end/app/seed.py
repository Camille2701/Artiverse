"""Seed the database with sample media, users, ratings and reviews.

Run it (with the stack up) via:

    docker-compose exec backend python -m app.seed

The script is idempotent: existing rows (matched by username / media title)
are skipped, so it can be run multiple times safely.
"""

from datetime import datetime

from app.db import SessionLocal
from app.models import User, Media, MediaType, Rating, Review
from app.utils.security import get_password_hash


def _cover(slug: str) -> str:
    """Deterministic placeholder cover image for visual testing."""
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


# media_type, title, original_title, year, month, day, synopsis, average_rating, popularity
MEDIA = [
    # ---------------- Movies ----------------
    ("movie", "Inception", None, 2010, 7, 16,
     "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.",
     8.8, 95.0),
    ("movie", "Parasite", "기생충", 2019, 5, 30,
     "Greed and class discrimination threaten the newly formed symbiotic relationship between a wealthy family and a destitute clan.",
     8.5, 88.0),
    ("movie", "Dune: Part Two", None, 2024, 3, 1,
     "Paul Atreides unites with the Fremen to wage war against House Harkonnen.",
     8.6, 99.0),
    ("movie", "Spirited Away", "千と千尋の神隠し", 2001, 7, 20,
     "A young girl wanders into a world of spirits and must work to free herself and her parents.",
     8.6, 82.0),
    ("movie", "The Matrix", None, 1999, 3, 31,
     "A hacker discovers the true nature of his reality and his role in the war against its controllers.",
     8.7, 79.0),

    # ---------------- TV series ----------------
    ("tv_series", "Breaking Bad", None, 2008, 1, 20,
     "A chemistry teacher diagnosed with cancer turns to manufacturing methamphetamine to secure his family's future.",
     9.5, 97.0),
    ("tv_series", "The Wire", None, 2002, 6, 2,
     "The Baltimore drug scene seen through the eyes of law enforcement and the dealers alike.",
     9.3, 74.0),
    ("tv_series", "Arcane", None, 2021, 11, 6,
     "The origins of two iconic League of Legends champions and the power that will tear them apart.",
     9.0, 91.0),
    ("tv_series", "Severance", None, 2022, 2, 18,
     "Employees surgically divide their memories between work and personal life.",
     8.7, 85.0),

    # ---------------- Books ----------------
    ("book", "Dune", None, 1965, 8, 1,
     "On the desert planet Arrakis, young Paul Atreides becomes embroiled in a struggle for the most valuable substance in the universe.",
     8.2, 70.0),
    ("book", "1984", None, 1949, 6, 8,
     "In a totalitarian superstate, a man rebels against the omnipresent surveillance of Big Brother.",
     8.4, 76.0),
    ("book", "The Name of the Wind", None, 2007, 3, 27,
     "Kvothe recounts his transformation from a gifted young man into the most notorious wizard of his world.",
     8.5, 68.0),
    ("book", "Project Hail Mary", None, 2021, 5, 4,
     "A lone astronaut wakes up with no memory and must save humanity from extinction.",
     8.7, 80.0),

    # ---------------- Video games ----------------
    ("video_game", "The Witcher 3: Wild Hunt", None, 2015, 5, 19,
     "Monster hunter Geralt of Rivia searches for his adopted daughter while a spectral army hunts her.",
     9.3, 96.0),
    ("video_game", "Elden Ring", None, 2022, 2, 25,
     "Rise, Tarnished, and explore the Lands Between to become the Elden Lord.",
     9.5, 98.0),
    ("video_game", "The Legend of Zelda: Breath of the Wild", None, 2017, 3, 3,
     "Link awakens from a hundred-year slumber to a vast open world and a quest to defeat Calamity Ganon.",
     9.4, 90.0),
    ("video_game", "Hades", None, 2020, 9, 17,
     "Defy the god of the dead as you hack and slash out of the Underworld in this rogue-like dungeon crawler.",
     8.8, 83.0),
]


REVIEWS = [
    # (media_title, username, title, content, spoiler)
    ("Inception", "cinephile", "A dream within a dream",
     "Nolan at his most ambitious. The practical effects still hold up beautifully.", False),
    ("Inception", "gamer_gwen", "Loud and brilliant",
     "The score alone earns an extra star. The ending is a perfect debate starter.", False),
    ("Breaking Bad", "cinephile", "The gold standard",
     "Character writing this tight is rare. Every season raises the stakes.", False),
    ("Elden Ring", "gamer_gwen", "Open world done right",
     "Exploration is endlessly rewarding and the bosses are unforgettable.", False),
    ("Dune", "bookworm", "Dense but rewarding",
     "Herbert's world-building is unmatched. Give it 100 pages and it clicks.", False),
    ("Project Hail Mary", "bookworm", "Could not put it down",
     "Funny, smart and genuinely moving. The best sci-fi I've read in years.", False),
    ("The Witcher 3: Wild Hunt", "gamer_gwen", "Side quests > main story",
     "Even the smallest contracts feel hand-crafted. A masterpiece.", False),
    ("Arcane", "cinephile", "Animation peak",
     "You don't need to know the game. The visuals and writing carry it.", False),
]


# (media_title, username, score 1-10)
RATINGS = [
    ("Inception", "cinephile", 9),
    ("Inception", "gamer_gwen", 8),
    ("Inception", "bookworm", 9),
    ("Breaking Bad", "cinephile", 10),
    ("Breaking Bad", "gamer_gwen", 9),
    ("Elden Ring", "gamer_gwen", 10),
    ("Elden Ring", "cinephile", 9),
    ("Dune", "bookworm", 8),
    ("Project Hail Mary", "bookworm", 9),
    ("The Witcher 3: Wild Hunt", "gamer_gwen", 10),
    ("Arcane", "cinephile", 9),
    ("Severance", "cinephile", 9),
]


def run():
    db = SessionLocal()
    created = {"users": 0, "media": 0, "reviews": 0, "ratings": 0}
    try:
        # ---- Users ----
        users = {}
        for u in USERS:
            user = db.query(User).filter(User.username == u["username"]).first()
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
                db.flush()
                created["users"] += 1
            users[u["username"]] = user
        db.commit()

        # ---- Media ----
        media_by_title = {}
        for mtype, title, original, y, mo, d, synopsis, avg, pop in MEDIA:
            media = db.query(Media).filter(Media.title == title).first()
            if not media:
                slug = title.lower().replace(" ", "-").replace(":", "")
                media = Media(
                    media_type=MediaType(mtype),
                    title=title,
                    original_title=original,
                    synopsis=synopsis,
                    release_date=datetime(y, mo, d),
                    cover_image=_cover(slug),
                    banner_image=_banner(slug),
                    average_rating=avg,
                    popularity_score=pop,
                )
                db.add(media)
                db.flush()
                created["media"] += 1
            media_by_title[title] = media
        db.commit()

        # ---- Reviews ----
        for title, username, rtitle, content, spoiler in REVIEWS:
            media = media_by_title.get(title)
            user = users.get(username)
            if not media or not user:
                continue
            exists = db.query(Review).filter(
                Review.media_id == media.id, Review.user_id == user.id
            ).first()
            if exists:
                continue
            db.add(Review(
                user_id=user.id,
                media_id=media.id,
                title=rtitle,
                content=content,
                spoiler=spoiler,
            ))
            created["reviews"] += 1
        db.commit()

        # ---- Ratings ----
        for title, username, score in RATINGS:
            media = media_by_title.get(title)
            user = users.get(username)
            if not media or not user:
                continue
            exists = db.query(Rating).filter(
                Rating.media_id == media.id, Rating.user_id == user.id
            ).first()
            if exists:
                continue
            db.add(Rating(user_id=user.id, media_id=media.id, score=score))
            created["ratings"] += 1
        db.commit()

        print(
            "Seed complete. Created "
            f"{created['users']} users, {created['media']} media, "
            f"{created['reviews']} reviews, {created['ratings']} ratings."
        )
        print("Sample login: cinephile / password123")
    finally:
        db.close()


if __name__ == "__main__":
    run()
