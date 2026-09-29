"""
chat_schema.py
====================
Request/response shapes for chat_router.py. The annotations on the fields
are required -- Pydantic uses them to validate incoming data.
"""

from pydantic import BaseModel, Field

from src.config import constants


class ChatRequest(BaseModel):
    question: str = Field(
        ..., min_length=1, max_length=constants.MAX_QUESTION_LENGTH,
        description="A natural-language question about customer reviews.",
    )
    session_id: str = Field(
        default=constants.DEFAULT_SESSION_ID, max_length=constants.SESSION_ID_MAX_LENGTH,
        description="Identifies one conversation so follow-up questions keep context. "
                    "Generate one random ID per browser session and reuse it.",
    )


class ChatMessage(BaseModel):
    role: str  
    content: str
