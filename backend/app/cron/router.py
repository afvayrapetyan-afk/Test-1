"""
Cron API Router
Endpoints для запуска автоматических задач
"""

from fastapi import APIRouter, HTTPException, Query, Header
from typing import Optional
import os
import asyncio
from datetime import datetime
import structlog

from app.cron.daily_analysis import run_daily_analysis

router = APIRouter()
logger = structlog.get_logger()

# Секретный ключ для защиты cron endpoints
CRON_SECRET = os.getenv("CRON_SECRET", "your-secret-key-change-me")

# Хранение статуса последнего запуска
_last_run_status = {
    "running": False,
    "last_started": None,
    "last_completed": None,
    "last_result": None
}


async def _run_analysis_background():
    """Фоновая задача для генерации идей"""
    global _last_run_status

    try:
        api_base_url = os.getenv(
            "API_BASE_URL",
            "https://ai-portfolio-api-czhs.onrender.com"
        )

        result = await run_daily_analysis(api_base_url=api_base_url)

        _last_run_status["last_completed"] = datetime.now().isoformat()
        _last_run_status["last_result"] = {
            "success": True,
            "ideas_saved": result.get("saved_count", 0),
            "ideas_generated": result.get("ideas_generated", 0)
        }
        logger.info("✅ Background analysis completed", result=_last_run_status["last_result"])

    except Exception as e:
        _last_run_status["last_completed"] = datetime.now().isoformat()
        _last_run_status["last_result"] = {"success": False, "error": str(e)}
        logger.error("❌ Background analysis failed", error=str(e))
    finally:
        _last_run_status["running"] = False


@router.post("/daily-analysis")
async def trigger_daily_analysis(
    ideas_count: int = Query(5, ge=3, le=10, description="Количество идей для генерации"),
    x_cron_secret: Optional[str] = Header(None, alias="X-Cron-Secret"),
    wait: bool = Query(False, description="Ждать завершения (для тестирования)")
):
    """
    Запустить ежедневный анализ рынка и генерацию бизнес-идей

    По умолчанию запускает в фоне и сразу возвращает ответ (для cron-job.org).
    Добавьте ?wait=true чтобы дождаться результата.
    """
    global _last_run_status

    # Если уже запущено - не запускать повторно
    if _last_run_status["running"]:
        return {
            "success": True,
            "message": "Analysis already running",
            "started_at": _last_run_status["last_started"]
        }

    _last_run_status["running"] = True
    _last_run_status["last_started"] = datetime.now().isoformat()

    if wait:
        # Синхронный режим - ждём результат (для тестирования)
        try:
            api_base_url = os.getenv(
                "API_BASE_URL",
                "https://ai-portfolio-api-czhs.onrender.com"
            )
            result = await run_daily_analysis(api_base_url=api_base_url)
            _last_run_status["running"] = False
            _last_run_status["last_completed"] = datetime.now().isoformat()
            _last_run_status["last_result"] = {"success": True, "data": result}
            return {"success": True, "data": result}
        except Exception as e:
            _last_run_status["running"] = False
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    else:
        # Асинхронный режим - запускаем в фоне, сразу отвечаем
        asyncio.create_task(_run_analysis_background())

        return {
            "success": True,
            "message": "Analysis started in background",
            "started_at": _last_run_status["last_started"],
            "check_status": "/api/v1/cron/status"
        }


@router.get("/status")
async def cron_status():
    """
    Проверить статус cron системы и последний запуск
    """
    return {
        "status": "active",
        "scheduled_tasks": [
            {
                "name": "daily-analysis",
                "schedule": "0 9 * * *",
                "description": "Ежедневный анализ рынка и генерация идей в 9:00 МСК"
            }
        ],
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "api_base_url": os.getenv("API_BASE_URL", "https://ai-portfolio-api-czhs.onrender.com"),
        "last_run": {
            "is_running": _last_run_status["running"],
            "started_at": _last_run_status["last_started"],
            "completed_at": _last_run_status["last_completed"],
            "result": _last_run_status["last_result"]
        }
    }


@router.post("/migrate")
async def run_migration():
    """
    Запустить миграцию базы данных для добавления новых колонок
    """
    from app.core.database import engine
    from sqlalchemy import text

    results = []

    with engine.connect() as conn:
        # Add is_favorite column
        try:
            conn.execute(text("ALTER TABLE ideas ADD COLUMN is_favorite INTEGER DEFAULT 0"))
            conn.commit()
            results.append("Added is_favorite column")
        except Exception as e:
            results.append(f"is_favorite: {str(e)}")

        # Add is_disliked column
        try:
            conn.execute(text("ALTER TABLE ideas ADD COLUMN is_disliked INTEGER DEFAULT 0"))
            conn.commit()
            results.append("Added is_disliked column")
        except Exception as e:
            results.append(f"is_disliked: {str(e)}")

        # Create indexes
        try:
            conn.execute(text("CREATE INDEX idx_ideas_is_favorite ON ideas(is_favorite)"))
            conn.commit()
            results.append("Created index idx_ideas_is_favorite")
        except Exception as e:
            results.append(f"idx_ideas_is_favorite: {str(e)}")

        try:
            conn.execute(text("CREATE INDEX idx_ideas_is_disliked ON ideas(is_disliked)"))
            conn.commit()
            results.append("Created index idx_ideas_is_disliked")
        except Exception as e:
            results.append(f"idx_ideas_is_disliked: {str(e)}")

    return {
        "success": True,
        "results": results
    }
