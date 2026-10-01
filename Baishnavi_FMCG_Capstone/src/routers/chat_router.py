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

from typing import Annotated, List

from fastapi import APIRouter, Query

from src.config import constants
from src.schemas.request_schema import ChatRequest, SessionQuery
from src.schemas.response_schema import (
    ApiResponse,
    ChatMessage,
    ChatResponse,
    ClearHistoryResponse,
    success_response,
)
from src.services.chat_service import get_answer
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

_chat_history_by_session = {}


def _history_for(session_id):
    return _chat_history_by_session.setdefault(session_id, [])



@router.post("/ask", response_model=ApiResponse[ChatResponse])
async def ask_question(request: ChatRequest):
    logger.info("[%s] question received (%s chars)", request.session_id, len(request.question))
    answer = await get_answer(request.question, session_id=request.session_id)

    history = _history_for(request.session_id)
    history.append(ChatMessage(role="user", content=request.question))
    history.append(ChatMessage(role="assistant", content=answer))
    del history[: -constants.CHAT_HISTORY_MAX_MESSAGES]  

    return success_response(ChatResponse(answer=answer), constants.MSG_CHAT_ANSWERED)



@router.get("/history", response_model=ApiResponse[List[ChatMessage]])
def get_history(params: Annotated[SessionQuery, Query()]):
    return success_response(_history_for(params.session_id), constants.MSG_HISTORY_FETCHED)


@router.post("/history/clear", response_model=ApiResponse[ClearHistoryResponse])
def clear_history(params: Annotated[SessionQuery, Query()]):
    session_id = params.session_id
    _history_for(session_id).clear()
    return success_response(
        ClearHistoryResponse(status="cleared", session_id=session_id),
        constants.MSG_HISTORY_CLEARED,
    )
