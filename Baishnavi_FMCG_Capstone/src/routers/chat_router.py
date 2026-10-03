"""
chat_router.py
====================
Chat endpoints, backed by the agent through chat_service.py. Errors are
NOT caught here: anything the service raises is turned into a clean JSON
response by the global handler registered in main.py.

Storing and clearing the per-session chat history lives in chat_service.py;
the router only receives requests and shapes responses.
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
from src.services.chat_service import clear_chat_history, get_answer, get_chat_history
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/ask", response_model=ApiResponse[ChatResponse])
async def ask_question(request: ChatRequest):
    logger.info("[%s] question received (%s chars)", request.session_id, len(request.question))
    answer = await get_answer(request.question, session_id=request.session_id)
    return success_response(ChatResponse(answer=answer), constants.MSG_CHAT_ANSWERED)



@router.get("/history", response_model=ApiResponse[List[ChatMessage]])
def get_history(params: Annotated[SessionQuery, Query()]):
    return success_response(get_chat_history(params.session_id), constants.MSG_HISTORY_FETCHED)


@router.post("/history/clear", response_model=ApiResponse[ClearHistoryResponse])
def clear_history(params: Annotated[SessionQuery, Query()]):
    session_id = params.session_id
    clear_chat_history(session_id)
    return success_response(
        ClearHistoryResponse(status="cleared", session_id=session_id),
        constants.MSG_HISTORY_CLEARED,
    )

