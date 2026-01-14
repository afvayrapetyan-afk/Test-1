"""
Idea Analyst Agent
Analyzes trends and generates AI-focused business ideas

ФОКУС: AI-помощники и агенты, решающие РЕАЛЬНЫЕ проблемы бизнеса и физлиц
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
    Idea Analyst Agent - Generates AI-FOCUSED business ideas

    🎯 КЛЮЧЕВОЙ ФОКУС:
    - AI-помощники (assistants) для физлиц и бизнеса
    - AI-агенты для автоматизации задач
    - Решение РЕАЛЬНЫХ проблем (не выдуманных)
    - Проверенные данные из нескольких источников

    Scoring metrics (0-100 each):
    1. Market Size - Total addressable market potential
    2. Competition - Level of existing competition (lower = better)
    3. Demand - Current demand and pain point severity
    4. Monetization - Revenue potential and business model viability
    5. Feasibility - Technical and operational feasibility
    6. Time to Market - Speed of MVP development and launch

    Process:
    1. Fetch trends from database
    2. Analyze with focus on AI solutions
    3. Verify data from multiple sources
    4. Generate AI assistant/agent ideas
    5. Score each idea on 6 metrics
    6. Store verified ideas in database
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
        🎯 ЗАДАЧА: Создай бизнес-идею на базе AI-ПОМОЩНИКА или AI-АГЕНТА

        **Анализируемый тренд:**
        - Название: {trend.title}
        - Описание: {trend.description}
        - Источник: {trend.source}
        - Категория: {trend.category}
        - Популярность: {trend.engagement_score}
        - Теги: {', '.join(trend.tags) if trend.tags else 'N/A'}

        ═══════════════════════════════════════════════════════════════
        🤖 ФОКУС: AI-ПОМОЩНИКИ И АГЕНТЫ
        ═══════════════════════════════════════════════════════════════

        Твоя задача - найти РЕАЛЬНУЮ ПРОБЛЕМУ, которую AI может решить.
        Не придумывай проблемы - ищи те, которые уже существуют!

        **ТИП AI-РЕШЕНИЯ (выбери один):**

        1. 🤖 AI-АССИСТЕНТ (помощник):
           - Помогает человеку выполнять задачи
           - Отвечает на вопросы, даёт рекомендации
           - Примеры: персональный финансовый советник, AI-репетитор

        2. 🔄 AI-АГЕНТ (автономный):
           - Выполняет задачи самостоятельно
           - Минимум участия человека
           - Примеры: агент для бронирования, агент для мониторинга цен

        3. 🛠️ AI-ИНСТРУМЕНТ (утилита):
           - Специализированный инструмент для конкретной задачи
           - Примеры: генератор контента, анализатор документов

        ═══════════════════════════════════════════════════════════════
        📊 ТРЕБОВАНИЯ К АНАЛИЗУ (ПЕРЕПРОВЕРЬ ДАННЫЕ!)
        ═══════════════════════════════════════════════════════════════

        **1. РЕАЛЬНАЯ ПРОБЛЕМА (обязательно):**
        ❓ Какую конкретную проблему решает AI?
        ❓ Кто страдает от этой проблемы? (бизнес/физлица)
        ❓ Как сейчас люди решают эту проблему без AI?
        ❓ Почему AI решит это лучше?

        **2. ПОДТВЕРЖДЕНИЕ СПРОСА (с доказательствами):**
        ✓ Поисковые запросы (тренды Google)
        ✓ Обсуждения в социальных сетях
        ✓ Существующие решения и их популярность
        ✓ Статистика рынка (цифры!)

        **3. АКТУАЛЬНОСТЬ ДЛЯ РЕГИОНОВ:**

        🇷🇺 **Россия** (is_russia_relevant):
        - Есть спрос на российском рынке
        - Можно оплатить без международных карт
        - Работает с учётом санкций
        - Нет сильных местных конкурентов

        🇦🇲 **Армения** (is_armenia_relevant):
        - Подходит для рынка в 3 млн человек
        - Учитывает армянскую диаспору (10+ млн)
        - IT-хаб региона (потенциал)

        🌍 **Глобально** (is_global_relevant):
        - Универсальная проблема
        - Можно масштабировать

        **4. ФИНАНСЫ (реалистичные для региона):**
        - investment: Сколько нужно на MVP ($)
        - payback_months: Когда окупится
        - margin: Маржа бизнеса (%)
        - arr: Доход через год ($)

        ═══════════════════════════════════════════════════════════════
        📝 ФОРМАТ ОТВЕТА (JSON, ВСЁ НА РУССКОМ!)
        ═══════════════════════════════════════════════════════════════

        {{
            "title": "AI-помощник для [чего] / AI-агент для [чего]",
            "description": "Решает проблему [какую] для [кого] путём [как]",
            "emoji": "🤖",
            "category": "ai",
            "ai_type": "assistant|agent|tool",
            "problem_solved": "Конкретная проблема, которую решает",
            "target_audience": "Кто целевая аудитория",
            "is_russia_relevant": true,
            "is_armenia_relevant": false,
            "is_global_relevant": true,
            "scores": {{
                "market_size": {{
                    "score": 85,
                    "reasoning": "Размер рынка с цифрами",
                    "evidence": "Источники данных"
                }},
                "competition": {{
                    "score": 60,
                    "reasoning": "Какие есть конкуренты",
                    "evidence": "Названия и доли рынка"
                }},
                "demand": {{
                    "score": 90,
                    "reasoning": "Доказательства спроса",
                    "evidence": "Поисковые запросы, обсуждения"
                }},
                "monetization": {{
                    "score": 75,
                    "reasoning": "Как будет зарабатывать",
                    "evidence": "Модель и цены"
                }},
                "feasibility": {{
                    "score": 70,
                    "reasoning": "Технически реализуемо?",
                    "evidence": "Какие технологии нужны"
                }},
                "time_to_market": {{
                    "score": 80,
                    "reasoning": "Сроки MVP",
                    "evidence": "Что нужно сделать"
                }}
            }},
            "financial": {{
                "investment": 50000,
                "payback_months": 12,
                "margin": 30,
                "arr": 100000
            }}
        }}

        ⚠️ ВСЕ ТЕКСТЫ ТОЛЬКО НА РУССКОМ ЯЗЫКЕ!
        ⚠️ НЕ ВЫДУМЫВАЙ ДАННЫЕ - ИСПОЛЬЗУЙ РЕАЛЬНЫЕ!
        """

        response = self.call_llm(
            messages=[
                {
                    "role": "system",
                    "content": """Ты эксперт по AI-продуктам и бизнес-анализу. Твоя специализация:

🎯 ФОКУС: AI-помощники и AI-агенты для бизнеса и физлиц

Твои принципы:
1. РЕАЛЬНЫЕ ПРОБЛЕМЫ - не выдумывай, ищи существующие
2. ПРОВЕРЕННЫЕ ДАННЫЕ - используй статистику и исследования
3. AI КАК РЕШЕНИЕ - объясни, почему именно AI нужен
4. РЕГИОНАЛЬНАЯ СПЕЦИФИКА - учитывай особенности РФ, Армении, мира

Всегда отвечай ТОЛЬКО на русском языке.
Никогда не выдумывай цифры - лучше скажи "нет данных"."""
                },
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o",  # GPT-4 для глубокого анализа
            temperature=0.5,  # Меньше креативности, больше точности
            max_tokens=4000,
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

        # Determine region relevance
        is_russia_relevant = analysis.get("is_russia_relevant", False)
        is_armenia_relevant = analysis.get("is_armenia_relevant", False)
        is_global_relevant = analysis.get("is_global_relevant", True)

        # Create IdeaCreate schema
        idea_create = IdeaCreate(
            title=analysis["title"],
            description=analysis["description"],
            emoji=analysis.get("emoji", "💡"),
            source=trend.source if hasattr(trend, 'source') else "AI Analysis",
            category=analysis.get("category", "ai"),
            is_trending=is_trending,
            is_russia_relevant=is_russia_relevant,
            is_armenia_relevant=is_armenia_relevant,
            is_global_relevant=is_global_relevant,
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
