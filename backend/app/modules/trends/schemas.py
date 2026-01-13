"""
Pydantic Schemas for Trends API
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime


class TrendBase(BaseModel):
    """Base schema for Trend"""
    title: str = Field(..., min_length=5, max_length=500)
    description: Optional[str] = None
    url: Optional[str] = None
    source: str = Field(..., pattern="^(reddit|google_trends|telegram|vk|youtube|instagram|facebook|product_hunt)$")
    category: Optional[str] = Field(None, max_length=50)
    tags: List[str] = Field(default_factory=list, max_items=20)


class TrendCreate(TrendBase):
    """Schema for creating a new trend"""
    engagement_score: int = Field(default=0, ge=0)
    velocity: float = Field(default=0.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TrendUpdate(BaseModel):
    """Schema for updating a trend"""
    title: Optional[str] = Field(None, min_length=5, max_length=500)
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    engagement_score: Optional[int] = Field(None, ge=0)
    velocity: Optional[float] = None


class TrendOut(TrendBase):
    """Schema for trend output (API response)"""
    id: int
    engagement_score: int
    velocity: float
    discovered_at: datetime
    metadata: Dict[str, Any] = Field(alias="extra_metadata")

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)
        populate_by_name = True  # Allow using field name or alias


class TrendList(BaseModel):
    """Schema for paginated trend list"""
    items: List[TrendOut]
    total: int
    skip: int
    limit: int
    has_more: bool


class TrendStats(BaseModel):
    """Schema for trend statistics"""
    total_trends: int
    by_category: Dict[str, int]
    by_source: Dict[str, int]
    top_trending: List[Dict[str, Any]]
