"""
Result routes
"""

from fastapi import (
    APIRouter,
    Depends,
    status
)

from app.schemas.result_schema import (
    ResultResponse,
    AttemptHistoryResponse
)

from app.services.result_service import (
    ResultService
)

from app.security.auth_guard import (
    get_current_user,
    admin_only
)

from app.utils.loggers import (
    logger
)


router = APIRouter(

    prefix="/results",

    tags=["Result"]

)


@router.get(

    "/history",

    response_model=list[
        AttemptHistoryResponse
    ]

)
async def get_student_results(
        current_user=Depends(
            get_current_user
        )
):
    """
    Retrieve result history
    of the logged-in student.
    """

    logger.info(
        "Result history requested by '%s'.",
        current_user["email"]
    )

    response= await ResultService.get_student_results(

        current_user

    )
    return response


@router.get(

    "/admin",

    response_model=list[
        AttemptHistoryResponse
    ]

)
async def get_all_results(
        current_user=Depends(
            admin_only
        )
):
    """
    Retrieve all quiz results.
    """

    logger.info(
        "All results requested by admin '%s'.",
        current_user["email"]
    )

    response= await ResultService.get_all_results()
    return response


@router.get(

    "/admin/{attempt_id}",

    response_model=ResultResponse

)
async def get_result_admin(
        attempt_id: str,
        current_user=Depends(
            admin_only
        )
):
    """
    Retrieve result of any
    student's quiz attempt.
    """

    logger.info(
        "Result for attempt '%s' requested by admin '%s'.",
        attempt_id,
        current_user["email"]
    )

    response= await ResultService.get_result_admin(

        attempt_id

    )
    return response

@router.get(

    "/{attempt_id}",

    response_model=ResultResponse

)
async def get_result(
        attempt_id: str,
        current_user=Depends(
            get_current_user
        )
):
    """
    Retrieve result of a
    quiz attempt.
    """

    logger.info(
        "Result for attempt '%s' requested by '%s'.",
        attempt_id,
        current_user["email"]
    )

    response= await ResultService.get_result(

        attempt_id,

        current_user

    )
    return response