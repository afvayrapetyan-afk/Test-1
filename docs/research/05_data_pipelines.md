# Research: Data Pipeline Best Practices

**Дата**: 2026-01-13
**Статус**: ✅ Completed

## Summary

Изучили best practices для построения scalable data pipelines: Celery + Redis для task queue, real-time scraping с rate limiting и deduplication, ETL patterns (batch vs streaming), и modern frameworks (Airflow, Prefect, Pathway). Для нашего проекта рекомендуем **hybrid approach**: streaming scraping → Celery processing → batch embedding generation.

---

## Key Findings

### 1. Celery + Redis: Task Queue Best Practices

**Позиционирование**:
Celery - distributed task queue для Python с async execution. Redis - message broker и result backend.

**Архитектура**:

```
┌────────────────────────────────────────────────┐
│         FastAPI Application                    │
│    - Publishes tasks to Celery                 │
└──────────────────┬─────────────────────────────┘
                   │ task.delay(args)
┌──────────────────┴─────────────────────────────┐
│         Redis (Message Broker)                 │
│    - Task queues (scraping, agents, analysis)  │
│    - Results (optional)                        │
└──────────────────┬─────────────────────────────┘
                   │ fetch tasks
┌──────────────────┴─────────────────────────────┐
│         Celery Workers                         │
│  ┌──────────────────────────────────────────┐  │
│  │   Worker 1 (scraping queue)              │  │
│  │   - Gevent pool (I/O bound)              │  │
│  │   - 1000 concurrent connections          │  │
│  └──────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────┐  │
│  │   Worker 2 (agents queue)                │  │
│  │   - Prefork pool (CPU bound)             │  │
│  │   - 4-8 processes                        │  │
│  └──────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────┐  │
│  │   Worker 3 (analysis queue)              │  │
│  │   - Prefork pool (batch processing)      │  │
│  │   - 2-4 processes                        │  │
│  └──────────────────────────────────────────┘  │
└────────────────────────────────────────────────┘
```

**Best Practices 2026**:

#### 1. Configuration & Serialization

```python
# backend/app/core/celery_config.py

from celery import Celery
from kombu import Exchange, Queue

app = Celery('business_portfolio')

# Broker & Backend
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/1'

# Serialization (Security: use JSON, not pickle)
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.timezone = 'UTC'
app.conf.enable_utc = True

# Message Compression (Performance)
app.conf.task_compression = 'gzip'
app.conf.result_compression = 'gzip'

# Task Routing (Multiple Queues)
app.conf.task_routes = {
    'app.tasks.scraping.*': {'queue': 'scraping'},
    'app.tasks.agents.*': {'queue': 'agents'},
    'app.tasks.analysis.*': {'queue': 'analysis'},
}

# Queues Definition
app.conf.task_queues = (
    Queue('scraping', Exchange('scraping'), routing_key='scraping',
          priority=10),  # High priority
    Queue('agents', Exchange('agents'), routing_key='agents',
          priority=5),   # Medium priority
    Queue('analysis', Exchange('analysis'), routing_key='analysis',
          priority=1),   # Low priority
)

# Worker Settings
app.conf.worker_prefetch_multiplier = 1  # Fair distribution
app.conf.worker_max_tasks_per_child = 1000  # Restart after N tasks
app.conf.task_acks_late = True  # Acknowledge after completion
app.conf.task_reject_on_worker_lost = True  # Retry if worker dies

# Retry Policy
app.conf.task_autoretry_for = (Exception,)
app.conf.task_retry_kwargs = {'max_retries': 3}
app.conf.task_default_retry_delay = 60  # 1 minute

# Result Expiry
app.conf.result_expires = 3600  # 1 hour (don't store forever)

# Visibility Timeout
app.conf.broker_transport_options = {
    'visibility_timeout': 3600,  # 1 hour
    'fanout_prefix': True,
    'fanout_patterns': True,
}
```

#### 2. Task Design (Atomic, Idempotent)

```python
# backend/app/tasks/scraping_tasks.py

from celery import Task
from app.core.celery_config import app
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class BaseTask(Task):
    """Base task with retry logic"""
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 3, 'countdown': 5}
    retry_backoff = True
    retry_backoff_max = 600  # 10 minutes
    retry_jitter = True

# Good: Atomic, small tasks
@app.task(base=BaseTask, bind=True, name='scraping.reddit')
def scrape_reddit_task(self, subreddit: str) -> Dict:
    """
    Scrape single subreddit (atomic operation)
    bind=True gives access to self (task instance)
    """
    try:
        logger.info(f"Scraping r/{subreddit}")

        # Actual scraping
        posts = scrape_reddit_subreddit(subreddit)

        # Return small payload (don't store large data in result)
        return {
            "subreddit": subreddit,
            "count": len(posts),
            "stored_ids": [p.id for p in posts]  # IDs only, not full data
        }

    except Exception as exc:
        # Custom retry logic
        logger.error(f"Error scraping r/{subreddit}: {exc}")
        raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))

# Fire-and-forget task (no result storage)
@app.task(name='scraping.process_trend', ignore_result=True)
def process_trend_task(trend_id: int):
    """
    Process trend without storing result
    ignore_result=True saves Redis memory
    """
    trend = get_trend(trend_id)
    process_and_store(trend)
    # No return needed

# Batch processing task
@app.task(name='analysis.batch_embeddings', bind=True)
def batch_embeddings_task(self, trend_ids: List[int]) -> Dict:
    """
    Generate embeddings in batches (efficient)
    """
    from app.services.embedding_service import EmbeddingService

    service = EmbeddingService()

    # Process in chunks
    chunk_size = 100
    total_processed = 0

    for i in range(0, len(trend_ids), chunk_size):
        chunk = trend_ids[i:i+chunk_size]

        # Update task progress (visible in Flower UI)
        self.update_state(
            state='PROGRESS',
            meta={'current': i, 'total': len(trend_ids)}
        )

        # Batch process
        service.batch_generate(chunk)
        total_processed += len(chunk)

    return {"processed": total_processed}

# Chord: Parallel + Callback
from celery import chord

def scrape_all_sources():
    """
    Scrape multiple sources in parallel, then aggregate
    """
    # Parallel tasks
    callback = aggregate_trends.s()

    header = [
        scrape_reddit_task.s('SideProject'),
        scrape_reddit_task.s('startups'),
        scrape_google_trends_task.s(),
        scrape_telegram_task.s(),
    ]

    # Execute: parallel tasks → callback
    result = chord(header)(callback)
    return result

@app.task(name='scraping.aggregate')
def aggregate_trends(results: List[Dict]) -> Dict:
    """
    Aggregate results from parallel scraping
    """
    total_count = sum(r['count'] for r in results)
    all_ids = [id for r in results for id in r['stored_ids']]

    # Deduplicate
    unique_ids = list(set(all_ids))

    return {
        "total": total_count,
        "unique": len(unique_ids),
        "sources": len(results)
    }
```

#### 3. Worker Configuration

```bash
# Start workers for different queues

# Scraping worker (I/O bound - gevent pool)
celery -A app.core.celery_config worker \
  -Q scraping \
  --pool=gevent \
  --concurrency=1000 \
  --loglevel=info \
  --hostname=scraping@%h

# Agents worker (CPU bound - prefork pool)
celery -A app.core.celery_config worker \
  -Q agents \
  --pool=prefork \
  --concurrency=4 \
  --loglevel=info \
  --hostname=agents@%h

# Analysis worker (batch processing)
celery -A app.core.celery_config worker \
  -Q analysis \
  --pool=prefork \
  --concurrency=2 \
  --loglevel=info \
  --hostname=analysis@%h

# Celery Beat (scheduler)
celery -A app.core.celery_config beat \
  --loglevel=info
```

#### 4. Periodic Tasks (Celery Beat)

```python
# backend/app/core/celery_config.py

from celery.schedules import crontab

app.conf.beat_schedule = {
    # Scrape trends every hour
    'scrape-trends-hourly': {
        'task': 'scraping.scrape_all_trends',
        'schedule': crontab(minute=0),  # Every hour at :00
    },

    # Generate embeddings every 2 hours
    'batch-embeddings': {
        'task': 'analysis.batch_embeddings_all',
        'schedule': crontab(minute=0, hour='*/2'),  # Every 2 hours
    },

    # Cluster trends daily
    'cluster-trends-daily': {
        'task': 'analysis.cluster_trends',
        'schedule': crontab(hour=3, minute=0),  # Daily at 3 AM
    },

    # Cleanup old data weekly
    'cleanup-weekly': {
        'task': 'maintenance.cleanup_old_data',
        'schedule': crontab(day_of_week=0, hour=2, minute=0),  # Sunday 2 AM
    },
}
```

#### 5. Monitoring (Flower)

```bash
# Start Flower UI for monitoring
celery -A app.core.celery_config flower \
  --port=5555 \
  --basic_auth=admin:password

# Access at http://localhost:5555
# - Task monitoring
# - Worker status
# - Queue depth
# - Task history
```

**Pros**:
- ✅ Mature ecosystem (10+ years)
- ✅ Python-native
- ✅ Flexible routing
- ✅ Multiple broker support
- ✅ Battle-tested at scale

**Cons**:
- ❌ Complex configuration
- ❌ Memory leaks if не configured properly
- ❌ Debugging может быть сложным

---

### 2. Real-Time Scraping Pipeline

**Challenges**:
1. Rate limiting (API limits)
2. Deduplication (same content from different sources)
3. Data validation
4. Error recovery

**Architecture (2026 Best Practices)**:

```
┌────────────────────────────────────────────────────┐
│         Scrapers (Celery Workers)                  │
│  - Reddit, Google Trends, Telegram, etc.           │
└───────────────────┬────────────────────────────────┘
                    │ Raw Data
┌───────────────────▼────────────────────────────────┐
│         Kafka (Streaming Platform)                 │
│  Topic: raw_trends                                 │
└───────────────────┬────────────────────────────────┘
                    │
        ┌───────────┴────────────┐
        │                        │
┌───────▼──────────┐    ┌────────▼─────────┐
│ Consumer Group 1 │    │ Consumer Group 2 │
│ (Validation)     │    │ (Deduplication)  │
└───────┬──────────┘    └────────┬─────────┘
        │                        │
        └───────────┬────────────┘
                    │ Validated & Unique
┌───────────────────▼────────────────────────────────┐
│         Processing Pipeline                        │
│  - Cleaning                                        │
│  - Enrichment                                      │
│  - Categorization                                  │
└───────────────────┬────────────────────────────────┘
                    │
        ┌───────────┴────────────┐
        │                        │
┌───────▼──────────┐    ┌────────▼─────────┐
│   PostgreSQL     │    │     Qdrant       │
│ (Structured)     │    │   (Vectors)      │
└──────────────────┘    └──────────────────┘
```

#### 2.1 Rate Limiting Strategies

```python
# backend/app/scrapers/base_scraper.py

from ratelimit import limits, sleep_and_retry
from functools import wraps
import redis
import time

class RateLimiter:
    """Redis-based distributed rate limiter"""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def limit(self, key: str, max_requests: int, window: int):
        """
        Decorator для rate limiting
        key: unique identifier (e.g., 'reddit_api')
        max_requests: max requests per window
        window: time window in seconds
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Redis key для tracking
                redis_key = f"rate_limit:{key}"

                # Increment counter
                pipe = self.redis.pipeline()
                pipe.incr(redis_key)
                pipe.expire(redis_key, window)
                current, _ = pipe.execute()

                if current > max_requests:
                    # Rate limit exceeded
                    wait_time = self.redis.ttl(redis_key)
                    raise RateLimitExceeded(f"Rate limit exceeded. Wait {wait_time}s")

                return func(*args, **kwargs)

            return wrapper
        return decorator

# Usage
rate_limiter = RateLimiter(redis_client)

class RedditScraper:
    @rate_limiter.limit(key='reddit_api', max_requests=60, window=60)
    def fetch_posts(self, subreddit: str):
        """Max 60 requests per minute"""
        # Scraping logic
        pass

# Adaptive rate limiting (sophisticated)
class AdaptiveRateLimiter:
    """
    Adjusts rate based on API responses
    If we get 429 (Too Many Requests), slow down
    """

    def __init__(self, initial_rate=10):
        self.current_rate = initial_rate
        self.min_rate = 1
        self.max_rate = 100

    def adjust(self, response_code: int):
        if response_code == 429:
            # Slow down (exponential backoff)
            self.current_rate = max(self.min_rate, self.current_rate * 0.5)
        elif response_code == 200:
            # Speed up (additive increase)
            self.current_rate = min(self.max_rate, self.current_rate + 1)

    def wait(self):
        time.sleep(1.0 / self.current_rate)
```

#### 2.2 Deduplication (Bloom Filters + Exact Matching)

```python
# backend/app/services/deduplication_service.py

from pybloom_live import BloomFilter
import hashlib
from typing import Optional
import redis

class DeduplicationService:
    """
    Two-level deduplication:
    1. Bloom filter (fast, probabilistic)
    2. Redis set (exact, for recent items)
    """

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

        # Bloom filter for 1M items, 0.1% false positive rate
        self.bloom = BloomFilter(capacity=1_000_000, error_rate=0.001)

        # Redis set для exact matching (last 24h)
        self.recent_key = "trends:recent:hashes"
        self.ttl = 86400  # 24 hours

    def hash_content(self, content: dict) -> str:
        """Generate content hash"""
        # Normalize content
        text = f"{content.get('title', '')}{content.get('url', '')}"
        text = text.lower().strip()

        return hashlib.sha256(text.encode()).hexdigest()

    def is_duplicate(self, content: dict) -> bool:
        """
        Check if content is duplicate
        Returns True if likely duplicate
        """
        content_hash = self.hash_content(content)

        # Level 1: Bloom filter (fast check)
        if content_hash not in self.bloom:
            # Definitely not seen before
            self.bloom.add(content_hash)
            self.redis.sadd(self.recent_key, content_hash)
            self.redis.expire(self.recent_key, self.ttl)
            return False

        # Level 2: Exact check in Redis
        if self.redis.sismember(self.recent_key, content_hash):
            # Confirmed duplicate
            return True

        # Bloom filter false positive
        self.redis.sadd(self.recent_key, content_hash)
        self.redis.expire(self.recent_key, self.ttl)
        return False

    def merge_duplicates(self, existing: dict, new: dict) -> dict:
        """
        Smart merging of duplicate content
        Keep higher engagement metrics
        """
        return {
            "title": existing["title"],
            "url": existing["url"],
            "engagement": max(
                existing.get("engagement", 0),
                new.get("engagement", 0)
            ),
            "sources": list(set(
                existing.get("sources", []) + new.get("sources", [])
            )),
            "first_seen": existing.get("first_seen"),
            "last_seen": new.get("timestamp")
        }

# Usage in scraping task
@app.task(name='scraping.process_scraped_data')
def process_scraped_data(data: dict):
    dedup_service = DeduplicationService(redis_client)

    if dedup_service.is_duplicate(data):
        # Update existing record
        existing = get_existing_trend(data)
        merged = dedup_service.merge_duplicates(existing, data)
        update_trend(merged)
    else:
        # New trend
        create_trend(data)
```

#### 2.3 Data Validation (Pydantic + Great Expectations)

```python
# backend/app/models/trend_schemas.py

from pydantic import BaseModel, HttpUrl, Field, validator
from datetime import datetime
from typing import List, Optional

class ScrapedTrend(BaseModel):
    """Validated trend data"""

    title: str = Field(..., min_length=5, max_length=500)
    url: HttpUrl
    source: str = Field(..., regex='^(reddit|google_trends|telegram|vk)$')
    engagement_score: int = Field(ge=0, le=1000000)
    timestamp: datetime
    category: Optional[str] = Field(None, max_length=50)
    tags: List[str] = Field(default_factory=list, max_items=10)

    @validator('title')
    def title_not_spam(cls, v):
        """Check for spam patterns"""
        spam_keywords = ['viagra', 'casino', 'porn']
        if any(keyword in v.lower() for keyword in spam_keywords):
            raise ValueError('Spam detected')
        return v

    @validator('tags')
    def tags_normalized(cls, v):
        """Normalize tags"""
        return [tag.lower().strip() for tag in v if tag]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Usage
def validate_scraped_data(raw_data: dict) -> ScrapedTrend:
    """Validate and clean scraped data"""
    try:
        trend = ScrapedTrend(**raw_data)
        return trend
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        raise

# Great Expectations (Advanced validation)
import great_expectations as gx

context = gx.get_context()

# Define expectations
suite = context.add_or_update_expectation_suite("trends_suite")

# Add expectations
suite.add_expectation(
    gx.core.ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "title"}
    )
)

suite.add_expectation(
    gx.core.ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_between",
        kwargs={"column": "engagement_score", "min_value": 0, "max_value": 1000000}
    )
)

# Validate batch
def validate_batch(df: pd.DataFrame):
    """Validate batch of trends with Great Expectations"""
    validator = context.get_validator(
        batch_request=df,
        expectation_suite_name="trends_suite"
    )

    results = validator.validate()

    if not results.success:
        logger.warning(f"Validation failures: {results}")

    return results
```

---

### 3. ETL Pipeline Patterns

**Batch vs Streaming vs Hybrid**

| Pattern | Use Case | Tools | Latency |
|---------|----------|-------|---------|
| **Batch** | Historical analysis, reports | Airflow, Luigi | Hours/Days |
| **Streaming** | Real-time dashboards, alerts | Kafka, Flink | Seconds |
| **Hybrid** | Fresh data + historical context | Airflow + Kafka | Minutes |

#### 3.1 Batch Processing (Airflow)

```python
# dags/trend_analysis_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_trend_analysis',
    default_args=default_args,
    description='Daily batch processing of trends',
    schedule_interval='0 2 * * *',  # 2 AM daily
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
) as dag:

    # Task 1: Extract trends from DB
    extract = PythonOperator(
        task_id='extract_trends',
        python_callable=extract_trends_from_db,
        op_kwargs={'lookback_days': 1}
    )

    # Task 2: Clean and deduplicate
    clean = PythonOperator(
        task_id='clean_data',
        python_callable=clean_and_deduplicate
    )

    # Task 3: Enrich with external data
    enrich = PythonOperator(
        task_id='enrich_data',
        python_callable=enrich_with_market_data
    )

    # Task 4: Generate embeddings (batch)
    embeddings = PythonOperator(
        task_id='generate_embeddings',
        python_callable=batch_generate_embeddings,
        pool='embedding_pool',  # Limit concurrency
        execution_timeout=timedelta(hours=2)
    )

    # Task 5: Cluster trends
    cluster = PythonOperator(
        task_id='cluster_trends',
        python_callable=cluster_with_dbscan
    )

    # Task 6: Store results
    store = PythonOperator(
        task_id='store_results',
        python_callable=store_to_qdrant
    )

    # Dependencies
    extract >> clean >> enrich >> embeddings >> cluster >> store
```

#### 3.2 Streaming Processing (Kafka + Consumer Groups)

```python
# backend/app/streaming/trend_consumer.py

from kafka import KafkaConsumer, KafkaProducer
from typing import Dict
import json

class TrendStreamProcessor:
    """Process trends from Kafka stream"""

    def __init__(self):
        # Consumer for raw trends
        self.consumer = KafkaConsumer(
            'raw_trends',
            bootstrap_servers=['localhost:9092'],
            group_id='trend_processors',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True,
            max_poll_records=100  # Batch size
        )

        # Producer for processed trends
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def process_message(self, trend: Dict) -> Dict:
        """Process single trend"""
        # Validate
        validated = validate_scraped_data(trend)

        # Deduplicate
        if dedup_service.is_duplicate(validated.dict()):
            return None

        # Enrich
        enriched = enrich_trend(validated)

        return enriched.dict()

    def run(self):
        """Main processing loop"""
        for message in self.consumer:
            trend = message.value

            try:
                # Process
                processed = self.process_message(trend)

                if processed:
                    # Send to processed topic
                    self.producer.send('processed_trends', value=processed)

                    # Store in DB (async)
                    store_trend_task.delay(processed)

            except Exception as e:
                logger.error(f"Error processing trend: {e}")
                # Send to DLQ (Dead Letter Queue)
                self.producer.send('trends_dlq', value={
                    'original': trend,
                    'error': str(e)
                })

# Run consumer
if __name__ == '__main__':
    processor = TrendStreamProcessor()
    processor.run()
```

#### 3.3 Hybrid Approach (Recommended)

```python
# backend/app/pipeline/hybrid_pipeline.py

class HybridTrendPipeline:
    """
    Hybrid pipeline:
    - Streaming: Real-time scraping → Kafka → Processing
    - Batch: Hourly embedding generation, daily clustering
    """

    def __init__(self):
        self.kafka_producer = KafkaProducer(...)
        self.dedup_service = DeduplicationService(redis_client)

    # Real-time ingestion
    async def ingest_trend(self, trend: dict):
        """
        Real-time: scrape → validate → dedupe → Kafka
        """
        # Validate immediately
        validated = validate_scraped_data(trend)

        # Quick deduplication (Bloom filter)
        if self.dedup_service.is_duplicate(validated.dict()):
            logger.info(f"Duplicate: {validated.title}")
            return

        # Send to Kafka for async processing
        self.kafka_producer.send('raw_trends', value=validated.dict())

    # Batch processing (Celery + Airflow)
    def schedule_batch_jobs(self):
        """
        Batch jobs via Celery Beat:
        - Every 2 hours: Generate embeddings for new trends
        - Every 6 hours: Update trend scores
        - Daily: Cluster all trends
        """
        pass

# Integration with scraper
@app.task(name='scraping.reddit_realtime')
def scrape_reddit_realtime():
    """Real-time scraping task"""
    pipeline = HybridTrendPipeline()

    scraper = RedditScraper()
    posts = scraper.fetch_new_posts(limit=100)

    for post in posts:
        # Send to pipeline (async)
        asyncio.run(pipeline.ingest_trend(post))
```

---

## Python ETL Tools Comparison (2026)

| Tool | Type | Best For | Learning Curve | Performance |
|------|------|----------|----------------|-------------|
| **Apache Airflow** | Orchestration | Complex DAGs, batch | Medium | ⭐⭐⭐⭐ |
| **Prefect** | Orchestration | Pythonic workflows | Easy | ⭐⭐⭐⭐ |
| **Dagster** | Orchestration | Data quality focus | Medium | ⭐⭐⭐⭐ |
| **Luigi** | Orchestration | Dependency management | Easy | ⭐⭐⭐ |
| **PySpark** | Processing | Big data, streaming | Hard | ⭐⭐⭐⭐⭐ |
| **Pandas** | Processing | Small/medium data | Easy | ⭐⭐⭐ |
| **Polars** | Processing | High-performance | Easy | ⭐⭐⭐⭐⭐ |
| **Pathway** | Streaming | Real-time AI pipelines | Medium | ⭐⭐⭐⭐ |

---

## Recommendation для нашего проекта

### ✅ Hybrid Architecture

**Layer 1: Real-Time Ingestion**
- **Scrapers** (Celery workers) → **Kafka** (raw_trends topic)
- High throughput, low latency
- Handles 1000+ trends/hour

**Layer 2: Stream Processing**
- **Kafka Consumer Groups**:
  - Group 1: Validation & cleaning
  - Group 2: Deduplication
  - Group 3: Storage (PostgreSQL + cache)
- Sub-second processing

**Layer 3: Batch Processing**
- **Celery Beat + Workers**:
  - Hourly: Batch embedding generation (OpenAI API)
  - Every 6h: Trend scoring & ranking
  - Daily: Clustering (DBSCAN)
- Cost-effective (batch API calls)

**Layer 4: Orchestration** (optional)
- **Airflow** для complex workflows
- **Prefect** для modern Python-first approach

### Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│  Scrapers (Celery - Gevent Pool)                    │
│  - Reddit, Google Trends, Telegram, VK              │
│  - 1000 concurrent connections                      │
│  - Rate limiting per source                         │
└────────────┬────────────────────────────────────────┘
             │ ~100-500 trends/hour
             ▼
┌─────────────────────────────────────────────────────┐
│  Kafka Topic: raw_trends                            │
│  - Partitions: 4                                    │
│  - Replication: 2                                   │
│  - Retention: 24h                                   │
└─┬───────────────────┬───────────────────┬───────────┘
  │                   │                   │
  ▼                   ▼                   ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Consumer    │ │ Consumer    │ │ Consumer    │
│ Group 1     │ │ Group 2     │ │ Group 3     │
│ (Validate)  │ │ (Dedupe)    │ │ (Store)     │
└─────────────┘ └─────────────┘ └─────────────┘
                                       │
                      ┌────────────────┴────────────────┐
                      ▼                                 ▼
              ┌───────────────┐               ┌──────────────┐
              │  PostgreSQL   │               │  Redis Cache │
              │  (Structured) │               │  (Recent)    │
              └───────┬───────┘               └──────────────┘
                      │
                      │ Celery Beat triggers
                      ▼
              ┌───────────────────────────┐
              │  Batch Jobs (Celery)      │
              │  - Embeddings (2h)        │
              │  - Scoring (6h)           │
              │  - Clustering (24h)       │
              └───────┬───────────────────┘
                      │
                      ▼
              ┌───────────────┐
              │    Qdrant     │
              │   (Vectors)   │
              └───────────────┘
```

### Cost Estimate

**Infrastructure**:
- Kafka cluster (3 brokers): $150-300/month
- Redis (managed): $50-100/month
- Celery workers (5 instances): Included in K8s
- **Total**: ~$200-400/month

**API Costs**:
- Scraping: Free (except TGStat $50-200/mo)
- Embeddings: $100-200/month (batch processing)
- **Total**: ~$150-400/month

**Combined**: $350-800/month для data pipeline

---

## Best Practices Summary

### 1. Task Queue (Celery)
- ✅ JSON serialization (security)
- ✅ Multiple queues (priority)
- ✅ Atomic tasks
- ✅ Retry with exponential backoff
- ✅ Message compression
- ✅ Worker prefetch = 1

### 2. Scraping
- ✅ Adaptive rate limiting
- ✅ Distributed rate limiting (Redis)
- ✅ Multi-level caching
- ✅ Respectful delays
- ✅ User-agent rotation

### 3. Deduplication
- ✅ Bloom filters (fast check)
- ✅ Redis sets (exact match)
- ✅ Content hashing (SHA-256)
- ✅ Smart merging (keep best data)

### 4. Data Validation
- ✅ Pydantic schemas
- ✅ Great Expectations
- ✅ Fail fast
- ✅ Dead letter queue

### 5. Monitoring
- ✅ Flower UI (Celery)
- ✅ Prometheus metrics
- ✅ Grafana dashboards
- ✅ Alerting (queue depth, error rate)

---

## Implementation Roadmap

### Week 1: Foundation
1. Setup Celery + Redis
2. Create task queues (scraping, agents, analysis)
3. Implement base scrapers
4. Test rate limiting

### Week 2: Streaming
1. Setup Kafka cluster
2. Implement consumer groups
3. Add deduplication service
4. Test throughput

### Week 3: Batch Processing
1. Setup Celery Beat
2. Implement periodic tasks
3. Batch embedding generation
4. Clustering jobs

### Week 4: Monitoring
1. Deploy Flower UI
2. Add Prometheus metrics
3. Create Grafana dashboards
4. Setup alerts

---

## Resources

### Documentation
- [Celery Documentation](https://docs.celeryq.dev/)
- [Kafka Python Client](https://kafka-python.readthedocs.io/)
- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [Prefect Docs](https://docs.prefect.io/)
- [Great Expectations](https://docs.greatexpectations.io/)

### Tutorials
- [Implementing Task Queues with Celery and Redis](https://blog.naveenpn.com/implementing-task-queues-in-python-using-celery-and-redis-scalable-background-jobs)
- [Building a Job Queue in Python with Celery](https://oneuptime.com/blog/post/2025-01-06-python-celery-redis-job-queue/view)
- [Real-Time Web Scraping with Kafka](https://www.confluent.io/blog/real-time-web-scraping/)

### Best Practices
- [Celery Best Practices](https://reintech.io/blog/combining-celery-redis-caching-task-queuing)
- [ETL Pipeline Architecture](https://www.mage.ai/blog/etl-pipeline-architecture-101-building-scalable-data-pipelines-with-python-sql-cloud)
- [Scalable Web Data Extraction](https://forage.ai/blog/scalable-web-data-extraction-pipeline/)

---

**Sources:**
- [Implementing Task Queues in Python Using Celery and Redis](https://blog.naveenpn.com/implementing-task-queues-in-python-using-celery-and-redis-scalable-background-jobs)
- [How to Build a Job Queue in Python with Celery and Redis](https://oneuptime.com/blog/post/2025-01-06-python-celery-redis-job-queue/view)
- [Celery and Redis: Combining Caching with Task Queuing](https://reintech.io/blog/combining-celery-redis-caching-task-queuing)
- [Zero to Production Scraping Pipeline](https://scrapegraphai.com/blog/zero-to-production-scraping-pipeline)
- [Reworkd Scales Real-Time Web Scraping With Data Streaming](https://www.confluent.io/blog/real-time-web-scraping/)
- [How Enterprise Web Data Extraction Systems Scale Reliably](https://forage.ai/blog/scalable-web-data-extraction-pipeline/)
- [ETL Pipeline Architecture 101](https://www.mage.ai/blog/etl-pipeline-architecture-101-building-scalable-data-pipelines-with-python-sql-cloud)
- [How to Build an ETL Pipeline in Python](https://airbyte.com/data-engineering-resources/python-etl)
- [Top Python ETL Tools for Data Engineering](https://www.kdnuggets.com/top-7-python-etl-tools-for-data-engineering)
