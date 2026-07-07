"""
Quiz attempt business logic
"""

from datetime import (
    datetime,
    timezone
)

from app.repository import Repository

from app.schemas.quiz_attempt_schema import (
    QuizSnapshot,
    AttemptQuestionSnapshot,
    AttemptResponse,
    AttemptQuestionResponse,
    StudentAnswer
)

from app.schemas.common_schema import (
    MessageResponse
)

from app.utils.helpers import (
    validate_object_id
)

from app.utils.constants import (
    CategoryMessage,
    QuizMessage,
    QuestionMessage,
    QuizAttemptMessage,
    QuizAttemptStatus
)

from app.utils.loggers import (
    logger
)

from app.exceptions.bad_request_exception import (
    BadRequestException
)

from app.exceptions.resource_not_found_exception import (
    ResourceNotFoundException
)

def create_quiz_snapshot(
        quiz: dict,
        questions: list[dict],
        category: dict
) -> QuizSnapshot:
    """
    Create quiz snapshot for an attempt.
    """

    snapshot = QuizSnapshot(

        title=quiz["title"],

        description=quiz["description"],

        category_id=quiz["category_id"],

        category_name=category["name"],

        duration=quiz["duration"],

        questions=[

            AttemptQuestionSnapshot(

                question_id=str(
                    question["_id"]
                ),

                question=question["question"],

                question_type=question["question_type"],

                options=question["options"],

                correct_answer=question["correct_answer"],

                difficulty=question["difficulty"],

                tags=question["tags"],

                marks=question["marks"]

            )

            for question in questions

        ]

    )

    return snapshot

def attempt_helper(
        attempt: dict
) -> AttemptResponse:
    """
    Convert MongoDB attempt document
    into AttemptResponse.
    """

    response = AttemptResponse(

        id=str(
            attempt["_id"]
        ),

        quiz_id=attempt["quiz_id"],

        attempt_number=attempt["attempt_number"],

        status=attempt["status"],

        started_at=attempt["started_at"],

        submitted_at=attempt.get(
            "submitted_at"
        )

    )

    return response

def check_attempt_time_expired(
        attempt: dict
) -> bool:
    """
    Check whether quiz attempt
    has exceeded the allowed time.
    """
    started_at = attempt["started_at"]
    if started_at.tzinfo is None:
        started_at = started_at.replace(
            tzinfo=timezone.utc
        )
    time_spent = (

        datetime.now(
            timezone.utc
        ) - started_at

    ).total_seconds()

    allowed_time = (
        attempt["snapshot"]["duration"] * 60
    )

    return time_spent >= allowed_time

def calculate_score(
        attempt: dict
) -> int:
    """
    Calculate quiz score using
    snapshot and student answers.
    """

    score = 0

    answers = attempt.get(
        "answers",
        {}
    )

    questions = attempt[
        "snapshot"
    ][
        "questions"
    ]

    for question in questions:

        selected_answer = answers.get(
            question["question_id"]
        )

        if (
            selected_answer
            ==
            question["correct_answer"]
        ):

            score += question["marks"]

    return score

async def auto_submit_attempt(
        attempt: dict
):
    """
    Automatically submit an expired
    quiz attempt.
    """

    score = calculate_score(
        attempt
    )

    update_data = {

        "status": QuizAttemptStatus.TIME_EXPIRED,

        "score": score,

        "submitted_at": datetime.now(
            timezone.utc
        )

    }

    await Repository.update_attempt(

        validate_object_id(
            str(
                attempt["_id"]
            )
        ),

        update_data

    )

class QuizAttemptService:
    """
    Handles quiz attempt-related operations.
    """

    @staticmethod
    async def start_attempt(
            quiz_id: str,
            current_user: dict
    ):
        """
        Start a new quiz attempt.
        """

        logger.info(
            "Starting quiz attempt for quiz '%s'.",
            quiz_id
        )

        quiz_object_id = validate_object_id(
            quiz_id
        )

        quiz = await Repository.get_quiz_by_id(
            quiz_object_id
        )

        if not quiz:

            logger.warning(
                "Quiz '%s' not found.",
                quiz_id
            )

            raise ResourceNotFoundException(
                QuizMessage.NOT_FOUND
            )

        if not quiz["is_published"]:

            logger.warning(
                "Quiz '%s' is not published.",
                quiz_id
            )

            raise BadRequestException(
                QuizMessage.NOT_PUBLISHED
            )

        questions = await Repository.get_questions_by_quiz(
            quiz_id
        )

        if not questions:

            logger.warning(
                "No questions found for quiz '%s'.",
                quiz_id
            )

            raise ResourceNotFoundException(
                QuestionMessage.NOT_FOUND
            )
        

        category = await Repository.get_category_by_id(
            validate_object_id(
                quiz["category_id"]
            )
        )
        if not category:

            logger.warning(
                "Category '%s' not found for quiz '%s'.",
                quiz["category_id"],
                quiz_id
            )

            raise ResourceNotFoundException(
                CategoryMessage.NOT_FOUND
            )
        
        active_attempt = (
            await Repository.get_active_attempt(
                current_user["user_id"],
                quiz_id
            )
        )

        if active_attempt:

            logger.warning(
                "Student '%s' already has an active attempt for quiz '%s'.",
                current_user["email"],
                quiz_id
            )

            raise BadRequestException(
                QuizAttemptMessage.ATTEMPT_ALREADY_IN_PROGRESS
            )

        previous_attempts = (
            await Repository.get_student_attempts(
                current_user["user_id"],
                quiz_id
            )
        )

        if len(previous_attempts) >= 3:

            logger.warning(
                "Maximum attempts reached for student '%s'.",
                current_user["email"]
            )

            raise BadRequestException(
                QuizAttemptMessage.MAX_ATTEMPTS_REACHED
            )

        attempt_number = (
            len(previous_attempts) + 1
        )
        snapshot = create_quiz_snapshot(

            quiz,

            questions,

            category

        )

        attempt_data = {

            "quiz_id": quiz_id,

            "student_id": current_user["user_id"],

            "attempt_number": attempt_number,

            "status": QuizAttemptStatus.IN_PROGRESS,

            "started_at": datetime.now(
                timezone.utc
            ),

            "submitted_at": None,

            "score": 0,

            "answers": {},

            "snapshot": snapshot.model_dump()

        }

        result = await Repository.create_attempt(

            attempt_data

        )

        created_attempt = await Repository.get_attempt_by_id(

            result.inserted_id

        )

        logger.info(

            "Quiz attempt started successfully for student '%s'.",

            current_user["email"]

        )

        response = attempt_helper(

            created_attempt

        )

        return response

    @staticmethod
    async def get_attempt_questions(
            attempt_id: str,
            current_user: dict
    ):
        """
        Retrieve questions of an attempt.
        """

        logger.info(
            "Fetching questions for attempt '%s'.",
            attempt_id
        )

        attempt_object_id = validate_object_id(
            attempt_id
        )

        attempt = await Repository.get_attempt_by_id(
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
        
        if attempt["student_id"] != current_user["user_id"]:

            logger.warning(
                "Unauthorized access for attempt '%s'.",
                attempt_id
            )

            raise ResourceNotFoundException(
                QuizAttemptMessage.NOT_FOUND
            )
        if (
            attempt["status"]
            ==
            QuizAttemptStatus.SUBMITTED
        ):

            raise BadRequestException(
                QuizAttemptMessage.ATTEMPT_ALREADY_SUBMITTED
            )
        
        if check_attempt_time_expired(
            attempt
        ):

            await auto_submit_attempt(
                attempt
            )

            raise BadRequestException(
                QuizAttemptMessage.TIME_EXPIRED
            )
        
        response = []

        for question in attempt[
            "snapshot"
        ][
            "questions"
        ]:

            response.append(

                AttemptQuestionResponse(

                    id=question[
                        "question_id"
                    ],

                    question=question[
                        "question"
                    ],

                    question_type=question[
                        "question_type"
                    ],

                    options=question[
                        "options"
                    ],

                    difficulty=question[
                        "difficulty"
                    ],

                    tags=question[
                        "tags"
                    ],

                    marks=question[
                        "marks"
                    ],

                    selected_answer=attempt.get(
                        "answers",
                        {}
                    ).get(
                        question[
                            "question_id"
                        ]
                    )

                )

            )

        logger.info(
            "Questions fetched successfully for attempt '%s'.",
            attempt_id
        )

        return response

    @staticmethod
    async def save_answer(
            attempt_id: str,
            answer: StudentAnswer,
            current_user: dict
    ):
        """
        Save student's answer.
        """

        logger.info(
            "Saving answer for attempt '%s'.",
            attempt_id
        )

        attempt_object_id = validate_object_id(
            attempt_id
        )

        attempt = await Repository.get_attempt_by_id(
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

        if attempt["student_id"] != current_user["user_id"]:

            logger.warning(
                "Unauthorized access for attempt '%s'.",
                attempt_id
            )

            raise ResourceNotFoundException(
                QuizAttemptMessage.NOT_FOUND
            )

        if (
            attempt["status"]
            ==
            QuizAttemptStatus.SUBMITTED
        ):

            raise BadRequestException(
                QuizAttemptMessage.ATTEMPT_ALREADY_SUBMITTED
            )

        if check_attempt_time_expired(
            attempt
        ):

            await auto_submit_attempt(
                attempt
            )

            raise BadRequestException(
                QuizAttemptMessage.TIME_EXPIRED
            )
        question_exists = False

        for question in attempt[
            "snapshot"
        ][
            "questions"
        ]:

            if (
                question["question_id"]
                ==
                answer.question_id
            ):

                question_exists = True

                break

        if not question_exists:

            logger.warning(
                "Question '%s' not found in attempt.",
                answer.question_id
            )

            raise ResourceNotFoundException(
                QuestionMessage.NOT_FOUND
            )
        
        answers = attempt.get(
            "answers",
            {}
        )

        answers[
            answer.question_id
        ] = answer.selected_answer

        await Repository.update_attempt(

            attempt_object_id,

            {
                "answers": answers
            }

        )

        logger.info(
            "Answer saved successfully."
        )

        return MessageResponse(

            message=QuizAttemptMessage.ANSWER_SAVED

        )
    
    @staticmethod
    async def submit_attempt(
            attempt_id: str,
            current_user: dict
    ):
        """
        Submit a quiz attempt.
        """

        logger.info(
            "Submitting attempt '%s'.",
            attempt_id
        )

        attempt_object_id = validate_object_id(
            attempt_id
        )

        attempt = await Repository.get_attempt_by_id(
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

        if attempt["student_id"] != current_user["user_id"]:

            logger.warning(
                "Unauthorized access for attempt '%s'.",
                attempt_id
            )

            raise ResourceNotFoundException(
                QuizAttemptMessage.NOT_FOUND
            )

        if (
            attempt["status"]
            ==
            QuizAttemptStatus.SUBMITTED
        ):

            raise BadRequestException(
                QuizAttemptMessage.ATTEMPT_ALREADY_SUBMITTED
            )
        if check_attempt_time_expired(
            attempt
        ):

            await auto_submit_attempt(
                attempt
            )

            raise BadRequestException(
                QuizAttemptMessage.TIME_EXPIRED
            )
        
        score = calculate_score(
            attempt
        )

        update_data = {

            "status": QuizAttemptStatus.SUBMITTED,

            "score": score,

            "submitted_at": datetime.now(
                timezone.utc
            )

        }

        await Repository.update_attempt(

            attempt_object_id,

            update_data

        )

        logger.info(
            "Attempt '%s' submitted successfully.",
            attempt_id
        )

        return MessageResponse(

            message=QuizAttemptMessage.SUBMITTED

        )
    
    @staticmethod
    async def get_student_attempts(
            quiz_id: str,
            current_user: dict
    ):
        """
        Retrieve all attempts of a student for a quiz.
        """

        logger.info(
            "Fetching attempts for student '%s' and quiz '%s'.",
            current_user["email"],
            quiz_id
        )

        quiz_object_id = validate_object_id(
            quiz_id 
         )
        quiz = await Repository.get_quiz_by_id(
            quiz_object_id  
        )
        if not quiz:

            logger.warning(
                "Quiz '%s' not found.",
                quiz_id
            )

            raise ResourceNotFoundException(
                QuizMessage.NOT_FOUND
            )

        attempts = (
            await Repository.get_student_attempts(
                current_user["user_id"],
                quiz_id
            )
        )

        response = []
        for attempt in attempts:

            response.append(
                attempt_helper(
                    attempt
                )
            )

        logger.info(
            "%d attempts fetched successfully for student '%s' and quiz '%s'.",
            len(response),
            current_user["email"],
            quiz_id
        )

        return response