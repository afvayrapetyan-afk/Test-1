"""
Pydantic Schemas for Ideas
API request/response models with validation
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
from datetime import datetime


class ScoreDetail(BaseModel):
    """Individual score with reasoning"""
    score: int = Field(..., ge=0, le=100)
    reasoning: str = Field(default="")
    evidence: str = Field(default="")


class IdeaScores(BaseModel):
    """All 6 scoring metrics"""
    market_size: int = Field(..., ge=0, le=100)
    competition: int = Field(..., ge=0, le=100)
    demand: int = Field(..., ge=0, le=100)
    monetization: int = Field(..., ge=0, le=100)
    feasibility: int = Field(..., ge=0, le=100)
    time_to_market: int = Field(..., ge=0, le=100)


class IdeaScoresDetailed(BaseModel):
    """All 6 scoring metrics with reasoning"""
    market_size: ScoreDetail
    competition: ScoreDetail
    demand: ScoreDetail
    monetization: ScoreDetail
    feasibility: ScoreDetail
    time_to_market: ScoreDetail


class IdeaBase(BaseModel):
    """Base schema for Idea"""
    title: str = Field(..., min_length=5, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)
    emoji: Optional[str] = Field(default="💡", max_length=10)
    source: Optional[str] = Field(default="AI Analysis", max_length=200)
    category: Optional[str] = Field(None, max_length=50)
    is_trending: Optional[bool] = Field(default=False)
    # Region relevance
    is_russia_relevant: Optional[bool] = Field(default=False)
    is_armenia_relevant: Optional[bool] = Field(default=False)
    is_global_relevant: Optional[bool] = Field(default=True)
    trend_id: Optional[int] = None

    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        if v is None:
            return v
        allowed = ['ai', 'saas', 'ecommerce', 'fintech', 'health', 'education', 'entertainment']
        if v not in allowed:
            raise ValueError(f'Category must be one of {allowed}')
        return v


class IdeaCreate(IdeaBase):
    """Schema for creating new idea"""
    market_size_score: int = Field(..., ge=0, le=100)
    competition_score: int = Field(..., ge=0, le=100)
    demand_score: int = Field(..., ge=0, le=100)
    monetization_score: int = Field(..., ge=0, le=100)
    feasibility_score: int = Field(..., ge=0, le=100)
    time_to_market_score: int = Field(..., ge=0, le=100)

    # Financial projections
    investment: Optional[int] = Field(default=50000, ge=1000)  # Min $1K
    payback_months: Optional[int] = Field(default=12, ge=1, le=120)  # 1-120 months
    margin: Optional[int] = Field(default=30, ge=0, le=100)  # 0-100%
    arr: Optional[int] = Field(default=100000, ge=0)  # Min $0

    analysis: Dict[str, Any] = Field(default_factory=dict)
    status: str = Field(default="pending")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        allowed = ['pending', 'approved', 'rejected', 'in_development', 'launched']
        if v not in allowed:
            raise ValueError(f'Status must be one of {allowed}')
        return v


class IdeaUpdate(BaseModel):
    """Schema for updating existing idea"""
    title: Optional[str] = Field(None, min_length=5, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)
    market_size_score: Optional[int] = Field(None, ge=0, le=100)
    competition_score: Optional[int] = Field(None, ge=0, le=100)
    demand_score: Optional[int] = Field(None, ge=0, le=100)
    monetization_score: Optional[int] = Field(None, ge=0, le=100)
    feasibility_score: Optional[int] = Field(None, ge=0, le=100)
    time_to_market_score: Optional[int] = Field(None, ge=0, le=100)
    status: Optional[str] = None
    analysis: Optional[Dict[str, Any]] = None

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is None:
            return v
        allowed = ['pending', 'approved', 'rejected', 'in_development', 'launched']
        if v not in allowed:
            raise ValueError(f'Status must be one of {allowed}')
        return v


class IdeaMetrics(BaseModel):
    """Frontend-compatible metrics"""
    marketSize: float
    competition: float
    demand: float
    monetization: float


class IdeaFinancial(BaseModel):
    """Financial projections"""
    investment: int
    paybackMonths: int
    margin: int
    arr: int


class IdeaRegions(BaseModel):
    """Region relevance flags"""
    russia: bool = False
    armenia: bool = False
    global_: bool = Field(default=True, alias='global', serialization_alias='global')

    model_config = {
        'populate_by_name': True,
    }


class IdeaFrontendOut(BaseModel):
    """Schema for idea output - Frontend format"""
    id: str
    title: str
    description: Optional[str] = None
    emoji: str
    source: str
    category: str
    isTrending: bool
    regions: IdeaRegions
    score: float
    timeAgo: str
    createdAt: Optional[str] = None
    metrics: IdeaMetrics
    financial: IdeaFinancial
    status: str

    class Config:
        from_attributes = True


class IdeaOut(IdeaBase):
    """Schema for idea output (simple) - Legacy format"""
    id: int
    market_size_score: Optional[int] = None
    competition_score: Optional[int] = None
    demand_score: Optional[int] = None
    monetization_score: Optional[int] = None
    feasibility_score: Optional[int] = None
    time_to_market_score: Optional[int] = None
    total_score: int
    status: str
    analyzed_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IdeaDetailedOut(IdeaBase):
    """Schema for idea output with full analysis"""
    id: int
    scores: IdeaScoresDetailed
    total_score: int
    status: str
    analyzed_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IdeaListFrontend(BaseModel):
    """Paginated list of ideas - Frontend format"""
    items: List[IdeaFrontendOut]
    total: int
    skip: int
    limit: int
    has_more: bool


class IdeaList(BaseModel):
    """Paginated list of ideas - Legacy format"""
    items: List[IdeaOut]
    total: int
    skip: int
    limit: int
    has_more: bool


class IdeaStats(BaseModel):
    """Aggregated statistics for ideas"""
    total_ideas: int
    by_status: Dict[str, int]
    avg_score: float
    top_ideas: List[Dict[str, Any]]
