# Artiverse Deployment Guide (100% Free Tier)

This guide deploys the full stack for a student demo using **free tiers only**:

| Component | Provider | Free tier |
|-----------|----------|-----------|
| Database | [Neon](https://neon.tech) | 0.5 GB storage, serverless Postgres |
| Backend API | [Render](https://render.com) | Free web service (cold starts ~50s) |
| Frontend | [Vercel](https://vercel.com) | Free hobby plan, native Nuxt 3 |

> **Note:** Railway no longer offers a meaningful free tier for new projects. Render + Neon + Vercel is the recommended student stack.

## Architecture

```
Browser → Vercel (Nuxt) → Render (FastAPI) → Neon (PostgreSQL)
```

Cover images for the demo use external URLs (picsum.photos) seeded in the database — no paid object storage required.

---

## Step 1 — Database (Neon)

1. Create a free account at [neon.tech](https://neon.tech).
2. Create a project named `artiverse`.
3. Copy the **connection string** (pooled recommended).
4. Convert the URL for async SQLAlchemy:

```bash
# Neon gives:
postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require

# Use this format in Render:
postgresql+asyncpg://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
```

---

## Step 2 — Backend (Render)

### Option A: Blueprint (render.yaml)

The repo includes [`render.yaml`](./render.yaml). In Render dashboard:

1. **New → Blueprint** → connect your GitHub repo.
2. Set environment variables when prompted:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | `postgresql+asyncpg://...` (from Neon) |
| `SECRET_KEY` | Auto-generated or a long random string |
| `ENVIRONMENT` | `production` |
| `DEBUG` | `false` |
| `STORAGE_BACKEND` | `local` |
| `ALLOWED_ORIGINS` | `["https://your-app.vercel.app"]` |

3. Deploy. First request may take ~50s (free tier cold start).

### Option B: Manual Web Service

1. **New → Web Service** → connect repo.
2. **Root directory:** `back-end`
3. **Build command:** `pip install -r requirements/base.txt`
4. **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add the environment variables from the table above.

### Schema creation

On first startup, FastAPI runs `Base.metadata.create_all` and creates all tables automatically. No manual migration needed for a fresh database.

To add metadata columns on an **existing** database:

```bash
cd back-end
alembic upgrade head
```

### Seed the demo dataset

After the backend is running, open Render **Shell** (or run locally against Neon):

```bash
python -m app.seed
```

This creates 3 demo users, 30+ media items across franchises (Star Wars, Dune, Witcher…), ratings and reviews.

**Demo login:** `cinephile` / `password123`

### Health check

```bash
curl https://your-backend.onrender.com/health
# {"status":"healthy","environment":"production"}
```

---

## Step 3 — Frontend (Vercel)

1. Import the repo at [vercel.com](https://vercel.com).
2. **Root directory:** `front-end`
3. Framework preset: **Nuxt.js** (auto-detected).
4. Environment variables:

| Variable | Value |
|----------|-------|
| `BACKEND_URL` | `https://your-backend.onrender.com` |

5. Deploy.

The Nuxt server proxies `/api/v1/**` to `BACKEND_URL` via Nitro routes in `server/api/`.

### Update backend CORS

After you know your Vercel URL, update Render env:

```bash
ALLOWED_ORIGINS=["https://your-app.vercel.app","http://localhost:3000"]
```

Redeploy the backend.

---

## Step 4 — Verify end-to-end

1. Open `https://your-app.vercel.app`
2. Register or log in with `cinephile` / `password123`
3. Browse catalogue → open a Star Wars film → see cross-media suggestions
4. Toggle light/dark mode in the navbar
5. Open **Paramètres** from the navbar

---

## Local development (Docker)

```bash
docker-compose up -d
docker-compose exec backend python -m app.seed
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000/api/v1/docs

---

## Environment variables reference

### Backend

```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host/db?sslmode=require
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
DEBUG=false
STORAGE_BACKEND=local
ALLOWED_ORIGINS=["https://your-app.vercel.app"]
```

### Frontend

```bash
BACKEND_URL=https://your-backend.onrender.com
```

See [`front-end/.env.example`](../front-end/.env.example).

---

## Troubleshooting

### Cold start (Render free tier)

The first request after inactivity takes ~50 seconds. For a live presentation, hit `/health` a few minutes before demoing.

### Database connection errors

- URL must use `postgresql+asyncpg://` (not `postgresql://`)
- Neon requires `?sslmode=require`
- Check Neon dashboard → connection pooling is enabled

### CORS errors in browser

- `ALLOWED_ORIGINS` must include your exact Vercel URL (with `https://`, no trailing slash)
- Redeploy backend after changing CORS

### Empty catalogue

Run the seed script: `python -m app.seed`

### Auth lost on page refresh

Fixed in frontend via `plugins/auth.client.ts` — ensure `BACKEND_URL` is set correctly on Vercel.

---

## Optional: image uploads in production

For user-uploaded covers, use [Supabase Storage](https://supabase.com) free tier (1 GB):

```bash
STORAGE_BACKEND=s3
S3_ENDPOINT_URL=https://xxx.supabase.co/storage/v1/s3
S3_BUCKET_NAME=artiverse
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_PUBLIC_URL=https://xxx.supabase.co/storage/v1/object/public/artiverse
```

For the presentation demo, seeded picsum URLs are sufficient.

---

**Last updated:** 2026-06-11
