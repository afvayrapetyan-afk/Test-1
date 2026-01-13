"""
Agent Executions Service - Business Logic Layer
"""

from sqlalchemy.orm import Session
from typing import Optional, Union
import structlog

from app.modules.agents.repository import AgentExecutionRepository
from app.modules.agents.schemas import (
    AgentExecutionCreate, AgentExecutionUpdate,
    AgentExecutionOut, AgentExecutionDetailedOut,
    AgentExecutionList, AgentStats
)

logger = structlog.get_logger()


class AgentExecutionService:
    """
    Business logic for agent executions
    Orchestrates between repository and API
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = AgentExecutionRepository(db)

    def get_executions(
        self,
        skip: int = 0,
        limit: int = 100,
        agent_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> AgentExecutionList:
        """
        Get paginated list of agent executions with filters
        """
        executions, total = self.repository.get_many(
            skip=skip,
            limit=limit,
            agent_type=agent_type,
            status=status
        )

        has_more = (skip + limit) < total

        return AgentExecutionList(
            items=[AgentExecutionOut.model_validate(e) for e in executions],
            total=total,
            skip=skip,
            limit=limit,
            has_more=has_more
        )

    def get_execution(self, execution_id: int, detailed: bool = False) -> Optional[Union[AgentExecutionOut, AgentExecutionDetailedOut]]:
        """Get single agent execution by ID"""
        execution = self.repository.get_by_id(execution_id)
        if not execution:
            return None

        if detailed:
            return AgentExecutionDetailedOut.model_validate(execution)
        else:
            return AgentExecutionOut.model_validate(execution)

    def create_execution(self, execution_data: AgentExecutionCreate) -> AgentExecutionOut:
        """
        Create new agent execution
        """
        execution = self.repository.create(execution_data)

        logger.info(
            "Agent execution created",
            execution_id=execution.id,
            agent_type=execution.agent_type,
            status=execution.status
        )

        return AgentExecutionOut.model_validate(execution)

    def update_execution(self, execution_id: int, execution_data: AgentExecutionUpdate) -> Optional[AgentExecutionOut]:
        """Update existing agent execution"""
        execution = self.repository.update(execution_id, execution_data)
        if not execution:
            logger.warning("Agent execution not found for update", execution_id=execution_id)
            return None

        logger.info(
            "Agent execution updated",
            execution_id=execution_id,
            status=execution.status
        )
        return AgentExecutionOut.model_validate(execution)

    def delete_execution(self, execution_id: int) -> bool:
        """Delete agent execution"""
        success = self.repository.delete(execution_id)
        if success:
            logger.info("Agent execution deleted", execution_id=execution_id)
        else:
            logger.warning("Agent execution not found for deletion", execution_id=execution_id)

        return success

    def get_stats(self) -> AgentStats:
        """Get aggregated statistics"""
        stats = self.repository.get_stats()
        return AgentStats(**stats)
