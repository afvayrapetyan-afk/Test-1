# Quick Start Guide

**Время до запуска**: ~10 минут

Этот guide поможет запустить локальное окружение для разработки за несколько команд.

---

## Prerequisites

Убедитесь, что у вас установлено:

- **Docker** 24.0+ ([Download](https://www.docker.com/products/docker-desktop))
- **Docker Compose** 2.20+ (включен в Docker Desktop)
- **Git** 2.40+
- **Node.js** 18+ (для frontend development)
- **Python** 3.11+ (для backend development)

Проверьте версии:
```bash
docker --version
docker-compose --version
git --version
node --version
python --version
```

---

## Step 1: Clone & Setup

```bash
# Клонировать репозиторий
git clone <your-repo-url>
cd ai-business-portfolio

# Создать .env из примера
cp .env.example .env

# Редактировать .env и добавить API keys
nano .env  # или используйте любой editor
```

**Минимально необходимые ключи для старта**:
```env
OPENAI_API_KEY=sk-your-actual-openai-key

# Остальные можно оставить как есть для локальной разработки
```

---

## Step 2: Start Infrastructure (Docker)

Запустите все сервисы (PostgreSQL, Redis, Qdrant) одной командой:

```bash
docker-compose up -d
```

Эта команда запустит:
- ✅ **PostgreSQL** (порт 5432) - основная база данных
- ✅ **Redis** (порт 6379) - кэш + message broker
- ✅ **Qdrant** (порт 6333) - vector database
- ✅ **Backend API** (порт 8000) - FastAPI
- ✅ **Celery Workers** - фоновые задачи
- ✅ **Celery Beat** - планировщик
- ✅ **Flower** (порт 5555) - мониторинг Celery
- ✅ **Frontend** (порт 5173) - React dashboard

### Проверка статуса

```bash
# Посмотреть логи
docker-compose logs -f

# Проверить статус контейнеров
docker-compose ps

# Должно быть running:
# - postgres (healthy)
# - redis (healthy)
# - qdrant (healthy)
# - api (running)
# - celery-scraping (running)
# - celery-agents (running)
# - celery-beat (running)
# - flower (running)
# - frontend (running)
```

---

## Step 3: Initialize Database

```bash
# Применить миграции
docker-compose exec api alembic upgrade head

# Создать initial data (опционально)
docker-compose exec api python -m app.db.init_data
```

---

## Step 4: Access Services

### 🌐 Frontend Dashboard
```
http://localhost:5173
```
- Trend Explorer
- Idea Viewer
- Agent Monitor

### 🚀 Backend API (Swagger Docs)
```
http://localhost:8000/docs
```
- Interactive API documentation
- Test endpoints

### 📊 Flower (Celery Monitor)
```
http://localhost:5555
```
- Username: `admin`
- Password: `flower123`
- Monitor background tasks
- View worker status

### 🗄️ Database Connections

**PostgreSQL**:
```
Host: localhost
Port: 5432
Database: business_portfolio
User: admin
Password: admin123
```

**Redis**:
```
Host: localhost
Port: 6379
Password: redis123
```

**Qdrant**:
```
REST API: http://localhost:6333
gRPC API: http://localhost:6334
Dashboard: http://localhost:6333/dashboard
```

---

## Step 5: Test Everything

### 5.1 Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Should return:
# {"status": "healthy"}

# Get trends
curl http://localhost:8000/api/v1/trends

# Should return:
# {"success": true, "data": {"items": [], "total": 0}}
```

### 5.2 Test Frontend

Открыть http://localhost:5173 в браузере. Вы должны увидеть dashboard.

### 5.3 Test Celery

```bash
# Trigger a test task
curl -X POST http://localhost:8000/api/v1/agents/run \
  -H "Content-Type: application/json" \
  -d '{"agent_type": "trend_scout", "params": {}}'

# Check Flower UI to see task execution
open http://localhost:5555
```

---

## Development Workflow

### Backend Development

```bash
# Option 1: Run inside Docker (recommended for beginners)
docker-compose up -d

# Option 2: Run locally (for active development)
# Stop API container first
docker-compose stop api

# Start locally
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend Development

```bash
# Option 1: Run inside Docker
docker-compose up -d frontend

# Option 2: Run locally (hot reload)
cd frontend
npm install
npm run dev  # http://localhost:5173
```

### Database Changes

```bash
# Create new migration
docker-compose exec api alembic revision --autogenerate -m "Add new table"

# Apply migrations
docker-compose exec api alembic upgrade head

# Rollback
docker-compose exec api alembic downgrade -1
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f celery-scraping
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 api
```

---

## Common Tasks

### Run Scraping Manually

```bash
# Scrape Reddit
curl -X POST http://localhost:8000/api/v1/agents/run \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "trend_scout",
    "params": {"sources": ["reddit"], "subreddits": ["SideProject", "startups"]}
  }'
```

### Analyze Trends into Ideas

```bash
# Get trend IDs first
curl http://localhost:8000/api/v1/trends

# Analyze specific trends
curl -X POST http://localhost:8000/api/v1/ideas/analyze \
  -H "Content-Type: application/json" \
  -d '{"trend_ids": [1, 2, 3]}'
```

### Clear Cache

```bash
# Connect to Redis
docker-compose exec redis redis-cli -a redis123

# Flush all cache
FLUSHDB

# Or specific pattern
KEYS "trends:*"
DEL "trends:list:*"
```

---

## Troubleshooting

### Port Already in Use

Если порты заняты, измените их в `docker-compose.yml`:

```yaml
services:
  api:
    ports:
      - "8001:8000"  # Change 8000 → 8001
```

### Database Connection Refused

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart if needed
docker-compose restart postgres
```

### Celery Worker Not Processing

```bash
# Check Flower UI
open http://localhost:5555

# Check worker logs
docker-compose logs -f celery-scraping

# Restart workers
docker-compose restart celery-scraping celery-agents
```

### Frontend Can't Connect to API

Проверьте CORS settings в `.env`:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

Перезапустите API:
```bash
docker-compose restart api
```

---

## Stop & Cleanup

### Stop Services

```bash
# Stop all services
docker-compose stop

# Stop specific service
docker-compose stop api
```

### Remove Everything

```bash
# Stop and remove containers (но сохранить volumes)
docker-compose down

# Remove containers AND volumes (⚠️ удалит все данные!)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

---

## Next Steps

После успешного запуска:

1. ✅ **Explore API**: http://localhost:8000/docs
2. ✅ **Check Dashboard**: http://localhost:5173
3. ✅ **Monitor Tasks**: http://localhost:5555
4. 📖 **Read Architecture**: [docs/ARCHITECTURE.md](ARCHITECTURE.md)
5. 🛠 **Start Developing**: [docs/guides/DEVELOPMENT.md](guides/DEVELOPMENT.md)

---

## Getting Help

- 📖 [Architecture Documentation](ARCHITECTURE.md)
- 📖 [Research Documents](research/)
- 🐛 [Report Issues](https://github.com/your-repo/issues)
- 💬 [Discussions](https://github.com/your-repo/discussions)

---

**Estimated Resource Usage**:
- RAM: ~4-6 GB
- Disk: ~2-3 GB
- CPU: Low (idle), Medium (during scraping/analysis)

Happy building! 🚀
