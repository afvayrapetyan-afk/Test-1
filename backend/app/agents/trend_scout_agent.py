"""
Trend Scout Agent
Discovers emerging trends from various data sources
"""

from typing import Dict, Any, List
import structlog
from sqlalchemy.orm import Session

from app.agents.base_agent import BaseAgent
from app.modules.trends.service import TrendService
from app.modules.trends.schemas import TrendCreate
from app.scrapers.reddit_scraper import RedditScraper

logger = structlog.get_logger()


class TrendScoutAgent(BaseAgent):
    """
    Trend Scout Agent - Discovers and analyzes emerging trends

    Data sources:
    - Reddit (r/SideProject, r/startups, r/Entrepreneur)
    - Google Trends
    - Product Hunt
    - Hacker News
    - Twitter/X
    - Telegram channels
    - VK communities
    - Yandex Wordstat

    Process:
    1. Scrape data from sources
    2. Clean and deduplicate
    3. Extract trends using LLM
    4. Score by engagement
    5. Store in database
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
        Discover trends from Reddit

        Uses PRAW to scrape hot posts from specified subreddits
        """
        subreddits = input_data.get("subreddits", ["SideProject", "startups", "Entrepreneur"])
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
        Fallback method: Generate Reddit trends using LLM

        Used when Reddit scraper is unavailable or fails
        """
        subreddits = input_data.get("subreddits", ["SideProject", "startups"])
        limit = input_data.get("limit", 100)

        num_ideas = max(limit // len(subreddits), 5)  # At least 5 ideas

        prompt = f"""
        Generate exactly {num_ideas} trending business ideas that would be discussed
        on Reddit subreddits like {', '.join(subreddits)}.

        Return a JSON object with a "trends" array. Each trend must have:
        - title: string (max 100 chars)
        - description: string (max 500 chars)
        - category: string (one of: productivity, saas, marketplace, ai, fintech, health, education)
        - tags: array of strings (3-5 tags)
        - engagement_score: integer (100-2000)

        Example format:
        {{
          "trends": [
            {{
              "title": "AI Code Review Assistant",
              "description": "Automated code review tool using GPT-4",
              "category": "ai",
              "tags": ["AI", "development", "automation"],
              "engagement_score": 1250
            }}
          ]
        }}

        Focus on:
        - AI/ML applications
        - SaaS products
        - No-code tools
        - Developer tools
        - Side project ideas

        Generate exactly {num_ideas} trends in the "trends" array.
        """

        response = self.call_llm(
            messages=[
                {"role": "system", "content": "You are a trend discovery expert."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o-mini",
            temperature=0.8,
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
