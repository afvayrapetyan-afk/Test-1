# AI Business Portfolio Manager

> Автоматизированная система для управления портфелем бизнесов с помощью AI-агентов

## 🎯 Текущая Фаза: Development & Integration

**Статус**: ✅ Code Integration - GitHub ↔ Website ↔ AI Agents

## 📁 Структура Проекта

```
.
├── docs/                       # Документация
│   ├── PROJECT_OVERVIEW.md     # Обзор проекта и scope
│   ├── RESEARCH_PLAN.md        # План исследования
│   ├── research/               # Research notes по каждой теме
│   ├── architecture/           # Архитектурные решения
│   └── guides/                 # Гайды по реализации
│
├── backend/                    # ✅ Python FastAPI backend
│   ├── api/                    # REST API endpoints
│   ├── services/               # GitHub, Code Indexer
│   └── agents/                 # AI Agents с доступом к коду
│
├── frontend/                   # ✅ React TypeScript frontend
│   ├── src/components/         # Code Viewer компоненты
│   └── src/pages/              # Страницы приложения
└── .github/                    # CI/CD workflows
```

## 🔬 Research Phase

Перед началом разработки мы проводим исследование:

1. **AI Agent Architectures** - изучаем AutoGPT, LangChain, CrewAI
2. **Trend Discovery Systems** - анализируем Exploding Topics, Product Hunt
3. **Vector Databases** - сравниваем Qdrant, Pinecone, Weaviate
4. **Workflow Engines** - изучаем n8n, Temporal, Apache Airflow
5. **Data Pipelines** - best practices для real-time scraping
6. **LLM Integration** - оптимизация costs и performance
7. **Scalable Architecture** - паттерны для 1000+ бизнесов

📖 См. [RESEARCH_PLAN.md](docs/RESEARCH_PLAN.md) для деталей

## 🔗 Новое: Code Integration System

### Что реализовано:

**✅ GitHub Integration**
- GitHub Service для работы с API
- Чтение файлов, поиск, история
- Создание PR и веток

**✅ Backend API (FastAPI)**
- `/api/code/files` - дерево файлов
- `/api/code/search` - поиск по коду
- `/api/code/semantic-search` - AI поиск
- `/webhooks/github` - синхронизация

**✅ Frontend Code Viewer**
- File Explorer (дерево файлов)
- Code Editor (подсветка синтаксиса)
- Search (текстовый + AI)

**✅ AI Agents Framework**
- BaseAgent с доступом к коду
- Semantic search через embeddings
- Автоматическое создание PR

📖 **Документация:**
- [Архитектура интеграции](docs/architecture/CODE_INTEGRATION.md)
- [Setup Guide](docs/SETUP_GUIDE.md)

---

## 🎬 Quick Start

```bash
# 1. Setup GitHub
git init
gh repo create ai-business-portfolio --private --source=. --push

# 2. Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настроить .env (см. .env.example)
# GITHUB_TOKEN=ghp_xxx
# GITHUB_REPO=username/ai-business-portfolio

python main.py  # http://localhost:8000

# 3. Frontend
cd ../frontend
npm install
npm run dev  # http://localhost:5173
```

📖 Полная инструкция: [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)



## 🛠 Tech Stack

### MVP (Phase 1)
- **Backend**: Python 3.11 + FastAPI
- **Frontend**: React 18 + TypeScript
- **AI**: OpenAI GPT-4o + Anthropic Claude
- **Database**: PostgreSQL + Qdrant
- **Queue**: Celery + Redis
- **Cloud**: AWS/GCP/Azure

## 📊 Roadmap

### ✅ Phase 1: Code Integration (Completed!)
- [x] GitHub Integration (PyGithub)
- [x] Backend API (FastAPI)
- [x] Frontend Code Viewer (React)
- [x] AI Agents Framework (BaseAgent)
- [x] Semantic Search (Qdrant + embeddings)
- [x] Documentation & Setup Guide

### Phase 2: AI Agents Development - 2 weeks (Next)
- [ ] CodeAnalystAgent - анализ кода
- [ ] DevAgent - автоматическая генерация кода
- [ ] TestAgent - генерация тестов
- [ ] Auto-PR workflow

### Phase 3: Business Analysis Agents - 2 weeks
- [ ] TrendScoutAgent - поиск трендов
- [ ] IdeaAnalystAgent - анализ идей
- [ ] Agent Orchestrator - управление агентами

### Phase 4: Frontend Dashboard - 2 weeks
- [ ] React setup
- [ ] Visualization components
- [ ] Real-time updates
- [ ] Interactive dashboards

## 📚 Documentation

- [Project Overview](docs/PROJECT_OVERVIEW.md) - Общий обзор и цели
- [Research Plan](docs/RESEARCH_PLAN.md) - План исследования
- [Architecture](docs/architecture/) - Архитектурные решения (soon)
- [Guides](docs/guides/) - Гайды по разработке (soon)

## 💰 Estimated Costs

**MVP (Monthly)**:
- Cloud Infrastructure: $100-200
- AI API (OpenAI + Claude): $150-250
- Managed Database: $50-100
- **Total**: ~$300-550/month

**At Scale (1000 businesses)**:
- Infrastructure: $600-1100
- AI API: $3100-7200
- **Total**: ~$3700-8300/month ($3.70-8.30 per business)

## 🤝 Contributing

Пока в режиме исследования и планирования.

## 📄 License

TBD

## 📧 Contact

TBD
