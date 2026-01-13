# 🤖 AI Agents Guide

Полное руководство по использованию AI агентов

---

## Обзор агентов

### 1. CodeAnalystAgent (GPT-4o)
**Назначение:** Анализ качества кода, поиск багов, security audit

**Возможности:**
- ✅ Анализ файла (quality score, readability, maintainability)
- ✅ Поиск потенциальных багов
- ✅ Рекомендации по улучшению
- ✅ Security проверка (OWASP Top 10)

### 2. DevAgent (Claude Opus 4.5)
**Назначение:** Автоматическая разработка кода

**Возможности:**
- ✅ Реализация фичей (auto-PR)
- ✅ Рефакторинг кода
- ✅ Генерация тестов
- ✅ Исправление багов

---

## 🚀 Quick Start

### 1. Setup API Keys

```bash
# .env
OPENAI_API_KEY=sk-proj-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
```

### 2. Использование через API

#### CodeAnalystAgent

**Анализ файла:**
```bash
curl -X POST http://localhost:8000/api/agents/code-analyst/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "backend/main.py",
    "branch": "main"
  }'
```

**Ответ:**
```json
{
  "status": "success",
  "data": {
    "file": "backend/main.py",
    "analysis": {
      "quality_score": 85,
      "readability_score": 90,
      "maintainability_score": 80,
      "performance_score": 85,
      "strengths": [
        "Clear structure and organization",
        "Good error handling",
        "Well-documented functions"
      ],
      "issues": [
        {
          "type": "performance",
          "severity": "medium",
          "description": "Potential N+1 query issue",
          "line": 42,
          "recommendation": "Use eager loading with joins"
        }
      ],
      "refactoring_suggestions": [...]
    }
  }
}
```

**Поиск багов:**
```bash
curl -X POST http://localhost:8000/api/agents/code-analyst/find-bugs \
  -H "Content-Type: application/json" \
  -d '{"file_path": "backend/services/github_service.py"}'
```

**Security проверка:**
```bash
curl -X POST http://localhost:8000/api/agents/code-analyst/security \
  -H "Content-Type: application/json" \
  -d '{"file_path": "backend/api/auth.py"}'
```

---

#### DevAgent

**Реализовать фичу:**
```bash
curl -X POST http://localhost:8000/api/agents/dev-agent/implement \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Add rate limiting to API endpoints",
    "create_pr": true
  }'
```

**Ответ:**
```json
{
  "status": "success",
  "data": {
    "description": "Add rate limiting to API endpoints",
    "branch": "feature/add-rate-limiting-to-api-endpoints",
    "files_modified": 3,
    "files": [
      {"path": "backend/middleware/rate_limit.py", "sha": "abc123"},
      {"path": "backend/main.py", "sha": "def456"},
      {"path": "backend/tests/test_rate_limit.py", "sha": "ghi789"}
    ],
    "pr": {
      "number": 42,
      "title": "Feature: Add rate limiting to API endpoints",
      "url": "https://github.com/user/repo/pull/42"
    }
  }
}
```

**Рефакторинг:**
```bash
curl -X POST http://localhost:8000/api/agents/dev-agent/refactor \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "backend/services/old_code.py",
    "goals": ["improve performance", "reduce complexity"]
  }'
```

**Генерация тестов:**
```bash
curl -X POST http://localhost:8000/api/agents/dev-agent/generate-tests \
  -H "Content-Type": application/json" \
  -d '{"file_path": "backend/api/code.py"}'
```

---

### 3. Использование в Python коде

```python
from backend.agents import CodeAnalystAgent, DevAgent

# CodeAnalystAgent
async def analyze_project():
    agent = CodeAnalystAgent()

    # Полный анализ файла
    analysis = await agent.analyze_file("backend/main.py")
    print(f"Quality score: {analysis['analysis']['quality_score']}")

    # Поиск багов
    bugs = await agent.find_bugs("backend/main.py")
    print(f"Found {len(bugs)} potential bugs")

    # Security проверка
    security = await agent.check_security("backend/api/auth.py")
    print(f"Security score: {security['security_score']}")


# DevAgent
async def implement_features():
    agent = DevAgent()

    # Реализовать фичу
    result = await agent.implement_feature(
        description="Add user authentication with JWT",
        create_pr=True
    )
    print(f"PR created: {result['pr']['url']}")

    # Генерировать тесты
    tests = await agent.generate_tests("backend/api/users.py")
    print(f"Tests generated: {tests['test_file']}")

    # Рефакторинг
    refactored = await agent.refactor_code(
        "backend/old_module.py",
        goals=["improve readability", "add type hints"]
    )
    print(f"Refactored: {refactored['refactored_lines']} lines")


# Запуск
import asyncio
asyncio.run(analyze_project())
asyncio.run(implement_features())
```

---

## 📊 Use Cases

### Case 1: Code Review Automation

```python
# Автоматический review всех файлов в PR

async def review_pr(pr_number: int):
    """Review all files in a PR"""
    agent = CodeAnalystAgent()

    # Get PR files (через GitHub API)
    files = get_pr_files(pr_number)

    reviews = []
    for file in files:
        analysis = await agent.analyze_file(file['path'])
        reviews.append({
            "file": file['path'],
            "score": analysis['analysis']['quality_score'],
            "issues": analysis['analysis']['issues']
        })

    # Post review comment
    post_review_comment(pr_number, reviews)
```

### Case 2: Automated Feature Development

```python
# Автоматическая разработка фичи от идеи до PR

async def auto_implement(feature_description: str):
    """Полностью автоматическая реализация фичи"""

    # 1. DevAgent реализует фичу
    dev_agent = DevAgent()
    result = await dev_agent.implement_feature(
        description=feature_description,
        create_pr=False  # Сначала без PR
    )

    # 2. CodeAnalystAgent проверяет код
    analyst = CodeAnalystAgent()
    for file_info in result['files']:
        analysis = await analyst.analyze_file(file_info['path'])

        if analysis['analysis']['quality_score'] < 70:
            # Плохой код - рефакторим
            refactored = await dev_agent.refactor_code(
                file_info['path'],
                goals=["improve quality"]
            )

    # 3. Генерируем тесты
    for file_info in result['files']:
        tests = await dev_agent.generate_tests(file_info['path'])

    # 4. Создаём PR
    pr = create_pr(result['branch'], result['files'])

    return pr
```

### Case 3: Security Audit Pipeline

```python
# Регулярный security audit всего кода

async def security_audit():
    """Аудит безопасности всех файлов"""

    agent = CodeAnalystAgent()
    vulnerabilities = []

    # Найти все Python файлы
    files = find_all_python_files()

    for file_path in files:
        report = await agent.check_security(file_path)

        # Собрать критичные уязвимости
        critical = [
            v for v in report['vulnerabilities']
            if v['severity'] == 'critical'
        ]

        if critical:
            vulnerabilities.extend(critical)

    # Создать issue в GitHub для каждой уязвимости
    for vuln in vulnerabilities:
        create_github_issue(
            title=f"Security: {vuln['type']}",
            body=f"File: {vuln['file']}\n{vuln['description']}"
        )
```

---

## 🎯 Best Practices

### 1. Использование CodeAnalystAgent

✅ **DO:**
- Анализировать код перед merge
- Регулярно проверять на security
- Использовать для code review
- Искать баги в legacy коде

❌ **DON'T:**
- Анализировать генерируемый код (vendor/, node_modules/)
- Полагаться только на AI (нужен human review)
- Игнорировать рекомендации высокого приоритета

### 2. Использование DevAgent

✅ **DO:**
- Давать чёткие описания фичей
- Указывать target_files если известны
- Проверять generated код перед merge
- Генерировать тесты для критичных функций

❌ **DON'T:**
- Коммитить без review
- Использовать для критичных security-related изменений без проверки
- Генерировать код для production без тестирования

---

## 💡 Advanced Features

### Semantic Code Search

```python
# Агенты используют semantic search для поиска релевантных файлов

agent = DevAgent()

# Agent автоматически найдёт релевантные файлы
await agent.implement_feature(
    "Add caching to API responses"
    # Агент сам найдёт API endpoints через semantic search
)
```

### Context-Aware Generation

```python
# Агенты понимают контекст проекта

agent = DevAgent()

# Agent прочитает существующие auth файлы и создаст согласованный код
await agent.implement_feature(
    "Add OAuth2 authentication alongside existing JWT"
)
```

### Automatic PR Creation

```python
# DevAgent автоматически создаёт PR

result = await agent.implement_feature(
    "Add rate limiting",
    create_pr=True  # Auto-create PR
)

print(f"Review PR: {result['pr']['url']}")
```

---

## 📈 Monitoring & Costs

### API Usage Tracking

```python
# Track LLM API calls

@router.post("/agents/code-analyst/analyze")
async def analyze_code(request: AnalyzeFileRequest):
    start_time = time.time()

    agent = CodeAnalystAgent()
    result = await agent.analyze_file(...)

    # Log usage
    log_api_usage(
        agent="CodeAnalystAgent",
        method="analyze_file",
        duration=time.time() - start_time,
        tokens_used=estimate_tokens(result)
    )

    return result
```

### Cost Estimates

**CodeAnalystAgent (GPT-4o):**
- Analyze file: ~$0.02-0.05 per file
- Find bugs: ~$0.01-0.03 per file
- Security check: ~$0.03-0.06 per file

**DevAgent (Claude Opus 4.5):**
- Implement feature: ~$0.10-0.50 per feature
- Refactor code: ~$0.05-0.15 per file
- Generate tests: ~$0.03-0.10 per file

**Monthly estimates** (для активного проекта):
- 100 analyses/month: ~$3-5
- 20 features/month: ~$5-10
- 50 test generations: ~$2-5
- **Total: ~$10-20/month**

---

## 🔧 Troubleshooting

### API ключи не работают

```bash
# Проверить статус агентов
curl http://localhost:8000/api/agents/status

# Должен вернуть:
{
  "agents": [...],
  "api_keys": {
    "openai": true,
    "anthropic": true
  }
}
```

### Agent возвращает ошибку

```python
# Обработка ошибок

try:
    result = await agent.analyze_file("path.py")
except FileNotFoundError:
    print("File not found in GitHub")
except Exception as e:
    print(f"Agent error: {e}")
```

---

## 📚 API Reference

См. полную документацию: http://localhost:8000/docs

**Endpoints:**
- `POST /api/agents/code-analyst/analyze`
- `POST /api/agents/code-analyst/find-bugs`
- `POST /api/agents/code-analyst/improvements`
- `POST /api/agents/code-analyst/security`
- `POST /api/agents/dev-agent/implement`
- `POST /api/agents/dev-agent/refactor`
- `POST /api/agents/dev-agent/generate-tests`
- `GET /api/agents/status`

---

**Версия:** 1.0
**Дата:** 2026-01-13
**Статус:** ✅ Production Ready
