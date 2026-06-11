# ARTIVERSE Backend - Phase 1 (MVP)

## Setup Instructions

### Prerequisites
- Python 3.12
- PostgreSQL 12+
- pip

### Installation

1. **Create a virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Create database:**
```bash
# Create PostgreSQL database
createdb artiverse
```

5. **Run migrations (optional):**
```bash
alembic upgrade head
```

## Running the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login with username
- `POST /api/v1/auth/login-form` - Login with form data

### Users
- `GET /api/v1/users/me` - Get current user profile
- `GET /api/v1/users/{user_id}` - Get user profile
- `PATCH /api/v1/users/me` - Update current user
- `GET /api/v1/users/{user_id}/reviews` - Get user reviews
- `GET /api/v1/users/{user_id}/lists` - Get user lists

### Media
- `POST /api/v1/media` - Create new media
- `GET /api/v1/media` - List all media
- `GET /api/v1/media/search` - Search media by title
- `GET /api/v1/media/trending` - Get trending media
- `GET /api/v1/media/{media_id}` - Get media details
- `PATCH /api/v1/media/{media_id}` - Update media

### Ratings
- `POST /api/v1/ratings` - Create/update rating
- `GET /api/v1/ratings/media/{media_id}` - Get media ratings
- `GET /api/v1/ratings/{rating_id}` - Get specific rating
- `PATCH /api/v1/ratings/{rating_id}` - Update rating
- `DELETE /api/v1/ratings/{rating_id}` - Delete rating

### Reviews
- `POST /api/v1/reviews` - Create review
- `GET /api/v1/reviews/media/{media_id}` - Get media reviews
- `GET /api/v1/reviews/{review_id}` - Get specific review
- `PATCH /api/v1/reviews/{review_id}` - Update review
- `DELETE /api/v1/reviews/{review_id}` - Delete review

### Lists
- `POST /api/v1/lists` - Create new list
- `GET /api/v1/lists/user/me` - Get current user's lists
- `GET /api/v1/lists/{list_id}` - Get list details
- `PATCH /api/v1/lists/{list_id}` - Update list
- `POST /api/v1/lists/{list_id}/items/{media_id}` - Add media to list
- `DELETE /api/v1/lists/{list_id}/items/{media_id}` - Remove media from list
- `DELETE /api/v1/lists/{list_id}` - Delete list

## Project Structure

```
app/
├── api/v1/
│   ├── auth.py          # Authentication routes
│   ├── users.py         # User management routes
│   ├── media.py         # Media management routes
│   ├── ratings.py       # Ratings routes
│   ├── reviews.py       # Reviews routes
│   ├── lists.py         # User lists routes
│   └── __init__.py
├── core/
│   ├── config.py        # Configuration settings
│   └── __init__.py
├── models/
│   ├── models.py        # SQLAlchemy ORM models
│   └── __init__.py
├── schemas/
│   ├── schemas.py       # Pydantic validation schemas
│   └── __init__.py
├── services/
│   ├── services.py      # Business logic
│   └── __init__.py
├── dependencies/
│   ├── auth.py          # FastAPI dependencies
│   └── __init__.py
├── db/
│   ├── base.py          # SQLAlchemy base
│   ├── session.py       # Database session
│   └── __init__.py
├── utils/
│   ├── security.py      # JWT and password utilities
│   └── __init__.py
├── middleware/
└── main.py              # FastAPI application
```

## Authentication

The API uses JWT tokens for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

## Database Models

### User
- id (UUID)
- username
- email
- hashed_password
- avatar_url
- bio
- level
- experience_points
- created_at, updated_at

### Media
- id (UUID)
- media_type (movie, tv_series, book, video_game)
- title
- original_title
- synopsis
- release_date
- cover_image
- banner_image
- average_rating
- popularity_score
- created_at, updated_at

### Rating
- id (UUID)
- user_id (FK)
- media_id (FK)
- score (1-10)
- created_at, updated_at
- Unique constraint: one rating per user per media

### Review
- id (UUID)
- user_id (FK)
- media_id (FK)
- title
- content
- spoiler (boolean)
- like_count
- created_at, updated_at

### List
- id (UUID)
- user_id (FK)
- name
- visibility (private, friends, public)
- created_at, updated_at

### ListItem
- id (UUID)
- list_id (FK)
- media_id (FK)
- created_at

## Next Steps (Phase 2)

- Social features (follow users, activity feed)
- Comments on reviews
- User statistics
- Advanced search with Elasticsearch
- Real-time notifications
- Content moderation system

## Configuration

Edit `.env` file to configure:
- DATABASE_URL
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES
- DEBUG
- ENVIRONMENT

## Testing

```bash
pytest
```

## License

Proprietary - ESGI Project
