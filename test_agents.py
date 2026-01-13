"""
Тест AI агентов
Запуск: python test_agents.py
"""
import asyncio
import sys
import os

# Добавить backend в path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from agents import CodeAnalystAgent, DevAgent


async def test_code_analyst():
    """Тест CodeAnalystAgent"""
    print("=" * 60)
    print("🔍 CodeAnalystAgent Test")
    print("=" * 60)

    try:
        agent = CodeAnalystAgent()

        # 1. Анализ файла
        print("\n1️⃣ Analyzing backend/main.py...")
        analysis = await agent.analyze_file("backend/main.py")

        scores = analysis['analysis']
        print(f"\n📊 Scores:")
        print(f"  Quality:        {scores['quality_score']}/100")
        print(f"  Readability:    {scores['readability_score']}/100")
        print(f"  Maintainability: {scores['maintainability_score']}/100")
        print(f"  Performance:    {scores['performance_score']}/100")

        print(f"\n✨ Strengths:")
        for strength in scores['strengths'][:3]:
            print(f"  ✓ {strength}")

        print(f"\n⚠️  Issues found: {len(scores['issues'])}")
        for issue in scores['issues'][:2]:
            print(f"  - [{issue['severity']}] {issue['description']}")

        # 2. Найти баги
        print("\n2️⃣ Finding bugs...")
        bugs = await agent.find_bugs("backend/main.py")
        print(f"🐛 Found {len(bugs)} potential bugs")

        for bug in bugs[:3]:
            print(f"  - Line {bug.get('line', '?')}: {bug['description'][:60]}...")

        # 3. Security проверка
        print("\n3️⃣ Security check...")
        security = await agent.check_security("backend/main.py")
        print(f"🔒 Security score: {security['security_score']}/100")
        print(f"🚨 Vulnerabilities: {len(security['vulnerabilities'])}")

        print("\n✅ CodeAnalystAgent test completed!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


async def test_dev_agent():
    """Тест DevAgent"""
    print("\n" + "=" * 60)
    print("🚀 DevAgent Test")
    print("=" * 60)

    try:
        agent = DevAgent()

        # 1. Генерация тестов
        print("\n1️⃣ Generating tests for backend/main.py...")
        tests = await agent.generate_tests("backend/main.py")

        print(f"✅ Test file: {tests['test_file']}")
        print(f"📝 Framework: {tests['framework']}")
        print(f"📊 Estimated coverage: {tests['estimated_coverage']}")

        # Сохранить тесты
        test_dir = os.path.dirname(tests['test_file'])
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)

        with open(tests['test_file'], 'w') as f:
            f.write(tests['test_code'])
        print(f"💾 Saved to {tests['test_file']}")

        # 2. Рефакторинг (симуляция)
        print("\n2️⃣ Refactoring example...")
        print("  (Skipping actual refactor to avoid changes)")
        print("  Would refactor with goals: ['improve performance']")

        print("\n✅ DevAgent test completed!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Главная функция"""
    print("\n" + "🤖" * 30)
    print("AI AGENTS TEST SUITE")
    print("🤖" * 30 + "\n")

    # Проверить API ключи
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    if not openai_key:
        print("⚠️  Warning: OPENAI_API_KEY not set - CodeAnalystAgent will fail")
    if not anthropic_key:
        print("⚠️  Warning: ANTHROPIC_API_KEY not set - DevAgent will fail")
    if not github_token:
        print("⚠️  Warning: GITHUB_TOKEN not set - GitHub integration will fail")

    print()

    # Запустить тесты
    await test_code_analyst()
    await test_dev_agent()

    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Загрузить .env
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

    # Запуск
    asyncio.run(main())
