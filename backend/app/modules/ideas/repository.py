"""
Ideas Repository - Data Access Layer
Handles all database operations for ideas
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc, case
from typing import List, Tuple, Optional

from app.modules.ideas.models import Idea
from app.modules.ideas.schemas import IdeaCreate, IdeaUpdate


class IdeaRepository:
    """
    Data access layer for Ideas
    Separates database logic from business logic
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, idea_id: int) -> Optional[Idea]:
        """Get single idea by ID"""
        return self.db.query(Idea).filter(Idea.id == idea_id).first()

    def get_many(
        self,
        skip: int = 0,
        limit: int = 100,
        min_score: Optional[int] = None,
        status: Optional[str] = None,
        trend_id: Optional[int] = None,
        category: Optional[str] = None,
        is_trending: Optional[bool] = None,
        sort_by: str = "date"
    ) -> Tuple[List[Idea], int]:
        """
        Get paginated list of ideas with filters and sorting

        Returns (ideas, total_count)
        """
        query = self.db.query(Idea)

        # Apply filters
        if status:
            query = query.filter(Idea.status == status)

        if trend_id:
            query = query.filter(Idea.trend_id == trend_id)

        if category:
            query = query.filter(Idea.category == category)

        if is_trending is not None:
            query = query.filter(Idea.is_trending == (1 if is_trending else 0))

        # Get total count before pagination
        total = query.count()

        # Apply sorting - disliked items always go to the end
        # First sort by is_disliked (0 first, 1 last), then by the chosen criteria
        if sort_by == "score":
            query = query.order_by(
                asc(Idea.is_disliked),  # Non-disliked first
                desc(Idea.market_size_score)
            )
        else:  # date
            query = query.order_by(
                asc(Idea.is_disliked),  # Non-disliked first
                desc(Idea.analyzed_at)
            )

        # Pagination
        ideas = query.offset(skip).limit(limit).all()

        # Apply min_score filter after fetch (since total_score is computed property)
        if min_score is not None:
            ideas = [idea for idea in ideas if idea.total_score >= min_score]

        return ideas, total

    def create(self, idea_data: IdeaCreate) -> Idea:
        """Create new idea"""
        idea = Idea(
            title=idea_data.title,
            description=idea_data.description,
            emoji=idea_data.emoji,
            source=idea_data.source,
            category=idea_data.category,
            is_trending=1 if idea_data.is_trending else 0,
            is_russia_relevant=1 if idea_data.is_russia_relevant else 0,
            is_armenia_relevant=1 if idea_data.is_armenia_relevant else 0,
            is_global_relevant=1 if idea_data.is_global_relevant else 0,
            trend_id=idea_data.trend_id,
            market_size_score=idea_data.market_size_score,
            competition_score=idea_data.competition_score,
            demand_score=idea_data.demand_score,
            monetization_score=idea_data.monetization_score,
            feasibility_score=idea_data.feasibility_score,
            time_to_market_score=idea_data.time_to_market_score,
            investment=idea_data.investment,
            payback_months=idea_data.payback_months,
            margin=idea_data.margin,
            arr=idea_data.arr,
            analysis=idea_data.analysis,
            status=idea_data.status
        )

        self.db.add(idea)
        self.db.commit()
        self.db.refresh(idea)

        return idea

    def update(self, idea_id: int, idea_data: IdeaUpdate) -> Optional[Idea]:
        """Update existing idea"""
        idea = self.get_by_id(idea_id)
        if not idea:
            return None

        # Update only provided fields
        update_data = idea_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(idea, field, value)

        self.db.commit()
        self.db.refresh(idea)

        return idea

    def delete(self, idea_id: int) -> bool:
        """Delete idea"""
        idea = self.get_by_id(idea_id)
        if not idea:
            return False

        self.db.delete(idea)
        self.db.commit()

        return True

    def get_stats(self) -> dict:
        """Get aggregated statistics"""
        total_ideas = self.db.query(func.count(Idea.id)).scalar()

        # By status
        by_status = {}
        status_counts = (
            self.db.query(Idea.status, func.count(Idea.id))
            .group_by(Idea.status)
            .all()
        )
        for status, count in status_counts:
            by_status[status] = count

        # Average score (compute in Python since it's a property)
        ideas = self.db.query(Idea).all()
        avg_score = sum(idea.total_score for idea in ideas) / len(ideas) if ideas else 0

        # Top ideas (by total score)
        top_ideas = sorted(ideas, key=lambda x: x.total_score, reverse=True)[:10]
        top_ideas_data = [
            {
                "id": idea.id,
                "title": idea.title,
                "total_score": idea.total_score
            }
            for idea in top_ideas
        ]

        return {
            "total_ideas": total_ideas,
            "by_status": by_status,
            "avg_score": round(avg_score, 2),
            "top_ideas": top_ideas_data
        }

    def get_by_trend(self, trend_id: int) -> List[Idea]:
        """Get all ideas for a specific trend"""
        return (
            self.db.query(Idea)
            .filter(Idea.trend_id == trend_id)
            .order_by(desc(Idea.total_score))
            .all()
        )

    def toggle_favorite(self, idea_id: int) -> Optional[Idea]:
        """Toggle favorite status for an idea"""
        idea = self.get_by_id(idea_id)
        if not idea:
            return None

        idea.is_favorite = 0 if idea.is_favorite else 1
        self.db.commit()
        self.db.refresh(idea)
        return idea

    def toggle_dislike(self, idea_id: int) -> Optional[Idea]:
        """Toggle dislike status for an idea"""
        idea = self.get_by_id(idea_id)
        if not idea:
            return None

        idea.is_disliked = 0 if idea.is_disliked else 1
        # If disliking, remove from favorites
        if idea.is_disliked:
            idea.is_favorite = 0
        self.db.commit()
        self.db.refresh(idea)
        return idea

    def get_favorites_count(self) -> int:
        """Get count of favorited ideas"""
        return self.db.query(func.count(Idea.id)).filter(Idea.is_favorite == 1).scalar() or 0
