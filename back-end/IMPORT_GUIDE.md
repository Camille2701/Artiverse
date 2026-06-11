# Media Import Guide for Artiverse

This guide explains how to use the media import script to populate your Artiverse database with real media data from TMDb, GoodReads, and RAWG.

## Quick Start

### Option 1: Import Sample Data (Easiest - No API Key Required)

```bash
docker compose exec backend python -m app.import_media --sample
```

This imports 5 carefully selected media items with proper cover images and metadata:
- The Shawshank Redemption (Movie)
- The Godfather (Movie)
- Breaking Bad (TV Series)
- The Legend of Zelda: Breath of the Wild (Game)
- 1984 (Book)

---

## Option 2: Import from TMDb (Recommended)

### Get Your Free API Key

1. Go to https://www.themoviedb.org/
2. Sign up for a free account
3. Go to Settings → API → Create a new API key
4. Copy your API key

### Import Popular Movies & TV Shows

```bash
# Import 25 movies and 25 TV shows (default 50 total)
docker compose exec backend python -m app.import_media --source tmdb --api-key YOUR_TMDB_KEY

# Import 100 items (50 movies + 50 shows)
docker compose exec backend python -m app.import_media --source tmdb --api-key YOUR_TMDB_KEY --limit 100

# Import 500 items
docker compose exec backend python -m app.import_media --source tmdb --api-key YOUR_TMDB_KEY --limit 500
```

**What gets imported:**
- High-quality cover images and banners from TMDb
- Movie/TV show metadata (title, synopsis, release date, genres, creators)
- Average ratings and popularity scores
- Franchise information (e.g., "The Godfather" franchise)
- Crew members (directors, writers, creators)

---

## Option 3: Import from RAWG (Video Games)

### Get Your Free API Key

1. Go to https://rawg.io/
2. Sign up for a free account
3. Go to https://rawg.io/apidocs to get your API key

### Import Popular Games

```bash
# Import 50 popular games
docker compose exec backend python -m app.import_media --source rawg --api-key YOUR_RAWG_KEY

# Import 100 games
docker compose exec backend python -m app.import_media --source rawg --api-key YOUR_RAWG_KEY --limit 100
```

**What gets imported:**
- Game titles and descriptions
- Cover images and additional screenshots
- Release dates
- Rating information
- Genres and publishers
- Metacritic scores (when available)

---

## Option 4: Import from GoodReads (Books)

### Download the Dataset

1. Go to https://cseweb.ucsd.edu/~jmcauley/datasets/goodreads.html
2. Download "goodreads_books.json" or any book dataset
3. Place it in `back-end/data/` directory

### Import Books

```bash
# Import from JSON file
docker compose exec backend python -m app.import_media --source goodreads --file /app/data/goodreads_books.json --limit 100
```

**What gets imported:**
- Book titles and authors
- Descriptions
- Publication years
- Cover images (from dataset or Open Library API)
- ISBN identifiers

---

## Examples

### Import Sample Data + TMDb Data

```bash
# First, import sample data
docker compose exec backend python -m app.import_media --sample

# Then, add 50 TMDb movies and shows
docker compose exec backend python -m app.import_media --source tmdb --api-key YOUR_KEY --limit 50
```

### Import from All Sources

```bash
# Sample data (5 items)
docker compose exec backend python -m app.import_media --sample

# TMDb (100 movies + shows)
docker compose exec backend python -m app.import_media --source tmdb --api-key YOUR_KEY --limit 100

# RAWG (50 games)
docker compose exec backend python -m app.import_media --source rawg --api-key YOUR_KEY --limit 50

# GoodReads (if you have the dataset)
docker compose exec backend python -m app.import_media --source goodreads --file /app/data/goodreads_books.json --limit 100
```

---

## What the Script Does

1. **Fetches data** from the chosen source (TMDb, RAWG, GoodReads)
2. **Formats and validates** the data for Artiverse's schema
3. **Checks for duplicates** by title and media type
4. **Imports to database** only new items
5. **Provides progress feedback** showing successes, skips, and errors

---

## Features

### Smart Deduplication
The script checks if media already exists before importing:
- ✓ Success: New media imported
- ⊝ Skipped: Media already exists (by title + type)
- ✗ Error: Import failed (shown in output)

### High-Quality Images
- **TMDb**: High-resolution posters (w500) and banners (w1280)
- **RAWG**: Background images and additional screenshots
- **GoodReads**: Cover images from dataset or Open Library API

### Rich Metadata
- **Genres**: Action, Drama, Comedy, RPG, Sci-Fi, etc.
- **Creators**: Directors, writers, developers, authors
- **Franchises**: Marvel, Star Wars, The Legend of Zelda, etc.
- **Ratings**: Average ratings and popularity scores

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"

```bash
docker compose exec backend pip install requests pandas
```

### "Error: TMDb requires --api-key"

You need a TMDb API key:
1. Sign up at https://www.themoviedb.org/
2. Get your free API key from Settings → API
3. Use it in the command: `--api-key YOUR_KEY`

### "Error: File not found" (GoodReads)

Make sure the file path is correct:
```bash
# Copy file to container first
docker cp goodreads_books.json artiverse-backend:/app/data/

# Then import
docker compose exec backend python -m app.import_media --source goodreads --file /app/data/goodreads_books.json
```

### Import Too Slow?

Reduce the limit:
```bash
# Import 25 items instead of 100
docker compose exec backend python -m app.import_media --source tmdb --api-key YOUR_KEY --limit 25
```

---

## Tips

1. **Start with sample data** to test the script
2. **Use TMDb first** - it has the best data and images
3. **Run imports multiple times** - duplicates are automatically skipped
4. **Monitor the output** - check for errors and skipped items
5. **Combine sources** - use TMDb for movies/shows, RAWG for games

---

## Data Sources Comparison

| Source | Media Types | Image Quality | API Key | Data Quality | Speed |
|--------|-------------|---------------|---------|-------------|-------|
| **TMDb** | Movies, TV | ⭐⭐⭐⭐⭐ | Free (req) | ⭐⭐⭐⭐⭐ | Fast |
| **RAWG** | Games | ⭐⭐⭐⭐ | Free (req) | ⭐⭐⭐⭐ | Medium |
| **GoodReads** | Books | ⭐⭐⭐ | None | ⭐⭐⭐ | Fast |
| **Sample** | All types | ⭐⭐⭐⭐ | None | ⭐⭐⭐⭐⭐ | Instant |

---

## Next Steps

After importing media:

1. **Check your catalogue**: Visit http://localhost:3000/home
2. **View media details**: Click on any media item
3. **Add to lists**: Log in and create custom lists
4. **Rate and review**: Leave ratings and reviews
5. **View statistics**: Check your profile page for stats

---

## API Links

- **TMDb API Docs**: https://developers.themoviedb.org/3
- **RAWG API Docs**: https://api.rawg.io/docs/
- **GoodReads Datasets**: https://cseweb.ucsd.edu/~jmcauley/datasets/goodreads.html
- **Open Library Covers**: https://covers.openlibrary.org/

---

## Notes

- **Rate Limits**: TMDb allows ~4 requests per second. The script handles this automatically.
- **Free Usage**: All mentioned APIs and datasets are free for non-commercial use.
- **Image Storage**: Images are stored as URLs, not downloaded. This saves database space.
- **Database Size**: 1000 media items ≈ 5-10MB database size (without images).

---

## Support

If you encounter issues:
1. Check the error message in the output
2. Ensure your API key is valid
3. Verify database connection: `docker compose ps`
4. Try with `--limit 10` to test with small batches
