# Technical Decisions Summary

**Date**: 2026-01-13
**Phase**: Research → Architecture → Setup Complete
**Status**: ✅ Ready for Implementation

Этот документ содержит все ключевые технические решения, принятые на основе comprehensive research.

---

## 📊 Quick Reference Table

| Component | Decision | Cost (MVP) | Rationale |
|-----------|----------|------------|-----------|
| **Architecture** | Modular Monolith | $200-400/mo | Faster development, simpler ops |
| **AI Agents** | CrewAI + LangGraph | $60-120/mo | Role-based + state management |
| **Vector DB** | Qdrant (self-hosted) | $100-200/mo | Best performance, 65% cheaper |
| **Workflows** | Temporal + Celery | $250-400/mo | Durable workflows + tasks |
| **Data Pipeline** | Hybrid (Stream + Batch) | $200-400/mo | Fresh data + cost optimization |
| **LLM Strategy** | Multi-model | $60-120/mo | Right model for each task |
| **Scaling** | Vertical → Horizontal | $200 → $3000/mo | Start simple, scale as needed |
| **TOTAL MVP** | All components | **$610-1,320/mo** | (~$6-13 per business) |

---

## 1. Architecture Pattern

### ✅ Decision: Modular Monolith

**WHY**: Based on [research/07_scalable_architecture.md](research/07_scalable_architecture.md)

**Rationale**:
- Team < 10 engineers ✅
- MVP/early stage ✅
- Shared data models ✅
- 2026 trend: 42% consolidating back to monoliths
- Faster time to market
- Simpler debugging
- Lower operational cost ($200-400/mo vs $1000+ for microservices)

**Migration Path**:
```
Phase 1 (MVP): Modular Monolith
  ↓
Phase 2 (100-500 businesses): Add read replicas + caching
  ↓
Phase 3 (1000+ businesses): Extract to microservices if needed
```

**Structure**:
```
backend/app/
├── modules/          # Clear service boundaries
│   ├── trends/      # Can extract later
│   ├── ideas/
│   ├── agents/
│   └── businesses/
├── core/            # Shared infrastructure
└── shared/          # Shared utilities
```

---

## 2. AI Agent Framework

### ✅ Decision: CrewAI + LangGraph (Hybrid)

**WHY**: Based on [research/01_ai_agents.md](research/01_ai_agents.md)

**CrewAI** for:
- Role-based orchestration
- Autonomous collaboration between agents
- Built-in delegation

**LangGraph** for:
- Multi-step reasoning workflows
- State management
- Checkpointing (resume from failures)

**Example**:
```python
# CrewAI: Team coordination
crew = Crew(
    agents=[trend_scout, idea_analyst],
    tasks=[discovery_task, analysis_task]
)

# LangGraph: Internal agent workflow
workflow = StateGraph(AnalysisState)
workflow.add_node("research", research_node)
workflow.add_node("score", scoring_node)
workflow.add_node("rank", ranking_node)
```

**Cost**: $60-120/mo для LLM API calls (с оптимизацией)

---

## 3. Vector Database

### ✅ Decision: Qdrant (Self-Hosted)

**WHY**: Based on [research/03_vector_databases.md](research/03_vector_databases.md)

**Performance**:
- p50 latency: 5-10ms (vs 10-15ms Pinecone)
- Throughput: 15,000 QPS
- HNSW index on Rust (fastest)

**Cost Savings**:
- **MVP**: ~$100-200/mo (Qdrant) vs $200-500/mo (Pinecone)
- **At Scale**: ~$800-1200/mo vs $3,500+/mo (Pinecone)
- **Savings**: 65-70% at scale

**Features We Need**:
- ✅ Metadata filtering (category, engagement_score)
- ✅ Quantization (4x memory reduction)
- ✅ Hybrid search (vector + BM25)
- ✅ Python SDK

**Deployment**:
- MVP: Docker Compose (local/single server)
- Production: Kubernetes (3-node cluster)

---

## 4. Workflow Orchestration

### ✅ Decision: Temporal + Celery

**WHY**: Based on [research/04_workflow_engines.md](research/04_workflow_engines.md)

**Temporal** for:
- Long-running business workflows (days/months)
- Durable execution (survives crashes)
- Human-in-the-loop (approval signals)
- Event sourcing

**Celery** for:
- Simple async tasks
- Distributed workers
- Periodic jobs (Celery Beat)

**Division of Labor**:
```
Temporal:
  - Business lifecycle workflows
  - Approval workflows
  - Multi-day processes

Celery:
  - Scraping tasks (hourly)
  - Embedding generation (batch, 2h)
  - Clustering (daily)
```

**Cost**: Infrastructure included in K8s (~$250-400/mo)

---

## 5. Data Pipeline

### ✅ Decision: Hybrid (Streaming + Batch)

**WHY**: Based on [research/05_data_pipelines.md](research/05_data_pipelines.md)

**Real-Time Layer**:
```
Scrapers (Celery) → Kafka (optional) → Consumer Groups
  ↓
PostgreSQL + Redis Cache
```
- Latency: Sub-second
- Use case: User-facing data, dashboards

**Batch Layer**:
```
Celery Beat → Batch Tasks
  ↓
- Embeddings (every 2h) - 50% discount with OpenAI Batch API
- Clustering (daily)
- Analytics (daily)
```
- Cost optimization: 50% savings on LLM
- Use case: Heavy processing

**Cost**: $200-400/mo (Kafka optional, Celery included)

---

## 6. LLM Integration Strategy

### ✅ Decision: Multi-Model + Caching + Batching

**WHY**: Based on [research/06_llm_integration.md](research/06_llm_integration.md)

**Model Selection**:
| Task Complexity | Model | Cost/1M Input | Use Case |
|----------------|-------|---------------|----------|
| **Simple** | GPT-3.5 Turbo | $0.50 | Categorization, extraction |
| **Medium** | GPT-4o-mini | $0.150 | Analysis, summarization |
| **Complex** | GPT-4o | $2.50 | Reasoning, planning |

**Optimizations**:

**1. Prompt Caching** (45% savings):
```python
SYSTEM_PROMPT = """..."""  # 1024+ tokens, static → cached

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},  # Cached!
    {"role": "user", "content": dynamic_data}  # Not cached
]
```

**2. Batch API** (50% savings):
```python
# For non-urgent bulk operations
batch = openai.batches.create(
    input_file_id=file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
)
# 50% discount on input + output tokens
```

**3. Model Router**:
```python
model = ModelSelector.select_model(task_type)
# Auto-select cheapest model for task complexity
```

**Total Cost (Optimized)**: $60-120/mo для MVP

---

## 7. Data Sources Priority

**WHY**: Based on [research/02_data_sources.md](research/02_data_sources.md)

### Priority 1: Search Engines (Foundation)
- **Google Trends** - Free
- **Яндекс Wordstat** - $50-100/mo

### Priority 2: Social Media
- **Reddit** - Free
- **YouTube** - Free
- **Telegram (TGStat)** - $50-200/mo
- **VK** - Free

### Priority 3: Investment Portals
- **Product Hunt** - Free
- **Crunchbase** - $299/mo (optional)

### Priority 4: News
- **TechCrunch** - Free (RSS)
- **Habr, VC.ru** - Free (RSS)

**Total Cost**: $50-200/mo (only TGStat + Yandex paid)

---

## 8. Scaling Strategy

**WHY**: Based on [research/07_scalable_architecture.md](research/07_scalable_architecture.md)

### Phase 1: MVP (0-100 businesses)
**Infrastructure**:
- 1 server (4 CPU, 16GB RAM)
- Vertical scaling only
- **Cost**: $200-400/mo

### Phase 2: Growth (100-500 businesses)
**Infrastructure**:
- 3-5 API pods (Kubernetes HPA)
- Read replicas (2x)
- Redis cluster
- **Cost**: $600-1,000/mo

### Phase 3: Scale (1000+ businesses)
**Infrastructure**:
- 10-20 API pods (auto-scaling)
- Database sharding (4 shards)
- Multi-region (optional)
- **Cost**: $3,000-5,000/mo

**Cost per Business**:
- MVP: $2-8/business/month
- At Scale: $3-5/business/month

---

## 9. Caching Strategy

**Multi-Layer Cache**:

```
Layer 1: Browser (60s) → Static assets
    ↓
Layer 2: CDN (5min) → Images, API responses
    ↓
Layer 3: Application (5min) → lru_cache, in-memory
    ↓
Layer 4: Redis (15min) → Distributed cache
    ↓
Layer 5: Database → Source of truth
```

**Cache Hit Rate Target**: 70-80%

**Benefits**:
- 90% reduction in database queries
- 10x faster API responses
- Lower infrastructure costs

---

## 10. Security

**Authentication**: JWT tokens
**Authorization**: Role-based (RBAC)
**API Keys**: Environment variables only
**Secrets**: Kubernetes Secrets (production)
**HTTPS**: TLS 1.3 only
**Input Validation**: Pydantic schemas
**Rate Limiting**: Redis-based (100 req/min per IP)

---

## 11. Monitoring & Observability

**Metrics**: Prometheus
**Dashboards**: Grafana
**Error Tracking**: Sentry
**Logging**: Structured logs (structlog)
**APM**: DataDog (optional)

**Key Metrics**:
- API response time (p95 < 200ms)
- LLM API costs (daily)
- Agent execution time
- Cache hit rate
- Celery queue depth

---

## 12. Cost Breakdown (MVP)

| Category | Component | Monthly Cost |
|----------|-----------|--------------|
| **Infrastructure** | K8s, PostgreSQL, Redis | $200-400 |
| **Vector DB** | Qdrant (self-hosted) | $100-200 |
| **LLM APIs** | OpenAI (optimized) | $60-120 |
| **Data Sources** | TGStat, Yandex | $50-200 |
| **Data Pipeline** | Celery, Kafka (opt) | Included |
| **Workflows** | Temporal (opt) | Included |
| **TOTAL** | | **$610-1,320/mo** |

**At Scale (1000 businesses)**: $3,700-8,300/mo

---

## 13. Development Stack

**Backend**:
- Python 3.11+
- FastAPI 0.110+
- SQLAlchemy 2.0+ (ORM)
- Pydantic 2.0+ (validation)
- Celery 5.3+ (tasks)

**Frontend**:
- React 18+
- TypeScript 5+
- Vite 5+
- Tailwind CSS
- shadcn/ui

**Infrastructure**:
- Docker
- Docker Compose
- Kubernetes (production)
- Helm (packaging)

---

## 14. Testing Strategy

**Backend**:
- pytest (unit + integration)
- pytest-asyncio
- pytest-cov (>80% coverage target)

**Frontend**:
- Vitest (unit)
- Testing Library (component)
- Playwright (E2E)

**Performance**:
- k6 (load testing)
- Locust (stress testing)

---

## 15. Deployment Strategy

**Development**: Docker Compose
**Staging**: Kubernetes (single cluster)
**Production**: Kubernetes (multi-az)
**CI/CD**: GitHub Actions
**Registry**: Docker Hub / GHCR

**Deployment Frequency**: Daily (MVP), Multiple/day (mature)

---

## Next Steps

1. ✅ Research Complete (7 documents)
2. ✅ Architecture Design
3. ✅ Docker Compose Setup
4. ✅ Database Schema
5. ⏳ Backend Implementation
6. ⏳ Frontend Integration
7. ⏳ AI Agents Development
8. ⏳ MVP Deployment

📖 **See**: [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture
📖 **See**: [QUICK_START.md](QUICK_START.md) to run the project

---

**Research Documents**:
1. [AI Agents](research/01_ai_agents.md)
2. [Data Sources](research/02_data_sources.md)
3. [Vector Databases](research/03_vector_databases.md)
4. [Workflow Engines](research/04_workflow_engines.md)
5. [Data Pipelines](research/05_data_pipelines.md)
6. [LLM Integration](research/06_llm_integration.md)
7. [Scalable Architecture](research/07_scalable_architecture.md)

---

**Last Updated**: 2026-01-13
**Version**: 1.0
**Status**: ✅ Architecture Complete, Ready for Implementation
