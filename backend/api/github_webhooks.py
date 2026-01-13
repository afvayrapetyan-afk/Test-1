"""
GitHub Webhooks - для получения событий от GitHub
"""
from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
import hmac
import hashlib
import os

router = APIRouter()


async def verify_signature(payload: bytes, signature: str) -> bool:
    """
    Проверить подпись webhook от GitHub

    Args:
        payload: Тело запроса
        signature: Подпись из заголовка X-Hub-Signature-256

    Returns:
        True если подпись валидна
    """
    webhook_secret = os.getenv("GITHUB_WEBHOOK_SECRET")
    if not webhook_secret:
        # Если секрет не установлен, пропускаем проверку (dev mode)
        return True

    # Вычислить HMAC
    expected_signature = "sha256=" + hmac.new(
        webhook_secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, signature)


@router.post("/github")
async def github_webhook(
    request: Request,
    x_github_event: Optional[str] = Header(None),
    x_hub_signature_256: Optional[str] = Header(None)
):
    """
    Webhook endpoint для событий от GitHub

    Events:
    - push: код изменён
    - pull_request: PR создан/обновлён
    - issues: issue создан/обновлён
    """

    # Получить тело запроса
    payload = await request.body()
    data = await request.json()

    # Проверить подпись
    if x_hub_signature_256:
        if not await verify_signature(payload, x_hub_signature_256):
            raise HTTPException(status_code=401, detail="Invalid signature")

    # Обработать событие
    event_type = x_github_event

    if event_type == "push":
        return await handle_push_event(data)

    elif event_type == "pull_request":
        return await handle_pr_event(data)

    elif event_type == "issues":
        return await handle_issue_event(data)

    return {"status": "ok", "event": event_type}


async def handle_push_event(data: dict):
    """
    Обработать push event

    Actions:
    1. Синхронизировать изменённые файлы
    2. Обновить vector embeddings
    3. Уведомить frontend через WebSocket
    """
    ref = data.get("ref")  # refs/heads/main
    commits = data.get("commits", [])

    # TODO: Sync changed files
    # TODO: Update vector store
    # TODO: Broadcast to WebSocket clients

    return {
        "status": "processed",
        "event": "push",
        "ref": ref,
        "commits_count": len(commits)
    }


async def handle_pr_event(data: dict):
    """
    Обработать pull request event

    Actions:
    1. Анализировать изменения через CodeAnalystAgent
    2. Добавить комментарий с ревью
    """
    action = data.get("action")  # opened, closed, synchronized
    pr_number = data["pull_request"]["number"]
    pr_title = data["pull_request"]["title"]

    # TODO: Analyze PR with CodeAnalystAgent
    # TODO: Post review comment

    return {
        "status": "processed",
        "event": "pull_request",
        "action": action,
        "pr": pr_number,
        "title": pr_title
    }


async def handle_issue_event(data: dict):
    """
    Обработать issues event

    Actions:
    1. Проверить, это задача для агента?
    2. Создать task для DevAgent
    """
    action = data.get("action")  # opened, closed
    issue_number = data["issue"]["number"]
    issue_title = data["issue"]["title"]

    # TODO: Parse issue and create agent task

    return {
        "status": "processed",
        "event": "issues",
        "action": action,
        "issue": issue_number,
        "title": issue_title
    }
