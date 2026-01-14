"""
SQLAlchemy Models for Ideas
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, CheckConstraint, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Idea(Base):
    """
    Idea model - business ideas analyzed from trends
    """
    __tablename__ = "ideas"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    trend_id = Column(Integer, ForeignKey("trends.id", ondelete="CASCADE"), nullable=True, index=True)

    # Content
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    emoji = Column(String(10), nullable=True, default="💡")  # Emoji for card
    source = Column(String(200), nullable=True, default="AI Analysis")  # Trend source

    # Category
    category = Column(
        String(50),
        nullable=True,
        index=True
    )  # ai, saas, ecommerce, fintech, health, education, entertainment

    is_trending = Column(Integer, default=0)  # Boolean flag for trending ideas

    # Region relevance flags
    is_russia_relevant = Column(Integer, default=0)  # 🇷🇺 Russia
    is_armenia_relevant = Column(Integer, default=0)  # 🇦🇲 Armenia
    is_global_relevant = Column(Integer, default=1)  # 🌍 Global/World

    # Scores (0-100 for each metric)
    market_size_score = Column(
        Integer,
        CheckConstraint("market_size_score >= 0 AND market_size_score <= 100"),
        nullable=True
    )
    competition_score = Column(
        Integer,
        CheckConstraint("competition_score >= 0 AND competition_score <= 100"),
        nullable=True
    )
    demand_score = Column(
        Integer,
        CheckConstraint("demand_score >= 0 AND demand_score <= 100"),
        nullable=True
    )
    monetization_score = Column(
        Integer,
        CheckConstraint("monetization_score >= 0 AND monetization_score <= 100"),
        nullable=True
    )
    feasibility_score = Column(
        Integer,
        CheckConstraint("feasibility_score >= 0 AND feasibility_score <= 100"),
        nullable=True
    )
    time_to_market_score = Column(
        Integer,
        CheckConstraint("time_to_market_score >= 0 AND time_to_market_score <= 100"),
        nullable=True
    )

    # Note: total_score is a GENERATED column in PostgreSQL (defined in init.sql)
    # We'll compute it in Python as a property
    @property
    def total_score(self) -> int:
        """Calculate average of all 6 scores"""
        scores = [
            self.market_size_score or 0,
            self.competition_score or 0,
            self.demand_score or 0,
            self.monetization_score or 0,
            self.feasibility_score or 0,
            self.time_to_market_score or 0
        ]
        return sum(scores) // 6 if any(scores) else 0

    # Financial projections
    investment = Column(Integer, nullable=True)  # Initial investment in USD
    payback_months = Column(Integer, nullable=True)  # Payback period in months
    margin = Column(Integer, nullable=True)  # Profit margin in percentage (0-100)
    arr = Column(Integer, nullable=True)  # Annual Recurring Revenue in USD

    # Analysis details
    analysis = Column(JSON, default=dict)  # Full LLM analysis with reasoning

    # Timestamps
    analyzed_at = Column(TIMESTAMP, default=datetime.utcnow, index=True)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Status
    status = Column(
        String(20),
        default="pending",
        index=True
    )  # pending, approved, rejected, in_development, launched

    # Relationships
    # trend = relationship("Trend", backref="ideas")

    def __repr__(self):
        return f"<Idea(id={self.id}, title='{self.title[:30]}...', total_score={self.total_score})>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        from datetime import datetime
        import timeago

        # Calculate timeAgo
        time_ago = ""
        if self.analyzed_at:
            try:
                time_ago = timeago.format(self.analyzed_at, datetime.utcnow(), 'ru')
            except:
                time_ago = "недавно"

        return {
            "id": str(self.id),  # Frontend expects string
            "trend_id": self.trend_id,
            "title": self.title,
            "description": self.description,
            "emoji": self.emoji or "💡",
            "source": self.source or "AI Analysis",
            "category": self.category or "ai",
            "isTrending": bool(self.is_trending),
            "regions": {
                "russia": bool(self.is_russia_relevant),
                "armenia": bool(self.is_armenia_relevant),
                "global": bool(self.is_global_relevant),
            },
            "score": round(self.total_score / 10, 1),  # Convert 0-100 to 0-10 scale
            "timeAgo": time_ago,
            "createdAt": self.analyzed_at.isoformat() if self.analyzed_at else None,
            "metrics": {
                "marketSize": round((self.market_size_score or 0) / 10, 1),
                "competition": round((self.competition_score or 0) / 10, 1),
                "demand": round((self.demand_score or 0) / 10, 1),
                "monetization": round((self.monetization_score or 0) / 10, 1),
            },
            "financial": {
                "investment": self.investment or 50000,  # Default $50K
                "paybackMonths": self.payback_months or 12,  # Default 12 months
                "margin": self.margin or 30,  # Default 30% margin
                "arr": self.arr or 100000,  # Default $100K ARR
            },
            "status": self.status,
            "analyzed_at": self.analyzed_at.isoformat() if self.analyzed_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def to_dict_detailed(self):
        """Convert to detailed dictionary with full analysis breakdown"""
        base_dict = self.to_dict()

        # Extract reasoning from analysis JSONB
        analysis_data = self.analysis or {}

        base_dict["scores"] = {
            "market_size": {
                "score": self.market_size_score,
                "reasoning": analysis_data.get("market_size", {}).get("reasoning", ""),
                "evidence": analysis_data.get("market_size", {}).get("evidence", "")
            },
            "competition": {
                "score": self.competition_score,
                "reasoning": analysis_data.get("competition", {}).get("reasoning", ""),
                "evidence": analysis_data.get("competition", {}).get("evidence", "")
            },
            "demand": {
                "score": self.demand_score,
                "reasoning": analysis_data.get("demand", {}).get("reasoning", ""),
                "evidence": analysis_data.get("demand", {}).get("evidence", "")
            },
            "monetization": {
                "score": self.monetization_score,
                "reasoning": analysis_data.get("monetization", {}).get("reasoning", ""),
                "evidence": analysis_data.get("monetization", {}).get("evidence", "")
            },
            "feasibility": {
                "score": self.feasibility_score,
                "reasoning": analysis_data.get("feasibility", {}).get("reasoning", ""),
                "evidence": analysis_data.get("feasibility", {}).get("evidence", "")
            },
            "time_to_market": {
                "score": self.time_to_market_score,
                "reasoning": analysis_data.get("time_to_market", {}).get("reasoning", ""),
                "evidence": analysis_data.get("time_to_market", {}).get("evidence", "")
            }
        }

        return base_dict
