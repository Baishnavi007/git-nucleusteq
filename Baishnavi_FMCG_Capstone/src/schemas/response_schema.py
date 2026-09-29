"""
response_schema.py
====================
Response shapes shared across routers. Field annotations are required by
Pydantic.
"""

from pydantic import BaseModel


class ChatResponse(BaseModel):
    answer: str


class DashboardSummaryResponse(BaseModel):
    total_reviews: int
    avg_rating: float
    negative_pct: float
    high_severity_count: int


class HealthResponse(BaseModel):
    status: str
