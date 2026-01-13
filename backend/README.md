# AI Business Portfolio Manager - Backend

FastAPI backend для автоматизированной системы управления портфелем бизнесов.

## 📁 Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── core/                # Core infrastructure
│   │   ├── config.py        # Settings management
│   │   ├── database.py      # Database connection
│   │   └── cache.py         # Redis cache (TODO)
│   ├── modules/             # Business logic modules (Modular Monolith)
│   │   ├── trends/          # Trend discovery service
│   │   │   └── router.py    # API endpoints
│   │   ├── ideas/           # Idea analysis service
│   │   │   └── router.py
│   │   ├── agents/          # Agent management
│   │   │   └── router.py
│   │   └── businesses/      # Business lifecycle (TODO)
│   ├── agents/              # AI Agents (CrewAI + LangGraph)
│   │   ├── base_agent.py    # Base agent class (TODO)
│   │   ├── trend_scout.py   # Trend discovery agent (TODO)
│   │   └── idea_analyst.py  # Idea analysis agent (TODO)
│   ├── scrapers/            # Data source scrapers
│   │   ├── reddit.py        # Reddit scraper (TODO)
│   │   ├── google_trends.py # Google Trends (TODO)
│   │   └── telegram.py      # Telegram scraper (TODO)
│   ├── tasks/               # Celery background tasks
│   │   └── celery_config.py # Celery setup (TODO)
│   └── shared/              # Shared utilities
├── db/
│   └── init.sql             # ✅ Database initialization
├── requirements.txt         # ✅ Python dependencies
├── Dockerfile               # ✅ Container configuration
└── .env.example             # ✅ Environment variables template
```

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Qdrant (optional for MVP)

### 1. Install Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Environment

```bash
# Copy .env.example to .env
cp ../.env.example .env

# Edit .env and add your API keys
nano .env
```

Minimum required:
```env
DATABASE_URL=postgresql://admin:admin123@localhost:5432/business_portfolio
REDIS_URL=redis://:redis123@localhost:6379/0
OPENAI_API_KEY=sk-your-actual-key
SECRET_KEY=your-secret-key-min-32-chars
```

### 3. Initialize Database

```bash
# Make sure PostgreSQL is running
# Create database
createdb business_portfolio

# Or using psql
psql -U admin -c "CREATE DATABASE business_portfolio;"

# Run init script
psql -U admin -d business_portfolio -f db/init.sql
```

### 4. Run Development Server

```bash
# Start FastAPI with hot reload
uvicorn app.main:app --reload --port 8000

# Or using Python directly
python -m app.main
```

API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 Docker Development

### Using Docker Compose (Recommended)

```bash
# From project root
docker-compose up -d

# View logs
docker-compose logs -f api

# Rebuild after code changes
docker-compose up -d --build api
```

### Standalone Docker

```bash
# Build image
docker build -t business-portfolio-api .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  -e OPENAI_API_KEY=sk-... \
  business-portfolio-api
```

## 📚 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Trends
```bash
# Get trends
curl http://localhost:8000/api/v1/trends

# Get single trend
curl http://localhost:8000/api/v1/trends/1

# Get statistics
curl http://localhost:8000/api/v1/trends/stats
```

### Ideas
```bash
# Get ideas
curl http://localhost:8000/api/v1/ideas

# Analyze trends into ideas
curl -X POST http://localhost:8000/api/v1/ideas/analyze \
  -H "Content-Type: application/json" \
  -d '{"trend_ids": [1, 2, 3]}'
```

### Agents
```bash
# Get agent status
curl http://localhost:8000/api/v1/agents/status

# Run agent
curl -X POST http://localhost:8000/api/v1/agents/run \
  -H "Content-Type: application/json" \
  -d '{"agent_type": "trend_scout", "params": {}}'

# Get execution history
curl http://localhost:8000/api/v1/agents/executions
```

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_trends.py

# Watch mode
pytest-watch
```

## 🛠 Development Tools

### Code Formatting

```bash
# Format code with Black
black app/

# Sort imports
isort app/

# Lint with flake8
flake8 app/
```

### Type Checking

```bash
# Run mypy
mypy app/
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 📊 Monitoring

### Celery (Background Tasks)

```bash
# Start Celery worker
celery -A app.core.celery_config worker -Q scraping --loglevel=info

# Start Celery Beat (scheduler)
celery -A app.core.celery_config beat --loglevel=info

# Monitor with Flower
celery -A app.core.celery_config flower --port=5555
# Access at http://localhost:5555
```

### Logs

```bash
# View application logs
tail -f logs/app.log

# Structured logs in JSON
tail -f logs/app.json
```

## 🔧 Configuration

See [.env.example](../.env.example) for all available environment variables.

Key settings:
- `ENVIRONMENT`: development/staging/production
- `DEBUG`: Enable debug mode
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `OPENAI_API_KEY`: OpenAI API key
- `SECRET_KEY`: JWT secret key

## 📖 Documentation

- [Architecture](../docs/ARCHITECTURE.md) - System architecture
- [Tech Decisions](../docs/TECH_DECISIONS.md) - Technology choices
- [Quick Start](../docs/QUICK_START.md) - Complete setup guide

## 🐛 Troubleshooting

### Import errors

```bash
# Make sure you're in the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt
```

### Database connection refused

```bash
# Check PostgreSQL is running
pg_isready

# Check connection string in .env
echo $DATABASE_URL
```

### Port already in use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001
```

## 📝 Next Steps

1. ✅ Basic structure created
2. ⏳ Implement database models (SQLAlchemy)
3. ⏳ Implement AI agents (CrewAI + LangGraph)
4. ⏳ Implement scrapers (Reddit, Google Trends, etc.)
5. ⏳ Implement Celery tasks
6. ⏳ Add authentication
7. ⏳ Add WebSocket support for real-time updates

## 🤝 Contributing

See main [README.md](../README.md) for contributing guidelines.
