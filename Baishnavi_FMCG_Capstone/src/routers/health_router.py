"""
health_router.py
====================
Standard liveness check.
"""

from fastapi import APIRouter

from src.config import constants
from src.schemas.response_schema import ApiResponse, HealthResponse, success_response

router = APIRouter(tags=["health"])


@router.get("/health", response_model=ApiResponse[HealthResponse])
def health_check():
    """Basic liveness check."""
    return success_response(
        HealthResponse(status=constants.HEALTH_STATUS_OK), constants.MSG_HEALTH_OK,
    )
