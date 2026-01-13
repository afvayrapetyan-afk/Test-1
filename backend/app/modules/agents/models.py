"""
SQLAlchemy Models for Agent Executions
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, DECIMAL, JSON
from datetime import datetime

from app.core.database import Base


class AgentExecution(Base):
    """
    AgentExecution model - log of AI agent executions
    """
    __tablename__ = "agent_executions"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Agent info
    agent_type = Column(String(50), nullable=False, index=True)  # trend_scout, idea_analyst, etc.

    # Execution data
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)

    # Status tracking
    status = Column(
        String(20),
        default="pending",
        index=True
    )  # pending, running, completed, failed, cancelled
    error = Column(Text, nullable=True)

    # Timing
    started_at = Column(TIMESTAMP, default=datetime.utcnow, index=True)
    completed_at = Column(TIMESTAMP, nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    # Cost tracking
    llm_tokens_used = Column(Integer, default=0)
    llm_cost_usd = Column(DECIMAL(10, 4), default=0.0)

    # Additional metadata
    extra_metadata = Column(JSON, default=dict)

    def __repr__(self):
        return f"<AgentExecution(id={self.id}, agent={self.agent_type}, status={self.status})>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "agent_type": self.agent_type,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "llm_tokens_used": self.llm_tokens_used,
            "llm_cost_usd": float(self.llm_cost_usd) if self.llm_cost_usd else 0.0,
            "error": self.error
        }

    def to_dict_detailed(self):
        """Convert to detailed dictionary with input/output data"""
        base_dict = self.to_dict()
        base_dict.update({
            "input_data": self.input_data or {},
            "output_data": self.output_data or {},
            "metadata": self.extra_metadata or {}
        })
        return base_dict
