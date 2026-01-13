"""
Trends API Router
Endpoints for trend discovery and management
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.modules.trends.service import TrendService
from app.modules.trends.schemas import TrendCreate, TrendUpdate, TrendOut, TrendList, TrendStats

router = APIRouter()


@router.get("/", response_model=TrendList)
async def get_trends(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    source: Optional[str] = None,
    min_engagement: Optional[int] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    """
    Get list of trends

    Parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum number of records to return
    - category: Filter by category (tech, saas, marketplace, etc.)
    - source: Filter by source (reddit, google_trends, telegram, etc.)
    - min_engagement: Minimum engagement score filter
    """
    service = TrendService(db)
    return service.get_trends(
        skip=skip,
        limit=limit,
        category=category,
        source=source,
        min_engagement=min_engagement
    )


@router.get("/{trend_id}", response_model=TrendOut)
async def get_trend(
    trend_id: int,
    db: Session = Depends(get_db)
):
    """
    Get single trend by ID
    """
    service = TrendService(db)
    trend = service.get_trend(trend_id)

    if not trend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trend with id {trend_id} not found"
        )

    return trend


@router.get("/stats", response_model=TrendStats)
async def get_trends_stats(db: Session = Depends(get_db)):
    """
    Get aggregated statistics for trends
    """
    service = TrendService(db)
    return service.get_stats()


@router.post("/", response_model=TrendOut, status_code=status.HTTP_201_CREATED)
async def create_trend(
    trend_data: TrendCreate,
    db: Session = Depends(get_db)
):
    """
    Create new trend

    Includes automatic duplicate detection based on title and URL
    """
    service = TrendService(db)
    return service.create_trend(trend_data)


@router.put("/{trend_id}", response_model=TrendOut)
async def update_trend(
    trend_id: int,
    trend_data: TrendUpdate,
    db: Session = Depends(get_db)
):
    """
    Update existing trend
    """
    service = TrendService(db)
    trend = service.update_trend(trend_id, trend_data)

    if not trend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trend with id {trend_id} not found"
        )

    return trend


@router.delete("/{trend_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trend(
    trend_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete trend
    """
    service = TrendService(db)
    success = service.delete_trend(trend_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trend with id {trend_id} not found"
        )


@router.post("/search", response_model=TrendList)
async def search_trends(
    query: str = Query(..., min_length=3),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Search trends using full-text search

    Parameters:
    - query: Search query (minimum 3 characters)
    - skip: Number of records to skip (pagination)
    - limit: Maximum number of records to return
    """
    service = TrendService(db)
    return service.search_trends(query=query, skip=skip, limit=limit)
