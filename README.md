# ARTIVERSE 🎨

*A centralized transmedia cataloging and review platform for movies, TV series, books, and video games.*

## 🚀 Quick Start with Docker (Recommended)

### Option 1: One-Click Start (Easiest)

**Windows**: Double-click `docker-start.bat`

**macOS/Linux**: Run `./docker-start.sh` (after `chmod +x docker-start.sh`)

### Option 2: Using Make
```bash
make up
```

### Option 3: Manual Docker
```bash
docker-compose up -d
```

Then access:
- 🌐 **Frontend**: http://localhost:3000
- 🔌 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/api/v1/docs

---

## 📖 Project Structure

```
Artiverse/
├── back-end/              # FastAPI Backend (Python 3.12)
│   ├── app/              # Application code
│   ├── alembic/          # Database migrations
│   ├── requirements.txt   # Python dependencies
│   ├── Dockerfile        # Backend Docker image
│   └── README.md         # Backend documentation
├── front-end/            # Nuxt 3 Frontend (Vue.js)
│   ├── app/              # Frontend application
│   ├── package.json      # Node dependencies
│   ├── Dockerfile        # Production build
│   └── README.md         # Frontend documentation
├── docker-compose.yml    # Full-stack Docker setup
├── docker-start.sh       # Linux/Mac startup
├── docker-start.bat      # Windows startup
├── Makefile              # Command shortcuts
└── DOCKER_SETUP.md       # Docker documentation
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy 2.0** - ORM
- **Pydantic** - Data validation
- **JWT** - Authentication

### Frontend
- **Nuxt 3** - Vue.js meta-framework
- **Tailwind CSS** - Utility CSS framework
- **TypeScript** - Type-safe JavaScript

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

---

## 📦 Services

| Service | Port | Tech |
|---------|------|------|
| Frontend | 3000 | Nuxt 3 / Node.js |
| Backend API | 8000 | FastAPI / Python |
| PostgreSQL | 5432 | PostgreSQL 16 |

---

## 🔧 Common Commands

### Start/Stop
```bash
make up           # Start all services
make down         # Stop all services
make restart      # Restart all services
```

### Monitoring
```bash
make logs         # View all logs
make logs-backend  # Backend logs only
make status       # Container status
```

### Development
```bash
make shell-backend   # Access backend shell
make shell-frontend  # Access frontend shell
make shell-postgres  # Access database
```

### Maintenance
```bash
make build        # Build images
make rebuild      # Rebuild from scratch
make clean        # Remove everything
```

---

## 📚 Documentation

- **[Docker Setup](./DOCKER_SETUP.md)** - Complete Docker guide
- **[Backend](./back-end/README.md)** - Backend setup & API docs
- **[Backend Docker](./back-end/DOCKER.md)** - Backend-specific Docker guide
- **[Deployment](./back-end/DEPLOYMENT.md)** - Production deployment
- **[Frontend](./front-end/README.md)** - Frontend setup

---

## 🎯 Phase 1 MVP Features

### ✅ Implemented
- User authentication (JWT)
- User profiles & management
- Media catalog (4 types)
- Rating system (1-10)
- Review system with spoilers
- Custom user lists
- RESTful API with full CRUD

### 📋 Phase 2 (Planned)
- Social features (follow, activity)
- Comments on reviews
- User statistics
- Advanced search
- Real-time notifications

### 🎮 Phase 3 (Planned)
- Gamification system
- Recommendation engine
- Transmedia connections
- Badge system

---

## 🔐 Database Credentials

When using Docker:
```
User: artiverse_user
Password: artiverse_password_dev
Database: artiverse
Host: localhost (on your machine)
```

⚠️ **Change in production!**

---

## 🌍 API Endpoints

### Authentication
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
```

### Users
```
GET    /api/v1/users/me
GET    /api/v1/users/{id}
PATCH  /api/v1/users/me
```

### Media
```
GET    /api/v1/media
POST   /api/v1/media
GET    /api/v1/media/{id}
GET    /api/v1/media/search
GET    /api/v1/media/trending
```

### Ratings & Reviews
```
POST   /api/v1/ratings
GET    /api/v1/ratings/media/{media_id}
POST   /api/v1/reviews
GET    /api/v1/reviews/media/{media_id}
```

### Lists
```
POST   /api/v1/lists
GET    /api/v1/lists/user/me
POST   /api/v1/lists/{id}/items/{media_id}
```

See full API docs at http://localhost:8000/api/v1/docs

---

## 🚨 Troubleshooting

### Containers won't start
```bash
make clean          # Clean up
make rebuild        # Rebuild everything
make up             # Start again
```

### Port already in use
```bash
# Check what's using the port
lsof -i :3000      # macOS/Linux
netstat -ano | findstr :3000  # Windows
```

### Database issues
```bash
docker-compose logs postgres
docker-compose restart postgres
```

See [DOCKER_SETUP.md](./DOCKER_SETUP.md#troubleshooting) for more help.

---

## 📝 License

Proprietary - ESGI Project

---

## 👥 Team

Built as part of ESGI M1 annual project.

---

## 💡 Next Steps

1. **Start the application**: `make up`
2. **Access frontend**: http://localhost:3000
3. **Try the API**: http://localhost:8000/api/v1/docs
4. **Check documentation**: See links above

Enjoy ARTIVERSE! 🎬📚🎮🎸
