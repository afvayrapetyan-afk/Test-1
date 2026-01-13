"""
Trends Repository - Data Access Layer
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict

from app.modules.trends.models import Trend
from app.modules.trends.schemas import TrendCreate, TrendUpdate


class TrendRepository:
    """
    Repository for Trend database operations
    Handles all database queries for trends
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, trend_id: int) -> Optional[Trend]:
        """Get trend by ID"""
        return self.db.query(Trend).filter(Trend.id == trend_id).first()

    def get_many(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        source: Optional[str] = None,
        min_engagement: Optional[int] = None
    ) -> tuple[List[Trend], int]:
        """
        Get multiple trends with filters and pagination

        Returns:
            (trends, total_count)
        """
        query = self.db.query(Trend)

        # Apply filters
        if category:
            query = query.filter(Trend.category == category)

        if source:
            query = query.filter(Trend.source == source)

        if min_engagement is not None:
            query = query.filter(Trend.engagement_score >= min_engagement)

        # Get total count before pagination
        total = query.count()

        # Apply pagination and ordering
        trends = (
            query
            .order_by(desc(Trend.discovered_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

        return trends, total

    def create(self, trend_data: TrendCreate) -> Trend:
        """Create new trend"""
        data = trend_data.model_dump()
        # Map metadata -> extra_metadata for database column
        if 'metadata' in data:
            data['extra_metadata'] = data.pop('metadata')

        trend = Trend(**data)
        self.db.add(trend)
        self.db.commit()
        self.db.refresh(trend)
        return trend

    def update(self, trend_id: int, trend_data: TrendUpdate) -> Optional[Trend]:
        """Update existing trend"""
        trend = self.get_by_id(trend_id)
        if not trend:
            return None

        # Update only provided fields
        update_data = trend_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(trend, field, value)

        self.db.commit()
        self.db.refresh(trend)
        return trend

    def delete(self, trend_id: int) -> bool:
        """Delete trend"""
        trend = self.get_by_id(trend_id)
        if not trend:
            return False

        self.db.delete(trend)
        self.db.commit()
        return True

    def get_stats(self) -> Dict:
        """
        Get aggregated statistics
        """
        # Total trends
        total = self.db.query(func.count(Trend.id)).scalar()

        # By category
        by_category = (
            self.db.query(
                Trend.category,
                func.count(Trend.id).label("count")
            )
            .filter(Trend.category.isnot(None))
            .group_by(Trend.category)
            .all()
        )

        # By source
        by_source = (
            self.db.query(
                Trend.source,
                func.count(Trend.id).label("count")
            )
            .group_by(Trend.source)
            .all()
        )

        # Top trending (by engagement score)
        top_trending = (
            self.db.query(Trend)
            .order_by(desc(Trend.engagement_score))
            .limit(10)
            .all()
        )

        return {
            "total_trends": total,
            "by_category": {cat: count for cat, count in by_category},
            "by_source": {src: count for src, count in by_source},
            "top_trending": [
                {
                    "id": t.id,
                    "title": t.title,
                    "engagement_score": t.engagement_score
                }
                for t in top_trending
            ]
        }

    def search(
        self,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Trend], int]:
        """
        Full-text search in trends

        Uses PostgreSQL full-text search
        """
        # PostgreSQL full-text search
        search_query = self.db.query(Trend).filter(
            func.to_tsvector('english', Trend.title + ' ' + func.coalesce(Trend.description, '')).match(query)
        )

        total = search_query.count()

        trends = (
            search_query
            .order_by(desc(Trend.engagement_score))
            .offset(skip)
            .limit(limit)
            .all()
        )

        return trends, total

    def check_duplicate(self, title: str, url: Optional[str] = None) -> Optional[Trend]:
        """
        Check if trend already exists (duplicate detection)
        """
        query = self.db.query(Trend).filter(Trend.title == title)

        if url:
            query = query.filter(Trend.url == url)

        return query.first()
