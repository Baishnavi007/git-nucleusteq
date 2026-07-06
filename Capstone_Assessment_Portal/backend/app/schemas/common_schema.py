"""
Common request and response schemas
"""

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """
    Standard schema for returning a message response
    """
    message: str