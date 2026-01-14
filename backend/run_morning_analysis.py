#!/usr/bin/env python3
"""
Morning Analysis Runner
Запуск утреннего анализа AI-трендов вручную

Использование:
    python run_morning_analysis.py

Этот скрипт:
1. Ищет свежие AI-тренды
2. Генерирует бизнес-идеи на базе AI-помощников/агентов
3. Сохраняет результаты в базу данных
"""

import asyncio
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.agents.trend_scout_agent import TrendScoutAgent
from app.agents.idea_analyst_agent import IdeaAnalystAgent


async def run_trend_discovery(db):
    """Поиск AI-трендов"""
    print("\n" + "=" * 60)
    print("📍 ШАГ 1: Поиск AI-трендов")
    print("=" * 60)

    agent = TrendScoutAgent(db)

    execution = await agent.run({
        "sources": ["reddit"],
        "limit": 15,
        "focus": "ai_solutions",
    })

    trends_count = execution.output_data.get('trends_stored', 0)
    cost = float(execution.llm_cost_usd)

    print(f"✅ Найдено трендов: {trends_count}")
    print(f"💰 Стоимость: ${cost:.4f}")

    return {
        "trends_count": trends_count,
        "cost": cost
    }


async def run_idea_generation(db):
    """Генерация AI бизнес-идей"""
    print("\n" + "=" * 60)
    print("📍 ШАГ 2: Генерация AI бизнес-идей")
    print("=" * 60)
    print("🎯 Фокус: AI-помощники и агенты для реальных проблем")

    agent = IdeaAnalystAgent(db)

    execution = await agent.run({
        "limit": 10,
        "min_total_score": 60,
        "focus": "ai_assistants_agents",
    })

    ideas_count = execution.output_data.get('ideas_stored', 0)
    avg_score = execution.output_data.get('avg_score', 0)
    top_idea = execution.output_data.get('top_idea')
    cost = float(execution.llm_cost_usd)

    print(f"✅ Сгенерировано идей: {ideas_count}")
    print(f"📊 Средний скор: {avg_score}")
    if top_idea:
        print(f"🏆 Лучшая идея: {top_idea.get('title', 'N/A')} (скор: {top_idea.get('score', 0)})")
    print(f"💰 Стоимость: ${cost:.4f}")

    return {
        "ideas_count": ideas_count,
        "avg_score": avg_score,
        "top_idea": top_idea,
        "cost": cost
    }


async def main():
    """Главная функция утреннего анализа"""
    print("\n" + "🌅" * 30)
    print(f"\n🤖 УТРЕННИЙ AI-АНАЛИЗ")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "🌅" * 30)

    db = SessionLocal()
    total_cost = 0.0

    try:
        # 1. Поиск трендов
        trends_result = await run_trend_discovery(db)
        total_cost += trends_result["cost"]

        # 2. Генерация идей
        ideas_result = await run_idea_generation(db)
        total_cost += ideas_result["cost"]

        # Итоги
        print("\n" + "=" * 60)
        print("📊 ИТОГИ УТРЕННЕГО АНАЛИЗА")
        print("=" * 60)
        print(f"🔍 Трендов найдено: {trends_result['trends_count']}")
        print(f"💡 Идей сгенерировано: {ideas_result['ideas_count']}")
        print(f"📈 Средний скор идей: {ideas_result['avg_score']}")
        print(f"💰 Общая стоимость: ${total_cost:.4f}")
        print("\n✅ Анализ завершён! Сайт обновлён свежими AI-идеями.")

        return {
            "status": "success",
            "trends": trends_result,
            "ideas": ideas_result,
            "total_cost": total_cost
        }

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        return {"status": "error", "message": str(e)}

    finally:
        db.close()


if __name__ == "__main__":
    result = asyncio.run(main())

    if result["status"] == "success":
        print("\n🎉 Готово к 9:00!")
        sys.exit(0)
    else:
        print(f"\n💥 Ошибка: {result.get('message', 'Unknown error')}")
        sys.exit(1)
