"""
Scheduled Tasks for AI Business Portfolio Manager
Автоматические задачи для регулярного обновления данных

ФОКУС: AI-помощники и агенты, решающие реальные проблемы бизнеса и физлиц
Анализ: широкий и глубокий с перепроверкой данных
"""

from celery import Celery
from celery.schedules import crontab
import asyncio
import os
from datetime import datetime
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.agents.trend_scout_agent import TrendScoutAgent
from app.agents.idea_analyst_agent import IdeaAnalystAgent
from app.modules.trends.service import TrendService
from app.modules.ideas.service import IdeaService

# Initialize Celery with Redis from environment
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

celery_app = Celery(
    'ai_portfolio_tasks',
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Celery Configuration - Moscow timezone (UTC+3)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',  # Московское время
    enable_utc=False,
)

# Фокусные категории для поиска AI-решений
AI_FOCUS_CATEGORIES = [
    "ai_assistants",      # AI-помощники
    "ai_agents",          # AI-агенты
    "automation",         # Автоматизация процессов
    "productivity",       # Продуктивность
    "customer_service",   # Клиентский сервис
    "data_analysis",      # Анализ данных
    "content_creation",   # Создание контента
    "business_ops",       # Бизнес-операции
]

# Источники данных для трендов
TREND_SOURCES = [
    "reddit",
    "producthunt",
    "hackernews",
    "twitter",
    "google_trends",
]


@celery_app.task(name='discover_trends')
def discover_trends_task():
    """
    Автоматический поиск трендов для AI-помощников и агентов
    Запускается каждое утро в 6:00 (чтобы к 9:00 были готовы идеи)

    ФОКУС:
    - Реальные проблемы бизнеса и физлиц
    - Как AI может решить эти проблемы
    - Проверенные данные из нескольких источников
    """
    print(f"🔍 [{datetime.now()}] Starting AI-focused trend discovery...")
    print("📌 Focus: AI assistants & agents solving real problems")

    db = SessionLocal()
    try:
        trend_agent = TrendScoutAgent(db)

        # Запускаем поиск трендов с фокусом на AI
        async def run():
            execution = await trend_agent.run({
                "sources": TREND_SOURCES,
                "categories": AI_FOCUS_CATEGORIES,
                "focus": "ai_solutions",  # Фокус на AI-решениях
                "limit": 15,  # Больше трендов для анализа
                "verify_data": True,  # Перепроверка данных
            })
            return execution

        execution = asyncio.run(run())

        trends_count = execution.output_data.get('trends_count', 0)
        print(f"✅ AI trends discovered: {trends_count}")
        print(f"💰 Cost: ${float(execution.llm_cost_usd):.4f}")

        return {
            "status": "success",
            "trends_count": trends_count,
            "cost": float(execution.llm_cost_usd),
            "focus": "ai_assistants_agents",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"❌ Error discovering trends: {e}")
        return {"status": "error", "message": str(e)}

    finally:
        db.close()


@celery_app.task(name='analyze_ideas')
def analyze_ideas_task():
    """
    Глубокий анализ трендов и генерация AI бизнес-идей
    Запускается каждое утро в 7:00 (готово к 9:00)

    КРИТЕРИИ АНАЛИЗА:
    1. Реальная проблема/потребность (не выдуманная)
    2. AI/агент может решить эту проблему эффективно
    3. Есть подтверждённый спрос (данные, исследования)
    4. Реалистичная монетизация
    5. Актуальность для РФ/Армении/Мира
    """
    print(f"💡 [{datetime.now()}] Starting deep AI idea analysis...")
    print("🎯 Criteria: Real problems + AI solutions + Verified data")

    db = SessionLocal()
    try:
        trend_service = TrendService(db)
        idea_service = IdeaService(db)
        idea_agent = IdeaAnalystAgent(db)

        # Получаем тренды без идей (еще не проанализированные)
        all_trends = trend_service.get_trends(skip=0, limit=100)

        # Находим тренды, которые еще не анализировались
        analyzed_trend_ids = set()
        all_ideas = idea_service.get_ideas(skip=0, limit=1000)
        for idea in all_ideas.get('items', []):
            if hasattr(idea, 'trend_id'):
                analyzed_trend_ids.add(idea.trend_id)
            elif isinstance(idea, dict):
                analyzed_trend_ids.add(idea.get('trend_id'))

        unanalyzed_trends = [
            t for t in all_trends.get('items', [])
            if (t.id if hasattr(t, 'id') else t.get('id')) not in analyzed_trend_ids
        ]

        print(f"📊 Found {len(unanalyzed_trends)} unanalyzed trends")

        # Анализируем до 10 новых трендов за раз
        trends_to_analyze = unanalyzed_trends[:10]
        ideas_generated = 0
        total_cost = 0.0
        verified_ideas = 0

        for trend in trends_to_analyze:
            trend_title = trend.title if hasattr(trend, 'title') else trend.get('title', 'Unknown')
            trend_id = trend.id if hasattr(trend, 'id') else trend.get('id')
            print(f"🔬 Deep analyzing: {trend_title}")

            async def run():
                execution = await idea_agent.run({
                    "trend_ids": [trend_id],
                    "focus": "ai_assistants_agents",
                    "verify_data": True,
                    "deep_analysis": True,
                })
                return execution

            execution = asyncio.run(run())

            if execution.status == "completed":
                count = execution.output_data.get('ideas_count', 0)
                verified = execution.output_data.get('verified_count', count)
                ideas_generated += count
                verified_ideas += verified
                total_cost += float(execution.llm_cost_usd)
                print(f"   ✅ Generated {count} idea(s), {verified} verified")

        print(f"✅ Total ideas generated: {ideas_generated}")
        print(f"✓ Verified ideas: {verified_ideas}")
        print(f"💰 Total cost: ${total_cost:.4f}")

        return {
            "status": "success",
            "ideas_generated": ideas_generated,
            "verified_ideas": verified_ideas,
            "cost": total_cost,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"❌ Error analyzing ideas: {e}")
        return {"status": "error", "message": str(e)}

    finally:
        db.close()


@celery_app.task(name='cleanup_old_data')
def cleanup_old_data_task():
    """
    Очистка старых данных (опционально)
    Запускается раз в неделю
    """
    print("🧹 Starting data cleanup...")

    # TODO: Implement cleanup logic
    # - Удаление трендов старше 90 дней с низким engagement
    # - Архивация старых идей

    return {"status": "success", "message": "Cleanup completed"}


# Celery Beat Schedule - расписание автоматических задач
# Время: Московское (Europe/Moscow)
celery_app.conf.beat_schedule = {
    # 1. Поиск трендов каждый день в 6:00 (чтобы к 9:00 были идеи)
    'discover-trends-morning': {
        'task': 'discover_trends',
        'schedule': crontab(minute=0, hour=6),  # 6:00 утра МСК
        'options': {'queue': 'trends'}
    },

    # 2. Глубокий анализ и генерация идей в 7:00
    'analyze-ideas-morning': {
        'task': 'analyze_ideas',
        'schedule': crontab(minute=0, hour=7),  # 7:00 утра МСК
        'options': {'queue': 'ideas'}
    },

    # 3. Дополнительный анализ вечером (для свежих вечерних трендов)
    'analyze-ideas-evening': {
        'task': 'analyze_ideas',
        'schedule': crontab(minute=0, hour=19),  # 19:00 МСК
        'options': {'queue': 'ideas'}
    },

    # 4. Очистка данных раз в неделю (воскресенье в 03:00)
    'cleanup-weekly': {
        'task': 'cleanup_old_data',
        'schedule': crontab(minute=0, hour=3, day_of_week=0),
    },
}


# ===== MANUAL TRIGGER FUNCTION =====
# Для запуска анализа вручную (не через Celery)

def run_morning_analysis_now():
    """
    Запустить утренний анализ прямо сейчас (без Celery)
    Использование: python -c "from app.tasks.scheduled_tasks import run_morning_analysis_now; run_morning_analysis_now()"
    """
    print("🌅 Starting manual morning analysis...")
    print("=" * 50)

    # 1. Поиск трендов
    print("\n📍 Step 1: Discovering AI trends...")
    trends_result = discover_trends_task()
    print(f"   Result: {trends_result}")

    # 2. Анализ и генерация идей
    print("\n📍 Step 2: Analyzing and generating AI ideas...")
    ideas_result = analyze_ideas_task()
    print(f"   Result: {ideas_result}")

    print("\n" + "=" * 50)
    print("✅ Morning analysis completed!")
    print(f"   Trends: {trends_result.get('trends_count', 0)}")
    print(f"   Ideas: {ideas_result.get('ideas_generated', 0)}")

    return {
        "trends": trends_result,
        "ideas": ideas_result
    }
