"""
Result business logic
"""

from app.repository import Repository

from app.schemas.result_schema import (
    ResultResponse,
    ResultQuestionResponse,
    AttemptHistoryResponse
)

from app.utils.helpers import (
    validate_object_id
)

from app.utils.constants import (
    QuizAttemptMessage
)

from app.utils.loggers import (
    logger
)

from app.exceptions.resource_not_found_exception import (
    ResourceNotFoundException
)



def result_helper(
        attempt: dict
) -> ResultResponse:
    """
    Convert quiz attempt into
    detailed result response.
    """

    total_marks = attempt[
        "snapshot"
    ][
        "total_marks"
    ]

    score = attempt[
        "score"
    ]

    passing_marks = attempt[
        "snapshot"
    ][
        "passing_marks"
    ]

    

    answers = attempt.get(
        "answers",
        {}
    )

    questions = []

    for question in attempt[
        "snapshot"
    ][
        "questions"
    ]:

        selected_answer = answers.get(
            question[
                "question_id"
            ]
        )

        is_correct = (

            selected_answer

            ==

            question[
                "correct_answer"
            ]

        )

        obtained_marks = (

            question[
                "marks"
            ]

            if is_correct

            else

            0

        )

        questions.append(

            ResultQuestionResponse(

                question=question[
                    "question"
                ],

                options=question[
                    "options"
                ],

                selected_answer=selected_answer,

                correct_answer=question[
                    "correct_answer"
                ],

                marks=question[
                    "marks"
                ],

                obtained_marks=obtained_marks,

                is_correct=is_correct

            )

        )

    response= ResultResponse(

        attempt_id=str(
            attempt["_id"]
        ),

        quiz_id=attempt[
            "quiz_id"
        ],

        quiz_title=attempt[
            "snapshot"
        ][
            "title"
        ],

        attempt_number=attempt[
            "attempt_number"
        ],

        score=score,

        total_marks=total_marks,


        passing_percentage=attempt[
            "snapshot"
        ][
            "passing_percentage"
        ],

        passing_marks=passing_marks,

        is_pass=(
            score >= passing_marks
        ),
        percentage = round(
            (score/total_marks)*100,
            2
        ),

        started_at=attempt[
            "started_at"
        ],

        submitted_at=attempt[
            "submitted_at"
        ],

        questions=questions

    )
    return response

def history_helper(
        attempt: dict
) -> AttemptHistoryResponse:
    """
    Convert quiz attempt into
    attempt history response.
    """

    total_marks = attempt[
        "snapshot"
    ][
        "total_marks"
    ]

    score = attempt[
        "score"
    ]


    response= AttemptHistoryResponse(

        attempt_id=str(
            attempt["_id"]
        ),

        quiz_id=attempt[
            "quiz_id"
        ],

        quiz_title=attempt[
            "snapshot"
        ][
            "title"
        ],

        attempt_number=attempt[
            "attempt_number"
        ],

        score=score,

        total_marks=total_marks,

        is_pass=(

            score

            >=

            attempt[
                "snapshot"
            ][
                "passing_marks"
            ]

        ),
        percentage=round(
            (score/total_marks)*100,
            2
        ),

        submitted_at=attempt[
            "submitted_at"
        ]

    )
    return response


async def get_attempt(
        attempt_id: str
) -> dict:
    """
    Retrieve a submitted
    quiz attempt.
    """

    logger.info(
        "Fetching result for attempt '%s'.",
        attempt_id
    )

    attempt_object_id = validate_object_id(
        attempt_id
    )

    attempt = await Repository.get_result_by_attempt_id(
        attempt_object_id
    )

    if not attempt:

        logger.warning(
            "Attempt '%s' not found.",
            attempt_id
        )

        raise ResourceNotFoundException(
            QuizAttemptMessage.NOT_FOUND
        )

    return attempt

class ResultService:
    @staticmethod
    async def get_result(
            attempt_id: str,
            current_user: dict
    ) -> ResultResponse:
        """
        Retrieve result of a student's
        quiz attempt.
        """

        logger.info(
            "Fetching result for attempt '%s'.",
            attempt_id
        )

        attempt = await get_attempt(
            attempt_id
        )

        if attempt["student_id"] != current_user["user_id"]:

            logger.warning(
                "Unauthorized access for attempt '%s'.",
                attempt_id
            )

            raise ResourceNotFoundException(
                QuizAttemptMessage.NOT_FOUND
            )

        logger.info(
            "Result retrieved successfully."
        )

        return result_helper(
            attempt
        )
    
    @staticmethod
    async def get_student_results(
            current_user: dict
    ) -> list[AttemptHistoryResponse]:
        """
        Retrieve all submitted quiz
        attempts of the logged-in student.
        """

        logger.info(
            "Fetching student results."
        )

        attempts = await Repository.get_student_results(
            current_user["user_id"]
        )

        logger.info(
            "Student results retrieved successfully."
        )

        return [

            history_helper(
                attempt
            )

            for attempt in attempts

        ]
    
    @staticmethod
    async def get_result_admin(
            attempt_id: str
    ) -> ResultResponse:
        """
        Retrieve result of any
        student's quiz attempt.
        """

        logger.info(
            "Fetching admin result for attempt '%s'.",
            attempt_id
        )

        attempt = await get_attempt(
            attempt_id
        )

        logger.info(
            "Admin result retrieved successfully."
        )

        return result_helper(
            attempt
        )
    @staticmethod
    async def get_all_results(
    ) -> list[AttemptHistoryResponse]:
        """
        Retrieve all submitted
        quiz results.
        """

        logger.info(
            "Fetching all quiz results."
        )

        attempts = await Repository.get_all_results()

        logger.info(
            "All quiz results retrieved successfully."
        )

        return [

            history_helper(
                attempt
            )

            for attempt in attempts

        ]


