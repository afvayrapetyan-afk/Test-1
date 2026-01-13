"""
Agent Executions Repository - Data Access Layer
Handles all database operations for agent executions
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Tuple, Optional
from decimal import Decimal

from app.modules.agents.models import AgentExecution
from app.modules.agents.schemas import AgentExecutionCreate, AgentExecutionUpdate


class AgentExecutionRepository:
    """
    Data access layer for Agent Executions
    Separates database logic from business logic
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, execution_id: int) -> Optional[AgentExecution]:
        """Get single execution by ID"""
        return self.db.query(AgentExecution).filter(AgentExecution.id == execution_id).first()

    def get_many(
        self,
        skip: int = 0,
        limit: int = 100,
        agent_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> Tuple[List[AgentExecution], int]:
        """
        Get paginated list of executions with filters

        Returns (executions, total_count)
        """
        query = self.db.query(AgentExecution)

        # Apply filters
        if agent_type:
            query = query.filter(AgentExecution.agent_type == agent_type)

        if status:
            query = query.filter(AgentExecution.status == status)

        # Get total count before pagination
        total = query.count()

        # Apply ordering and pagination
        executions = (
            query
            .order_by(desc(AgentExecution.started_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

        return executions, total

    def create(self, execution_data: AgentExecutionCreate) -> AgentExecution:
        """Create new agent execution"""
        execution = AgentExecution(
            agent_type=execution_data.agent_type,
            input_data=execution_data.input_data,
            status=execution_data.status,
            metadata=execution_data.metadata
        )

        self.db.add(execution)
        self.db.commit()
        self.db.refresh(execution)

        return execution

    def update(self, execution_id: int, execution_data: AgentExecutionUpdate) -> Optional[AgentExecution]:
        """Update existing agent execution"""
        execution = self.get_by_id(execution_id)
        if not execution:
            return None

        # Update only provided fields
        update_data = execution_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(execution, field, value)

        self.db.commit()
        self.db.refresh(execution)

        return execution

    def delete(self, execution_id: int) -> bool:
        """Delete agent execution"""
        execution = self.get_by_id(execution_id)
        if not execution:
            return False

        self.db.delete(execution)
        self.db.commit()

        return True

    def get_stats(self) -> dict:
        """Get aggregated statistics"""
        total_executions = self.db.query(func.count(AgentExecution.id)).scalar()

        # By agent type
        by_agent_type = {}
        agent_type_counts = (
            self.db.query(AgentExecution.agent_type, func.count(AgentExecution.id))
            .group_by(AgentExecution.agent_type)
            .all()
        )
        for agent_type, count in agent_type_counts:
            by_agent_type[agent_type] = count

        # By status
        by_status = {}
        status_counts = (
            self.db.query(AgentExecution.status, func.count(AgentExecution.id))
            .group_by(AgentExecution.status)
            .all()
        )
        for status, count in status_counts:
            by_status[status] = count

        # Total tokens and cost
        total_tokens = (
            self.db.query(func.sum(AgentExecution.llm_tokens_used)).scalar() or 0
        )
        total_cost = (
            self.db.query(func.sum(AgentExecution.llm_cost_usd)).scalar() or Decimal('0.0')
        )

        # Average duration (only completed executions)
        avg_duration = (
            self.db.query(func.avg(AgentExecution.duration_seconds))
            .filter(AgentExecution.status == 'completed')
            .scalar() or 0
        )

        # Success rate
        completed_count = (
            self.db.query(func.count(AgentExecution.id))
            .filter(AgentExecution.status == 'completed')
            .scalar() or 0
        )
        success_rate = (completed_count / total_executions * 100) if total_executions > 0 else 0

        return {
            "total_executions": total_executions,
            "by_agent_type": by_agent_type,
            "by_status": by_status,
            "total_tokens_used": total_tokens,
            "total_cost_usd": total_cost,
            "avg_duration_seconds": round(float(avg_duration), 2) if avg_duration else 0,
            "success_rate": round(success_rate, 2)
        }

    def get_recent_by_agent(self, agent_type: str, limit: int = 10) -> List[AgentExecution]:
        """Get recent executions for specific agent type"""
        return (
            self.db.query(AgentExecution)
            .filter(AgentExecution.agent_type == agent_type)
            .order_by(desc(AgentExecution.started_at))
            .limit(limit)
            .all()
        )
