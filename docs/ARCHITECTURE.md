# System Architecture

**Version**: 1.0
**Date**: 2026-01-13
**Status**: MVP Design

## Executive Summary

Архитектура автоматизированной системы управления портфелем из 1000+ бизнесов. Система использует AI-агентов для полного цикла: discovery трендов → анализ идей → разработка → маркетинг → продажи → запуск.

**MVP Focus**: Automated Trend Discovery + Business Idea Analysis

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Decisions](#architecture-decisions)
3. [Technology Stack](#technology-stack)
4. [Component Architecture](#component-architecture)
5. [Data Flow](#data-flow)
6. [Database Design](#database-design)
7. [API Design](#api-design)
8. [Deployment Architecture](#deployment-architecture)
9. [Security](#security)
10. [Scalability](#scalability)

---

## 1. System Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
│              React + TypeScript Dashboard                       │
│  - Trend Explorer - Idea Viewer - Agent Monitor - Analytics    │
└───────────────────────────┬─────────────────────────────────────┘
                            │ REST API / WebSocket
┌───────────────────────────▼─────────────────────────────────────┐
│                    API Gateway (FastAPI)                        │
│  - Authentication - Rate Limiting - Request Routing             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼──────┐  ┌─────────▼────────┐  ┌──────▼────────┐
│   Trends     │  │     Ideas        │  │   Businesses  │
│   Service    │  │    Service       │  │    Service    │
└───────┬──────┘  └─────────┬────────┘  └──────┬────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼──────┐  ┌─────────▼────────┐  ┌──────▼────────┐
│  Scraping    │  │   AI Agents      │  │  Workflow     │
│  Workers     │  │  (CrewAI +       │  │  Engine       │
│  (Celery)    │  │   LangGraph)     │  │  (Temporal)   │
└───────┬──────┘  └─────────┬────────┘  └──────┬────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼──────┐  ┌─────────▼────────┐  ┌──────▼────────┐
│  PostgreSQL  │  │     Qdrant       │  │     Redis     │
│ (Structured) │  │   (Vectors)      │  │   (Cache +    │
│              │  │                  │  │    Queue)     │
└──────────────┘  └──────────────────┘  └───────────────┘
```

### 1.2 Core Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | React + TypeScript | User dashboard, visualization |
| **API Gateway** | FastAPI | REST API, WebSocket, auth |
| **Services** | Python modules | Business logic (modular monolith) |
| **AI Agents** | CrewAI + LangGraph | Autonomous agents |
| **Workflows** | Temporal | Long-running business processes |
| **Task Queue** | Celery + Redis | Async job processing |
| **Data Pipeline** | Kafka (optional) | Real-time streaming |
| **Storage** | PostgreSQL | Structured data |
| **Vector DB** | Qdrant | Semantic search |
| **Cache** | Redis | Multi-layer caching |

---

## 2. Architecture Decisions

### 2.1 Monolith vs Microservices

**Decision**: ✅ **Modular Monolith** (Phase 1-2)

**Rationale** (based on [research/07_scalable_architecture.md](research/07_scalable_architecture.md)):
- Team < 10 engineers
- MVP/early stage
- Shared data models
- Simpler deployment and debugging
- Lower operational cost ($200-400/mo vs $1000+)

**Future Migration Path**:
- Clear module boundaries allow extraction to microservices
- Services communicate via well-defined interfaces
- Database can be split later (sharding)

**Structure**:
```
backend/
├── app/
│   ├── main.py                   # FastAPI app
│   ├── modules/
│   │   ├── trends/              # Self-contained module
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── ideas/
│   │   ├── agents/
│   │   └── businesses/
│   ├── core/                    # Shared infrastructure
│   │   ├── database.py
│   │   ├── cache.py
│   │   └── config.py
│   └── shared/                  # Shared utilities
```

### 2.2 AI Agent Framework

**Decision**: ✅ **CrewAI + LangGraph** (Hybrid)

**Rationale** (based on [research/01_ai_agents.md](research/01_ai_agents.md)):
- **CrewAI**: Role-based orchestration, autonomous collaboration
- **LangGraph**: State management, complex workflows, checkpointing
- Best of both worlds

**Usage**:
- CrewAI for agent teams (TrendScout + IdeaAnalyst collaboration)
- LangGraph for internal agent state (multi-step reasoning)

### 2.3 Vector Database

**Decision**: ✅ **Qdrant (self-hosted)**

**Rationale** (based on [research/03_vector_databases.md](research/03_vector_databases.md)):
- Best performance (5-10ms p50 latency)
- 65-70% cheaper than Pinecone at scale
- Full control over infrastructure
- Quantization support (4x memory reduction)

### 2.4 Workflow Orchestration

**Decision**: ✅ **Temporal** (for business workflows) + **Celery** (for tasks)

**Rationale** (based on [research/04_workflow_engines.md](research/04_workflow_engines.md)):
- **Temporal**: Durable execution, long-running workflows (days/months)
- **Celery**: Simple async tasks, distributed workers
- Temporal manages business lifecycle, Celery handles background jobs

### 2.5 Data Pipeline

**Decision**: ✅ **Hybrid** (Streaming + Batch)

**Rationale** (based on [research/05_data_pipelines.md](research/05_data_pipelines.md)):
- **Real-time**: Scrapers → Kafka → Consumer groups (low latency)
- **Batch**: Celery Beat for embeddings (cost optimization)
- Best balance of freshness and cost

### 2.6 LLM Strategy

**Decision**: ✅ **Hybrid Model Selection** + **Prompt Caching** + **Batching**

**Rationale** (based on [research/06_llm_integration.md](research/06_llm_integration.md)):
- GPT-3.5 Turbo ($0.50/1M) for simple tasks
- GPT-4o-mini ($0.150/1M) for medium tasks
- GPT-4o ($2.50/1M) for complex reasoning
- 45% savings with prompt caching
- 50% savings with batch API

---

## 3. Technology Stack

### 3.1 Backend

```yaml
Core Framework:
  - FastAPI 0.110+              # Modern async API framework
  - Python 3.11+                # Latest stable Python
  - Pydantic 2.0+               # Data validation

Database:
  - PostgreSQL 15+              # Primary database
  - SQLAlchemy 2.0+             # ORM
  - Alembic                     # Migrations
  - Qdrant 1.7+                 # Vector database

AI & ML:
  - OpenAI Python SDK           # GPT-4o, embeddings
  - Anthropic Python SDK        # Claude (fallback)
  - LangChain 0.1+              # LLM utilities
  - CrewAI 0.28+                # Agent orchestration
  - LangGraph 0.0.40+           # Workflow graphs

Task Queue & Workers:
  - Celery 5.3+                 # Distributed task queue
  - Redis 7+                    # Message broker + cache
  - Flower                      # Celery monitoring

Workflow:
  - Temporal (optional)         # Durable workflows
  - Apache Airflow (optional)   # Batch orchestration

Data Processing:
  - Pandas 2.1+                 # Data manipulation
  - NumPy                       # Numerical operations
  - Polars (optional)           # High-performance alternative

Scraping:
  - httpx                       # Async HTTP client
  - BeautifulSoup4              # HTML parsing
  - Playwright (optional)       # Browser automation

Testing:
  - pytest                      # Test framework
  - pytest-asyncio              # Async tests
  - pytest-cov                  # Coverage

DevOps:
  - Docker                      # Containerization
  - Docker Compose              # Local orchestration
  - Kubernetes (production)     # Container orchestration
```

### 3.2 Frontend

```yaml
Core Framework:
  - React 18+                   # UI library
  - TypeScript 5+               # Type safety
  - Vite 5+                     # Build tool

State Management:
  - Zustand                     # Lightweight state
  - React Query                 # Server state

UI Components:
  - Tailwind CSS                # Utility-first CSS
  - shadcn/ui                   # Component library
  - Recharts                    # Data visualization
  - React Flow                  # Graph visualization

Real-time:
  - Socket.io-client            # WebSocket client

Forms & Validation:
  - React Hook Form             # Form handling
  - Zod                         # Schema validation

Testing:
  - Vitest                      # Unit testing
  - Testing Library             # Component testing
  - Playwright                  # E2E testing
```

### 3.3 Infrastructure

```yaml
Containerization:
  - Docker                      # Application containers
  - Docker Compose              # Local development

Orchestration:
  - Kubernetes                  # Production (GKE/EKS/AKS)
  - Helm                        # Package manager

Databases:
  - PostgreSQL (managed)        # AWS RDS / GCP Cloud SQL
  - Redis (managed)             # AWS ElastiCache
  - Qdrant (self-hosted)        # Kubernetes deployment

Monitoring:
  - Prometheus                  # Metrics
  - Grafana                     # Dashboards
  - Sentry                      # Error tracking
  - DataDog (optional)          # APM

CI/CD:
  - GitHub Actions              # CI/CD pipelines
  - Docker Registry             # Container registry

Cloud:
  - AWS / GCP / Azure           # Cloud provider
  - CDN (Cloudflare)            # Static assets
```

---

## 4. Component Architecture

### 4.1 Backend Services (Modular Monolith)

#### 4.1.1 Trends Service

```python
# app/modules/trends/

router.py:
  - GET  /api/v1/trends              # List trends
  - POST /api/v1/trends              # Create trend (scraper)
  - GET  /api/v1/trends/{id}         # Get trend
  - GET  /api/v1/trends/search       # Semantic search

service.py:
  class TrendService:
    - get_trends(filters, pagination)
    - create_trend(trend_data)
    - search_trends(query, filters)
    - get_trending_categories()

repository.py:
  class TrendRepository:
    - get_many(skip, limit, filters)
    - create(trend_data)
    - update(trend_id, data)
    - semantic_search(embedding, filters)

schemas.py:
  - TrendCreate
  - TrendOut
  - TrendSearch
```

#### 4.1.2 Ideas Service

```python
# app/modules/ideas/

router.py:
  - GET  /api/v1/ideas               # List ideas
  - POST /api/v1/ideas/analyze       # Analyze trend → idea
  - GET  /api/v1/ideas/{id}          # Get idea
  - PATCH /api/v1/ideas/{id}         # Update scores

service.py:
  class IdeaService:
    - analyze_trend(trend_id)        # AI analysis
    - get_ideas(filters)
    - score_idea(idea_id)
    - rank_ideas()

repository.py:
  class IdeaRepository:
    - create_from_trend(trend, analysis)
    - get_top_rated(limit)
    - update_scores(idea_id, scores)
```

#### 4.1.3 Agents Service

```python
# app/modules/agents/

service.py:
  class AgentOrchestrator:
    - run_trend_discovery()          # Orchestrate TrendScout
    - run_idea_analysis(trend_ids)   # Orchestrate IdeaAnalyst
    - get_agent_status()

agents/:
  - base_agent.py                    # BaseAgent class
  - trend_scout_agent.py             # Trend discovery
  - idea_analyst_agent.py            # Idea analysis
```

### 4.2 AI Agents Architecture

```python
# app/agents/base_agent.py

from crewai import Agent, Task, Crew
from langgraph.graph import StateGraph

class BaseAgent:
    """Base class for all agents"""

    def __init__(self, role: str, goal: str, backstory: str):
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=self.get_tools(),
            verbose=True
        )

    def get_tools(self) -> List[Tool]:
        """Override in subclass"""
        return []

    async def run(self, **kwargs):
        """Execute agent task"""
        raise NotImplementedError


# app/agents/trend_scout_agent.py

class TrendScoutAgent(BaseAgent):
    """
    Discovers trends from multiple sources
    """

    def __init__(self):
        super().__init__(
            role="Trend Discovery Specialist",
            goal="Find 100+ emerging trends daily",
            backstory="""You monitor Twitter, Reddit, Google Trends,
            Telegram, and VK to identify rising topics..."""
        )

    def get_tools(self) -> List[Tool]:
        return [
            reddit_scraper_tool,
            google_trends_tool,
            telegram_monitor_tool,
            vk_scraper_tool
        ]

    async def run(self, sources: List[str]) -> List[Trend]:
        """Discover trends from sources"""
        # CrewAI handles execution
        task = Task(
            description=f"Scrape trends from {sources}",
            agent=self.agent,
            expected_output="List of 100+ trends with metadata"
        )

        crew = Crew(agents=[self.agent], tasks=[task])
        result = await crew.kickoff()

        return self.parse_trends(result)


# app/agents/idea_analyst_agent.py

class IdeaAnalystAgent(BaseAgent):
    """
    Analyzes trends and scores business ideas
    """

    def __init__(self):
        super().__init__(
            role="Business Analyst",
            goal="Score business ideas on 6 metrics",
            backstory="""Expert at evaluating market opportunities..."""
        )

        # LangGraph for multi-step reasoning
        self.workflow = self.build_workflow()

    def build_workflow(self) -> StateGraph:
        """Multi-step analysis workflow"""
        workflow = StateGraph(AnalysisState)

        workflow.add_node("research", self.research_market)
        workflow.add_node("score", self.score_metrics)
        workflow.add_node("rank", self.rank_ideas)

        workflow.set_entry_point("research")
        workflow.add_edge("research", "score")
        workflow.add_edge("score", "rank")

        return workflow.compile()

    async def run(self, trends: List[Trend]) -> List[Idea]:
        """Analyze trends into business ideas"""
        state = {
            "trends": trends,
            "research": {},
            "scores": {},
            "ideas": []
        }

        result = await self.workflow.ainvoke(state)
        return result["ideas"]
```

### 4.3 Data Pipeline Architecture

```python
# app/pipeline/scraping_pipeline.py

class ScrapingPipeline:
    """
    Real-time + Batch hybrid pipeline
    """

    def __init__(self):
        self.kafka_producer = KafkaProducer(...)  # Optional
        self.dedup_service = DeduplicationService()

    # Real-time ingestion
    async def ingest_trend(self, trend: dict):
        """Scraper → Kafka → Processing"""

        # Validate
        validated = validate_scraped_data(trend)

        # Deduplicate
        if self.dedup_service.is_duplicate(validated):
            return

        # Send to Kafka (or direct to DB for MVP)
        await self.kafka_producer.send('raw_trends', validated)


# app/tasks/celery_tasks.py

@app.task(name='scraping.reddit')
def scrape_reddit_task(subreddit: str):
    """Celery task for Reddit scraping"""
    scraper = RedditScraper()
    posts = scraper.fetch_posts(subreddit, limit=100)

    pipeline = ScrapingPipeline()
    for post in posts:
        asyncio.run(pipeline.ingest_trend(post))


@app.task(name='analysis.batch_embeddings')
def batch_embeddings_task():
    """Batch generate embeddings (every 2 hours)"""
    service = EmbeddingService()

    # Get trends without embeddings
    trends = get_trends_needing_embeddings()

    # Batch generate (50% discount with OpenAI Batch API)
    service.batch_generate(trends)


# Celery Beat schedule
app.conf.beat_schedule = {
    'scrape-hourly': {
        'task': 'scraping.scrape_all',
        'schedule': crontab(minute=0),  # Every hour
    },
    'embeddings-2h': {
        'task': 'analysis.batch_embeddings',
        'schedule': crontab(minute=0, hour='*/2'),
    },
}
```

---

## 5. Data Flow

### 5.1 Trend Discovery Flow

```
1. Scraping (Every hour)
   Celery Task → Scrapers (Reddit, Google Trends, etc.)
                     ↓
2. Validation & Deduplication
   Pydantic validation → Bloom filter → Redis check
                     ↓
3. Storage (Dual write)
   PostgreSQL (metadata) + Qdrant (embedding - batch)
                     ↓
4. Real-time Updates
   WebSocket → Frontend (new trends notification)
```

### 5.2 Idea Analysis Flow

```
1. Trigger (Manual or Auto)
   User clicks "Analyze" OR Daily cron job
                     ↓
2. Agent Execution
   IdeaAnalystAgent → LLM calls (GPT-4o)
                     ↓
3. Multi-step Reasoning (LangGraph)
   Research → Scoring → Ranking
                     ↓
4. Storage
   PostgreSQL (idea + scores)
                     ↓
5. Notification
   WebSocket → Frontend (analysis complete)
```

### 5.3 Business Lifecycle Flow (Future)

```
Temporal Workflow:
   Trend Discovery (Activity)
         ↓
   Idea Analysis (Activity)
         ↓
   Human Approval (Signal - wait days)
         ↓
   Development (Activity - DevAgent)
         ↓
   Marketing (Activity - MarketingAgent)
         ↓
   Sales Setup (Activity - SalesAgent)
         ↓
   Launch (Activity)
```

---

## 6. Database Design

### 6.1 PostgreSQL Schema

```sql
-- Trends table
CREATE TABLE trends (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    url TEXT,
    source VARCHAR(50) NOT NULL,  -- reddit, google_trends, telegram, vk
    category VARCHAR(50),
    tags TEXT[],
    engagement_score INTEGER DEFAULT 0,
    velocity FLOAT DEFAULT 0,  -- Trend velocity (growth rate)
    discovered_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB,  -- Flexible metadata
    CONSTRAINT valid_source CHECK (source IN ('reddit', 'google_trends', 'telegram', 'vk', 'youtube', 'instagram'))
);

CREATE INDEX idx_trends_source ON trends(source);
CREATE INDEX idx_trends_category ON trends(category);
CREATE INDEX idx_trends_engagement ON trends(engagement_score DESC);
CREATE INDEX idx_trends_discovered ON trends(discovered_at DESC);
CREATE INDEX idx_trends_tags ON trends USING GIN(tags);

-- Ideas table
CREATE TABLE ideas (
    id SERIAL PRIMARY KEY,
    trend_id INTEGER REFERENCES trends(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,

    -- Scores (0-100)
    market_size_score INTEGER,
    competition_score INTEGER,
    demand_score INTEGER,
    monetization_score INTEGER,
    feasibility_score INTEGER,
    time_to_market_score INTEGER,

    -- Overall
    total_score INTEGER GENERATED ALWAYS AS (
        (market_size_score + competition_score + demand_score +
         monetization_score + feasibility_score + time_to_market_score) / 6
    ) STORED,

    -- Analysis
    analysis JSONB,  -- Full LLM analysis
    analyzed_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending',  -- pending, approved, rejected, in_development

    CONSTRAINT valid_scores CHECK (
        market_size_score BETWEEN 0 AND 100 AND
        competition_score BETWEEN 0 AND 100 AND
        demand_score BETWEEN 0 AND 100 AND
        monetization_score BETWEEN 0 AND 100 AND
        feasibility_score BETWEEN 0 AND 100 AND
        time_to_market_score BETWEEN 0 AND 100
    )
);

CREATE INDEX idx_ideas_total_score ON ideas(total_score DESC);
CREATE INDEX idx_ideas_status ON ideas(status);
CREATE INDEX idx_ideas_trend ON ideas(trend_id);

-- Businesses table (Future)
CREATE TABLE businesses (
    id SERIAL PRIMARY KEY,
    idea_id INTEGER REFERENCES ideas(id),
    name VARCHAR(200) NOT NULL,
    domain VARCHAR(100),
    status VARCHAR(50) DEFAULT 'development',  -- development, launched, active, paused

    -- Metrics
    revenue_monthly DECIMAL(10, 2),
    users_count INTEGER,

    -- Lifecycle
    developed_at TIMESTAMP,
    launched_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),

    metadata JSONB
);

-- Agent executions log
CREATE TABLE agent_executions (
    id SERIAL PRIMARY KEY,
    agent_type VARCHAR(50) NOT NULL,  -- trend_scout, idea_analyst, dev_agent
    input_data JSONB,
    output_data JSONB,
    status VARCHAR(20),  -- running, completed, failed
    error TEXT,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    duration_seconds INTEGER
);

CREATE INDEX idx_executions_agent ON agent_executions(agent_type);
CREATE INDEX idx_executions_status ON agent_executions(status);
```

### 6.2 Qdrant Collections

```python
# Vector embeddings for semantic search

# Trends collection
client.create_collection(
    collection_name="trends",
    vectors_config=VectorParams(
        size=768,  # text-embedding-3-small (reduced from 1536)
        distance=Distance.COSINE,
        quantization_config=ScalarQuantization(
            scalar=ScalarQuantizationConfig(
                type=ScalarType.INT8,
                quantile=0.99
            )
        )
    )
)

# Point structure:
{
    "id": 12345,  # Same as PostgreSQL trend.id
    "vector": [0.123, -0.456, ...],  # 768 dimensions
    "payload": {
        "title": "AI-powered note-taking",
        "category": "productivity",
        "engagement_score": 1523,
        "source": "reddit",
        "tags": ["AI", "SaaS"],
        "url": "https://..."
    }
}

# Ideas collection (similar structure)
client.create_collection(
    collection_name="ideas",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)
```

### 6.3 Redis Structure

```
# Cache keys pattern: {entity}:{operation}:{params}
trends:list:skip:0:limit:100          → List cache
trends:stats:category:tech            → Aggregations
trends:{id}                           → Single item

# Deduplication
trends:recent:hashes                  → Set of recent hashes (24h TTL)

# Rate limiting
rate_limit:reddit_api                 → Counter (60/min)
rate_limit:openai_api                 → Counter (500/min)

# Celery queues
celery:scraping                       → Task queue (high priority)
celery:agents                         → Task queue (medium priority)
celery:analysis                       → Task queue (low priority)

# Session/Auth
session:{user_id}                     → User session
```

---

## 7. API Design

### 7.1 REST API Endpoints

```yaml
# Trends
GET    /api/v1/trends
  Query params: skip, limit, category, source, min_engagement
  Response: {items: [...], total: int, has_more: bool}

POST   /api/v1/trends
  Body: {title, description, url, source, ...}
  Response: Trend object

GET    /api/v1/trends/{id}
  Response: Trend object with full details

GET    /api/v1/trends/search
  Query params: q (query), category, limit
  Response: Semantic search results

GET    /api/v1/trends/stats
  Response: {total, by_category, by_source, top_trending}

# Ideas
GET    /api/v1/ideas
  Query params: skip, limit, min_score, status
  Response: {items: [...], total: int}

POST   /api/v1/ideas/analyze
  Body: {trend_ids: [int]}
  Response: {job_id: str}  # Async task ID

GET    /api/v1/ideas/{id}
  Response: Idea object with full analysis

PATCH  /api/v1/ideas/{id}
  Body: {status: "approved"}
  Response: Updated idea

# Agents
GET    /api/v1/agents/status
  Response: {trend_scout: {status, last_run}, ...}

POST   /api/v1/agents/run
  Body: {agent_type: "trend_scout", params: {...}}
  Response: {job_id: str}

GET    /api/v1/agents/executions
  Response: Recent agent execution history

# Websocket
WS     /ws
  Events:
    - trend.created
    - idea.analyzed
    - agent.status_update
```

### 7.2 API Response Format

```json
// Success response
{
  "success": true,
  "data": {...},
  "meta": {
    "total": 100,
    "page": 1,
    "has_more": true
  }
}

// Error response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {...}
  }
}
```

---

## 8. Deployment Architecture

### 8.1 Development (Docker Compose)

```yaml
# docker-compose.yml

services:
  # Databases
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: business_portfolio
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  qdrant:
    image: qdrant/qdrant:v1.7
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

  # Backend
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@postgres/business_portfolio
      REDIS_URL: redis://redis:6379
      QDRANT_URL: http://qdrant:6333
    depends_on:
      - postgres
      - redis
      - qdrant
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  # Celery workers
  celery-worker:
    build: ./backend
    command: celery -A app.core.celery_config worker -Q scraping --loglevel=info
    depends_on:
      - redis
      - postgres

  celery-beat:
    build: ./backend
    command: celery -A app.core.celery_config beat --loglevel=info
    depends_on:
      - redis

  # Frontend
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev

volumes:
  postgres_data:
  qdrant_data:
  redis_data:
```

### 8.2 Production (Kubernetes)

```yaml
# k8s/api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: business-portfolio/api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
        readinessProbe:
          httpGet:
            path: /health
            port: 8000

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## 9. Security

### 9.1 Authentication & Authorization

```python
# JWT-based authentication
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY)
        return payload
    except:
        raise HTTPException(status_code=401)

# Usage
@app.get("/api/v1/trends")
async def get_trends(user = Depends(get_current_user)):
    # Authorized access
    pass
```

### 9.2 Rate Limiting

```python
# Redis-based rate limiting
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.get("/api/v1/trends", dependencies=[Depends(RateLimiter(times=100, seconds=60))])
async def get_trends():
    # Max 100 requests per minute
    pass
```

### 9.3 Data Protection

- API keys in environment variables (never commit)
- Secrets stored in Kubernetes Secrets
- Database encryption at rest
- HTTPS only (TLS 1.3)
- CORS configuration
- Input validation (Pydantic)
- SQL injection protection (SQLAlchemy ORM)

---

## 10. Scalability

### 10.1 Scaling Strategy

**Phase 1: Vertical (MVP)**
- Single server: 4 CPU, 16GB RAM
- Cost: $150-250/month

**Phase 2: Horizontal (100-500 businesses)**
- 3-5 API pods (Kubernetes)
- Read replicas (2x)
- Redis cluster
- Cost: $600-1000/month

**Phase 3: Distributed (1000+ businesses)**
- 10-20 API pods (auto-scaling)
- Database sharding (4 shards)
- Multi-region deployment
- Cost: $3000-5000/month

### 10.2 Performance Targets

| Metric | Target | Strategy |
|--------|--------|----------|
| API Response Time (p95) | <200ms | Caching, DB indexes |
| Search Latency (p95) | <500ms | Qdrant optimization |
| Agent Execution | <5min | Parallel LLM calls |
| Trend Discovery | 1000+/hour | Distributed scrapers |
| Concurrent Users | 1000+ | Horizontal scaling |

---

## 11. Monitoring & Observability

### 11.1 Metrics

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram

api_requests = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
llm_calls = Counter('llm_calls_total', 'Total LLM API calls', ['model', 'status'])
agent_duration = Histogram('agent_execution_seconds', 'Agent execution time')

@app.middleware("http")
async def track_requests(request: Request, call_next):
    api_requests.labels(method=request.method, endpoint=request.url.path).inc()
    response = await call_next(request)
    return response
```

### 11.2 Logging

```python
import structlog

logger = structlog.get_logger()

logger.info("trend_discovered",
    trend_id=123,
    source="reddit",
    engagement=1523
)
```

### 11.3 Alerts

- API error rate > 5% → PagerDuty
- Database connection pool > 80% → Slack
- Celery queue depth > 1000 → Email
- LLM API costs > $50/day → Slack

---

## 12. Cost Optimization

### 12.1 Infrastructure Costs (MVP)

| Component | Monthly Cost |
|-----------|--------------|
| Kubernetes cluster (3 nodes) | $150-300 |
| PostgreSQL (managed) | $50-100 |
| Redis (managed) | $30-50 |
| Qdrant (self-hosted on K8s) | Included |
| CDN (Cloudflare) | $0-20 |
| **Total Infrastructure** | **$230-470** |

### 12.2 API Costs (MVP)

| Service | Monthly Cost |
|---------|--------------|
| OpenAI (optimized) | $60-120 |
| Data Sources (TGStat, Yandex) | $50-200 |
| **Total APIs** | **$110-320** |

### 12.3 Total MVP Cost

**$340-790/month** для 50-100 businesses
**$3,700-8,300/month** at scale (1000 businesses)

---

## Next Steps

1. ✅ Research complete (7 documents)
2. ✅ Architecture design (this document)
3. ⏳ Setup infrastructure (Docker Compose)
4. ⏳ Implement backend structure
5. ⏳ Integrate frontend
6. ⏳ Deploy MVP

📖 See implementation guides in [docs/guides/](guides/)
