"""
chat_router.py
====================
Chat endpoints, backed by the agent through chat_service.py. Errors are
NOT caught here: anything the service raises is turned into a clean JSON
response by the global handler registered in main.py.

History is kept per session_id so different browser tabs/users don't see
each other's conversation. It is a display log only, capped per session
(constants.CHAT_HISTORY_MAX_MESSAGES) -- the agent's own memory (in
agent.py, keyed by the same session_id) is what actually gives the model
conversational context.
"""

from typing import List

from fastapi import APIRouter

from src.config import constants
from src.schemas.chat_schema import ChatMessage, ChatRequest
from src.schemas.response_schema import ChatResponse
from src.services.chat_service import get_answer
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

_chat_history_by_session = {}


def _history_for(session_id):
    return _chat_history_by_session.setdefault(session_id, [])


# The annotation on `request` is required: FastAPI uses it to read the JSON body.
@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    logger.info("[%s] question received (%s chars)", request.session_id, len(request.question))
    answer = await get_answer(request.question, session_id=request.session_id)

    history = _history_for(request.session_id)
    history.append(ChatMessage(role="user", content=request.question))
    history.append(ChatMessage(role="assistant", content=answer))
    del history[: -constants.CHAT_HISTORY_MAX_MESSAGES]  # keep only the most recent messages

    return ChatResponse(answer=answer)


# The annotations below are required: FastAPI uses them to read session_id
# as a query parameter (e.g. /chat/history?session_id=abc).
@router.get("/history", response_model=List[ChatMessage])
def get_history(session_id: str = constants.DEFAULT_SESSION_ID):
    return _history_for(session_id)


@router.post("/history/clear")
def clear_history(session_id: str = constants.DEFAULT_SESSION_ID):
    _history_for(session_id).clear()
    return {"status": "cleared", "session_id": session_id}
