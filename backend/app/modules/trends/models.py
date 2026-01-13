"""
SQLAlchemy Models for Trends
"""

from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, ARRAY, func
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from app.core.database import Base


class Trend(Base):
    """
    Trend model - discovered trends from various data sources
    """
    __tablename__ = "trends"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Content
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=True)

    # Metadata
    source = Column(String(50), nullable=False, index=True)  # reddit, google_trends, etc.
    category = Column(String(50), nullable=True, index=True)
    tags = Column(ARRAY(Text), default=[])

    # Metrics
    engagement_score = Column(Integer, default=0, index=True)
    velocity = Column(Float, default=0.0)  # Growth rate

    # Timestamps
    discovered_at = Column(TIMESTAMP, default=datetime.utcnow, index=True)

    # Flexible metadata (source-specific data)
    metadata = Column(JSONB, default={})

    def __repr__(self):
        return f"<Trend(id={self.id}, title='{self.title[:30]}...', source={self.source})>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "source": self.source,
            "category": self.category,
            "tags": self.tags or [],
            "engagement_score": self.engagement_score,
            "velocity": self.velocity,
            "discovered_at": self.discovered_at.isoformat() if self.discovered_at else None,
            "metadata": self.metadata or {}
        }
