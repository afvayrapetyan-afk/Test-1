"""
Ideas Service - Business Logic Layer
"""

from sqlalchemy.orm import Session
from typing import List, Optional, Union
import structlog

from app.modules.ideas.repository import IdeaRepository
from app.modules.ideas.schemas import (
    IdeaCreate, IdeaUpdate, IdeaOut, IdeaDetailedOut,
    IdeaList, IdeaStats, IdeaScoresDetailed, ScoreDetail
)
from app.modules.ideas.models import Idea

logger = structlog.get_logger()


class IdeaService:
    """
    Business logic for ideas
    Orchestrates between repository and API
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = IdeaRepository(db)

    def get_ideas(
        self,
        skip: int = 0,
        limit: int = 100,
        min_score: Optional[int] = None,
        status: Optional[str] = None,
        trend_id: Optional[int] = None,
        category: Optional[str] = None,
        is_trending: Optional[bool] = None,
        sort_by: str = "date"
    ) -> IdeaList:
        """
        Get paginated list of ideas with filters and sorting
        """
        ideas, total = self.repository.get_many(
            skip=skip,
            limit=limit,
            min_score=min_score,
            status=status,
            trend_id=trend_id,
            category=category,
            is_trending=is_trending,
            sort_by=sort_by
        )

        has_more = (skip + limit) < total

        # Convert to frontend format using to_dict()
        items = [idea.to_dict() for idea in ideas]

        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": has_more
        }

    def get_idea(self, idea_id: int, detailed: bool = False) -> Optional[Union[IdeaOut, IdeaDetailedOut]]:
        """Get single idea by ID"""
        idea = self.repository.get_by_id(idea_id)
        if not idea:
            return None

        if detailed:
            return self._convert_to_detailed(idea)
        else:
            return IdeaOut.model_validate(idea)

    def _convert_to_detailed(self, idea: Idea) -> IdeaDetailedOut:
        """Convert Idea model to detailed output with score reasoning"""
        analysis = idea.analysis or {}

        scores = IdeaScoresDetailed(
            market_size=ScoreDetail(
                score=idea.market_size_score or 0,
                reasoning=analysis.get("market_size", {}).get("reasoning", ""),
                evidence=analysis.get("market_size", {}).get("evidence", "")
            ),
            competition=ScoreDetail(
                score=idea.competition_score or 0,
                reasoning=analysis.get("competition", {}).get("reasoning", ""),
                evidence=analysis.get("competition", {}).get("evidence", "")
            ),
            demand=ScoreDetail(
                score=idea.demand_score or 0,
                reasoning=analysis.get("demand", {}).get("reasoning", ""),
                evidence=analysis.get("demand", {}).get("evidence", "")
            ),
            monetization=ScoreDetail(
                score=idea.monetization_score or 0,
                reasoning=analysis.get("monetization", {}).get("reasoning", ""),
                evidence=analysis.get("monetization", {}).get("evidence", "")
            ),
            feasibility=ScoreDetail(
                score=idea.feasibility_score or 0,
                reasoning=analysis.get("feasibility", {}).get("reasoning", ""),
                evidence=analysis.get("feasibility", {}).get("evidence", "")
            ),
            time_to_market=ScoreDetail(
                score=idea.time_to_market_score or 0,
                reasoning=analysis.get("time_to_market", {}).get("reasoning", ""),
                evidence=analysis.get("time_to_market", {}).get("evidence", "")
            )
        )

        return IdeaDetailedOut(
            id=idea.id,
            title=idea.title,
            description=idea.description,
            trend_id=idea.trend_id,
            scores=scores,
            total_score=idea.total_score,
            status=idea.status,
            analyzed_at=idea.analyzed_at,
            updated_at=idea.updated_at
        )

    def create_idea(self, idea_data: IdeaCreate) -> IdeaOut:
        """
        Create new idea
        """
        idea = self.repository.create(idea_data)

        logger.info(
            "Idea created",
            idea_id=idea.id,
            trend_id=idea.trend_id,
            total_score=idea.total_score
        )

        return IdeaOut.model_validate(idea)

    def update_idea(self, idea_id: int, idea_data: IdeaUpdate) -> Optional[IdeaOut]:
        """Update existing idea"""
        idea = self.repository.update(idea_id, idea_data)
        if not idea:
            logger.warning("Idea not found for update", idea_id=idea_id)
            return None

        logger.info("Idea updated", idea_id=idea_id)
        return IdeaOut.model_validate(idea)

    def delete_idea(self, idea_id: int) -> bool:
        """Delete idea"""
        success = self.repository.delete(idea_id)
        if success:
            logger.info("Idea deleted", idea_id=idea_id)
        else:
            logger.warning("Idea not found for deletion", idea_id=idea_id)

        return success

    def get_stats(self) -> IdeaStats:
        """Get aggregated statistics"""
        stats = self.repository.get_stats()
        return IdeaStats(**stats)

    def get_ideas_by_trend(self, trend_id: int) -> List[IdeaOut]:
        """Get all ideas for a specific trend"""
        ideas = self.repository.get_by_trend(trend_id)
        return [IdeaOut.model_validate(idea) for idea in ideas]
