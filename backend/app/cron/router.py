"""
Cron API Router
Endpoints для запуска автоматических задач
"""

from fastapi import APIRouter, HTTPException, Query, Header
from typing import Optional
import os
import asyncio

from app.cron.daily_analysis import run_daily_analysis

router = APIRouter()

# Секретный ключ для защиты cron endpoints
CRON_SECRET = os.getenv("CRON_SECRET", "your-secret-key-change-me")


@router.post("/daily-analysis")
async def trigger_daily_analysis(
    ideas_count: int = Query(5, ge=3, le=10, description="Количество идей для генерации"),
    x_cron_secret: Optional[str] = Header(None, alias="X-Cron-Secret")
):
    """
    Запустить ежедневный анализ рынка и генерацию бизнес-идей

    Этот endpoint:
    1. Анализирует текущие тренды AI рынка
    2. Генерирует 3-5 новых бизнес-идей
    3. Сохраняет идеи с высокими оценками в базу данных

    Защищён секретным ключом X-Cron-Secret
    """
    # Проверяем секретный ключ (опционально для локальной разработки)
    if CRON_SECRET != "your-secret-key-change-me":
        if x_cron_secret != CRON_SECRET:
            raise HTTPException(
                status_code=401,
                detail="Invalid or missing X-Cron-Secret header"
            )

    try:
        # Определяем URL API
        api_base_url = os.getenv(
            "API_BASE_URL",
            "https://ai-portfolio-api-czhs.onrender.com"
        )

        # Запускаем анализ
        result = await run_daily_analysis(
            api_base_url=api_base_url
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/status")
async def cron_status():
    """
    Проверить статус cron системы
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
        "api_base_url": os.getenv("API_BASE_URL", "https://ai-portfolio-api-czhs.onrender.com")
    }
