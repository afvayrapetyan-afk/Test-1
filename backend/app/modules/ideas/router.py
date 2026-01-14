"""
Ideas API Router
Endpoints for business idea analysis and management
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.modules.ideas.service import IdeaService
from app.modules.ideas.schemas import (
    IdeaCreate, IdeaUpdate, IdeaOut, IdeaDetailedOut, IdeaList, IdeaListFrontend, IdeaStats
)

router = APIRouter()


class AnalyzeRequest(BaseModel):
    """Request model for analyzing trends"""
    trend_ids: List[int]


@router.get("/", response_model=IdeaListFrontend)
async def get_ideas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    min_score: Optional[int] = Query(None, ge=0, le=100),
    status: Optional[str] = None,
    trend_id: Optional[int] = None,
    category: Optional[str] = Query(None, description="Filter by category: ai, saas, ecommerce, fintech, health, education, entertainment"),
    is_trending: Optional[bool] = Query(None, description="Filter trending ideas only"),
    sort_by: str = Query("date", regex="^(date|score)$", description="Sort by: date or score"),
    db: Session = Depends(get_db)
):
    """
    Get list of business ideas

    Parameters:
    - skip: Number of records to skip
    - limit: Maximum number of records
    - min_score: Minimum total score filter
    - status: Filter by status (pending, approved, rejected, etc.)
    - trend_id: Filter by specific trend
    - category: Filter by category (ai, saas, ecommerce, fintech, health, education, entertainment)
    - is_trending: Show only trending ideas
    - sort_by: Sort by date (default) or score
    """
    service = IdeaService(db)
    return service.get_ideas(
        skip=skip,
        limit=limit,
        min_score=min_score,
        status=status,
        trend_id=trend_id,
        category=category,
        is_trending=is_trending,
        sort_by=sort_by
    )


@router.get("/{idea_id}", response_model=IdeaDetailedOut)
async def get_idea(
    idea_id: int,
    db: Session = Depends(get_db)
):
    """
    Get single idea with full analysis
    """
    service = IdeaService(db)
    idea = service.get_idea(idea_id, detailed=True)

    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Idea with id {idea_id} not found"
        )

    return idea


@router.post("/", response_model=IdeaOut, status_code=status.HTTP_201_CREATED)
async def create_idea(
    idea_data: IdeaCreate,
    db: Session = Depends(get_db)
):
    """
    Create new idea manually
    """
    service = IdeaService(db)
    return service.create_idea(idea_data)


@router.put("/{idea_id}", response_model=IdeaOut)
async def update_idea(
    idea_id: int,
    idea_data: IdeaUpdate,
    db: Session = Depends(get_db)
):
    """
    Update existing idea
    """
    service = IdeaService(db)
    idea = service.update_idea(idea_id, idea_data)

    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Idea with id {idea_id} not found"
        )

    return idea


@router.delete("/{idea_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_idea(
    idea_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete idea
    """
    service = IdeaService(db)
    success = service.delete_idea(idea_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Idea with id {idea_id} not found"
        )


@router.get("/stats", response_model=IdeaStats)
async def get_ideas_stats(db: Session = Depends(get_db)):
    """
    Get aggregated statistics for ideas
    """
    service = IdeaService(db)
    return service.get_stats()


@router.post("/analyze")
async def analyze_trends(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze trends and generate business ideas

    This is an async operation that triggers AI agents.
    Returns a job ID for tracking progress.
    """
    # TODO: Trigger Celery task for analysis

    return {
        "success": True,
        "data": {
            "job_id": "analysis-job-12345",
            "status": "pending",
            "trend_count": len(request.trend_ids),
            "message": "Analysis started. Check /api/v1/agents/executions for progress"
        }
    }


@router.post("/{idea_id}/favorite")
async def toggle_favorite(
    idea_id: int,
    db: Session = Depends(get_db)
):
    """
    Toggle favorite status for an idea
    """
    service = IdeaService(db)
    idea = service.toggle_favorite(idea_id)

    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Idea with id {idea_id} not found"
        )

    return {
        "success": True,
        "data": idea
    }


@router.post("/{idea_id}/dislike")
async def toggle_dislike(
    idea_id: int,
    db: Session = Depends(get_db)
):
    """
    Toggle dislike status for an idea.
    Disliked ideas appear at the end of any sorting.
    """
    service = IdeaService(db)
    idea = service.toggle_dislike(idea_id)

    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Idea with id {idea_id} not found"
        )

    return {
        "success": True,
        "data": idea
    }
