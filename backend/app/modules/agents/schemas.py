"""
Pydantic Schemas for Agent Executions
API request/response models with validation
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from decimal import Decimal


class AgentExecutionBase(BaseModel):
    """Base schema for AgentExecution"""
    agent_type: str = Field(..., min_length=3, max_length=50)


class AgentExecutionCreate(AgentExecutionBase):
    """Schema for creating new agent execution"""
    input_data: Dict[str, Any] = Field(default_factory=dict)
    status: str = Field(default="pending")
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        allowed = ['pending', 'running', 'completed', 'failed', 'cancelled']
        if v not in allowed:
            raise ValueError(f'Status must be one of {allowed}')
        return v

    @field_validator('agent_type')
    @classmethod
    def validate_agent_type(cls, v):
        allowed = ['trend_scout', 'idea_analyst', 'dev_agent', 'marketing_agent', 'sales_agent']
        if v not in allowed:
            raise ValueError(f'Agent type must be one of {allowed}')
        return v


class AgentExecutionUpdate(BaseModel):
    """Schema for updating existing agent execution"""
    status: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    llm_tokens_used: Optional[int] = None
    llm_cost_usd: Optional[Decimal] = None
    metadata: Optional[Dict[str, Any]] = None

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is None:
            return v
        allowed = ['pending', 'running', 'completed', 'failed', 'cancelled']
        if v not in allowed:
            raise ValueError(f'Status must be one of {allowed}')
        return v


class AgentExecutionOut(AgentExecutionBase):
    """Schema for agent execution output (simple)"""
    id: int
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: Optional[int]
    llm_tokens_used: int
    llm_cost_usd: Decimal
    error: Optional[str]

    class Config:
        from_attributes = True


class AgentExecutionDetailedOut(AgentExecutionBase):
    """Schema for agent execution output with full data"""
    id: int
    status: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: Optional[int]
    llm_tokens_used: int
    llm_cost_usd: Decimal
    error: Optional[str]
    metadata: Dict[str, Any]

    class Config:
        from_attributes = True


class AgentExecutionList(BaseModel):
    """Paginated list of agent executions"""
    items: List[AgentExecutionOut]
    total: int
    skip: int
    limit: int
    has_more: bool


class AgentStats(BaseModel):
    """Aggregated statistics for agent executions"""
    total_executions: int
    by_agent_type: Dict[str, int]
    by_status: Dict[str, int]
    total_tokens_used: int
    total_cost_usd: Decimal
    avg_duration_seconds: float
    success_rate: float


class RunAgentRequest(BaseModel):
    """Request model for running an agent"""
    agent_type: str = Field(..., min_length=3, max_length=50)
    params: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('agent_type')
    @classmethod
    def validate_agent_type(cls, v):
        allowed = ['trend_scout', 'idea_analyst', 'dev_agent', 'marketing_agent', 'sales_agent']
        if v not in allowed:
            raise ValueError(f'Agent type must be one of {allowed}')
        return v


class RunAgentResponse(BaseModel):
    """Response for running an agent"""
    job_id: str
    agent_type: str
    status: str
    message: str
