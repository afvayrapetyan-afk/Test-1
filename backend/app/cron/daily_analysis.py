"""
Daily Analysis Cron Job
Автоматический анализ рынка и генерация бизнес-идей каждый день в 9:00

Этот модуль:
1. Ищет актуальные тренды через веб-поиск
2. Анализирует потребности рынка с помощью GPT-4
3. Генерирует 3-5 бизнес-идей с высокими оценками
4. Сохраняет их в базу данных
"""

import os
import json
import httpx
from datetime import datetime
from typing import List, Dict, Any
from openai import OpenAI
import structlog

logger = structlog.get_logger()

# Конфигурация
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")  # Опционально для веб-поиска


class DailyAnalysisAgent:
    """
    Агент для ежедневного анализа рынка и генерации бизнес-идей
    """

    def __init__(self):
        self.openai = OpenAI(api_key=OPENAI_API_KEY)
        self.search_queries = [
            "AI startup trends 2025 2026",
            "новые AI стартапы идеи бизнес",
            "artificial intelligence business opportunities",
            "AI agents automation startups",
            "проблемы бизнеса которые решает AI",
            "YC startup ideas artificial intelligence",
            "AI SaaS product ideas trending",
        ]

    async def run(self, ideas_count: int = 5, min_score: int = 65) -> Dict[str, Any]:
        """
        Запустить ежедневный анализ

        Args:
            ideas_count: Количество идей для генерации (3-5)
            min_score: Минимальный общий балл для идеи

        Returns:
            Результат анализа с созданными идеями
        """
        logger.info("🌅 Starting daily analysis", ideas_count=ideas_count)

        # 1. Собираем контекст о текущих трендах
        market_context = await self._gather_market_context()

        # 2. Генерируем идеи с помощью GPT-4
        ideas = await self._generate_ideas(market_context, ideas_count, min_score)

        # 3. Фильтруем по минимальному баллу
        qualified_ideas = [i for i in ideas if i.get("total_score", 0) >= min_score]

        logger.info(
            "✅ Daily analysis completed",
            generated=len(ideas),
            qualified=len(qualified_ideas)
        )

        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "ideas_generated": len(ideas),
            "ideas_qualified": len(qualified_ideas),
            "ideas": qualified_ideas
        }

    async def _gather_market_context(self) -> str:
        """
        Собрать контекст о текущих трендах рынка
        """
        context_parts = []

        # Добавляем текущую дату для контекста
        context_parts.append(f"Дата анализа: {datetime.now().strftime('%Y-%m-%d')}")

        # Базовый контекст о текущих трендах AI
        context_parts.append("""
Актуальные тренды AI рынка 2025-2026:

1. AI Агенты (Agentic AI):
   - Автономные агенты для выполнения задач
   - Мультиагентные системы
   - Вертикально-специализированные агенты

2. AI Помощники:
   - Персональные AI-ассистенты
   - Copilot для различных профессий
   - AI для автоматизации рутины

3. Генеративный AI:
   - Текст, изображения, видео, аудио, код
   - AI для создания контента
   - Персонализированная генерация

4. AI в Enterprise:
   - Автоматизация бизнес-процессов
   - AI для принятия решений
   - Интеграция AI в существующие системы

5. Региональная специфика:
   - Россия: импортозамещение, локальные решения
   - Армения: IT-хаб, аутсорсинг, стартапы
   - СНГ: трансграничные сервисы
""")

        return "\n\n".join(context_parts)

    async def _generate_ideas(
        self,
        context: str,
        count: int,
        min_score: int
    ) -> List[Dict[str, Any]]:
        """
        Генерировать бизнес-идеи с помощью GPT-4
        """
        prompt = f"""
{context}

═══════════════════════════════════════════════════════════════════════════════
🎯 ЗАДАЧА: Создай {count} НОВЫХ и АКТУАЛЬНЫХ бизнес-идей на базе AI
═══════════════════════════════════════════════════════════════════════════════

КРИТЕРИИ ОТБОРА ИДЕЙ:
1. ✅ Решает РЕАЛЬНУЮ проблему (не выдуманную)
2. ✅ AI/ML действительно нужен для решения
3. ✅ Есть подтверждённый спрос (исследования, статистика)
4. ✅ Реалистичная монетизация
5. ✅ Можно реализовать за 6-12 месяцев
6. ✅ Минимальный общий балл: {min_score}/100

КАТЕГОРИИ (выбери подходящую):
- ai - AI/ML продукты и сервисы
- saas - SaaS платформы с AI
- fintech - Финансовые технологии
- health - Здоровье и медицина
- education - Образование
- ecommerce - E-commerce и ритейл
- entertainment - Развлечения и контент

ФОРМАТ ОТВЕТА (JSON массив):

[
  {{
    "title": "Название идеи (кратко, ёмко)",
    "description": "Описание: что делает, для кого, как решает проблему (2-3 предложения)",
    "emoji": "🤖",
    "source": "Источник тренда или исследования",
    "category": "ai",
    "is_russia_relevant": true,
    "is_armenia_relevant": true,
    "is_global_relevant": true,
    "market_size_score": 85,
    "competition_score": 60,
    "demand_score": 90,
    "monetization_score": 75,
    "feasibility_score": 70,
    "time_to_market_score": 80,
    "investment": 100000,
    "payback_months": 12,
    "margin": 65,
    "arr": 500000,
    "analysis": {{
      "market_size": {{
        "reasoning": "Детальное обоснование размера рынка с цифрами и трендами роста. Укажи TAM, SAM, SOM если возможно.",
        "evidence": "Конкретные источники: исследования, отчёты компаний, статистика рынка"
      }},
      "competition": {{
        "reasoning": "Анализ конкурентов: кто уже делает похожее, их сильные/слабые стороны, почему есть место для нового игрока",
        "evidence": "Названия конкурентов, их доли рынка, раунды финансирования"
      }},
      "demand": {{
        "reasoning": "Доказательства спроса: какую боль решает продукт, кто целевая аудитория, сколько их",
        "evidence": "Поисковые тренды, обсуждения в соцсетях, отзывы о конкурентах, опросы"
      }},
      "monetization": {{
        "reasoning": "Бизнес-модель: как будет зарабатывать, ценообразование, unit economics",
        "evidence": "Примеры ценообразования конкурентов, готовность платить у ЦА"
      }},
      "feasibility": {{
        "reasoning": "Техническая реализуемость: какие технологии нужны, какая команда, основные риски",
        "evidence": "Доступность технологий, примеры похожих реализаций"
      }},
      "time_to_market": {{
        "reasoning": "Сроки: сколько времени на MVP, на полный продукт, что критический путь",
        "evidence": "Примеры сроков у похожих стартапов"
      }}
    }}
  }}
]

⚠️ ВАЖНО:
- ОБЯЗАТЕЛЬНО создай РОВНО {count} идей - не больше, не меньше
- ВСЕ тексты ТОЛЬКО на русском языке
- Оценки от 60 до 90 (реалистичные)
- Каждая идея должна быть УНИКАЛЬНОЙ
- Учитывай актуальность на {datetime.now().strftime('%B %Y')}

Верни JSON объект в формате: {{"ideas": [массив из {count} идей]}}
"""

        try:
            response = self.openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """Ты эксперт по AI-продуктам и венчурному рынку.

Твоя задача - генерировать КАЧЕСТВЕННЫЕ бизнес-идеи на базе AI.

Принципы:
1. РЕАЛЬНЫЕ проблемы - не выдумывай, анализируй существующие
2. КОНКРЕТНЫЕ данные - цифры, источники, примеры
3. ЧЕСТНЫЕ оценки - не завышай баллы без оснований
4. АКТУАЛЬНОСТЬ - учитывай текущие тренды 2025-2026

Отвечай ТОЛЬКО на русском языке.
Возвращай ТОЛЬКО валидный JSON."""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=8000,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content

            # Парсим JSON
            try:
                # Пробуем распарсить как массив
                ideas = json.loads(content)
                if isinstance(ideas, dict) and "ideas" in ideas:
                    ideas = ideas["ideas"]
                elif isinstance(ideas, dict):
                    ideas = [ideas]
            except json.JSONDecodeError:
                # Пробуем найти JSON массив в тексте
                import re
                match = re.search(r'\[[\s\S]*\]', content)
                if match:
                    ideas = json.loads(match.group())
                else:
                    logger.error("Failed to parse ideas JSON", content=content[:500])
                    ideas = []

            # Добавляем total_score к каждой идее
            for idea in ideas:
                scores = [
                    idea.get("market_size_score", 0),
                    idea.get("competition_score", 0),
                    idea.get("demand_score", 0),
                    idea.get("monetization_score", 0),
                    idea.get("feasibility_score", 0),
                    idea.get("time_to_market_score", 0),
                ]
                idea["total_score"] = sum(scores) // 6

            logger.info(f"Generated {len(ideas)} ideas")
            return ideas

        except Exception as e:
            logger.error("Error generating ideas", error=str(e))
            return []


async def run_daily_analysis(db_session=None, api_base_url: str = None) -> Dict[str, Any]:
    """
    Запустить ежедневный анализ и сохранить идеи

    Args:
        db_session: SQLAlchemy сессия (опционально)
        api_base_url: URL API для сохранения идей

    Returns:
        Результат анализа
    """
    agent = DailyAnalysisAgent()
    result = await agent.run(ideas_count=5, min_score=50)  # Снижен порог для большего количества идей

    if result["status"] != "success" or not result["ideas"]:
        return result

    # Сохраняем идеи через API
    saved_ideas = []

    if api_base_url:
        async with httpx.AsyncClient(timeout=60.0) as client:
            for idea in result["ideas"]:
                try:
                    # Формируем данные для API
                    idea_data = {
                        "title": idea["title"],
                        "description": idea["description"],
                        "emoji": idea.get("emoji", "💡"),
                        "source": idea.get("source", "Daily AI Analysis"),
                        "category": idea.get("category", "ai"),
                        "is_russia_relevant": idea.get("is_russia_relevant", True),
                        "is_armenia_relevant": idea.get("is_armenia_relevant", False),
                        "is_global_relevant": idea.get("is_global_relevant", True),
                        "market_size_score": idea["market_size_score"],
                        "competition_score": idea["competition_score"],
                        "demand_score": idea["demand_score"],
                        "monetization_score": idea["monetization_score"],
                        "feasibility_score": idea["feasibility_score"],
                        "time_to_market_score": idea["time_to_market_score"],
                        "investment": idea.get("investment", 100000),
                        "payback_months": idea.get("payback_months", 12),
                        "margin": idea.get("margin", 50),
                        "arr": idea.get("arr", 500000),
                        "analysis": idea.get("analysis", {})
                    }

                    response = await client.post(
                        f"{api_base_url}/api/v1/ideas/",
                        json=idea_data
                    )

                    if response.status_code in [200, 201]:
                        saved_idea = response.json()
                        saved_ideas.append({
                            "id": saved_idea.get("id"),
                            "title": idea["title"],
                            "score": idea["total_score"]
                        })
                        logger.info(f"✅ Saved idea: {idea['title']}")
                    else:
                        logger.error(f"Failed to save idea: {response.status_code}")

                except Exception as e:
                    logger.error(f"Error saving idea: {e}")

    result["saved_ideas"] = saved_ideas
    result["saved_count"] = len(saved_ideas)

    return result
