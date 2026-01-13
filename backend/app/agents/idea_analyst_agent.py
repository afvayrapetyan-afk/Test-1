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
        Проведи ГЛУБОКИЙ анализ этого тренда и создай продуманную бизнес-идею ДЛЯ РОССИЙСКОГО РЫНКА.

        **Тренд:**
        - Название: {trend.title}
        - Описание: {trend.description}
        - Источник: {trend.source}
        - Категория: {trend.category}
        - Популярность: {trend.engagement_score}
        - Теги: {', '.join(trend.tags) if trend.tags else 'N/A'}

        **КРИТИЧЕСКИ ВАЖНО - ВСЁ НА РУССКОМ ЯЗЫКЕ:**
        - Название идеи - ТОЛЬКО на русском
        - Описание - ТОЛЬКО на русском
        - Все обоснования и доказательства - ТОЛЬКО на русском

        **Требования к анализу:**

        1. ПРОВЕДИ РЕАЛЬНЫЙ АНАЛИЗ РЫНКА:
           - Проверь существующих конкурентов (особенно на российском рынке)
           - Оцени реальный размер рынка с цифрами
           - Найди КОНКРЕТНЫЕ доказательства спроса в России
           - Проанализируй успешные российские и зарубежные аналоги

        2. ОПРЕДЕЛИ АКТУАЛЬНОСТЬ ДЛЯ РОССИИ:
           - is_russia_relevant: true/false - актуально ли это ИМЕННО для российского рынка
           - Критерии актуальности для России:
             * Есть спрос в российских условиях
             * Нет сильных местных конкурентов
             * Соответствует локальным потребностям
             * Можно реализовать с учётом российских реалий
             * Подходит для российского менталитета и культуры

        3. Оцени 6 метрик (0-100) с ПОДРОБНЫМ обоснованием НА РУССКОМ:
           - market_size: Общий объем рынка в России и количество клиентов
           - competition: Уровень конкуренции на российском рынке
           - demand: Острота проблемы и спрос в России
           - monetization: Потенциал дохода с российской аудитории
           - feasibility: Техническая сложность реализации
           - time_to_market: Скорость запуска MVP

        4. Рассчитай РЕАЛИСТИЧНЫЕ финансовые показатели для России:
           - investment: Начальные инвестиции в $ (с учётом российских цен)
           - payback_months: Срок окупаемости в месяцах
           - margin: Маржинальность в %
           - arr: Годовой доход через 12 месяцев в $

        5. Категория из: ai, saas, ecommerce, fintech, health, education, entertainment

        6. Подбери ОДИН подходящий эмодзи

        **Output Format (JSON):**
        {{
            "title": "Название идеи НА РУССКОМ (макс 100 символов)",
            "description": "Описание НА РУССКОМ (макс 500 символов)",
            "emoji": "💡",
            "category": "ai",
            "is_russia_relevant": true,
            "scores": {{
                "market_size": {{
                    "score": 85,
                    "reasoning": "Обоснование НА РУССКОМ",
                    "evidence": "Доказательства НА РУССКОМ"
                }},
                "competition": {{
                    "score": 60,
                    "reasoning": "Анализ конкурентов НА РУССКОМ",
                    "evidence": "Примеры НА РУССКОМ"
                }},
                "demand": {{
                    "score": 90,
                    "reasoning": "Анализ спроса НА РУССКОМ",
                    "evidence": "Сигналы рынка НА РУССКОМ"
                }},
                "monetization": {{
                    "score": 75,
                    "reasoning": "Модель монетизации НА РУССКОМ",
                    "evidence": "Примеры НА РУССКОМ"
                }},
                "feasibility": {{
                    "score": 70,
                    "reasoning": "Сложность реализации НА РУССКОМ",
                    "evidence": "Доступные технологии НА РУССКОМ"
                }},
                "time_to_market": {{
                    "score": 80,
                    "reasoning": "Сроки разработки НА РУССКОМ",
                    "evidence": "Объём MVP НА РУССКОМ"
                }}
            }},
            "financial": {{
                "investment": 50000,
                "payback_months": 12,
                "margin": 30,
                "arr": 100000
            }}
        }}

        ВАЖНО: Все тексты ТОЛЬКО на русском языке! Никакого английского!
        """

        response = self.call_llm(
            messages=[
                {
                    "role": "system",
                    "content": "Ты эксперт по бизнес-анализу, специализирующийся на стартап-идеях для РОССИЙСКОГО рынка. Всегда отвечай ТОЛЬКО на русском языке."
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

        # Determine if relevant for Russia
        is_russia_relevant = analysis.get("is_russia_relevant", False)

        # Create IdeaCreate schema
        idea_create = IdeaCreate(
            title=analysis["title"],
            description=analysis["description"],
            emoji=analysis.get("emoji", "💡"),
            source=trend.source if hasattr(trend, 'source') else "AI Analysis",
            category=analysis.get("category", "ai"),
            is_trending=is_trending,
            is_russia_relevant=is_russia_relevant,
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
