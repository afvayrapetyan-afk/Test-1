# Research: Scalable Architecture Patterns

**Дата**: 2026-01-13
**Статус**: ✅ Completed

## Summary

Изучили scalable architecture patterns для масштабирования Python applications: modular monolith vs microservices (2026 trend - consolidation back to monoliths), database sharding strategies (Citus, PgDog), multi-layer caching (local → Redis → CDN), и Kubernetes patterns. Для нашего проекта рекомендуем **modular monolith** для MVP с clear service boundaries для future migration.

---

## Key Findings

### 1. Monolith vs Microservices (2026 Perspective)

**Surprising Trend 2026**:
- **42% организаций** consolidating microservices back to monoliths
- Primary drivers: debugging complexity, operational overhead, network latency
- Emergence of sophisticated **modular monoliths**

#### 1.1 When to Choose Monolith

**Choose Monolith if**:
- ✅ Team < 10 engineers
- ✅ MVP/early stage product
- ✅ Shared data models
- ✅ Limited DevOps resources
- ✅ Faster time to market needed

**Benefits**:
- Simpler deployment (single unit)
- Easier debugging (single codebase)
- No network overhead between modules
- Shared database transactions
- Lower operational cost

**Example: Modular Monolith Structure**:

```
backend/
├── app/
│   ├── main.py                    # FastAPI app entry
│   │
│   ├── modules/                   # Service modules (clear boundaries)
│   │   ├── trends/                # TrendService
│   │   │   ├── __init__.py
│   │   │   ├── router.py          # API routes
│   │   │   ├── service.py         # Business logic
│   │   │   ├── repository.py      # Data access
│   │   │   └── schemas.py         # Pydantic models
│   │   │
│   │   ├── ideas/                 # IdeaService
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── agents/                # AgentService
│   │   │   └── ...
│   │   │
│   │   └── businesses/            # BusinessService
│   │       └── ...
│   │
│   ├── core/                      # Shared infrastructure
│   │   ├── database.py
│   │   ├── cache.py
│   │   ├── celery_config.py
│   │   └── config.py
│   │
│   └── shared/                    # Shared utilities
│       ├── utils.py
│       ├── exceptions.py
│       └── middleware.py
```

**Implementation**:

```python
# backend/app/main.py (Modular Monolith)

from fastapi import FastAPI
from app.modules.trends import router as trends_router
from app.modules.ideas import router as ideas_router
from app.modules.agents import router as agents_router
from app.modules.businesses import router as businesses_router
from app.core.config import settings

app = FastAPI(title="Business Portfolio Manager")

# Module routers (clear separation)
app.include_router(trends_router.router, prefix="/api/v1/trends", tags=["trends"])
app.include_router(ideas_router.router, prefix="/api/v1/ideas", tags=["ideas"])
app.include_router(agents_router.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(businesses_router.router, prefix="/api/v1/businesses", tags=["businesses"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Each module is self-contained but shares database & infrastructure
```

```python
# backend/app/modules/trends/service.py

from typing import List
from app.modules.trends.repository import TrendRepository
from app.modules.trends.schemas import TrendCreate, TrendOut
from app.core.cache import cache_service

class TrendService:
    """
    Business logic for trends
    Can be extracted to microservice later without changing interface
    """

    def __init__(self):
        self.repository = TrendRepository()

    async def get_trends(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[TrendOut]:
        """Get trends with caching"""

        # Cache key
        cache_key = f"trends:list:{skip}:{limit}"

        # Try cache first
        cached = await cache_service.get(cache_key)
        if cached:
            return cached

        # Fetch from DB
        trends = await self.repository.get_many(skip=skip, limit=limit)

        # Cache for 5 minutes
        await cache_service.set(cache_key, trends, ttl=300)

        return trends

    async def create_trend(self, trend_data: TrendCreate) -> TrendOut:
        """Create new trend"""
        trend = await self.repository.create(trend_data)

        # Invalidate cache
        await cache_service.delete_pattern("trends:list:*")

        return trend
```

#### 1.2 When to Choose Microservices

**Choose Microservices if**:
- ✅ Team > 20 engineers
- ✅ Need independent scaling per service
- ✅ Different tech stacks per service
- ✅ Strong DevOps culture
- ✅ Clear domain boundaries

**FastAPI Microservices Pattern**:

```
services/
├── trend-service/              # Independent service
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   └── models/
│   ├── Dockerfile
│   └── requirements.txt
│
├── idea-service/
│   └── ...
│
├── agent-service/
│   └── ...
│
└── business-service/
    └── ...
```

```python
# services/trend-service/app/main.py

from fastapi import FastAPI
from app.api import trends_router

app = FastAPI(title="Trend Service")

app.include_router(trends_router.router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"service": "trend-service", "status": "healthy"}

# Service communication via HTTP/gRPC
# Each service has its own database
```

**Service Communication**:

```python
# Inter-service communication (HTTP)
import httpx

class IdeaServiceClient:
    """Client for Idea Service"""

    def __init__(self):
        self.base_url = "http://idea-service:8000"

    async def analyze_trend(self, trend_id: int) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/analyze",
                json={"trend_id": trend_id}
            )
            return response.json()
```

**Pros**:
- Independent deployment
- Independent scaling
- Technology diversity
- Team autonomy

**Cons**:
- Complex deployment
- Network overhead
- Distributed debugging
- Data consistency challenges

---

### 2. Database Scaling Strategies

#### 2.1 Vertical Scaling (Easiest First Step)

**Approach**: Upgrade server resources (CPU, RAM, SSD)

```python
# PostgreSQL configuration for vertical scaling

# postgresql.conf optimizations
shared_buffers = 4GB            # 25% of RAM
effective_cache_size = 12GB     # 75% of RAM
maintenance_work_mem = 1GB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1          # For SSD
effective_io_concurrency = 200  # For SSD
work_mem = 128MB                # Per query operation
min_wal_size = 1GB
max_wal_size = 4GB
max_worker_processes = 8
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
```

**Cost**:
- Small (2 CPU, 8GB RAM): $50/month
- Medium (4 CPU, 16GB RAM): $150/month
- Large (8 CPU, 32GB RAM): $400/month

#### 2.2 Read Replicas

**Pattern**: Primary (write) + Replicas (read)

```python
# backend/app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

class DatabaseRouter:
    """Route reads to replicas, writes to primary"""

    def __init__(self):
        # Primary database (writes)
        self.primary_engine = create_engine(
            "postgresql://user:pass@primary:5432/db",
            pool_size=20,
            max_overflow=0
        )

        # Read replicas
        self.replica_engines = [
            create_engine("postgresql://user:pass@replica1:5432/db"),
            create_engine("postgresql://user:pass@replica2:5432/db"),
        ]

        self.primary_session = sessionmaker(bind=self.primary_engine)
        self.replica_sessions = [
            sessionmaker(bind=engine) for engine in self.replica_engines
        ]

    def get_write_session(self):
        """Get session for writes (primary)"""
        return self.primary_session()

    def get_read_session(self):
        """Get session for reads (random replica)"""
        session_maker = random.choice(self.replica_sessions)
        return session_maker()

# Usage
router = DatabaseRouter()

# Read operation
@app.get("/api/v1/trends")
async def get_trends():
    db = router.get_read_session()  # Use replica
    trends = db.query(Trend).all()
    return trends

# Write operation
@app.post("/api/v1/trends")
async def create_trend(trend: TrendCreate):
    db = router.get_write_session()  # Use primary
    new_trend = Trend(**trend.dict())
    db.add(new_trend)
    db.commit()
    return new_trend
```

**Benefits**:
- 3x read capacity (1 primary + 2 replicas)
- High availability (failover to replica)
- Geographic distribution

**Cost**: $150/month (primary) + $100/month × 2 (replicas) = $350/month

#### 2.3 Database Sharding

**When Needed**: >100M rows, >500GB database

**Sharding Strategies**:

| Strategy | Shard Key | Use Case | Pros | Cons |
|----------|-----------|----------|------|------|
| **Hash** | `hash(business_id)` | Even distribution | Balanced load | No range queries |
| **Range** | `business_id` ranges | Ordered data | Easy to add shards | Hotspots possible |
| **Geographic** | `region` | Multi-region app | Data locality | Uneven distribution |

**Implementation (Application-Level Sharding)**:

```python
# backend/app/core/sharding.py

import hashlib
from typing import List
from sqlalchemy import create_engine

class ShardManager:
    """Manage database shards"""

    def __init__(self, num_shards: int = 4):
        self.num_shards = num_shards
        self.shards = []

        # Create connections to shards
        for i in range(num_shards):
            engine = create_engine(
                f"postgresql://user:pass@shard{i}:5432/db",
                pool_size=10
            )
            self.shards.append(engine)

    def get_shard(self, business_id: int) -> int:
        """
        Determine which shard for business_id
        Hash-based sharding
        """
        # Hash business_id
        hash_value = int(hashlib.md5(str(business_id).encode()).hexdigest(), 16)

        # Modulo to get shard index
        shard_index = hash_value % self.num_shards

        return shard_index

    def get_shard_engine(self, business_id: int):
        """Get database engine for business"""
        shard_index = self.get_shard(business_id)
        return self.shards[shard_index]

# Usage
shard_manager = ShardManager(num_shards=4)

@app.get("/api/v1/businesses/{business_id}")
async def get_business(business_id: int):
    # Route to correct shard
    engine = shard_manager.get_shard_engine(business_id)

    with engine.connect() as conn:
        result = conn.execute(
            "SELECT * FROM businesses WHERE id = %s",
            (business_id,)
        )
        return result.fetchone()
```

**Citus Extension (Easier Sharding)**:

```sql
-- Setup Citus for distributed PostgreSQL
CREATE EXTENSION citus;

-- Distribute table across shards
SELECT create_distributed_table('businesses', 'business_id');

-- Citus handles sharding automatically
SELECT * FROM businesses WHERE business_id = 123;
```

**Benefits**:
- Linear scalability (add more shards)
- Handle billions of rows
- Independent shard maintenance

**Challenges**:
- Cross-shard queries expensive
- Rebalancing complexity
- Application logic complexity

---

### 3. Caching Strategies

#### 3.1 Multi-Layer Cache Architecture

```
┌─────────────────────────────────────────┐
│  Layer 1: Browser Cache (60s)           │
│  - Static assets                        │
│  - User preferences                     │
└──────────────────┬──────────────────────┘
                   │ Cache Miss
┌──────────────────▼──────────────────────┐
│  Layer 2: CDN (Cloudflare) (5min)       │
│  - Images, CSS, JS                      │
│  - API responses (public)               │
└──────────────────┬──────────────────────┘
                   │ Cache Miss
┌──────────────────▼──────────────────────┐
│  Layer 3: Application Cache (5min)      │
│  - In-memory (lru_cache)                │
│  - Process-local cache                  │
└──────────────────┬──────────────────────┘
                   │ Cache Miss
┌──────────────────▼──────────────────────┐
│  Layer 4: Redis (15min)                 │
│  - API responses                        │
│  - Session data                         │
│  - Aggregated data                      │
└──────────────────┬──────────────────────┘
                   │ Cache Miss
┌──────────────────▼──────────────────────┐
│  Layer 5: Database                      │
│  - PostgreSQL (source of truth)         │
└─────────────────────────────────────────┘
```

#### 3.2 Application-Level Cache (functools.lru_cache)

```python
# backend/app/core/cache.py

from functools import lru_cache
from typing import Dict, List
import asyncio

# Local in-memory cache (per-process)
@lru_cache(maxsize=1000)
def get_trend_categories() -> List[str]:
    """
    Expensive operation cached in memory
    Only recomputed if args change
    """
    # This is cached for lifetime of process
    return ["tech", "saas", "marketplace", "tool", "ai"]

# Async cache decorator
def async_lru_cache(maxsize=128):
    """LRU cache for async functions"""
    cache = {}
    cache_order = []

    def decorator(func):
        async def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)

            if key in cache:
                # Cache hit
                return cache[key]

            # Cache miss - compute
            result = await func(*args, **kwargs)

            # Store in cache
            cache[key] = result
            cache_order.append(key)

            # Evict oldest if over maxsize
            if len(cache_order) > maxsize:
                oldest = cache_order.pop(0)
                del cache[oldest]

            return result

        return wrapper
    return decorator

# Usage
@async_lru_cache(maxsize=100)
async def get_trend_stats(category: str) -> Dict:
    """Expensive aggregation cached"""
    # This runs only once per category until cache eviction
    stats = await aggregate_trend_stats(category)
    return stats
```

#### 3.3 Redis Cache (Distributed)

```python
# backend/app/core/redis_cache.py

import redis.asyncio as redis
import json
from typing import Optional, Any
import hashlib

class RedisCache:
    """Distributed cache with Redis"""

    def __init__(self):
        self.redis = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )

    async def get(self, key: str) -> Optional[Any]:
        """Get from cache"""
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = 900  # 15 minutes default
    ):
        """Set cache with TTL"""
        await self.redis.setex(
            key,
            ttl,
            json.dumps(value)
        )

    async def delete(self, key: str):
        """Invalidate cache"""
        await self.redis.delete(key)

    async def delete_pattern(self, pattern: str):
        """Delete keys matching pattern"""
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)

# Decorator for caching
def redis_cache(ttl: int = 900):
    """Cache function result in Redis"""
    cache = RedisCache()

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key from function + args
            key_data = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()

            # Try cache
            cached = await cache.get(cache_key)
            if cached is not None:
                return cached

            # Execute function
            result = await func(*args, **kwargs)

            # Cache result
            await cache.set(cache_key, result, ttl=ttl)

            return result

        return wrapper
    return decorator

# Usage
@redis_cache(ttl=300)  # 5 minutes
async def get_trending_ideas() -> List[Dict]:
    """Expensive query cached in Redis"""
    # This hits Redis first, DB only on cache miss
    ideas = await db.query(Idea).filter(
        Idea.score > 80
    ).order_by(Idea.created_at.desc()).limit(10).all()

    return [idea.dict() for idea in ideas]
```

#### 3.4 Cache Invalidation Strategies

```python
# backend/app/core/cache_invalidation.py

class CacheInvalidationService:
    """Smart cache invalidation"""

    def __init__(self):
        self.cache = RedisCache()

    async def invalidate_on_create(self, entity: str):
        """Invalidate list caches when new item created"""
        # Invalidate all list queries
        await self.cache.delete_pattern(f"{entity}:list:*")

        # Invalidate aggregations
        await self.cache.delete_pattern(f"{entity}:stats:*")

    async def invalidate_on_update(self, entity: str, entity_id: int):
        """Invalidate specific item + related caches"""
        # Invalidate single item cache
        await self.cache.delete(f"{entity}:{entity_id}")

        # Invalidate lists
        await self.cache.delete_pattern(f"{entity}:list:*")

    async def invalidate_on_delete(self, entity: str, entity_id: int):
        """Invalidate on delete"""
        await self.cache.delete(f"{entity}:{entity_id}")
        await self.cache.delete_pattern(f"{entity}:list:*")

# Usage
cache_invalidation = CacheInvalidationService()

@app.post("/api/v1/trends")
async def create_trend(trend: TrendCreate):
    # Create trend
    new_trend = await trend_service.create(trend)

    # Invalidate caches
    await cache_invalidation.invalidate_on_create("trends")

    return new_trend
```

#### 3.5 Cache Stampede Prevention

```python
# backend/app/core/cache_stampede.py

import asyncio
from typing import Optional, Callable

class StampedeProtection:
    """Prevent cache stampede with locks"""

    def __init__(self):
        self.redis = redis.Redis()
        self.local_locks = {}

    async def fetch_with_lock(
        self,
        cache_key: str,
        fetch_func: Callable,
        ttl: int = 900
    ):
        """
        Fetch with distributed lock
        Only one request fetches, others wait
        """

        # Try to get from cache first
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)

        # Acquire lock
        lock_key = f"lock:{cache_key}"
        lock_acquired = await self.redis.set(
            lock_key,
            "locked",
            ex=10,  # 10 second lock
            nx=True  # Only if not exists
        )

        if lock_acquired:
            # This request fetches the data
            try:
                result = await fetch_func()

                # Cache result
                await self.redis.setex(
                    cache_key,
                    ttl,
                    json.dumps(result)
                )

                return result

            finally:
                # Release lock
                await self.redis.delete(lock_key)

        else:
            # Another request is fetching, wait
            for _ in range(50):  # Wait up to 5 seconds
                await asyncio.sleep(0.1)

                # Check if result is ready
                cached = await self.redis.get(cache_key)
                if cached:
                    return json.loads(cached)

            # Timeout - fetch ourselves
            return await fetch_func()

# Usage
stampede = StampedeProtection()

@app.get("/api/v1/expensive-query")
async def expensive_query():
    async def fetch():
        # Expensive operation
        return await run_expensive_query()

    result = await stampede.fetch_with_lock(
        cache_key="expensive_query_result",
        fetch_func=fetch,
        ttl=600
    )

    return result
```

---

## 4. Kubernetes Deployment

### 4.1 Deployment Configuration

```yaml
# k8s/deployments/api-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
  labels:
    app: business-portfolio
    component: api
spec:
  replicas: 3  # Horizontal scaling
  selector:
    matchLabels:
      app: business-portfolio
      component: api
  template:
    metadata:
      labels:
        app: business-portfolio
        component: api
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
        - name: REDIS_URL
          value: "redis://redis-service:6379"
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
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: business-portfolio
    component: api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 4.2 Horizontal Pod Autoscaling

```yaml
# k8s/hpa.yaml

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
        averageUtilization: 70  # Scale up at 70% CPU
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50  # Increase by 50% at a time
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 min before scaling down
      policies:
      - type: Pods
        value: 1
        periodSeconds: 60
```

---

## Recommendation для нашего проекта

### ✅ Start with Modular Monolith

**Phase 1: MVP (Months 1-3)**
- Single FastAPI application
- Clear module boundaries (trends, ideas, agents, businesses)
- Shared database (PostgreSQL)
- Vertical scaling (upgrade server as needed)

**Benefits**:
- Fast development
- Simple deployment
- Easy debugging
- Lower costs ($200-400/month)

**Phase 2: Optimization (Months 4-6)**
- Add read replicas (2x)
- Multi-layer caching (Redis + CDN)
- Horizontal scaling (Kubernetes, 3-5 pods)

**Cost**: ~$600-1000/month

**Phase 3: Scale (1000+ Businesses)**
- Consider microservices for specific modules
- Database sharding (4 shards)
- Auto-scaling (2-10 pods)
- Global CDN

**Cost**: ~$3000-5000/month

---

## Resources

### Architecture
- [Monolith vs Microservices 2026](https://www.superblocks.com/blog/monolithic-vs-microservices)
- [FastAPI for Microservices](https://talent500.com/blog/fastapi-microservices-python-api-design-patterns-2025/)
- [Modular Monolith Blueprint](https://strategictech.substack.com/p/modular-monolith-blueprint)

### Database Scaling
- [Mastering PostgreSQL Scaling](https://doronsegal.medium.com/scaling-postgres-dfd9c5e175e6)
- [PostgreSQL Horizontal Scaling](https://pgdash.io/blog/horizontally-scaling-postgresql.html)
- [Citus for PostgreSQL](https://www.citusdata.com/)

### Caching
- [Mastering Redis Cache 2026](https://www.dragonflydb.io/guides/mastering-redis-cache-from-basic-to-advanced)
- [Multi-Layered Caching Strategies](https://medium.com/factset/multi-layered-caching-strategies-4427025cae6e)
- [AWS Database Caching Patterns](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html)

---

**Sources:**
- [Monolithic vs Microservices 2026](https://www.superblocks.com/blog/monolithic-vs-microservices)
- [Microservices vs Monoliths in 2026](https://www.javacodegeeks.com/2025/12/microservices-vs-monoliths-in-2026-when-each-architecture-wins.html)
- [FastAPI for Microservices](https://talent500.com/blog/fastapi-microservices-python-api-design-patterns-2025/)
- [Mastering PostgreSQL Scaling](https://doronsegal.medium.com/scaling-postgres-dfd9c5e175e6)
- [Exploring Sharding Strategies with PostgreSQL](https://medium.com/@gustavo.vallerp26/exploring-effective-sharding-strategies-with-postgresql-for-scalable-data-management-2c9ae7ef1759)
- [Horizontally Scaling PostgreSQL](https://pgdash.io/blog/horizontally-scaling-postgresql.html)
- [Mastering Redis Cache 2026 Guide](https://www.dragonflydb.io/guides/mastering-redis-cache-from-basic-to-advanced)
- [Multi-Layered Caching Strategies](https://medium.com/factset/multi-layered-caching-strategies-4427025cae6e)
- [Caching Patterns - AWS](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html)
