"""
Trends Service - Business Logic Layer
"""

from sqlalchemy.orm import Session
from typing import List, Optional
import structlog

from app.modules.trends.repository import TrendRepository
from app.modules.trends.schemas import TrendCreate, TrendUpdate, TrendOut, TrendList, TrendStats
from app.modules.trends.models import Trend

logger = structlog.get_logger()


class TrendService:
    """
    Business logic for trends
    Orchestrates between repository and API
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = TrendRepository(db)

    def get_trends(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        source: Optional[str] = None,
        min_engagement: Optional[int] = None
    ) -> TrendList:
        """
        Get paginated list of trends with filters
        """
        trends, total = self.repository.get_many(
            skip=skip,
            limit=limit,
            category=category,
            source=source,
            min_engagement=min_engagement
        )

        has_more = (skip + limit) < total

        return TrendList(
            items=[TrendOut.model_validate(t) for t in trends],
            total=total,
            skip=skip,
            limit=limit,
            has_more=has_more
        )

    def get_trend(self, trend_id: int) -> Optional[TrendOut]:
        """Get single trend by ID"""
        trend = self.repository.get_by_id(trend_id)
        if not trend:
            return None

        return TrendOut.model_validate(trend)

    def create_trend(self, trend_data: TrendCreate) -> TrendOut:
        """
        Create new trend

        Includes duplicate detection
        """
        # Check for duplicates
        existing = self.repository.check_duplicate(
            title=trend_data.title,
            url=trend_data.url
        )

        if existing:
            logger.warning(
                "Duplicate trend detected",
                title=trend_data.title,
                existing_id=existing.id
            )
            # Return existing trend instead of creating duplicate
            return TrendOut.model_validate(existing)

        # Create new trend
        trend = self.repository.create(trend_data)

        logger.info(
            "Trend created",
            trend_id=trend.id,
            source=trend.source,
            category=trend.category
        )

        return TrendOut.model_validate(trend)

    def update_trend(self, trend_id: int, trend_data: TrendUpdate) -> Optional[TrendOut]:
        """Update existing trend"""
        trend = self.repository.update(trend_id, trend_data)
        if not trend:
            logger.warning("Trend not found for update", trend_id=trend_id)
            return None

        logger.info("Trend updated", trend_id=trend_id)
        return TrendOut.model_validate(trend)

    def delete_trend(self, trend_id: int) -> bool:
        """Delete trend"""
        success = self.repository.delete(trend_id)
        if success:
            logger.info("Trend deleted", trend_id=trend_id)
        else:
            logger.warning("Trend not found for deletion", trend_id=trend_id)

        return success

    def get_stats(self) -> TrendStats:
        """Get aggregated statistics"""
        stats = self.repository.get_stats()
        return TrendStats(**stats)

    def search_trends(
        self,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> TrendList:
        """
        Search trends by query

        Uses full-text search
        """
        trends, total = self.repository.search(query, skip, limit)

        has_more = (skip + limit) < total

        return TrendList(
            items=[TrendOut.model_validate(t) for t in trends],
            total=total,
            skip=skip,
            limit=limit,
            has_more=has_more
        )
