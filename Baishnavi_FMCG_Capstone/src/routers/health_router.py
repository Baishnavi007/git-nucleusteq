"""
health_router.py
====================
Standard liveness check.
"""

from fastapi import APIRouter

from src.schemas.response_schema import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Basic liveness check."""
    return HealthResponse(status="ok")
