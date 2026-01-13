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
        Проведи ГЛУБОКИЙ анализ этого тренда и создай продуманную бизнес-идею:

        **Тренд:**
        - Название: {trend.title}
        - Описание: {trend.description}
        - Источник: {trend.source}
        - Категория: {trend.category}
        - Популярность: {trend.engagement_score}
        - Теги: {', '.join(trend.tags) if trend.tags else 'N/A'}

        **Требования к анализу:**

        1. КРИТИЧЕСКИ ВАЖНО: Проведи РЕАЛЬНЫЙ анализ рынка:
           - Проверь существующих конкурентов
           - Оцени реальный размер рынка с цифрами
           - Найди КОНКРЕТНЫЕ доказательства спроса
           - Проанализируй успешные аналоги

        2. Оцени 6 метрик (0-100) с ПОДРОБНЫМ обоснованием:
           - market_size: Общий объем рынка (TAM) в $ и количество потенциальных клиентов
           - competition: Уровень конкуренции (меньше = лучше) с примерами конкурентов
           - demand: Острота проблемы и реальный спрос (с доказательствами)
           - monetization: Потенциал дохода с конкретными моделями монетизации
           - feasibility: Техническая сложность реализации
           - time_to_market: Скорость запуска MVP (выше = быстрее)

        3. Рассчитай РЕАЛИСТИЧНЫЕ финансовые показатели:
           - investment: Начальные инвестиции в $ (учти разработку, маркетинг, инфраструктуру)
           - payback_months: Срок окупаемости в месяцах (реалистично!)
           - margin: Маржинальность бизнеса в % (0-100)
           - arr: Годовой доход (ARR) через 12 месяцев в $

        4. Определи правильную категорию из: ai, saas, ecommerce, fintech, health, education, entertainment

        5. Подбери ОДИН подходящий эмодзи для визуализации идеи

        6. Создай детальный план реализации (4-6 фаз)

        **КРИТИЧЕСКИ ВАЖНО:**
        - Все оценки должны быть РЕАЛИСТИЧНЫМИ, не завышенными
        - Обоснования должны содержать КОНКРЕТНЫЕ данные и примеры
        - Финансовые показатели должны быть выверенными и достижимыми
        - Если нет уверенности в метрике - ставь средние значения, НЕ высокие

        **Output Format (JSON):**
        {{
            "title": "Название идеи (макс 100 символов)",
            "description": "Детальное описание (макс 500 символов)",
            "emoji": "💡",
            "category": "ai",
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
            }},
            "financial": {{
                "investment": 50000,
                "payback_months": 12,
                "margin": 30,
                "arr": 100000
            }},
            "roadmap": {{
                "phases": [
                    {{
                        "phase": 1,
                        "title": "MVP Development",
                        "duration": "3 weeks",
                        "tasks": ["Setup infrastructure", "Core API", "Basic UI"],
                        "resources": ["1 backend dev", "1 frontend dev"],
                        "budget": 15000,
                        "dependencies": []
                    }}
                ],
                "totalDuration": "3-4 months",
                "totalBudget": 50000,
                "criticalPath": [1, 2, 3]
            }},
            "budget": {{
                "categories": [
                    {{
                        "category": "Development",
                        "items": [
                            {{"name": "Senior Backend Dev", "cost": 15000, "recurring": false}},
                            {{"name": "Frontend Dev", "cost": 12000, "recurring": false}}
                        ],
                        "total": 27000
                    }}
                ],
                "totalOneTime": 45000,
                "totalMonthly": 5000,
                "breakeven": {{"months": 8, "revenue": 50000}}
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
            max_tokens=4000,  # Increased for roadmap and budget
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
            **{
                metric: {
                    "reasoning": scores[metric]["reasoning"],
                    "evidence": scores[metric]["evidence"]
                }
                for metric in scores.keys()
            },
            "roadmap": analysis.get("roadmap", {}),
            "budget": analysis.get("budget", {})
        }

        # Extract financial data
        financial = analysis.get("financial", {})

        # Determine if trending based on engagement
        is_trending = trend.engagement_score > 500 if hasattr(trend, 'engagement_score') else False

        # Create IdeaCreate schema
        idea_create = IdeaCreate(
            title=analysis["title"],
            description=analysis["description"],
            emoji=analysis.get("emoji", "💡"),
            source=trend.source if hasattr(trend, 'source') else "AI Analysis",
            category=analysis.get("category", "ai"),
            is_trending=is_trending,
            trend_id=trend.id,
            market_size_score=scores["market_size"]["score"],
            competition_score=scores["competition"]["score"],
            demand_score=scores["demand"]["score"],
            monetization_score=scores["monetization"]["score"],
            feasibility_score=scores["feasibility"]["score"],
            time_to_market_score=scores["time_to_market"]["score"],
            investment=financial.get("investment", 50000),
            payback_months=financial.get("payback_months", 12),
            margin=financial.get("margin", 30),
            arr=financial.get("arr", 100000),
            analysis=analysis_data,
            status="pending"
        )

        return {
            "total_score": total_score,
            "create_data": idea_create
        }
