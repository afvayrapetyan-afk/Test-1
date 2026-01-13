"""
Agents API Router
Endpoints for AI agent management and execution
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.modules.agents.service import AgentExecutionService
from app.modules.agents.schemas import (
    RunAgentRequest, RunAgentResponse,
    AgentExecutionOut, AgentExecutionDetailedOut,
    AgentExecutionList, AgentStats
)

router = APIRouter()


@router.get("/status", response_model=AgentStats)
async def get_agents_status(db: Session = Depends(get_db)):
    """
    Get aggregated status and statistics of all AI agents
    """
    service = AgentExecutionService(db)
    return service.get_stats()


@router.post("/run", response_model=RunAgentResponse)
async def run_agent(
    request: RunAgentRequest,
    db: Session = Depends(get_db)
):
    """
    Trigger an AI agent execution

    Available agents:
    - trend_scout: Discovers trends from data sources
    - idea_analyst: Analyzes trends into business ideas
    - dev_agent: Generates code for business MVP (not yet implemented)
    - marketing_agent: Creates marketing strategy (not yet implemented)
    - sales_agent: Automates sales processes (not yet implemented)

    NOTE: Currently runs synchronously. Will be moved to Celery for async execution.
    """
    from app.agents.runner import run_agent_async

    try:
        # Run the agent asynchronously (but wait for completion)
        # TODO: Move to Celery background task for true async execution
        execution = await run_agent_async(db, request.agent_type, request.params)

        return RunAgentResponse(
            job_id=f"{request.agent_type}-{execution.id}",
            agent_type=request.agent_type,
            status=execution.status,
            message=f"{request.agent_type} agent {execution.status}. Check /api/v1/agents/executions/{execution.id} for details."
        )

    except NotImplementedError as e:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {str(e)}"
        )


@router.get("/executions", response_model=AgentExecutionList)
async def get_agent_executions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    agent_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get agent execution history

    Parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum number of records
    - agent_type: Filter by agent type
    - status: Filter by status (pending, running, completed, failed, cancelled)
    """
    service = AgentExecutionService(db)
    return service.get_executions(
        skip=skip,
        limit=limit,
        agent_type=agent_type,
        status=status
    )


@router.get("/executions/{execution_id}", response_model=AgentExecutionDetailedOut)
async def get_execution_detail(
    execution_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific execution
    """
    service = AgentExecutionService(db)
    execution = service.get_execution(execution_id, detailed=True)

    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent execution with id {execution_id} not found"
        )

    return execution
