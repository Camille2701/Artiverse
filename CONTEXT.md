# ARTIVERSE — Backend Context (FastAPI)

## Project Overview

ARTIVERSE is a centralized transmedia cataloging and review platform dedicated to movies, TV series, books, and video games.

The platform allows users to:
- Track and archive their cultural consumption
- Rate and review media
- Build a digital cultural identity
- Discover content socially
- Interact through gamification systems

The goal is to unify fragmented cultural tracking ecosystems (Letterboxd, Goodreads, Backloggd, SensCritique, etc.) into a single scalable social platform.

---

# Core Vision

ARTIVERSE is NOT just a database.

It is:
- A cultural identity platform
- A social discovery ecosystem
- A gamified progression system
- A personal media archive

Users should feel:
- Recognized for their expertise
- Motivated to interact
- Encouraged to discover new media
- Proud of their profile and achievements

---

# Tech Stack

## Backend
- Python 3.12+
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Alembic
- Pydantic v2
- JWT Authentication
- Redis (cache + sessions + queues)
- Celery or RQ for background jobs

## Optional Integrations
- TMDB API (movies/series)
- IGDB API (games)
- Google Books API / OpenLibrary
- S3-compatible storage for avatars/images

---

# Architecture Goals

The backend must be:
- Modular
- Scalable
- Async-first when relevant
- RESTful
- Clean Architecture inspired
- Easy to maintain
- Easy to extend

Recommended structure:

```txt
app/
├── api/
├── core/
├── models/
├── schemas/
├── services/
├── repositories/
├── dependencies/
├── middleware/
├── utils/
├── tasks/
├── db/
└── main.py
```

---

# Product Philosophy

## Main User Problems Solved

### 1. Fragmentation of Platforms

Users currently need:

* Letterboxd for movies
* Goodreads for books
* Backloggd for games
* SensCritique for mixed content

ARTIVERSE centralizes everything into one unified platform.

### 2. Digital Identity & Recognition

Cultural consumption is a strong identity marker.

ARTIVERSE must:

* Showcase user expertise
* Reward engagement
* Create collectible progression systems
* Encourage self-expression

### 3. Information Overload

Modern recommendation systems are impersonal.

ARTIVERSE focuses on:

* Human-based recommendations
* Community trust
* Shared taste profiles
* Discovery through social interaction

---

# Media Types

Supported media:

* Movie
* TV Series
* Book
* Video Game

The architecture MUST be extensible for future media types.

Use either:

* Single table inheritance
* Generic media model
* Polymorphic architecture

Avoid hardcoded media-specific logic.

---

# Core Domain Models

## User

Fields:

* id
* username
* email
* hashed_password
* avatar_url
* bio
* level
* experience_points
* created_at
* updated_at

Relations:

* reviews
* ratings
* badges
* lists
* followers
* following
* activities

---

## Media

Fields:

* id
* media_type
* title
* original_title
* synopsis
* release_date
* cover_image
* banner_image
* average_rating
* popularity_score
* metadata_json

Relations:

* genres
* creators
* reviews
* ratings
* franchises
* related_media

---

## Review

Fields:

* id
* user_id
* media_id
* title
* content
* spoiler
* like_count
* created_at
* updated_at

---

## Rating

Fields:

* id
* user_id
* media_id
* score

Constraints:

* One rating per user per media

---

## UserList

Examples:

* Watched
* Currently Watching
* Wishlist
* Completed
* Favorites

Fields:

* id
* user_id
* name
* visibility
* created_at

---

## ActivityLog

Tracks:

* Ratings
* Reviews
* Badge unlocks
* Completed media
* Follow actions

Used for:

* User history
* Social feed
* Gamification progression

---

## Badge

Examples:

* Cinephile Expert
* Horror Master
* RPG Veteran
* Sci-Fi Collector

Fields:

* id
* name
* description
* icon_url
* rarity
* condition_type
* condition_value

---

# Must Have Features

## Content Management

* Centralized catalog
* Detailed media pages
* Search engine
* Filters
* Genres
* Creator references

## User Accounts

* Register
* Login
* JWT auth
* User profiles
* Personal history

## Reviews & Ratings

* Rating system
* Review creation
* Public reviews
* Review aggregation

## Personal Tracking

* Custom lists
* Watched status
* Activity journal

---

# Should Have Features

## Social

* Follow users
* Activity feed
* Likes
* Comments

## Recommendations

* Similar media
* Taste-based suggestions
* Trending content

## Advanced Profiles

* Statistics
* Top genres
* Time spent
* Top media lists

---

# Could Have Features

## Gamification

* XP system
* Levels
* Achievements
* Seasonal challenges

## Personalization

* Themes
* Custom profiles
* Favorite showcases

## Advanced Transmedia

* Franchise connections
* Shared universes
* Adaptation relationships

## Planning

* Release calendar
* Notifications
* Reading/watch planning

---

# Won't Have

The project intentionally excludes:

* Integrated streaming
* Marketplace/e-commerce
* AI-generated reviews
* Full Facebook-like social features
* VR/metaverse features

---

# API Design Guidelines

## General Rules

* RESTful naming
* Versioned API (`/api/v1`)
* Pagination everywhere
* Strict validation
* Typed responses
* Consistent error handling

---

# Example Routes

## Auth

```txt
POST   /auth/register
POST   /auth/login
POST   /auth/refresh
GET    /auth/me
```

## Users

```txt
GET    /users/{id}
PATCH  /users/{id}
GET    /users/{id}/activity
GET    /users/{id}/lists
```

## Media

```txt
GET    /media
GET    /media/{id}
GET    /media/search
GET    /media/trending
```

## Reviews

```txt
POST   /reviews
PATCH  /reviews/{id}
DELETE /reviews/{id}
GET    /media/{id}/reviews
```

## Ratings

```txt
POST   /ratings
DELETE /ratings/{id}
```

## Social

```txt
POST   /users/{id}/follow
DELETE /users/{id}/follow
GET    /feed
```

---

# Security Requirements

* Password hashing with bcrypt/argon2
* JWT authentication
* Role-based permissions
* Rate limiting
* Input sanitization
* Anti-spam protection
* Review/report moderation system

---

# Performance Goals

Backend should support:

* Large catalog datasets
* Fast search
* Feed generation
* Recommendation queries
* High read throughput

Use:

* Redis caching
* Async DB operations where relevant
* Query optimization
* Background workers

---

# Search Strategy

Search must support:

* Title matching
* Genre filters
* Media type filters
* Release year filters
* Sorting by popularity/rating

Potential future integration:

* Elasticsearch / Meilisearch

---

# Gamification Logic

Gamification is a CORE feature, not cosmetic.

Users earn:

* XP
* Levels
* Badges
* Milestones

Examples:

* Watch 100 horror movies
* Review 50 books
* Complete a franchise
* Maintain activity streaks

Gamification should encourage:

* Retention
* Discovery
* Contribution
* Social engagement

---

# Recommendation Philosophy

Recommendations should prioritize:

* Human similarity
* Shared interests
* Trusted reviewers
* Community behavior

Avoid:

* Overly corporate algorithmic behavior
* Pure engagement farming

---

# Backend Development Principles

## Code Quality

* Strong typing everywhere
* Clear naming
* Small reusable services
* Repository pattern preferred
* Business logic isolated from routes

## Database

* Proper indexing
* Soft delete where relevant
* Audit timestamps everywhere
* UUIDs preferred over incremental IDs

## Testing

* Pytest
* Unit tests
* Integration tests
* API tests

---

# Future Scalability

The architecture should later support:

* Mobile apps
* GraphQL gateway
* Microservices transition
* Real-time notifications
* Recommendation engine
* Event-driven architecture

---

# Expected Backend Mindset

The backend should behave like:

* A scalable social platform
* A cultural archive
* A progression system
* A recommendation ecosystem

NOT just CRUD endpoints.

Every feature should reinforce:

* Identity
* Discovery
* Community
* Progression
* Retention

---

# Priority MVP

## Phase 1

* Authentication
* Media catalog
* Ratings
* Reviews
* Lists
* Basic profiles

## Phase 2

* Social features
* Activity feed
* Search improvements
* Statistics

## Phase 3

* Gamification
* Recommendations
* Advanced transmedia links
* Notifications

---

# Coding Standards

* Use async FastAPI endpoints when useful
* Use service layer abstraction
* Avoid fat routers
* Keep schemas separated from ORM models
* Use dependency injection cleanly
* Centralize configuration management
* Use environment variables for secrets

---

# Final Objective

ARTIVERSE should become:

* The definitive cultural tracking hub
* A social network centered around art & media
* A platform where users build cultural identity
* A long-term scalable ecosystem for media discovery