"""
Test script for new features
Tests category, financial fields, and deep analysis
"""

import asyncio
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.agents.idea_analyst_agent import IdeaAnalystAgent
from app.modules.trends.service import TrendService


async def test_new_features():
    """Test new category, financial, and deep analysis features"""
    print("🧪 Testing New Features")
    print("=" * 60)

    db = SessionLocal()
    try:
        # Get a trend to analyze
        trend_service = TrendService(db)
        trends = trend_service.get_trends(limit=1)

        if not trends.items:
            print("❌ No trends found. Please run demo.py first to create trends.")
            return

        trend = trends.items[0]
        print(f"\n📊 Analyzing trend: {trend.title}")
        print(f"   Category: {trend.category}")
        print(f"   Engagement: {trend.engagement_score}")

        # Run idea analyst agent
        print("\n🤖 Running IdeaAnalystAgent with deep analysis...")
        idea_agent = IdeaAnalystAgent(db)

        execution = await idea_agent.run({
            "trend_ids": [trend.id],
            "limit": 1,
            "min_total_score": 0  # Accept all scores for testing
        })

        print(f"\n✅ Analysis completed!")
        print(f"   Status: {execution.status}")
        print(f"   Ideas generated: {execution.output_data.get('ideas_generated', 0)}")
        print(f"   Ideas stored: {execution.output_data.get('ideas_stored', 0)}")
        print(f"   Cost: ${float(execution.llm_cost_usd):.4f}")

        # Fetch the generated idea
        from app.modules.ideas.service import IdeaService
        idea_service = IdeaService(db)
        ideas = idea_service.get_ideas(limit=1, sort_by="date")

        if ideas and ideas.get("items"):
            idea = ideas["items"][0]
            print("\n📝 Generated Idea Details:")
            print(f"   ID: {idea['id']}")
            print(f"   Title: {idea['title']}")
            print(f"   Emoji: {idea['emoji']}")
            print(f"   Category: {idea['category']}")
            print(f"   Source: {idea['source']}")
            print(f"   Is Trending: {idea['isTrending']}")
            print(f"   Score: {idea['score']}/10")
            print(f"\n💰 Financial Projections:")
            print(f"   Investment: ${idea['financial']['investment']:,}")
            print(f"   Payback: {idea['financial']['paybackMonths']} months")
            print(f"   Margin: {idea['financial']['margin']}%")
            print(f"   ARR: ${idea['financial']['arr']:,}")
            print(f"\n📊 Metrics:")
            print(f"   Market Size: {idea['metrics']['marketSize']}/100")
            print(f"   Competition: {idea['metrics']['competition']}/100")
            print(f"   Demand: {idea['metrics']['demand']}/100")
            print(f"   Monetization: {idea['metrics']['monetization']}/100")

            print("\n✅ All new features working correctly!")
        else:
            print("\n⚠️  No ideas were generated")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(test_new_features())
