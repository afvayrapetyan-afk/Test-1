"""
Code API endpoints - для работы с кодом из GitHub
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.github_service import GitHubService

router = APIRouter()


@router.get("/code/files")
async def list_files(
    path: str = Query("", description="Путь к директории"),
    branch: str = Query("main", description="Ветка")
):
    """
    Получить список файлов и папок

    Example: GET /api/code/files?path=backend&branch=main
    """
    try:
        github = GitHubService()
        tree = github.get_directory_tree(path, branch)

        return {
            "path": path,
            "branch": branch,
            "items": tree,
            "count": len(tree)
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/code/files/{file_path:path}")
async def get_file(
    file_path: str,
    branch: str = Query("main", description="Ветка")
):
    """
    Получить содержимое файла

    Example: GET /api/code/files/backend/main.py?branch=main
    """
    try:
        github = GitHubService()
        file_data = github.get_file_content(file_path, branch)

        return file_data

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/code/search")
async def search_code(
    q: str = Query(..., description="Поисковый запрос"),
    max_results: int = Query(20, ge=1, le=100, description="Максимум результатов")
):
    """
    Поиск по коду (GitHub code search)

    Example: GET /api/code/search?q=FastAPI&max_results=10
    """
    try:
        github = GitHubService()
        results = github.search_code(q, max_results)

        return {
            "query": q,
            "count": len(results),
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/code/history/{file_path:path}")
async def get_file_history(
    file_path: str,
    max_commits: int = Query(10, ge=1, le=50, description="Максимум коммитов")
):
    """
    История изменений файла

    Example: GET /api/code/history/backend/main.py?max_commits=5
    """
    try:
        github = GitHubService()
        history = github.get_file_history(file_path, max_commits)

        return {
            "file": file_path,
            "commits": history,
            "count": len(history)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/code/tree")
async def get_full_tree(
    branch: str = Query("main", description="Ветка"),
    max_depth: int = Query(3, ge=1, le=10, description="Максимальная глубина")
):
    """
    Получить полное дерево репозитория (рекурсивно)

    Example: GET /api/code/tree?branch=main&max_depth=3
    """
    try:
        github = GitHubService()

        def build_tree(path: str = "", depth: int = 0):
            """Рекурсивно построить дерево"""
            if depth >= max_depth:
                return []

            items = github.get_directory_tree(path, branch)

            for item in items:
                if item["type"] == "dir":
                    # Рекурсивно загрузить содержимое папки
                    item["children"] = build_tree(item["path"], depth + 1)

            return items

        tree = build_tree()

        return {
            "branch": branch,
            "max_depth": max_depth,
            "tree": tree
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
