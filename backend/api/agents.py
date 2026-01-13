"""
Agents API - для управления AI агентами
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional, List
from pydantic import BaseModel
from agents.code_analyst_agent import CodeAnalystAgent
from agents.dev_agent import DevAgent
import os

router = APIRouter()


# Pydantic models
class AnalyzeFileRequest(BaseModel):
    """Запрос на анализ файла"""
    file_path: str
    branch: str = "main"


class FindBugsRequest(BaseModel):
    """Запрос на поиск багов"""
    file_path: str


class SecurityCheckRequest(BaseModel):
    """Запрос на проверку безопасности"""
    file_path: str


class ImplementFeatureRequest(BaseModel):
    """Запрос на реализацию фичи"""
    description: str
    target_files: Optional[List[str]] = None
    create_pr: bool = True


class RefactorRequest(BaseModel):
    """Запрос на рефакторинг"""
    file_path: str
    goals: List[str]


class GenerateTestsRequest(BaseModel):
    """Запрос на генерацию тестов"""
    file_path: str


# CodeAnalystAgent endpoints

@router.post("/agents/code-analyst/analyze")
async def analyze_code(request: AnalyzeFileRequest):
    """
    Полный анализ файла

    Возвращает:
    - Quality score (0-100)
    - Readability score
    - Potential bugs
    - Security issues
    - Refactoring suggestions
    """
    try:
        agent = CodeAnalystAgent()
        result = await agent.analyze_file(request.file_path, request.branch)

        return {
            "status": "success",
            "data": result
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/code-analyst/find-bugs")
async def find_bugs(request: FindBugsRequest):
    """
    Найти потенциальные баги в коде
    """
    try:
        agent = CodeAnalystAgent()
        bugs = await agent.find_bugs(request.file_path)

        return {
            "status": "success",
            "file": request.file_path,
            "bugs_found": len(bugs),
            "bugs": bugs
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/code-analyst/improvements")
async def suggest_improvements(request: FindBugsRequest):
    """
    Получить рекомендации по улучшению кода
    """
    try:
        agent = CodeAnalystAgent()
        improvements = await agent.suggest_improvements(request.file_path)

        return {
            "status": "success",
            "file": request.file_path,
            "improvements": improvements
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/code-analyst/security")
async def check_security(request: SecurityCheckRequest):
    """
    Проверка кода на уязвимости безопасности
    """
    try:
        agent = CodeAnalystAgent()
        security_report = await agent.check_security(request.file_path)

        return {
            "status": "success",
            "file": request.file_path,
            "security_report": security_report
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# DevAgent endpoints

@router.post("/agents/dev-agent/implement")
async def implement_feature(request: ImplementFeatureRequest, background_tasks: BackgroundTasks):
    """
    Реализовать новую фичу

    Process:
    1. Находит релевантные файлы
    2. Генерирует код
    3. Создаёт ветку
    4. Коммитит изменения
    5. Создаёт Pull Request
    """
    try:
        agent = DevAgent()

        # Запустить в фоне если задача долгая
        result = await agent.implement_feature(
            description=request.description,
            target_files=request.target_files,
            create_pr=request.create_pr
        )

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/dev-agent/refactor")
async def refactor_code(request: RefactorRequest):
    """
    Рефакторинг кода

    Goals examples:
    - "improve performance"
    - "reduce complexity"
    - "add type hints"
    - "improve readability"
    """
    try:
        agent = DevAgent()
        result = await agent.refactor_code(request.file_path, request.goals)

        return {
            "status": "success",
            "data": result
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/dev-agent/generate-tests")
async def generate_tests(request: GenerateTestsRequest):
    """
    Генерировать unit tests для файла
    """
    try:
        agent = DevAgent()
        result = await agent.generate_tests(request.file_path)

        return {
            "status": "success",
            "data": result
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# General endpoints

@router.get("/agents/status")
async def get_agents_status():
    """Статус всех агентов и их возможностей"""

    # Проверить доступность API ключей
    openai_available = bool(os.getenv("OPENAI_API_KEY"))
    anthropic_available = bool(os.getenv("ANTHROPIC_API_KEY"))

    return {
        "agents": [
            {
                "name": "CodeAnalystAgent",
                "status": "active" if openai_available else "inactive",
                "model": "GPT-4o",
                "capabilities": [
                    "analyze_file",
                    "find_bugs",
                    "suggest_improvements",
                    "security_check"
                ],
                "api_configured": openai_available
            },
            {
                "name": "DevAgent",
                "status": "active" if anthropic_available else "inactive",
                "model": "Claude Opus 4.5",
                "capabilities": [
                    "implement_feature",
                    "refactor_code",
                    "generate_tests",
                    "fix_bug"
                ],
                "api_configured": anthropic_available
            }
        ],
        "api_keys": {
            "openai": openai_available,
            "anthropic": anthropic_available
        }
    }
