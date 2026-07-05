"""
Question routes
"""

from fastapi import (
    APIRouter,
    Depends,
    status
)

from app.schemas.question_schema import (
    QuestionCreate,
    QuestionUpdate,
    QuestionResponse
)

from app.services.question_service import (
    QuestionService
)

from app.security.auth_guard import (
    admin_only
)

from app.utils.loggers import (
    logger
)


router = APIRouter(

    prefix="/questions",

    tags=["Question"]

)


@router.post(

    "/quiz/{quiz_id}",

    status_code=status.HTTP_201_CREATED

)
async def create_question(
        quiz_id: str,
        question: QuestionCreate,
        current_user=Depends(
            admin_only
        )
):
    """
    Create a new question.
    """

    logger.info(
        "Create question requested by '%s'.",
        current_user["email"]
    )

    return await QuestionService.create_question(

        quiz_id,

        question,

        current_user

    )


@router.get(

    "/quiz/{quiz_id}",

    response_model=list[QuestionResponse]

)
async def get_questions_by_quiz(
        quiz_id: str,
        current_user=Depends(
            admin_only
        )
):
    """
    Retrieve all questions of a quiz.
    """

    logger.info(
        "Get questions for quiz '%s' requested by '%s'.",
        quiz_id,
        current_user["email"]
    )

    return await QuestionService.get_questions_by_quiz(

        quiz_id

    )


@router.get(

    "/{question_id}",

    response_model=QuestionResponse

)
async def get_question_by_id(
        question_id: str,
        current_user=Depends(
            admin_only
        )
):
    """
    Retrieve question by ID.
    """

    logger.info(
        "Get question '%s' requested by '%s'.",
        question_id,
        current_user["email"]
    )

    return await QuestionService.get_question_by_id(

        question_id

    )


@router.put(

    "/{question_id}",

    status_code=status.HTTP_200_OK

)
async def update_question(
        question_id: str,
        question: QuestionUpdate,
        current_user=Depends(
            admin_only
        )
):
    """
    Update an existing question.
    """

    logger.info(
        "Update question '%s' requested by '%s'.",
        question_id,
        current_user["email"]
    )

    return await QuestionService.update_question(

        question_id,

        question

    )


@router.delete(

    "/{question_id}",

    status_code=status.HTTP_200_OK

)
async def delete_question(
        question_id: str,
        current_user=Depends(
            admin_only
        )
):
    """
    Delete an existing question.
    """

    logger.info(
        "Delete question '%s' requested by '%s'.",
        question_id,
        current_user["email"]
    )

    return await QuestionService.delete_question(

        question_id

    )