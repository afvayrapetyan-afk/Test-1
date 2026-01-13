"""
Agent Runner
Simple runner for executing AI agents (temporary until Celery is set up)
"""

import asyncio
from typing import Dict, Any
from sqlalchemy.orm import Session
import structlog

from app.agents.trend_scout_agent import TrendScoutAgent
from app.agents.idea_analyst_agent import IdeaAnalystAgent
from app.modules.agents.models import AgentExecution

logger = structlog.get_logger()


async def run_agent_async(
    db: Session,
    agent_type: str,
    params: Dict[str, Any]
) -> AgentExecution:
    """
    Run an AI agent asynchronously

    Args:
        db: Database session
        agent_type: Type of agent to run
        params: Input parameters for the agent

    Returns:
        AgentExecution record with results

    Raises:
        ValueError: If agent_type is not supported
    """
    logger.info(
        "Running agent",
        agent_type=agent_type,
        params=params
    )

    # Create appropriate agent
    if agent_type == "trend_scout":
        agent = TrendScoutAgent(db)
    elif agent_type == "idea_analyst":
        agent = IdeaAnalystAgent(db)
    elif agent_type == "dev_agent":
        raise NotImplementedError("DevAgent not yet implemented")
    elif agent_type == "marketing_agent":
        raise NotImplementedError("MarketingAgent not yet implemented")
    elif agent_type == "sales_agent":
        raise NotImplementedError("SalesAgent not yet implemented")
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")

    # Run the agent
    execution = await agent.run(params)

    return execution


def run_agent_sync(
    db: Session,
    agent_type: str,
    params: Dict[str, Any]
) -> AgentExecution:
    """
    Run an AI agent synchronously (blocks until complete)

    This is a wrapper around run_agent_async for non-async contexts

    Args:
        db: Database session
        agent_type: Type of agent to run
        params: Input parameters for the agent

    Returns:
        AgentExecution record with results
    """
    return asyncio.run(run_agent_async(db, agent_type, params))
