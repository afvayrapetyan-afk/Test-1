"""
Trend Scout Agent
Discovers emerging AI trends from various data sources

🎯 ФОКУС: AI-помощники, AI-агенты, автоматизация
"""

from typing import Dict, Any, List
import structlog
from sqlalchemy.orm import Session

from app.agents.base_agent import BaseAgent
from app.modules.trends.service import TrendService
from app.modules.trends.schemas import TrendCreate
from app.scrapers.reddit_scraper import RedditScraper

logger = structlog.get_logger()

# AI-focused subreddits for trend discovery
AI_SUBREDDITS = [
    "MachineLearning",
    "artificial",
    "ChatGPT",
    "LocalLLaMA",
    "singularity",
    "SideProject",
    "startups",
    "Entrepreneur",
    "SaaS",
    "nocode",
    "AutomateYourself",
]

# Keywords for filtering AI-related trends
AI_KEYWORDS = [
    "AI", "GPT", "LLM", "agent", "assistant", "bot", "automation",
    "chatbot", "copilot", "помощник", "агент", "автоматизация",
    "нейросеть", "искусственный интеллект",
]


class TrendScoutAgent(BaseAgent):
    """
    Trend Scout Agent - Discovers AI-focused emerging trends

    🎯 ФОКУС:
    - AI-помощники для бизнеса и физлиц
    - AI-агенты для автоматизации
    - Инструменты на базе LLM
    - Решения реальных проблем с помощью AI

    Data sources:
    - Reddit (AI & startup subreddits)
    - Google Trends (AI keywords)
    - Product Hunt (AI category)
    - Hacker News (AI news)
    - Twitter/X (AI discussions)
    - Telegram channels (AI news RU)
    - Habr (AI articles)

    Process:
    1. Scrape data from AI-focused sources
    2. Filter for AI-related content
    3. Clean and deduplicate
    4. Extract trends using LLM
    5. Score by engagement & AI relevance
    6. Store in database
    """

    def __init__(self, db: Session):
        super().__init__(db, agent_type="trend_scout")
        self.trend_service = TrendService(db)

        # Initialize scrapers
        try:
            self.reddit_scraper = RedditScraper()
        except Exception as e:
            logger.warning(f"Reddit scraper initialization failed: {e}")
            self.reddit_scraper = None

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute trend discovery

        Input:
            {
                "sources": ["reddit", "google_trends", ...],
                "limit": 100,
                "subreddits": ["SideProject", "startups"],  # for reddit
                "keywords": ["AI", "SaaS"]  # for google trends
            }

        Output:
            {
                "trends_discovered": 156,
                "trends_stored": 142,
                "duplicates_filtered": 14,
                "breakdown_by_source": {"reddit": 89, "google_trends": 67}
            }
        """
        sources = input_data.get("sources", ["reddit"])
        limit = input_data.get("limit", 100)

        logger.info(
            "Starting trend discovery",
            sources=sources,
            limit=limit
        )

        trends_discovered = []
        breakdown = {}

        # Process each source
        for source in sources:
            if source == "reddit":
                source_trends = await self._discover_from_reddit(input_data)
            elif source == "google_trends":
                source_trends = await self._discover_from_google_trends(input_data)
            else:
                logger.warning(f"Unsupported source: {source}")
                continue

            trends_discovered.extend(source_trends)
            breakdown[source] = len(source_trends)

        # Store trends in database
        trends_stored = 0
        duplicates_filtered = 0

        for trend_data in trends_discovered:
            # TrendService handles duplicate detection
            trend = self.trend_service.create_trend(trend_data)

            # Check if it was a duplicate (same ID returned)
            existing_count = len([t for t in trends_discovered[:trends_discovered.index(trend_data)]
                                 if t.title == trend_data.title])
            if existing_count > 0:
                duplicates_filtered += 1
            else:
                trends_stored += 1

        output = {
            "trends_discovered": len(trends_discovered),
            "trends_stored": trends_stored,
            "duplicates_filtered": duplicates_filtered,
            "breakdown_by_source": breakdown
        }

        logger.info(
            "Trend discovery completed",
            **output
        )

        return output

    async def _discover_from_reddit(self, input_data: Dict[str, Any]) -> List[TrendCreate]:
        """
        Discover AI-focused trends from Reddit

        Uses PRAW to scrape hot posts from AI-related subreddits
        """
        subreddits = input_data.get("subreddits", AI_SUBREDDITS)
        limit = input_data.get("limit", 100)
        time_filter = input_data.get("time_filter", "week")
        sort = input_data.get("sort", "hot")

        logger.info(
            "Scraping Reddit",
            subreddits=subreddits,
            limit=limit,
            sort=sort,
            time_filter=time_filter
        )

        # Check if Reddit scraper is available
        if not self.reddit_scraper:
            logger.warning("Reddit scraper not available, falling back to LLM generation")
            return await self._generate_reddit_trends_with_llm(input_data)

        try:
            # Scrape Reddit using PRAW
            scraped_posts = await self.reddit_scraper.scrape({
                "subreddits": subreddits,
                "limit": limit,
                "time_filter": time_filter,
                "sort": sort
            })

            # Convert scraped posts to TrendCreate objects
            trends = []
            for post in scraped_posts:
                trend = TrendCreate(
                    title=post["title"],
                    description=post["description"],
                    url=post["url"],
                    source=post["source"],
                    category=post["category"],
                    tags=post["tags"],
                    engagement_score=post["engagement_score"],
                    velocity=post["velocity"],
                    metadata=post["metadata"]
                )
                trends.append(trend)

            logger.info(f"Scraped {len(trends)} trends from Reddit")
            return trends

        except Exception as e:
            logger.error(f"Reddit scraping failed: {e}")
            # Fallback to LLM generation
            logger.warning("Falling back to LLM generation")
            return await self._generate_reddit_trends_with_llm(input_data)

    async def _generate_reddit_trends_with_llm(self, input_data: Dict[str, Any]) -> List[TrendCreate]:
        """
        Generate AI-focused trends using LLM

        🎯 ФОКУС: AI-помощники и агенты для решения реальных проблем
        """
        subreddits = input_data.get("subreddits", AI_SUBREDDITS)
        limit = input_data.get("limit", 100)

        num_ideas = max(limit // max(len(subreddits), 1), 10)  # At least 10 ideas

        prompt = f"""
        🎯 Сгенерируй {num_ideas} АКТУАЛЬНЫХ трендов в сфере AI-помощников и AI-агентов.

        Тренды должны быть основаны на РЕАЛЬНЫХ проблемах, которые обсуждаются на Reddit,
        Hacker News, Product Hunt и в AI-сообществе.

        ═══════════════════════════════════════════════════════════════
        ТРЕБОВАНИЯ К ТРЕНДАМ:
        ═══════════════════════════════════════════════════════════════

        Каждый тренд должен относиться к одной из категорий:
        1. 🤖 AI-АССИСТЕНТЫ - помощники для людей
        2. 🔄 AI-АГЕНТЫ - автономные системы
        3. 🛠️ AI-ИНСТРУМЕНТЫ - специализированные утилиты
        4. 📊 AI для БИЗНЕСА - B2B решения
        5. 👤 AI для ЛИЧНОГО ИСПОЛЬЗОВАНИЯ - B2C решения

        Тренды должны отражать РЕАЛЬНЫЕ проблемы:
        - Экономия времени
        - Автоматизация рутины
        - Принятие решений
        - Обработка информации
        - Персонализация
        - Коммуникация

        ═══════════════════════════════════════════════════════════════
        ФОРМАТ ОТВЕТА (JSON):
        ═══════════════════════════════════════════════════════════════

        {{
          "trends": [
            {{
              "title": "AI-ассистент для управления личными финансами",
              "description": "Автоматический анализ расходов, рекомендации по экономии, прогноз бюджета",
              "category": "ai",
              "tags": ["AI", "fintech", "personal finance", "assistant"],
              "engagement_score": 1500,
              "problem_type": "personal",
              "ai_type": "assistant"
            }}
          ]
        }}

        Категории: ai, saas, fintech, health, education, productivity, automation

        ВСЕ НАЗВАНИЯ И ОПИСАНИЯ НА РУССКОМ ЯЗЫКЕ!
        """

        response = self.call_llm(
            messages=[
                {
                    "role": "system",
                    "content": """Ты эксперт по AI-трендам и продуктам на базе искусственного интеллекта.

Твоя задача - находить РЕАЛЬНЫЕ тренды в сфере AI-помощников и агентов.
Фокусируйся на проблемах, которые AI действительно может решить.

Отвечай только на русском языке."""
                },
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o",  # Better model for trend discovery
            temperature=0.7,
            json_mode=True
        )

        import json
        trends_data = json.loads(response["content"])

        # Handle different response formats
        trend_list = trends_data if isinstance(trends_data, list) else trends_data.get("trends", trends_data.get("items", []))

        trends = []
        for trend in trend_list[:limit]:
            trends.append(
                TrendCreate(
                    title=trend["title"],
                    description=trend["description"],
                    source="reddit",
                    category=trend["category"],
                    tags=trend["tags"],
                    engagement_score=trend["engagement_score"],
                    url=f"https://reddit.com/r/{subreddits[0]}/",
                    metadata={
                        "subreddit": subreddits[0],
                        "generated": True  # LLM-generated fallback
                    }
                )
            )

        return trends

    async def _discover_from_google_trends(self, input_data: Dict[str, Any]) -> List[TrendCreate]:
        """
        Discover trends from Google Trends

        Uses pytrends to get trending searches
        """
        keywords = input_data.get("keywords", ["AI", "SaaS", "startup"])
        limit = input_data.get("limit", 50)

        logger.info(f"Analyzing Google Trends: {keywords}")

        # TODO: Implement actual Google Trends analysis with pytrends
        # For now, use LLM to generate example trends

        prompt = f"""
        Generate {limit} trending search queries and business opportunities related to: {', '.join(keywords)}.

        Format as JSON array with objects containing:
        - title: Search trend or business idea
        - description: Why this is trending
        - category: Business category
        - tags: Relevant tags
        - velocity: Trend velocity score (0.0-1.0)

        Focus on emerging trends with business potential.
        """

        response = self.call_llm(
            messages=[
                {"role": "system", "content": "You are a Google Trends analysis expert."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o-mini",
            temperature=0.7,
            json_mode=True
        )

        import json
        trends_data = json.loads(response["content"])

        # Handle different response formats
        trend_list = trends_data if isinstance(trends_data, list) else trends_data.get("trends", trends_data.get("items", []))

        trends = []
        for trend in trend_list[:limit]:
            trends.append(
                TrendCreate(
                    title=trend["title"],
                    description=trend["description"],
                    source="google_trends",
                    category=trend.get("category", "tech"),
                    tags=trend.get("tags", []),
                    velocity=trend.get("velocity", 0.5),
                    metadata={
                        "keywords": keywords,
                        "generated": True  # Placeholder until real scraper
                    }
                )
            )

        return trends
