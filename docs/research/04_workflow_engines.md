# Research: Workflow Orchestration Engines

**Дата**: 2026-01-13
**Статус**: ✅ Completed

## Summary

Изучили четыре подхода к workflow orchestration: n8n (no-code automation с AI), Temporal (durable execution для microservices), Apache Airflow (batch data pipelines), и специализированные AI agent frameworks (LangGraph, CrewAI). Для нашего проекта рекомендуем **гибридный подход**: Temporal для durable state + LangGraph для AI agent orchestration.

---

## Key Findings

### 1. n8n: AI-Powered Workflow Automation

**Позиционирование**:
Fair-code workflow automation platform с native AI capabilities. Комбинирует visual building с custom code, 400+ готовых интеграций.

**Архитектура**:

```
┌────────────────────────────────────────────┐
│         n8n Frontend (Vue.js)              │
│    Visual Workflow Builder • Monitoring    │
└──────────────────┬─────────────────────────┘
                   │ REST API / WebSocket
┌──────────────────┴─────────────────────────┐
│         n8n Backend (Node.js)              │
│  ┌──────────────────────────────────────┐  │
│  │   Workflow Engine                    │  │
│  │   - Sequential/Parallel Execution    │  │
│  │   - Error Handling                   │  │
│  │   - Webhooks                         │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │   Queue Mode (Bull.js)               │  │
│  │   - Workers                          │  │
│  │   - Main Instance                    │  │
│  └──────────────────────────────────────┘  │
└──────────────────┬─────────────────────────┘
                   │
┌──────────────────┴─────────────────────────┐
│    PostgreSQL (metadata) + Redis (queue)   │
└────────────────────────────────────────────┘
```

**Ключевые Характеристики**:

1. **Performance**
   - **Throughput**: 220 workflow executions/second на single instance
   - **Queue Mode**: Multiple workers для horizontal scaling
   - **Low Latency**: Sub-second для простых workflows

2. **AI Capabilities (2026)**
   - Native AI nodes (OpenAI, Anthropic, HuggingFace)
   - AI Agent templates
   - Vector store integrations
   - Semantic search nodes

3. **Integration Ecosystem**
   - 400+ pre-built nodes
   - Custom node creation (TypeScript)
   - API-based connectors
   - Database connectors (PostgreSQL, MongoDB, Redis)

4. **Deployment Options**
   - **Self-Hosted**: Docker, Docker Compose, Kubernetes
   - **Cloud**: n8n Cloud (managed)
   - **Queue Mode**: Scalable architecture с workers

**Self-Hosting Best Practices**:

```yaml
# docker-compose.yml для n8n
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your_password
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=n8n
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
      - N8N_ENCRYPTION_KEY=your_encryption_key
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres
      - redis

  n8n-worker:
    image: n8nio/n8n:latest
    restart: always
    command: worker
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
    depends_on:
      - postgres
      - redis
    deploy:
      replicas: 3  # Horizontal scaling

  postgres:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=n8n
      - POSTGRES_DB=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data

volumes:
  n8n_data:
  postgres_data:
  redis_data:
```

**Pricing (Self-Hosted)**:
- Open-source: Free (Fair-code license)
- Infrastructure cost: ~$50-200/month (depending on scale)
- No per-execution fees

**Pricing (Cloud)**:
- Starter: $20/month (5000 executions)
- Pro: $50/month (10000 executions)
- Enterprise: Custom pricing

**Pros**:
- ✅ Visual workflow builder (non-technical users)
- ✅ 400+ integrations out of the box
- ✅ Native AI capabilities
- ✅ Self-hosted option
- ✅ Active community

**Cons**:
- ❌ Node.js based (не Python)
- ❌ Не подходит для complex state management
- ❌ Limited для long-running workflows (hours/days)
- ❌ Не предназначен для code-heavy workflows

**Use Cases**:
- API integrations
- Data synchronization
- Notification workflows
- Simple AI agent chains
- ETL для простых данных

---

### 2. Temporal: Durable Execution Platform

**Позиционирование**:
Workflow orchestration platform для reliability в microservices и business processes. Evolved from Uber's Cadence, uses event sourcing для state tracking.

**Архитектура**:

```
┌────────────────────────────────────────────┐
│         Application Code (Workers)         │
│    Python/Go/Java/TypeScript SDK           │
└──────────────────┬─────────────────────────┘
                   │ gRPC
┌──────────────────┴─────────────────────────┐
│         Temporal Server Cluster            │
│  ┌──────────────────────────────────────┐  │
│  │   Frontend Service                   │  │
│  │   - API Gateway                      │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │   History Service                    │  │
│  │   - Event Sourcing                   │  │
│  │   - State Management                 │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │   Matching Service                   │  │
│  │   - Task Queue Management            │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │   Worker Service                     │  │
│  │   - Background Processing            │  │
│  └──────────────────────────────────────┘  │
└──────────────────┬─────────────────────────┘
                   │
┌──────────────────┴─────────────────────────┐
│   Persistence (PostgreSQL/Cassandra)       │
│   Event History • Workflow State           │
└────────────────────────────────────────────┘
```

**Ключевые Характеристики**:

1. **Durable Execution**
   - Workflows survive process crashes
   - Automatic retry с exponential backoff
   - Event sourcing для full auditability
   - Deterministic replay для recovery

2. **State Management**
   - Long-running workflows (days, months, years)
   - Persistent state across restarts
   - Complex compensation logic
   - Child workflows и activities

3. **Scalability**
   - Horizontal scaling (add more workers)
   - Multi-region support
   - Handles millions of workflows
   - Low latency (10-100ms для activity start)

4. **Developer Experience**
   - Code-first approach (Python, Go, Java, TypeScript)
   - Local development environment
   - Testing framework
   - Strong typing

**Python SDK Example**:

```python
from datetime import timedelta
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker

# Define activity (single unit of work)
@activity.defn
async def scrape_trends(source: str) -> dict:
    """Scrape trends from a data source"""
    # Actual scraping logic
    trends = await scrape_data(source)
    return {"source": source, "trends": trends}

@activity.defn
async def analyze_trends(trends: list) -> list:
    """Analyze trends with AI"""
    # AI analysis
    ideas = await ai_analysis(trends)
    return ideas

# Define workflow (orchestrates activities)
@workflow.defn
class BusinessCreationWorkflow:
    @workflow.run
    async def run(self, business_id: str) -> dict:
        # Step 1: Discover trends (with retry)
        trends = await workflow.execute_activity(
            scrape_trends,
            args=["reddit"],
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy={"maximum_attempts": 3}
        )

        # Step 2: Analyze ideas
        ideas = await workflow.execute_activity(
            analyze_trends,
            args=[trends],
            start_to_close_timeout=timedelta(minutes=10)
        )

        # Step 3: Wait for approval (can wait days/weeks)
        approval = await workflow.wait_condition(
            lambda: self.is_approved,
            timeout=timedelta(days=7)
        )

        if not approval:
            return {"status": "timeout"}

        # Step 4: Deploy business
        deployment = await workflow.execute_activity(
            deploy_business,
            args=[ideas[0]],
            start_to_close_timeout=timedelta(hours=1)
        )

        return {"status": "success", "deployment": deployment}

    # Signal handler (external events)
    @workflow.signal
    async def approve(self):
        self.is_approved = True

# Worker setup
async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="business-creation",
        workflows=[BusinessCreationWorkflow],
        activities=[scrape_trends, analyze_trends, deploy_business]
    )

    await worker.run()

# Start workflow
async def start_workflow():
    client = await Client.connect("localhost:7233")

    handle = await client.start_workflow(
        BusinessCreationWorkflow.run,
        args=["business_123"],
        id="business-123-workflow",
        task_queue="business-creation"
    )

    result = await handle.result()
    print(result)
```

**Pricing**:
- **Open-Source**: Free (MIT license)
- **Self-Hosted**: Infrastructure cost only (~$200-500/month)
- **Temporal Cloud**: $200-2000+/month (based on actions)

**Pros**:
- ✅ Durable state (survives crashes)
- ✅ Long-running workflows (days/months)
- ✅ Excellent error handling
- ✅ Code-first (Python SDK)
- ✅ Strong consistency guarantees
- ✅ Built for microservices

**Cons**:
- ❌ Steep learning curve
- ❌ Complex setup (requires cluster)
- ❌ Overhead для simple tasks
- ❌ Not designed for batch data processing

**Use Cases**:
- Microservices orchestration
- AI agent workflows (long-running)
- Business process automation
- Saga patterns (distributed transactions)
- E-commerce order fulfillment
- Customer onboarding flows

---

### 3. Apache Airflow: Data Pipeline Orchestration

**Позиционирование**:
Veteran workflow orchestration для data engineering. Создан в Airbnb (2014), open-source с 2015. Scheduling DAGs (Directed Acyclic Graphs).

**Архитектура**:

```
┌────────────────────────────────────────────┐
│         Airflow Web UI (Flask)             │
│    DAG Visualization • Monitoring          │
└──────────────────┬─────────────────────────┘
                   │
┌──────────────────┴─────────────────────────┐
│         Airflow Scheduler                  │
│    - Monitors DAGs                         │
│    - Triggers Task Instances               │
└──────────────────┬─────────────────────────┘
                   │
┌──────────────────┴─────────────────────────┐
│         Executor (Celery/K8s)              │
│    - Distributes Tasks to Workers          │
└──────────────────┬─────────────────────────┘
                   │
┌──────────────────┴─────────────────────────┐
│         Workers (Task Execution)           │
│    - Python Operators                      │
│    - Sensor Operators                      │
└──────────────────┬─────────────────────────┘
                   │
┌──────────────────┴─────────────────────────┐
│   Metadata DB (PostgreSQL)                 │
│   Task State • DAG Runs • Logs             │
└────────────────────────────────────────────┘
```

**Ключевые Характеристики**:

1. **Scheduling**
   - Cron-based scheduling
   - Time-based triggers
   - External triggers
   - Backfilling для historical runs

2. **DAG Model**
   - Tasks with dependencies
   - Retry logic
   - SLA monitoring
   - Dynamic DAG generation

3. **Operators Library**
   - 200+ built-in operators
   - Python, Bash, SQL operators
   - Cloud providers (AWS, GCP, Azure)
   - Custom operators

4. **Monitoring**
   - Web UI для visualization
   - Gantt charts
   - Task duration metrics
   - Alerting (email, Slack)

**Python DAG Example**:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

# Define DAG
with DAG(
    'trend_discovery_pipeline',
    default_args=default_args,
    description='Daily trend discovery and analysis',
    schedule_interval='0 */6 * * *',  # Every 6 hours
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['trends', 'data-pipeline']
) as dag:

    # Task 1: Scrape Reddit
    scrape_reddit = PythonOperator(
        task_id='scrape_reddit',
        python_callable=scrape_reddit_trends,
        op_kwargs={'subreddits': ['SideProject', 'startups']}
    )

    # Task 2: Scrape Google Trends
    scrape_google = PythonOperator(
        task_id='scrape_google_trends',
        python_callable=scrape_google_trends
    )

    # Task 3: Process data
    process_data = PythonOperator(
        task_id='process_trends',
        python_callable=process_and_deduplicate,
        trigger_rule='all_success'  # Wait for all upstream
    )

    # Task 4: Generate embeddings
    generate_embeddings = PythonOperator(
        task_id='generate_embeddings',
        python_callable=create_embeddings,
        pool='embedding_pool',  # Limit concurrency
        execution_timeout=timedelta(minutes=30)
    )

    # Task 5: Store in Qdrant
    store_vectors = PythonOperator(
        task_id='store_in_qdrant',
        python_callable=store_in_vector_db
    )

    # Define dependencies
    [scrape_reddit, scrape_google] >> process_data >> generate_embeddings >> store_vectors
```

**Pricing**:
- **Open-Source**: Free (Apache license)
- **Self-Hosted**: Infrastructure only (~$100-300/month)
- **Managed** (Astronomer, Google Cloud Composer): $500-2000+/month

**Pros**:
- ✅ Mature ecosystem (10+ years)
- ✅ Rich operator library
- ✅ Excellent для batch processing
- ✅ Strong community
- ✅ Python-native
- ✅ Great monitoring UI

**Cons**:
- ❌ Не для real-time workflows
- ❌ Сложная архитектура
- ❌ Тяжелый (requires PostgreSQL, Celery, Redis)
- ❌ Не подходит для long-running stateful workflows
- ❌ Scheduler может быть bottleneck

**Use Cases**:
- ETL/ELT pipelines
- Data warehouse loading
- ML model training pipelines
- Report generation
- Scheduled batch jobs

---

### 4. AI Agent Orchestration Frameworks (2026)

**Тренд 2026**: Специализированные фреймворки для orchestration AI агентов. "Agent OS" platforms с human-on-the-loop.

#### 4.1 LangGraph (LangChain)

**Концепция**: Stateful graph-based workflows для AI agents.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class AgentState(TypedDict):
    trends: List[dict]
    ideas: List[dict]
    current_agent: str
    errors: List[str]

# Define nodes (agents)
def trend_scout_node(state: AgentState):
    """TrendScout agent"""
    trends = trend_scout_agent.run()
    return {**state, "trends": trends, "current_agent": "trend_scout"}

def idea_analyst_node(state: AgentState):
    """IdeaAnalyst agent"""
    ideas = idea_analyst_agent.run(state["trends"])
    return {**state, "ideas": ideas, "current_agent": "idea_analyst"}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("scout", trend_scout_node)
workflow.add_node("analyst", idea_analyst_node)

workflow.set_entry_point("scout")
workflow.add_edge("scout", "analyst")
workflow.add_edge("analyst", END)

app = workflow.compile()

# Run
result = app.invoke({
    "trends": [],
    "ideas": [],
    "current_agent": "",
    "errors": []
})
```

**Pros**:
- ✅ Python-native
- ✅ State management из коробки
- ✅ LangChain ecosystem integration
- ✅ Checkpointing support

**Cons**:
- ❌ Relatively new (2024)
- ❌ Не production-grade для scale
- ❌ Limited error recovery

#### 4.2 CrewAI (уже изучен в 01_ai_agents.md)

**Подход**: Role-based teams с autonomous collaboration.

**Pros**:
- ✅ Simple API
- ✅ Built-in delegation
- ✅ Enterprise-ready

**Cons**:
- ❌ Не для complex state management
- ❌ Limited workflow patterns

#### 4.3 AutoGen (Microsoft)

**Подход**: Multi-agent conversations.

**Pros**:
- ✅ Conversational workflows
- ✅ Human-in-the-loop
- ✅ Microsoft backing

**Cons**:
- ❌ Не для production orchestration
- ❌ Research-oriented

---

## Orchestration Patterns для AI Agents (2026 Best Practices)

### Pattern 1: Sequential Orchestration

**Use Case**: Step-by-step processing с clear dependencies.

```
Trend Discovery → Idea Analysis → Development → Marketing → Sales
```

**Best For**: Simple workflows, predictable flow.

### Pattern 2: Magentic Orchestration

**Use Case**: Open-ended problems, dynamic task list.

```
Manager Agent
    ├─> Specialist Agent 1 (research)
    ├─> Specialist Agent 2 (analysis)
    └─> Specialist Agent 3 (synthesis)
         └─> Feedback to Manager
              └─> New tasks generated
```

**Best For**: Complex problems requiring adaptation.

### Pattern 3: Human-in-the-Loop

**Critical 2026 Trend**: Human oversight для critical decisions.

```
Agent Execution → Checkpoint → Human Approval → Continue
```

**Implementation**:
- Temporal signals для approval
- n8n approval nodes
- Manual intervention dashboard

---

## Comparison Table

| Критерий | n8n | Temporal | Airflow | LangGraph |
|----------|-----|----------|---------|-----------|
| **Подход** | Visual + Code | Code-First | Code-First (DAGs) | Code-First (Graphs) |
| **State Management** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Long-Running** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| **Scheduling** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Error Recovery** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Scalability** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **AI Integration** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Learning Curve** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Maturity** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Cost (Self-Hosted)** | $50-200/mo | $200-500/mo | $100-300/mo | Minimal |
| **Python Support** | ❌ (Node.js) | ✅ | ✅ | ✅ |

---

## Temporal vs Airflow: Decision Matrix

**Choose Airflow if**:
- ✅ Building classic data pipelines (ETL/ELT)
- ✅ Need strict scheduling (cron-based)
- ✅ Batch processing на fixed intervals
- ✅ Want rich operator library
- ✅ Team familiar с data engineering

**Choose Temporal if**:
- ✅ Building microservices workflows
- ✅ Need long-running processes (days/months)
- ✅ Require durable state management
- ✅ Complex compensation logic
- ✅ AI agents с unpredictable duration
- ✅ Event-driven architecture

---

## Recommendation для нашего проекта

### ✅ Гибридный Подход: Temporal + LangGraph + (опционально) Airflow

**Почему гибрид**:

1. **Temporal** - для Business Workflow Orchestration
   - Управление жизненным циклом 1000+ бизнесов
   - Long-running workflows (trend discovery → deployment → sales)
   - Durable state (survive crashes)
   - Checkpointing для recovery
   - Human-in-the-loop (approval signals)

2. **LangGraph** - для AI Agent Coordination
   - Internal orchestration внутри каждого агента
   - State management для multi-step reasoning
   - Integration с LangChain tools
   - Checkpointing для agent state

3. **Airflow** (опционально) - для Batch Data Processing
   - Scheduled scraping (каждый час)
   - ETL для trend data
   - Batch embedding generation
   - Report generation

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│              Temporal Workflows                         │
│   ┌───────────────────────────────────────────────┐    │
│   │  Business Lifecycle Workflow                  │    │
│   │                                               │    │
│   │  1. Trend Discovery (Activity)                │    │
│   │     └─> Calls: Airflow DAG (scraping)        │    │
│   │                                               │    │
│   │  2. Idea Analysis (Activity)                  │    │
│   │     └─> Calls: IdeaAnalystAgent (LangGraph)  │    │
│   │                                               │    │
│   │  3. Wait for Approval (Signal)                │    │
│   │     └─> Human-in-the-loop                    │    │
│   │                                               │    │
│   │  4. Development (Activity)                    │    │
│   │     └─> Calls: DevAgent (LangGraph)          │    │
│   │                                               │    │
│   │  5. Marketing (Activity)                      │    │
│   │     └─> Calls: MarketingAgent (LangGraph)    │    │
│   │                                               │    │
│   │  6. Sales (Activity)                          │    │
│   │     └─> Calls: SalesAgent (LangGraph)        │    │
│   └───────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌────────────────┐  ┌──────────────────┐  ┌──────────────┐
│ Airflow        │  │  LangGraph       │  │ PostgreSQL   │
│ (Batch Jobs)   │  │  (Agent State)   │  │ (Persistent) │
└────────────────┘  └──────────────────┘  └──────────────┘
```

### Implementation Strategy

**Phase 1: Temporal Core (Week 3)**
```python
# backend/app/orchestrator/temporal_workflows.py

from temporalio import workflow, activity
from datetime import timedelta

@workflow.defn
class BusinessLifecycleWorkflow:
    def __init__(self):
        self.state = "initialized"
        self.approved = False

    @workflow.run
    async def run(self, business_id: str) -> dict:
        # Activity 1: Discover Trends (delegates to Airflow or direct scraping)
        trends = await workflow.execute_activity(
            discover_trends,
            start_to_close_timeout=timedelta(hours=2),
            retry_policy={"maximum_attempts": 3}
        )

        self.state = "trends_discovered"

        # Activity 2: Analyze Ideas (uses LangGraph agent)
        ideas = await workflow.execute_activity(
            analyze_ideas,
            args=[trends],
            start_to_close_timeout=timedelta(hours=1)
        )

        self.state = "ideas_analyzed"

        # Human approval (can wait days)
        await workflow.wait_condition(
            lambda: self.approved,
            timeout=timedelta(days=7)
        )

        if not self.approved:
            return {"status": "rejected"}

        # Activity 3: Develop MVP (LangGraph DevAgent)
        code = await workflow.execute_activity(
            develop_mvp,
            args=[ideas[0]],
            start_to_close_timeout=timedelta(hours=4)
        )

        self.state = "developed"

        # Activity 4: Marketing (LangGraph MarketingAgent)
        marketing = await workflow.execute_activity(
            create_marketing,
            args=[ideas[0]],
            start_to_close_timeout=timedelta(hours=2)
        )

        self.state = "marketing_ready"

        # Activity 5: Sales (LangGraph SalesAgent)
        sales = await workflow.execute_activity(
            setup_sales,
            args=[ideas[0]],
            start_to_close_timeout=timedelta(hours=1)
        )

        self.state = "live"

        return {
            "status": "success",
            "business_id": business_id,
            "state": self.state
        }

    @workflow.signal
    async def approve(self):
        """Signal from external system (human approval)"""
        self.approved = True

    @workflow.signal
    async def pause(self):
        """Pause workflow"""
        self.state = "paused"

    @workflow.query
    async def get_state(self) -> str:
        """Query current state"""
        return self.state
```

**Phase 2: LangGraph Agents (Week 4)**
```python
# backend/app/agents/idea_analyst_agent.py

from langgraph.graph import StateGraph, END
from typing import TypedDict

class AnalystState(TypedDict):
    trends: list
    research: dict
    scores: dict
    ideas: list

def research_node(state: AnalystState):
    """Research market for each trend"""
    # Use LLM to research
    research = llm_research(state["trends"])
    return {**state, "research": research}

def scoring_node(state: AnalystState):
    """Score ideas on 6 metrics"""
    scores = llm_scoring(state["research"])
    return {**state, "scores": scores}

def ranking_node(state: AnalystState):
    """Rank and select top ideas"""
    ideas = rank_ideas(state["scores"])
    return {**state, "ideas": ideas}

# Build agent workflow
analyst_workflow = StateGraph(AnalystState)
analyst_workflow.add_node("research", research_node)
analyst_workflow.add_node("scoring", scoring_node)
analyst_workflow.add_node("ranking", ranking_node)

analyst_workflow.set_entry_point("research")
analyst_workflow.add_edge("research", "scoring")
analyst_workflow.add_edge("scoring", "ranking")
analyst_workflow.add_edge("ranking", END)

analyst_app = analyst_workflow.compile()

# Use in Temporal activity
@activity.defn
async def analyze_ideas(trends: list) -> list:
    """Temporal activity that uses LangGraph agent"""
    result = analyst_app.invoke({
        "trends": trends,
        "research": {},
        "scores": {},
        "ideas": []
    })
    return result["ideas"]
```

**Phase 3: Airflow Integration (Week 5, optional)**
```python
# Airflow DAG для scheduled scraping
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(
    'hourly_trend_scraping',
    schedule_interval='0 * * * *',  # Every hour
    catchup=False
) as dag:

    scrape = PythonOperator(
        task_id='scrape_all_sources',
        python_callable=scrape_trends_multi_source
    )

    process = PythonOperator(
        task_id='process_and_store',
        python_callable=process_and_store_trends
    )

    scrape >> process
```

### Cost Analysis

**Temporal (self-hosted)**:
- Infrastructure: $200-500/month (Kubernetes cluster)
- PostgreSQL: $50-100/month
- **Total**: ~$250-600/month

**LangGraph**:
- Free (open-source)
- No additional infrastructure cost

**Airflow (optional)**:
- Infrastructure: $100-300/month
- **Total**: ~$100-300/month

**Combined Total**: $350-900/month для orchestration layer

---

## Best Practices для Production

### 1. Observability

**Temporal**:
- Built-in UI для workflow visualization
- Prometheus metrics
- Custom attributes для tracing

**LangGraph**:
- Checkpoints для debugging
- State visualization
- LangSmith integration

### 2. Error Handling

**Retry Strategies**:
```python
retry_policy = {
    "initial_interval": timedelta(seconds=1),
    "backoff_coefficient": 2.0,
    "maximum_interval": timedelta(minutes=10),
    "maximum_attempts": 5
}
```

**Circuit Breaker**:
- Stop retrying после N failures
- Fallback на alternative agent

### 3. Checkpointing

**Temporal**: Automatic event sourcing
**LangGraph**: Manual checkpoints

```python
# LangGraph checkpointing
from langgraph.checkpoint import MemorySaver

checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)

# Resume from checkpoint
result = app.invoke(
    state,
    config={"configurable": {"thread_id": "business-123"}}
)
```

### 4. Human-in-the-Loop

**Pattern**:
```python
# Temporal signal для approval
@workflow.signal
async def approve(self, approved: bool, comment: str):
    self.approval_status = approved
    self.approval_comment = comment

# Wait for approval
approved = await workflow.wait_condition(
    lambda: self.approval_status is not None,
    timeout=timedelta(days=7)
)
```

### 5. Monitoring & Alerting

**Metrics to Track**:
- Workflow success rate
- Average duration per stage
- Error rate by agent type
- Queue depth
- Worker utilization

**Alerts**:
- Workflow stuck > 24h
- Agent failure rate > 10%
- Queue depth > 1000

---

## Migration Path

### Week 1-2: Temporal Foundation
1. Setup Temporal cluster (Docker Compose → Kubernetes)
2. Implement BaseWorkflow class
3. Create first workflow (TrendDiscovery)
4. Test retry & recovery

### Week 3-4: LangGraph Integration
1. Convert existing agents to LangGraph
2. Add checkpointing
3. Integrate with Temporal activities
4. Test agent workflows

### Week 5-6: Airflow (if needed)
1. Setup Airflow для batch jobs
2. Create scraping DAGs
3. Trigger from Temporal
4. Monitor & optimize

---

## Resources

### Documentation
- [Temporal Documentation](https://docs.temporal.io/)
- [Temporal Python SDK](https://github.com/temporalio/sdk-python)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [n8n Documentation](https://docs.n8n.io/)

### Comparisons
- [Temporal vs Airflow](https://www.zenml.io/blog/temporal-vs-airflow)
- [Workflow Orchestration Platforms 2025](https://procycons.com/en/blogs/workflow-orchestration-platforms-comparison-2025/)

### Best Practices
- [AI Agent Orchestration Patterns - Azure](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Agentic AI Workflows with Temporal](https://intuitionlabs.ai/articles/agentic-ai-temporal-orchestration)
- [Deloitte: AI Agent Orchestration](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/ai-agent-orchestration.html)

### Tutorials
- [n8n Self-Hosting Guide](https://northflank.com/blog/how-to-self-host-n8n-setup-architecture-and-pricing-guide)
- [Temporal Getting Started](https://learn.temporal.io/getting_started/python/)
- [LangGraph Multi-Agent Tutorial](https://iterathon.tech/blog/ai-agent-orchestration-frameworks-2026)

---

## Next Steps

1. ✅ **Prototype с Temporal** - создать simple workflow
2. ⏳ **Integrate LangGraph** - convert один agent
3. ⏳ **Setup Monitoring** - Prometheus + Grafana
4. ⏳ **Test Recovery** - simulate failures
5. ⏳ **Evaluate Airflow** - decide if needed для batch jobs

---

**Sources:**
- [How to self-host n8n: Setup, architecture, and pricing guide (2026)](https://northflank.com/blog/how-to-self-host-n8n-setup-architecture-and-pricing-guide)
- [Temporal vs Airflow: Which Orchestrator Fits Your Workflows?](https://www.zenml.io/blog/temporal-vs-airflow)
- [Temporal vs Airflow: A Comparative Analysis](https://medium.com/@thinhda/temporal-vs-airflow-a-comparative-analysis-915d2954f592)
- [Comparing Top Workflow Engines: Camunda vs Apache Airflow vs Temporal](https://ngxptech.com/comparing-top-workflow-engines-camunda-vs-apache-airflow-vs-temporal/)
- [AI Agent Orchestration Patterns - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Agent Orchestration 2026: LangGraph, CrewAI & AutoGen Guide](https://iterathon.tech/blog/ai-agent-orchestration-frameworks-2026)
- [Agentic AI Workflows: Why Orchestration with Temporal is Key](https://intuitionlabs.ai/articles/agentic-ai-temporal-orchestration)
- [Unlocking exponential value with AI agent orchestration - Deloitte](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/ai-agent-orchestration.html)
