"""
Base Agent Class
Foundation for all AI agents with common functionality
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import structlog
from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.modules.agents.models import AgentExecution
from app.modules.agents.repository import AgentExecutionRepository

logger = structlog.get_logger()


class BaseAgent(ABC):
    """
    Base class for all AI agents

    Provides:
    - LLM integration (OpenAI/Anthropic)
    - Cost tracking
    - Error handling
    - Execution logging
    - Retry logic
    """

    def __init__(self, db: Session, agent_type: str):
        """
        Initialize base agent

        Args:
            db: Database session
            agent_type: Type of agent (trend_scout, idea_analyst, etc.)
        """
        self.db = db
        self.agent_type = agent_type
        self.repository = AgentExecutionRepository(db)

        # Initialize LLM client
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Tracking
        self.current_execution_id: Optional[int] = None
        self.tokens_used = 0
        self.cost_usd = 0.0

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main task

        Args:
            input_data: Input parameters for the agent

        Returns:
            Output data from the agent execution
        """
        pass

    async def run(self, input_data: Dict[str, Any]) -> AgentExecution:
        """
        Run the agent with full lifecycle management

        Creates execution record, runs agent, handles errors, tracks costs

        Args:
            input_data: Input parameters for the agent

        Returns:
            AgentExecution record with results
        """
        from app.modules.agents.schemas import AgentExecutionCreate, AgentExecutionUpdate

        # Create execution record
        execution_data = AgentExecutionCreate(
            agent_type=self.agent_type,
            input_data=input_data,
            status="running"
        )
        execution = self.repository.create(execution_data)
        self.current_execution_id = execution.id

        logger.info(
            "Agent execution started",
            execution_id=execution.id,
            agent_type=self.agent_type
        )

        start_time = datetime.utcnow()

        try:
            # Execute the agent
            output_data = await self.execute(input_data)

            # Calculate duration
            end_time = datetime.utcnow()
            duration = int((end_time - start_time).total_seconds())

            # Update execution with success
            update_data = AgentExecutionUpdate(
                status="completed",
                output_data=output_data,
                completed_at=end_time,
                duration_seconds=duration,
                llm_tokens_used=self.tokens_used,
                llm_cost_usd=self.cost_usd
            )

            execution = self.repository.update(execution.id, update_data)

            logger.info(
                "Agent execution completed",
                execution_id=execution.id,
                duration_seconds=duration,
                tokens_used=self.tokens_used,
                cost_usd=self.cost_usd
            )

            return execution

        except Exception as e:
            # Calculate duration even on failure
            end_time = datetime.utcnow()
            duration = int((end_time - start_time).total_seconds())

            # Update execution with failure
            update_data = AgentExecutionUpdate(
                status="failed",
                error=str(e),
                completed_at=end_time,
                duration_seconds=duration,
                llm_tokens_used=self.tokens_used,
                llm_cost_usd=self.cost_usd
            )

            execution = self.repository.update(execution.id, update_data)

            logger.error(
                "Agent execution failed",
                execution_id=execution.id,
                error=str(e),
                duration_seconds=duration
            )

            raise

    def call_llm(
        self,
        messages: list,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        json_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Call OpenAI LLM with cost tracking

        Args:
            messages: List of message dicts with role and content
            model: Model to use (gpt-3.5-turbo, gpt-4o, etc.)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            json_mode: Force JSON output

        Returns:
            Response dict with content and usage
        """
        try:
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            response = self.openai_client.chat.completions.create(**kwargs)

            # Track usage
            usage = response.usage
            self.tokens_used += usage.total_tokens

            # Calculate cost (approximate)
            cost = self._calculate_cost(model, usage.prompt_tokens, usage.completion_tokens)
            self.cost_usd += cost

            logger.debug(
                "LLM call completed",
                model=model,
                tokens=usage.total_tokens,
                cost_usd=cost
            )

            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens
                },
                "cost_usd": cost
            }

        except Exception as e:
            logger.error("LLM call failed", error=str(e), model=model)
            raise

    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Calculate approximate cost for LLM call

        Pricing (per 1M tokens):
        - gpt-3.5-turbo: $0.50 input, $1.50 output
        - gpt-4o: $2.50 input, $10.00 output
        - gpt-4o-mini: $0.15 input, $0.60 output
        """
        pricing = {
            "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        }

        if model not in pricing:
            # Default to gpt-3.5-turbo pricing
            model = "gpt-3.5-turbo"

        input_cost = (prompt_tokens / 1_000_000) * pricing[model]["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing[model]["output"]

        return round(input_cost + output_cost, 4)

    def reset_tracking(self):
        """Reset tokens and cost tracking"""
        self.tokens_used = 0
        self.cost_usd = 0.0
