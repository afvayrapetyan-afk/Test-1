# Research: LLM Integration Best Practices

**Дата**: 2026-01-13
**Статус**: ✅ Completed

## Summary

Изучили best practices для production LLM integration: cost optimization через prompt caching (10x cheaper) и batching (50% discount), reliability через fallback chains и circuit breakers, prompt engineering techniques (few-shot, chain-of-thought, роли). Для нашего проекта рекомендуем **гибридный подход**: GPT-4o для complex reasoning, Claude для long context, GPT-3.5 Turbo для simple tasks, local models для embeddings.

---

## Key Findings

### 1. Cost Optimization Strategies

#### 1.1 Prompt Caching (10x Cheaper)

**Как работает** (2026):
- OpenAI **автоматически** кэширует промпты ≥ 1024 tokens
- Cached tokens: 10x cheaper ($0.0015/1K vs $0.015/1K для GPT-4o)
- Cache TTL: 5-10 минут (до 1 часа off-peak)
- Hit rate: ~50% при repeated requests

**Best Practices**:

```python
# backend/app/services/llm_service.py

from openai import AsyncOpenAI
from typing import List, Dict
import hashlib

class LLMService:
    """Smart LLM service with caching"""

    def __init__(self):
        self.client = AsyncOpenAI()
        self.cache = {}  # Local application cache

    # Good: Static system prompt at начале (cached)
    SYSTEM_PROMPT = """You are an expert business analyst specializing in market trend analysis.
    Your task is to evaluate business ideas based on six key metrics:
    1. Market Size - potential TAM (Total Addressable Market)
    2. Competition - existing players and barriers to entry
    3. Demand - evidence of customer need
    4. Monetization - clear revenue model
    5. Feasibility - technical complexity and resource requirements
    6. Time to Market - speed of implementation

    For each metric, provide:
    - Score (0-100)
    - Reasoning (2-3 sentences)
    - Supporting evidence

    Respond in JSON format with the following structure:
    {
        "market_size": {"score": int, "reasoning": str, "evidence": str},
        "competition": {"score": int, "reasoning": str, "evidence": str},
        ...
    }
    """  # 200+ tokens - will be cached

    async def analyze_idea(self, trend: Dict) -> Dict:
        """
        Analyze business idea (benefits from caching)
        Static: system prompt (cached)
        Dynamic: trend data (not cached)
        """

        # Dynamic content at the end
        user_prompt = f"""
        Analyze the following trend for business potential:

        Title: {trend['title']}
        Description: {trend['description']}
        Source: {trend['source']}
        Engagement: {trend['engagement_score']}
        Tags: {', '.join(trend['tags'])}
        """

        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},  # Cached
                {"role": "user", "content": user_prompt}  # Not cached
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        return response.choices[0].message.content

    # Bad: Dynamic content in system prompt (breaks cache)
    async def analyze_idea_bad(self, trend: Dict) -> Dict:
        """
        ❌ Don't do this - dynamic content in system breaks caching
        """
        system_prompt = f"""You are analyzing trend: {trend['title']}
        Provide scores for..."""  # Different every time → no caching

        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}]
        )
        return response.choices[0].message.content
```

**Cache Optimization Tips**:
- ✅ Static instructions в system prompt
- ✅ Examples/templates в system prompt
- ✅ Large context (>1024 tokens) at beginning
- ✅ Dynamic content at the end
- ❌ Don't change system prompt frequently

**Expected Savings**:
- Without caching: 1M tokens input × $15/1M = $15
- With caching (50% hit rate): 500K cached × $1.50 + 500K new × $15 = $8.25
- **Savings: 45%**

#### 1.2 Batching (50% Discount)

**Use Case**: Non-time-sensitive bulk operations

**Benefits**:
- 50% discount на input + output tokens
- 24-hour completion window
- Ideal for: bulk analysis, embeddings, data enrichment

**Implementation**:

```python
# backend/app/services/batch_service.py

from openai import AsyncOpenAI
from typing import List
import json

class BatchProcessor:
    """Batch API for cost-effective processing"""

    def __init__(self):
        self.client = AsyncOpenAI()

    async def batch_analyze_ideas(self, trends: List[Dict]) -> str:
        """
        Create batch job for analyzing multiple trends
        Returns: batch_id for tracking
        """

        # Prepare batch file (JSONL format)
        batch_requests = []
        for idx, trend in enumerate(trends):
            request = {
                "custom_id": f"trend-{trend['id']}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o",
                    "messages": [
                        {"role": "system", "content": self.get_system_prompt()},
                        {"role": "user", "content": self.format_trend(trend)}
                    ],
                    "temperature": 0.3
                }
            }
            batch_requests.append(request)

        # Upload batch file
        batch_file_content = "\n".join(json.dumps(req) for req in batch_requests)

        batch_file = await self.client.files.create(
            file=batch_file_content.encode(),
            purpose="batch"
        )

        # Create batch job
        batch = await self.client.batches.create(
            input_file_id=batch_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h"
        )

        return batch.id

    async def get_batch_results(self, batch_id: str) -> List[Dict]:
        """
        Retrieve batch results
        """
        batch = await self.client.batches.retrieve(batch_id)

        if batch.status != "completed":
            return {"status": batch.status, "progress": batch.request_counts}

        # Download results
        result_file = await self.client.files.content(batch.output_file_id)
        results = []

        for line in result_file.text.split('\n'):
            if line:
                result = json.loads(line)
                results.append({
                    "trend_id": result["custom_id"].split("-")[1],
                    "analysis": result["response"]["body"]["choices"][0]["message"]["content"]
                })

        return results

# Usage with Celery
@app.task(name='analysis.batch_analyze')
def batch_analyze_task():
    """
    Nightly batch job:
    1. Collect all new trends from last 24h
    2. Submit batch analysis
    3. Process results when complete
    """
    processor = BatchProcessor()

    # Get new trends
    trends = get_trends_for_analysis(hours=24)

    if len(trends) < 10:
        # Too few for batch - use regular API
        return

    # Submit batch
    batch_id = await processor.batch_analyze_ideas(trends)

    # Schedule result collection (24h later)
    collect_batch_results.apply_async(
        args=[batch_id],
        countdown=86400  # 24 hours
    )

@app.task(name='analysis.collect_batch_results')
async def collect_batch_results(batch_id: str):
    """Collect and store batch results"""
    processor = BatchProcessor()
    results = await processor.get_batch_results(batch_id)

    for result in results:
        store_analysis(result['trend_id'], result['analysis'])
```

**Cost Comparison**:
| Method | Input Cost | Output Cost | Total (1M tokens) |
|--------|-----------|-------------|-------------------|
| Standard API | $15/1M | $60/1M | $75 |
| Batch API | $7.50/1M | $30/1M | $37.50 |
| **Savings** | **50%** | **50%** | **50%** |

#### 1.3 Model Selection (Right Tool for Job)

```python
# backend/app/services/model_selector.py

from enum import Enum
from typing import Dict

class TaskComplexity(Enum):
    SIMPLE = "simple"  # Classification, extraction
    MEDIUM = "medium"  # Analysis, summarization
    COMPLEX = "complex"  # Reasoning, planning

class ModelSelector:
    """Select cheapest model for task complexity"""

    MODELS = {
        TaskComplexity.SIMPLE: {
            "model": "gpt-3.5-turbo",
            "cost_per_1m_input": 0.50,
            "cost_per_1m_output": 1.50,
            "max_tokens": 16385
        },
        TaskComplexity.MEDIUM: {
            "model": "gpt-4o-mini",
            "cost_per_1m_input": 0.150,
            "cost_per_1m_output": 0.600,
            "max_tokens": 128000
        },
        TaskComplexity.COMPLEX: {
            "model": "gpt-4o",
            "cost_per_1m_input": 2.50,
            "cost_per_1m_output": 10.00,
            "max_tokens": 128000
        }
    }

    @staticmethod
    def select_model(task: str) -> str:
        """
        Auto-select model based on task
        """
        complexity_map = {
            "categorize": TaskComplexity.SIMPLE,
            "extract": TaskComplexity.SIMPLE,
            "tag": TaskComplexity.SIMPLE,
            "analyze": TaskComplexity.MEDIUM,
            "summarize": TaskComplexity.MEDIUM,
            "score": TaskComplexity.MEDIUM,
            "plan": TaskComplexity.COMPLEX,
            "reason": TaskComplexity.COMPLEX,
            "design": TaskComplexity.COMPLEX,
        }

        for keyword, complexity in complexity_map.items():
            if keyword in task.lower():
                return ModelSelector.MODELS[complexity]["model"]

        # Default to medium
        return ModelSelector.MODELS[TaskComplexity.MEDIUM]["model"]

# Usage
async def process_trend(trend: Dict, task: str):
    model = ModelSelector.select_model(task)

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "..."},
            {"role": "user", "content": f"{task}: {trend}"}
        ]
    )

    return response.choices[0].message.content

# Example savings:
# Simple task (categorize) with gpt-3.5-turbo: $0.50/1M
# vs GPT-4o: $2.50/1M
# Savings: 80%
```

---

### 2. Reliability Patterns

#### 2.1 Retry with Exponential Backoff

```python
# backend/app/core/llm_client.py

import asyncio
import random
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from openai import APIError, RateLimitError, APITimeoutError

class RobustLLMClient:
    """LLM client with retry logic"""

    def __init__(self):
        self.client = AsyncOpenAI()

    @retry(
        retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError)),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(5),
        reraise=True
    )
    async def complete(
        self,
        model: str,
        messages: List[Dict],
        **kwargs
    ) -> str:
        """
        Completion with automatic retry
        - Exponential backoff: 4s, 8s, 16s, 32s, 60s
        - Max 5 attempts
        - Random jitter to prevent thundering herd
        """

        # Add jitter
        await asyncio.sleep(random.uniform(0, 0.5))

        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )

        return response.choices[0].message.content

    # Manual retry with circuit breaker
    async def complete_with_circuit_breaker(
        self,
        model: str,
        messages: List[Dict],
        **kwargs
    ) -> str:
        """
        Advanced: Circuit breaker pattern
        Stops retrying if failure rate > threshold
        """

        # Check circuit state
        if self.circuit_breaker.is_open():
            raise CircuitBreakerOpen(f"Too many failures for {model}")

        try:
            response = await self.complete(model, messages, **kwargs)
            self.circuit_breaker.record_success()
            return response

        except Exception as e:
            self.circuit_breaker.record_failure()
            raise

class CircuitBreaker:
    """Simple circuit breaker"""

    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    def is_open(self) -> bool:
        if self.state == "open":
            # Check if timeout passed
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
                return False
            return True
        return False

    def record_success(self):
        self.failures = 0
        self.state = "closed"

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()

        if self.failures >= self.failure_threshold:
            self.state = "open"
```

#### 2.2 Fallback Chains

```python
# backend/app/services/llm_fallback.py

from typing import List, Optional

class FallbackLLMService:
    """
    Fallback chain: GPT-4o → Claude → GPT-3.5
    """

    def __init__(self):
        self.openai_client = AsyncOpenAI()
        self.anthropic_client = AsyncAnthropic()

    FALLBACK_CHAIN = [
        {
            "provider": "openai",
            "model": "gpt-4o",
            "timeout": 30,
            "cost_per_1m": 2.50
        },
        {
            "provider": "anthropic",
            "model": "claude-3-5-sonnet-20241022",
            "timeout": 45,
            "cost_per_1m": 3.00
        },
        {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "timeout": 20,
            "cost_per_1m": 0.50
        }
    ]

    async def complete_with_fallback(
        self,
        messages: List[Dict],
        **kwargs
    ) -> Dict:
        """
        Try each model in chain until success
        """

        last_error = None

        for config in self.FALLBACK_CHAIN:
            try:
                logger.info(f"Trying {config['provider']} - {config['model']}")

                if config['provider'] == 'openai':
                    response = await self.openai_client.chat.completions.create(
                        model=config['model'],
                        messages=messages,
                        timeout=config['timeout'],
                        **kwargs
                    )
                    return {
                        "content": response.choices[0].message.content,
                        "model": config['model'],
                        "provider": config['provider']
                    }

                elif config['provider'] == 'anthropic':
                    # Convert messages for Claude
                    claude_messages = self.convert_to_claude_format(messages)

                    response = await self.anthropic_client.messages.create(
                        model=config['model'],
                        messages=claude_messages,
                        max_tokens=kwargs.get('max_tokens', 4096),
                        timeout=config['timeout']
                    )

                    return {
                        "content": response.content[0].text,
                        "model": config['model'],
                        "provider": config['provider']
                    }

            except Exception as e:
                logger.warning(f"Failed with {config['model']}: {e}")
                last_error = e
                continue

        # All failed
        raise AllModelsFailedError(f"All models failed. Last error: {last_error}")

    def convert_to_claude_format(self, messages: List[Dict]) -> List[Dict]:
        """Convert OpenAI format to Claude format"""
        claude_messages = []

        for msg in messages:
            if msg['role'] == 'system':
                # Claude uses system parameter separately
                continue
            claude_messages.append({
                "role": msg['role'],
                "content": msg['content']
            })

        return claude_messages
```

#### 2.3 LiteLLM (Unified Interface)

```python
# backend/app/services/unified_llm.py

from litellm import acompletion
import litellm

# Configure LiteLLM
litellm.set_verbose = True
litellm.drop_params = True  # Auto-remove unsupported params

class UnifiedLLMService:
    """
    Unified interface for multiple providers
    Automatic fallback and retry
    """

    async def complete(
        self,
        messages: List[Dict],
        **kwargs
    ) -> str:
        """
        Call with automatic fallback
        """

        response = await acompletion(
            model="gpt-4o",
            messages=messages,
            fallbacks=["claude-3-5-sonnet-20241022", "gpt-3.5-turbo"],
            num_retries=3,
            timeout=30,
            **kwargs
        )

        return response.choices[0].message.content

# Even simpler - let LiteLLM handle everything
async def analyze_trend(trend: Dict) -> Dict:
    service = UnifiedLLMService()

    response = await service.complete(
        messages=[
            {"role": "system", "content": "You are a business analyst..."},
            {"role": "user", "content": f"Analyze: {trend}"}
        ],
        temperature=0.3
    )

    return json.loads(response)
```

---

### 3. Prompt Engineering Techniques

#### 3.1 Few-Shot Prompting

```python
# backend/app/prompts/few_shot_examples.py

FEW_SHOT_TREND_ANALYSIS = """
You are a business analyst. Analyze trends and score them 0-100.

Example 1:
Trend: "AI-powered meeting notes app"
Analysis:
{
    "market_size": {"score": 85, "reasoning": "Remote work = huge TAM, $50B+ market"},
    "competition": {"score": 60, "reasoning": "Otter.ai, Fireflies exist but room for differentiation"},
    "demand": {"score": 90, "reasoning": "Clear pain point, people hate note-taking"},
    "monetization": {"score": 75, "reasoning": "SaaS subscription, $10-30/month is viable"},
    "feasibility": {"score": 70, "reasoning": "Whisper API available, moderate complexity"},
    "time_to_market": {"score": 80, "reasoning": "MVP in 2-3 months with existing APIs"}
}

Example 2:
Trend: "Blockchain-based social network"
Analysis:
{
    "market_size": {"score": 70, "reasoning": "Social media TAM huge but crypto adoption limited"},
    "competition": {"score": 30, "reasoning": "Difficult to compete with Facebook, Twitter"},
    "demand": {"score": 50, "reasoning": "Niche appeal, privacy-focused users only"},
    "monetization": {"score": 40, "reasoning": "Unclear how to monetize decentralized platform"},
    "feasibility": {"score": 35, "reasoning": "Very complex, requires blockchain expertise"},
    "time_to_market": {"score": 20, "reasoning": "12+ months minimum for MVP"}
}

Now analyze this trend:
Trend: {trend_title}
Description: {trend_description}
"""

# Usage
async def analyze_with_few_shot(trend: Dict) -> Dict:
    prompt = FEW_SHOT_TREND_ANALYSIS.format(
        trend_title=trend['title'],
        trend_description=trend['description']
    )

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
```

#### 3.2 Chain-of-Thought (CoT) Prompting

```python
# backend/app/prompts/chain_of_thought.py

CHAIN_OF_THOUGHT_ANALYSIS = """
Analyze the following business trend step-by-step:

Trend: {trend_title}
Description: {trend_description}
Source: {source}
Engagement: {engagement}

Step 1: Market Analysis
Think through the market size:
- What problem does this solve?
- Who is the target audience?
- How large is the addressable market?

Step 2: Competition Assessment
Consider existing solutions:
- What alternatives exist today?
- What are their weaknesses?
- What would differentiate this?

Step 3: Demand Validation
Evaluate customer demand:
- Is this a proven pain point?
- What evidence supports demand?
- Are people already searching for solutions?

Step 4: Monetization Viability
Assess revenue potential:
- How would this make money?
- What's a realistic price point?
- Are customers willing to pay?

Step 5: Feasibility Check
Evaluate technical complexity:
- What tech is needed?
- Are there existing APIs/tools?
- What's the development effort?

Step 6: Time to Market
Estimate implementation speed:
- How quickly could an MVP launch?
- What's the minimum feature set?
- What dependencies exist?

Based on your step-by-step analysis above, provide final scores (0-100) for each metric in JSON format.
"""

# Usage
async def analyze_with_cot(trend: Dict) -> Dict:
    prompt = CHAIN_OF_THOUGHT_ANALYSIS.format(**trend)

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,  # Slightly higher for reasoning
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
```

#### 3.3 Role Prompting

```python
# backend/app/prompts/role_prompts.py

EXPERT_ROLES = {
    "market_analyst": """You are a senior market analyst with 15 years of experience at McKinsey & Company.
    You specialize in TAM analysis, market sizing, and competitive intelligence.
    Your strength is identifying market opportunities before they become obvious.""",

    "product_strategist": """You are a product strategist who has launched 20+ successful SaaS products.
    You understand product-market fit, user acquisition, and viral growth mechanics.
    You can spot which products will gain traction and which will fail.""",

    "technical_architect": """You are a seasoned CTO who has built multiple scalable systems.
    You can quickly assess technical feasibility, identify the right tech stack,
    and estimate development effort accurately.""",

    "venture_capitalist": """You are a Series A/B investor at Sequoia Capital.
    You've invested in 50+ startups with 10 exits > $1B.
    You can identify which trends will attract funding and scale."""
}

# Multi-expert analysis
async def multi_expert_analysis(trend: Dict) -> Dict:
    """
    Get analysis from multiple expert perspectives
    """

    results = {}

    for role, backstory in EXPERT_ROLES.items():
        prompt = f"""{backstory}

        Analyze this business opportunity:
        {trend['title']} - {trend['description']}

        Provide your expert opinion on:
        1. Opportunity score (0-100)
        2. Key insights
        3. Red flags
        4. Recommendation (pursue/skip/watch)
        """

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7  # Higher for diverse perspectives
        )

        results[role] = response.choices[0].message.content

    # Aggregate expert opinions
    return aggregate_expert_opinions(results)
```

---

## Model Comparison (2026 Pricing)

| Model | Provider | Input ($/1M) | Output ($/1M) | Context | Best For |
|-------|----------|--------------|---------------|---------|----------|
| **GPT-4o** | OpenAI | $2.50 | $10.00 | 128K | Complex reasoning |
| **GPT-4o-mini** | OpenAI | $0.150 | $0.600 | 128K | General purpose |
| **GPT-3.5 Turbo** | OpenAI | $0.50 | $1.50 | 16K | Simple tasks |
| **Claude 3.5 Sonnet** | Anthropic | $3.00 | $15.00 | 200K | Long context |
| **Claude 3 Haiku** | Anthropic | $0.25 | $1.25 | 200K | Fast & cheap |
| **Gemini 1.5 Pro** | Google | $1.25 | $5.00 | 2M | Huge context |
| **Llama 3.1 70B** | Meta (self-host) | ~$0.01 | ~$0.01 | 128K | Cost-sensitive |

---

## Recommendations для нашего проекта

### ✅ Hybrid LLM Strategy

**Layer 1: Simple Tasks (GPT-3.5 Turbo or Haiku)**
- Categorization (SaaS, marketplace, tool)
- Tag extraction
- Spam detection
- **Cost**: $0.50/1M input
- **Volume**: ~1M tokens/day
- **Monthly**: $15/month

**Layer 2: Medium Tasks (GPT-4o-mini)**
- Trend summarization
- Initial idea scoring
- Content enrichment
- **Cost**: $0.150/1M input
- **Volume**: ~5M tokens/day
- **Monthly**: $22.50/month

**Layer 3: Complex Tasks (GPT-4o)**
- Deep business analysis
- Strategic planning
- Code generation (DevAgent)
- Marketing strategy
- **Cost**: $2.50/1M input
- **Volume**: ~1M tokens/day
- **Monthly**: $75/month

**Layer 4: Embeddings (text-embedding-3-small)**
- Vector generation
- Semantic search
- **Cost**: $0.020/1M tokens
- **Volume**: ~10M tokens/day (batch)
- **Monthly**: $6/month

**Total Estimated Cost**: ~$120-150/month для MVP

### Optimization Strategy

1. **Prompt Caching**: 45% savings on repeated prompts
2. **Batching**: 50% savings на non-urgent tasks
3. **Model Selection**: 80% savings using cheaper models для simple tasks
4. **Local Models**: 90% savings для embeddings (use Llama 3.1)

**Optimized Cost**: ~$60-80/month

---

## Implementation Roadmap

### Week 1: Foundation
1. Setup OpenAI + Anthropic clients
2. Implement retry logic
3. Add fallback chains
4. Test error handling

### Week 2: Caching & Batching
1. Structure prompts for caching
2. Implement batch processor
3. Setup nightly batch jobs
4. Measure cache hit rate

### Week 3: Prompt Engineering
1. Create few-shot templates
2. Implement CoT prompts
3. Test role prompting
4. A/B test different approaches

### Week 4: Monitoring
1. Track token usage
2. Monitor costs per model
3. Measure latency
4. Optimize based on data

---

## Resources

### Documentation
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

### Cost Optimization
- [OpenAI Prompt Caching](https://platform.openai.com/docs/guides/prompt-caching)
- [Prompt Caching Explained](https://ngrok.com/blog/prompt-caching/)
- [Managing OpenAI Costs](https://platform.openai.com/docs/guides/realtime-costs)

### Reliability
- [LiteLLM Reliability](https://docs.litellm.ai/docs/completion/reliable_completions)
- [LangChain Fallbacks](https://python.langchain.com/v0.1/docs/guides/productionization/fallbacks/)
- [Retries, Fallbacks, and Circuit Breakers](https://portkey.ai/blog/retries-fallbacks-and-circuit-breakers-in-llm-apps/)

### Prompt Engineering
- [Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot)
- [Few-Shot Prompting](https://www.promptingguide.ai/techniques/fewshot)
- [Prompt Engineering Guide 2026](https://www.k2view.com/blog/prompt-engineering-techniques/)

---

**Sources:**
- [OpenAI Pricing in 2026](https://www.finout.io/blog/openai-pricing-in-2026)
- [OpenAI Prompt Caching Documentation](https://platform.openai.com/docs/guides/prompt-caching)
- [Prompt Caching: 10x Cheaper LLM Tokens](https://ngrok.com/blog/prompt-caching/)
- [OpenAI 80% Faster with Prompt Caching](https://sgryt.com/posts/openai-prompt-caching-cost-optimization/)
- [Reliability - Retries, Fallbacks | liteLLM](https://docs.litellm.ai/docs/completion/reliable_completions)
- [Retries, Fallbacks, and Circuit Breakers in LLM Apps](https://portkey.ai/blog/retries-fallbacks-and-circuit-breakers-in-llm-apps/)
- [Robust LLM API Strategies in Python](https://ai.gopubby.com/robust-llm-api-strategies-retries-fallbacks-in-python-caf9efa96908)
- [Chain-of-Thought Prompting Guide](https://www.promptingguide.ai/techniques/cot)
- [Few-Shot Prompting Guide](https://www.promptingguide.ai/techniques/fewshot)
- [Prompt Engineering Techniques for 2026](https://www.k2view.com/blog/prompt-engineering-techniques/)
