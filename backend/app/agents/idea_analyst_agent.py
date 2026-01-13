"""
Idea Analyst Agent
Analyzes trends and generates scored business ideas
"""

from typing import Dict, Any, List
import json
import structlog
from sqlalchemy.orm import Session

from app.agents.base_agent import BaseAgent
from app.modules.trends.service import TrendService
from app.modules.ideas.service import IdeaService
from app.modules.ideas.schemas import IdeaCreate

logger = structlog.get_logger()


class IdeaAnalystAgent(BaseAgent):
    """
    Idea Analyst Agent - Analyzes trends and generates business ideas

    Scoring metrics (0-100 each):
    1. Market Size - Total addressable market potential
    2. Competition - Level of existing competition (lower = better)
    3. Demand - Current demand and pain point severity
    4. Monetization - Revenue potential and business model viability
    5. Feasibility - Technical and operational feasibility
    6. Time to Market - Speed of MVP development and launch

    Process:
    1. Fetch trends from database
    2. Analyze each trend with LLM
    3. Generate business ideas
    4. Score each idea on 6 metrics
    5. Store top ideas in database
    """

    def __init__(self, db: Session):
        super().__init__(db, agent_type="idea_analyst")
        self.trend_service = TrendService(db)
        self.idea_service = IdeaService(db)

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute idea analysis

        Input:
            {
                "trend_ids": [1, 2, 3, ...],  # Optional: specific trends to analyze
                "limit": 10,  # Number of ideas to generate
                "min_total_score": 60  # Minimum score threshold
            }

        Output:
            {
                "trends_analyzed": 5,
                "ideas_generated": 8,
                "ideas_stored": 5,
                "avg_score": 72.5,
                "top_idea": {"id": 123, "title": "...", "score": 85}
            }
        """
        trend_ids = input_data.get("trend_ids")
        limit = input_data.get("limit", 10)
        min_score = input_data.get("min_total_score", 60)

        logger.info(
            "Starting idea analysis",
            trend_ids=trend_ids,
            limit=limit,
            min_score=min_score
        )

        # Fetch trends
        if trend_ids:
            trends = [self.trend_service.get_trend(tid) for tid in trend_ids]
            trends = [t for t in trends if t is not None]
        else:
            # Get recent high-engagement trends
            trends_list = self.trend_service.get_trends(
                limit=limit * 2,  # Analyze more trends to get enough good ideas
                min_engagement=100
            )
            trends = trends_list.items

        logger.info(f"Analyzing {len(trends)} trends")

        # Analyze each trend
        ideas_generated = []
        for trend in trends:
            try:
                idea = await self._analyze_trend(trend)
                if idea and idea["total_score"] >= min_score:
                    ideas_generated.append(idea)
            except Exception as e:
                logger.error(f"Failed to analyze trend {trend.id}", error=str(e))
                continue

        # Sort by score and take top N
        ideas_generated.sort(key=lambda x: x["total_score"], reverse=True)
        top_ideas = ideas_generated[:limit]

        # Store in database
        ideas_stored = []
        for idea_data in top_ideas:
            idea = self.idea_service.create_idea(idea_data["create_data"])
            ideas_stored.append({
                "id": idea.id,
                "title": idea.title,
                "score": idea.total_score
            })

        # Calculate stats
        avg_score = sum(i["total_score"] for i in ideas_generated) / len(ideas_generated) if ideas_generated else 0
        top_idea = ideas_stored[0] if ideas_stored else None

        output = {
            "trends_analyzed": len(trends),
            "ideas_generated": len(ideas_generated),
            "ideas_stored": len(ideas_stored),
            "avg_score": round(avg_score, 2),
            "top_idea": top_idea
        }

        logger.info(
            "Idea analysis completed",
            **output
        )

        return output

    async def _analyze_trend(self, trend) -> Dict[str, Any]:
        """
        Analyze a single trend and generate business idea with scoring

        Returns dict with idea data and scores
        """
        prompt = f"""
        Analyze this trend and generate a viable business idea:

        **Trend:**
        - Title: {trend.title}
        - Description: {trend.description}
        - Source: {trend.source}
        - Category: {trend.category}
        - Engagement: {trend.engagement_score}
        - Tags: {', '.join(trend.tags) if trend.tags else 'N/A'}

        **Your Task:**
        1. Generate a specific, actionable business idea based on this trend
        2. Score it on 6 metrics (0-100 scale):
           - market_size: Total addressable market potential
           - competition: Existing competition level (lower score = more competition)
           - demand: Current demand and pain point severity
           - monetization: Revenue potential and business model viability
           - feasibility: Technical and operational feasibility
           - time_to_market: Speed of MVP development (higher = faster)

        3. Provide detailed reasoning and evidence for each score

        **Output Format (JSON):**
        {{
            "title": "Business idea title (max 100 chars)",
            "description": "Detailed description (max 500 chars)",
            "scores": {{
                "market_size": {{
                    "score": 85,
                    "reasoning": "Why this score",
                    "evidence": "Supporting data/examples"
                }},
                "competition": {{
                    "score": 60,
                    "reasoning": "Analysis of competitors",
                    "evidence": "Existing solutions"
                }},
                "demand": {{
                    "score": 90,
                    "reasoning": "Pain point analysis",
                    "evidence": "Market signals"
                }},
                "monetization": {{
                    "score": 75,
                    "reasoning": "Revenue model viability",
                    "evidence": "Pricing benchmarks"
                }},
                "feasibility": {{
                    "score": 70,
                    "reasoning": "Technical complexity",
                    "evidence": "Available tech/APIs"
                }},
                "time_to_market": {{
                    "score": 80,
                    "reasoning": "Development timeline",
                    "evidence": "MVP scope"
                }}
            }}
        }}

        Be realistic and data-driven in your analysis.
        """

        response = self.call_llm(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert business analyst specializing in startup ideas and market analysis."
                },
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o",  # Use GPT-4 for better analysis
            temperature=0.7,
            max_tokens=2000,
            json_mode=True
        )

        analysis = json.loads(response["content"])

        # Calculate total score
        scores = analysis["scores"]
        total_score = sum(
            scores[metric]["score"]
            for metric in ["market_size", "competition", "demand", "monetization", "feasibility", "time_to_market"]
        ) // 6

        # Prepare analysis JSONB
        analysis_data = {
            metric: {
                "reasoning": scores[metric]["reasoning"],
                "evidence": scores[metric]["evidence"]
            }
            for metric in scores.keys()
        }

        # Create IdeaCreate schema
        idea_create = IdeaCreate(
            title=analysis["title"],
            description=analysis["description"],
            trend_id=trend.id,
            market_size_score=scores["market_size"]["score"],
            competition_score=scores["competition"]["score"],
            demand_score=scores["demand"]["score"],
            monetization_score=scores["monetization"]["score"],
            feasibility_score=scores["feasibility"]["score"],
            time_to_market_score=scores["time_to_market"]["score"],
            analysis=analysis_data,
            status="pending"
        )

        return {
            "total_score": total_score,
            "create_data": idea_create
        }
