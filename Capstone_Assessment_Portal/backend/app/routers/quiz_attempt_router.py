"""
Quiz attempt routes
"""

from fastapi import (
    APIRouter,
    Depends,
    status
)

from app.schemas.quiz_attempt_schema import (
    AttemptCreate,
    StudentAnswer,
    AttemptResponse,
    AttemptQuestionResponse
)

from app.schemas.common_schema import (
    MessageResponse
)

from app.services.quiz_attempt_service import (
    QuizAttemptService
)

from app.security.auth_guard import (
    student_only
)

from app.utils.loggers import (
    logger
)


router = APIRouter(

    prefix="/quiz-attempts",

    tags=["Quiz Attempt"]

)


@router.post(

    "/",

    status_code=status.HTTP_201_CREATED,

    response_model=AttemptResponse

)
async def start_attempt(
        attempt: AttemptCreate,
        current_user=Depends(
            student_only
        )
):
    """
    Start a new quiz attempt.
    """

    logger.info(
        "Quiz attempt requested by '%s'.",
        current_user["email"]
    )

    return await QuizAttemptService.start_attempt(

        attempt.quiz_id,

        current_user

    )


@router.get(

    "/{attempt_id}/questions",

    response_model=list[AttemptQuestionResponse]

)
async def get_attempt_questions(
        attempt_id: str,
        current_user=Depends(
            student_only
        )
):
    """
    Retrieve questions for a quiz attempt.
    """

    logger.info(
        "Questions requested for attempt '%s' by '%s'.",
        attempt_id,
        current_user["email"]
    )

    return await QuizAttemptService.get_attempt_questions(

        attempt_id,

        current_user

    )


@router.patch(

    "/{attempt_id}/answer",

    response_model=MessageResponse

)
async def save_answer(
        attempt_id: str,
        answer: StudentAnswer,
        current_user=Depends(
            student_only
        )
):
    """
    Save student's answer.
    """

    logger.info(
        "Saving answer for attempt '%s' by '%s'.",
        attempt_id,
        current_user["email"]
    )

    return await QuizAttemptService.save_answer(

        attempt_id,

        answer,

        current_user

    )


@router.post(

    "/{attempt_id}/submit",

    response_model=MessageResponse

)
async def submit_attempt(
        attempt_id: str,
        current_user=Depends(
            student_only
        )
):
    """
    Submit a quiz attempt.
    """

    logger.info(
        "Submitting attempt '%s' by '%s'.",
        attempt_id,
        current_user["email"]
    )

    return await QuizAttemptService.submit_attempt(

        attempt_id,

        current_user

    )


@router.get(

    "/quiz/{quiz_id}",

    response_model=list[AttemptResponse]

)
async def get_student_attempts(
        quiz_id: str,
        current_user=Depends(
            student_only
        )
):
    """
    Retrieve all attempts of the current student for a quiz.
    """

    logger.info(
        "Attempts requested for quiz '%s' by '%s'.",
        quiz_id,
        current_user["email"]
    )

    return await QuizAttemptService.get_student_attempts(

        quiz_id,

        current_user

    )