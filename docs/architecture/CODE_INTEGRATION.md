# 🔗 Архитектура Интеграции Кода

## Проблема
Нужно связать: Claude Code → GitHub → Веб-сайт → AI Агенты

## 🎯 Решение: Hub & Spoke Pattern

```
           GitHub (Центр)
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
Claude Code   Website   AI Agents
   Push      Read/View   Read/Write
```

## 🏗️ Архитектура

### 1. GitHub (Source of Truth)
- Хранит весь код
- Git history
- Pull Requests
- Webhooks для уведомлений

### 2. Backend API (FastAPI)
```
Backend Server:
├── GitHub Service (PyGithub)
├── Code Analyzer (AST parser)
├── Vector Store (Qdrant) - semantic search
├── Redis Cache - быстрый доступ
└── REST API endpoints
```

**Endpoints:**
- `GET /api/code/files` - дерево файлов
- `GET /api/code/files/{path}` - содержимое файла
- `GET /api/code/search?q=query` - поиск
- `GET /api/code/semantic-search?q=query` - AI поиск
- `POST /webhooks/github` - синхронизация

### 3. Frontend (React)
```
Code Viewer:
├── File Explorer (tree)
├── Code Editor (Monaco)
├── Search (text + AI)
└── Git History
```

### 4. AI Agents
```python
Agents с доступом к коду:
├── CodeAnalystAgent - анализ
├── DevAgent - пишет код
└── TestAgent - генерирует тесты
```

## 🔄 Workflow

### Сценарий 1: Разработка
```
1. Claude Code → git push
2. GitHub → webhook → Backend
3. Backend → обновляет кэш
4. Frontend → показывает изменения
```

### Сценарий 2: AI Agent создаёт PR
```
1. Agent → semantic search кода
2. Agent → генерирует новый код (LLM)
3. Agent → создаёт PR в GitHub
4. Developer → ревьюит в UI
```

## 🛠️ Tech Stack

**Backend:** Python + FastAPI + PyGithub + Qdrant + Redis
**Frontend:** React + TypeScript + Monaco Editor
**AI:** GPT-4o + Claude Opus 4.5 + embeddings

## 📝 Implementation Plan

**Week 1:** GitHub setup + Backend API
**Week 2:** Vector store + semantic search
**Week 3:** Frontend Code Viewer
**Week 4:** AI Agents integration
**Week 5:** Testing + production

## 💰 Cost: ~$160/month
- Infrastructure: $37/mo
- AI APIs: $125/mo

## 🚀 Quick Start

```bash
# 1. Git setup
git init
git add .
git commit -m "Initial commit"

# 2. GitHub (через gh CLI)
gh repo create ai-business-portfolio --private --source=. --push

# 3. Backend
cd backend
pip install fastapi pygithub qdrant-client redis

# 4. Environment
GITHUB_TOKEN=ghp_xxx
GITHUB_REPO=username/ai-business-portfolio
```

---

**Статус:** Ready to Implement
**Дата:** 2026-01-13
