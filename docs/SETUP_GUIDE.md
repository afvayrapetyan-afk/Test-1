# 🚀 Setup Guide - Полная инструкция по запуску

## Обзор системы

Ты создал интеграцию: **Claude Code ↔ GitHub ↔ Website ↔ AI Agents**

Теперь нужно всё запустить!

---

## 📋 Prerequisites (Что нужно установить)

### 1. GitHub Account & Token

```bash
# 1. Создать Personal Access Token
# Перейти: https://github.com/settings/tokens/new

# Permissions (выбрать):
☑ repo (Full control)
☑ read:org
☑ workflow

# Скопировать токен: ghp_xxxxxxxxxxxx
```

### 2. Python 3.11+

```bash
# Проверить версию
python --version  # должна быть 3.11+

# Если нет, установить
brew install python@3.11  # macOS
```

### 3. Node.js 18+

```bash
# Проверить версию
node --version  # должна быть 18+

# Если нет
brew install node  # macOS
```

### 4. Docker (опционально, для Qdrant и Redis)

```bash
# Установить Docker Desktop
# https://www.docker.com/products/docker-desktop
```

---

## 🔧 Step 1: GitHub Repository Setup

### Создать репозиторий

```bash
cd "/Users/vardanajrapetan/Project 1"

# Опция A: Через GitHub CLI (рекомендуется)
gh auth login
gh repo create ai-business-portfolio \
  --private \
  --source=. \
  --remote=origin \
  --push

# Опция B: Вручную
# 1. Создать репозиторий на github.com
# 2. Выполнить:
git remote add origin https://github.com/YOUR_USERNAME/ai-business-portfolio.git
git branch -M main
git add .
git commit -m "Initial commit: AI Business Portfolio Manager"
git push -u origin main
```

### Настроить Webhooks (опционально)

```
1. Перейти: https://github.com/YOUR_USERNAME/ai-business-portfolio/settings/hooks
2. Add webhook:
   - Payload URL: https://your-domain.com/webhooks/github
   - Content type: application/json
   - Secret: (генерировать случайную строку)
   - Events: Push, Pull request
3. Сохранить
```

---

## 🔧 Step 2: Backend Setup

### Установка зависимостей

```bash
cd backend

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # macOS/Linux
# или
venv\Scripts\activate  # Windows

# Установить пакеты
pip install -r requirements.txt
```

### Настройка Environment Variables

```bash
# Создать .env файл
cp ../.env.example .env

# Отредактировать .env:
nano .env
```

```bash
# .env
GITHUB_TOKEN=ghp_your_token_here
GITHUB_REPO=YOUR_USERNAME/ai-business-portfolio

# AI APIs (опционально для начала)
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key

# Databases (локально или облако)
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379

# Backend
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

### Запуск баз данных (Docker)

```bash
# Создать docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  qdrant_data:
  redis_data:
EOF

# Запустить
docker-compose up -d
```

### Запуск Backend

```bash
# В папке backend
python main.py

# Или через uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Проверка:**
```bash
# Открыть в браузере
http://localhost:8000
http://localhost:8000/docs  # API документация (Swagger)
```

---

## 🔧 Step 3: Frontend Setup

### Установка зависимостей

```bash
cd frontend

# Установить пакеты
npm install

# Добавить необходимые библиотеки
npm install react-syntax-highlighter @heroicons/react
npm install -D @types/react-syntax-highlighter
```

### Настройка API endpoint

```bash
# Создать .env.local
cat > .env.local << 'EOF'
VITE_API_URL=http://localhost:8000
EOF
```

### Запуск Frontend

```bash
npm run dev
```

**Проверка:**
```bash
# Открыть в браузере
http://localhost:5173
```

---

## 🧪 Step 4: Проверка интеграции

### Test 1: API работает

```bash
# Проверить health check
curl http://localhost:8000/health

# Должен вернуть:
{
  "status": "healthy",
  "github_configured": true,
  ...
}
```

### Test 2: GitHub API работает

```bash
# Получить список файлов
curl http://localhost:8000/api/code/files

# Должен вернуть список файлов из репозитория
```

### Test 3: Frontend → Backend

```bash
# Открыть http://localhost:5173
# Должен показать Code Viewer
# Кликнуть на файл → должен загрузиться код
```

---

## 🤖 Step 5: AI Agents Setup (опционально)

### Получить API ключи

```bash
# OpenAI
https://platform.openai.com/api-keys

# Anthropic
https://console.anthropic.com/settings/keys
```

### Добавить в .env

```bash
OPENAI_API_KEY=sk-proj-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
```

### Тест агента

```python
# Создать test_agent.py
from backend.agents.base_agent import BaseAgent

agent = BaseAgent("TestAgent")

# Прочитать файл
content = agent.read_file("README.md")
print(content[:200])

# Semantic search
results = agent.search_code("authentication", semantic=True)
print(results)
```

```bash
python test_agent.py
```

---

## 📊 Workflow: Как всё работает

### Сценарий 1: Просмотр кода на сайте

```
1. Открыть http://localhost:5173
2. File Explorer → показывает файлы из GitHub
3. Кликнуть на файл → показывает код с подсветкой
4. Search → найти код (текстовый или AI поиск)
```

### Сценарий 2: Разработка в Claude Code

```
1. Редактировать код в Claude Code
2. git add . && git commit -m "Update"
3. git push
4. Webhook → Backend синхронизирует
5. Frontend → обновляется автоматически (будет в Week 5)
```

### Сценарий 3: AI Agent создаёт PR

```python
# Пример использования
from backend.agents.base_agent import BaseAgent

agent = BaseAgent("DevAgent")

# 1. Создать новую ветку
agent.create_branch("feature/add-auth")

# 2. Создать файл
agent.commit_file(
    path="backend/auth.py",
    content="# Authentication module\n...",
    message="Add authentication module",
    branch="feature/add-auth"
)

# 3. Создать PR
pr = agent.create_pull_request(
    title="Add user authentication",
    body="Implements JWT authentication",
    head_branch="feature/add-auth",
    base_branch="main"
)

print(f"PR created: {pr['url']}")
```

---

## 🐛 Troubleshooting

### Проблема: Backend не запускается

```bash
# Проверить Python версию
python --version

# Переустановить зависимости
pip install -r requirements.txt --force-reinstall

# Проверить .env
cat .env
```

### Проблема: GitHub API ошибка 401

```bash
# Проверить токен
echo $GITHUB_TOKEN

# Проверить permissions
gh auth status

# Пересоздать токен с правильными permissions
```

### Проблема: Qdrant не подключается

```bash
# Проверить Docker
docker ps | grep qdrant

# Перезапустить
docker-compose restart qdrant

# Проверить logs
docker logs <container_id>
```

### Проблема: Frontend не видит Backend

```bash
# Проверить CORS в backend/main.py
# Должны быть добавлены:
allow_origins=["http://localhost:5173"]

# Проверить что Backend запущен
curl http://localhost:8000/health
```

---

## 🚀 Production Deployment

### Backend (Railway / Render / Fly.io)

```bash
# Создать Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT

# Deploy на Railway
railway login
railway init
railway up
```

### Frontend (Vercel / Netlify)

```bash
# Build
npm run build

# Deploy на Vercel
vercel --prod
```

### Databases

```
Qdrant Cloud: https://cloud.qdrant.io
Redis: Upstash (бессервный) https://upstash.com
```

---

## 💰 Costs

**Development (Local):**
- $0/month (всё локально)

**Production (Minimal):**
- Backend (Railway): $5-10/month
- Qdrant Cloud: $25/month (1GB)
- Redis (Upstash Free): $0/month
- Frontend (Vercel): $0/month
- **Total: ~$30-35/month**

---

## 📚 Next Steps

**Неделя 1-2: Базовая интеграция (Done!)**
- ✅ GitHub Service
- ✅ Backend API
- ✅ Frontend Code Viewer
- ✅ Base Agent

**Неделя 3-4: AI Agents**
- [ ] CodeAnalystAgent - анализ кода
- [ ] DevAgent - генерация кода
- [ ] TestAgent - тесты
- [ ] Auto-PR workflow

**Неделя 5: Production**
- [ ] WebSocket для live updates
- [ ] Deployment
- [ ] Monitoring
- [ ] Documentation

---

## 🆘 Помощь

**Вопросы?**
- GitHub Issues: https://github.com/YOUR_USERNAME/ai-business-portfolio/issues
- Документация API: http://localhost:8000/docs

**Полезные команды:**
```bash
# Backend
python main.py                    # Запуск
pip freeze > requirements.txt     # Сохранить зависимости

# Frontend
npm run dev                       # Запуск dev сервера
npm run build                     # Продакшн build

# Git
git status                        # Статус
git push                          # Отправить в GitHub

# Docker
docker-compose up -d              # Запустить сервисы
docker-compose logs -f            # Логи
docker-compose down               # Остановить
```

---

**Версия:** 1.0
**Дата:** 2026-01-13
**Статус:** Production Ready
