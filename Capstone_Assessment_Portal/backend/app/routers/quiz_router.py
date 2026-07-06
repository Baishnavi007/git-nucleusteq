"""
Quiz routes
"""

from fastapi import (
    APIRouter,
    Depends,
    status
)

from app.schemas.quiz_schema import (
    QuizCreate,
    QuizUpdate,
    QuizResponse
)

from app.services.quiz_service import (
    QuizService
)

from app.security.auth_guard import (
    get_current_user,
    admin_only
)

from app.utils.loggers import (
    logger
)


router = APIRouter(

    prefix="/quizzes",

    tags=["Quiz"]

)


@router.post(

    "/category/{category_id}",

    status_code=status.HTTP_201_CREATED

)
async def create_quiz(
        category_id: str,
        quiz: QuizCreate,
        current_user=Depends(
            admin_only
        )
):
    """
    Create a new quiz.
    """

    logger.info(
        "Create quiz '%s' requested by '%s'.",
        quiz.title,
        current_user["email"]
    )

    return await QuizService.create_quiz(

        category_id,

        quiz,

        current_user

    )


@router.get(

    "/category/{category_id}",

    response_model=list[QuizResponse]

)
async def get_quizzes_by_category(
        category_id: str,
        current_user=Depends(
            admin_only
        )
):
    """
    Retrieve all quizzes for a category.
    """

    logger.info(
        "Get quizzes for category '%s' requested by '%s'.",
        category_id,
        current_user["email"]
    )

    return await QuizService.get_quizzes_by_category(

        category_id

    )


@router.get(

    "/{quiz_id}",

    response_model=QuizResponse

)
async def get_quiz_by_id(
        quiz_id: str,
        current_user=Depends(
            get_current_user
        )
):
    """
    Retrieve quiz by ID.
    """

    logger.info(
        "Get quiz '%s' requested by '%s'.",
        quiz_id,
        current_user["email"]
    )

    return await QuizService.get_quiz_by_id(

        quiz_id

    )


@router.put(

    "/{quiz_id}",

    status_code=status.HTTP_200_OK

)
async def update_quiz(
        quiz_id: str,
        quiz: QuizUpdate,
        current_user=Depends(
            admin_only
        )
):
    """
    Update an existing quiz.
    """

    logger.info(
        "Update quiz '%s' requested by '%s'.",
        quiz_id,
        current_user["email"]
    )

    return await QuizService.update_quiz(

        quiz_id,

        quiz

    )

@router.patch(

    "/{quiz_id}/publish",

    status_code=status.HTTP_200_OK

)
async def publish_quiz(
        quiz_id: str,
        current_user=Depends(
            admin_only
        )
):
    """
    Publish an existing quiz.
    """

    logger.info(
        "Publish quiz '%s' requested by '%s'.",
        quiz_id,
        current_user["email"]
    )

    return await QuizService.publish_quiz(

        quiz_id

    )


@router.patch(

    "/{quiz_id}/unpublish",

    status_code=status.HTTP_200_OK

)
async def unpublish_quiz(
        quiz_id: str,
        current_user=Depends(
            admin_only
        )
):
    """
    Unpublish an existing quiz.
    """

    logger.info(
        "Unpublish quiz '%s' requested by '%s'.",
        quiz_id,
        current_user["email"]
    )

    return await QuizService.unpublish_quiz(

        quiz_id

    )

@router.delete(

    "/{quiz_id}",

    status_code=status.HTTP_200_OK

)
async def delete_quiz(
        quiz_id: str,
        current_user=Depends(
            admin_only
        )
):
    """
    Delete an existing quiz.
    """

    logger.info(
        "Delete quiz '%s' requested by '%s'.",
        quiz_id,
        current_user["email"]
    )

    return await QuizService.delete_quiz(

        quiz_id

    )

@router.get(
    
    "/category/{category_id}/published",

    response_model=list[QuizResponse]

)
async def get_published_quizzes_by_category(
        category_id: str,
        current_user=Depends(
            get_current_user
        )
):
    """
    Retrieve all published quizzes for a category.
    """

    logger.info(
        "Get published quizzes for category '%s' requested by '%s'.",
        category_id,
        current_user["email"]
    )

    return await QuizService.get_published_quizzes_by_category(

        category_id

    )