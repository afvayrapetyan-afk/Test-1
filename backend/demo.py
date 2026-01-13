#!/usr/bin/env python3
"""
Demo script to populate the AI Business Portfolio Manager with real data
Запускает AI агенты и наполняет систему данными
"""

import asyncio
import sys
from sqlalchemy.orm import Session

# Add backend to path
sys.path.insert(0, '/Users/vardanajrapetan/Project 1/backend')

from app.core.database import SessionLocal, init_db
from app.agents.trend_scout_agent import TrendScoutAgent
from app.agents.idea_analyst_agent import IdeaAnalystAgent
from app.modules.trends.service import TrendService
from app.modules.ideas.service import IdeaService


async def main():
    """Main demo function"""
    print("=" * 80)
    print("🚀 AI Business Portfolio Manager - Demo")
    print("=" * 80)
    print()

    # Initialize database
    print("📊 Initializing database...")
    init_db()
    print("✅ Database initialized")
    print()

    # Create database session
    db = SessionLocal()

    try:
        # Step 1: Run TrendScoutAgent
        print("=" * 80)
        print("🔍 STEP 1: Running TrendScoutAgent to discover trends")
        print("=" * 80)
        print()

        trend_agent = TrendScoutAgent(db)

        # Discover trends from multiple sources
        print("🌐 Discovering trends from Reddit (AI-generated)...")
        execution = await trend_agent.run({
            "sources": ["reddit"],
            "categories": ["technology", "business", "ai"],
            "limit": 5
        })

        print(f"✅ TrendScoutAgent completed!")
        print(f"   Status: {execution.status}")
        print(f"   Trends discovered: {execution.output_data.get('trends_count', 0)}")
        print(f"   Tokens used: {execution.llm_tokens_used}")
        print(f"   Cost: ${float(execution.llm_cost_usd):.4f}")
        print()

        # Get all trends
        trend_service = TrendService(db)
        idea_service = IdeaService(db)
        trends_list = trend_service.get_trends(skip=0, limit=100)

        print(f"📋 Total trends in database: {trends_list.total}")
        print()

        if trends_list.total > 0:
            print("Top 3 trends:")
            for i, trend in enumerate(trends_list.items[:3], 1):
                print(f"   {i}. {trend.title}")
                print(f"      Source: {trend.source} | Score: {trend.engagement_score}")
                print()

        # Step 2: Run IdeaAnalystAgent
        if trends_list.total > 0:
            print("=" * 80)
            print("💡 STEP 2: Running IdeaAnalystAgent to analyze trends")
            print("=" * 80)
            print()

            idea_agent = IdeaAnalystAgent(db)

            # Analyze first 3 trends
            trends_to_analyze = min(3, trends_list.total)
            print(f"🔬 Analyzing top {trends_to_analyze} trends...")
            print()

            for i, trend in enumerate(trends_list.items[:trends_to_analyze], 1):
                print(f"Analyzing trend {i}/{trends_to_analyze}: {trend.title[:60]}...")

                execution = await idea_agent.run({
                    "trend_ids": [trend.id]
                })

                if execution.status == "completed":
                    ideas_generated = execution.output_data.get('ideas_count', 0)
                    print(f"   ✅ Generated {ideas_generated} idea(s)")
                    print(f"   💰 Cost: ${float(execution.llm_cost_usd):.4f}")
                else:
                    print(f"   ❌ Failed: {execution.error}")
                print()

            # Get all ideas
            ideas_list = idea_service.get_ideas(skip=0, limit=100)

            print("=" * 80)
            print(f"💼 RESULTS: Total business ideas generated: {ideas_list.total}")
            print("=" * 80)
            print()

            if ideas_list.total > 0:
                print("Top business ideas:")
                for i, idea in enumerate(sorted(ideas_list.items, key=lambda x: x.total_score, reverse=True)[:5], 1):
                    print(f"\n{i}. {idea.title}")
                    print(f"   Total Score: {idea.total_score}/100")
                    print(f"   Scores:")
                    print(f"      • Market Size: {idea.market_size_score}/100")
                    print(f"      • Competition: {idea.competition_score}/100")
                    print(f"      • Demand: {idea.demand_score}/100")
                    print(f"      • Monetization: {idea.monetization_score}/100")
                    print(f"      • Feasibility: {idea.feasibility_score}/100")
                    print(f"      • Time to Market: {idea.time_to_market_score}/100")
                    print(f"   Status: {idea.status}")
                print()

        # Summary
        print("=" * 80)
        print("✨ DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print("🌐 Access the API:")
        print("   • Swagger UI: http://localhost:8000/docs")
        print("   • Health: http://localhost:8000/health")
        print("   • Trends: http://localhost:8000/api/v1/trends/")
        print("   • Ideas: http://localhost:8000/api/v1/ideas/")
        print()
        print("📊 View data in database:")
        print(f"   • Database file: /Users/vardanajrapetan/Project 1/backend/business_portfolio.db")
        print(f"   • Total trends: {trends_list.total}")
        print(f"   • Total ideas: {idea_service.get_ideas(skip=0, limit=1).total}")
        print()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
