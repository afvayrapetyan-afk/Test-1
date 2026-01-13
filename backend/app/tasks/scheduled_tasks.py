"""
Scheduled Tasks for AI Business Portfolio Manager
Автоматические задачи для регулярного обновления данных
"""

from celery import Celery
from celery.schedules import crontab
import asyncio
import os
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

# Celery Configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@celery_app.task(name='discover_trends')
def discover_trends_task():
    """
    Автоматический поиск трендов
    Запускается каждые 6 часов
    """
    print("🔍 Starting automated trend discovery...")

    db = SessionLocal()
    try:
        trend_agent = TrendScoutAgent(db)

        # Запускаем поиск трендов
        async def run():
            execution = await trend_agent.run({
                "sources": ["reddit"],
                "categories": ["technology", "business", "ai", "saas", "fintech"],
                "limit": 10  # Увеличено до 10 трендов
            })
            return execution

        execution = asyncio.run(run())

        print(f"✅ Trends discovered: {execution.output_data.get('trends_count', 0)}")
        print(f"💰 Cost: ${float(execution.llm_cost_usd):.4f}")

        return {
            "status": "success",
            "trends_count": execution.output_data.get('trends_count', 0),
            "cost": float(execution.llm_cost_usd)
        }

    except Exception as e:
        print(f"❌ Error discovering trends: {e}")
        return {"status": "error", "message": str(e)}

    finally:
        db.close()


@celery_app.task(name='analyze_ideas')
def analyze_ideas_task():
    """
    Автоматический анализ трендов и генерация бизнес-идей
    Запускается каждые 12 часов
    """
    print("💡 Starting automated idea analysis...")

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
        for idea in all_ideas.items:
            analyzed_trend_ids.add(idea.trend_id)

        unanalyzed_trends = [
            t for t in all_trends.items
            if t.id not in analyzed_trend_ids
        ]

        print(f"📊 Found {len(unanalyzed_trends)} unanalyzed trends")

        # Анализируем до 5 новых трендов за раз
        trends_to_analyze = unanalyzed_trends[:5]
        ideas_generated = 0
        total_cost = 0.0

        for trend in trends_to_analyze:
            print(f"🔬 Analyzing: {trend.title}")

            async def run():
                execution = await idea_agent.run({
                    "trend_ids": [trend.id]
                })
                return execution

            execution = asyncio.run(run())

            if execution.status == "completed":
                count = execution.output_data.get('ideas_count', 0)
                ideas_generated += count
                total_cost += float(execution.llm_cost_usd)
                print(f"   ✅ Generated {count} idea(s)")

        print(f"✅ Total ideas generated: {ideas_generated}")
        print(f"💰 Total cost: ${total_cost:.4f}")

        return {
            "status": "success",
            "ideas_generated": ideas_generated,
            "cost": total_cost
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
celery_app.conf.beat_schedule = {
    # Поиск трендов каждый день в 9:00 UTC
    'discover-trends-daily': {
        'task': 'discover_trends',
        'schedule': crontab(minute=0, hour=9),  # 9:00 утра каждый день
    },

    # Анализ идей каждый день в 9:30 UTC (после поиска трендов)
    'analyze-ideas-daily': {
        'task': 'analyze_ideas',
        'schedule': crontab(minute=30, hour=9),  # 9:30 утра каждый день
    },

    # Очистка данных раз в неделю (воскресенье в 03:00)
    'cleanup-weekly': {
        'task': 'cleanup_old_data',
        'schedule': crontab(minute=0, hour=3, day_of_week=0),
    },
}
