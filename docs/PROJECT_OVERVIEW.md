# AI Business Portfolio Manager

## Цель Проекта

Создать автоматизированную систему для управления портфелем из тысяч бизнесов без человеческого участия.

## MVP Scope (Phase 1)

**Фокус**: Автоматизация поиска трендов и генерации бизнес-идей

### Что входит в MVP:
1. **Automated Trend Discovery**
   - Мониторинг социальных сетей (Twitter, Reddit)
   - Анализ поисковых трендов (Google Trends)
   - Агрегация новостей
   - Ежедневное обновление данных

2. **AI-Powered Idea Analysis**
   - Конвертация трендов в бизнес-идеи
   - Скоринг идей по 6 метрикам
   - Ранжирование и фильтрация
   - Визуализация результатов

3. **Interactive Dashboard**
   - Просмотр трендов в реальном времени
   - Интерактивные графики и кластеры
   - Детальный анализ каждой идеи

### Что НЕ входит в MVP (Phase 2+):
- Автоматическая разработка (DevAgent)
- Маркетинг (MarketingAgent)
- Продажи (SalesAgent)
- Deployment бизнесов

## Tech Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **AI/LLM**: OpenAI API, Anthropic Claude
- **Task Queue**: Celery + Redis
- **Database**: PostgreSQL + Qdrant (vector DB)

### Frontend
- **Framework**: React 18 + TypeScript
- **State**: Zustand
- **Data Fetching**: TanStack Query
- **Visualization**: Recharts, D3.js, ReactFlow
- **UI**: Tailwind CSS + shadcn/ui

### Infrastructure
- **Cloud**: AWS/GCP/Azure
- **Containers**: Docker
- **Orchestration**: Kubernetes (optional for scaling)

## Key Features

1. **Real-time Trend Monitoring** - Автоматический сбор данных каждый час
2. **Semantic Search** - Векторный поиск по трендам и идеям
3. **Smart Scoring** - AI-анализ потенциала бизнес-идей
4. **Beautiful Visualizations** - Минимум текста, максимум графиков

## Success Metrics

- ✅ 100+ новых трендов в день
- ✅ 10+ квалифицированных бизнес-идей в неделю
- ✅ Автоматизация 90%+ процесса анализа
- ✅ Dashboard latency < 2s

## Budget Estimate (MVP)

**Monthly operational costs**: ~$300-500
- Cloud infrastructure: $100-200/mo
- AI API (OpenAI + Claude): $150-250/mo
- Database (managed): $50-100/mo

## Timeline

**Phase 1 (MVP)**: 4-6 weeks
- Week 1-2: Infrastructure + Data Pipeline
- Week 3-4: AI Agents (TrendScout, IdeaAnalyst)
- Week 5-6: Frontend Dashboard + Testing

## Links & Resources

- [Architecture Docs](./architecture/)
- [Research Notes](./research/)
- [Implementation Guides](./guides/)
