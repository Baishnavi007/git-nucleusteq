"""
Question business logic
"""

from datetime import (
    datetime,
    timezone
)

from app.repository import Repository
from app.schemas.common_schema import(
    MessageResponse
)
from app.schemas.question_schema import (
    QuestionCreate,
    QuestionUpdate
)

from app.utils.constants import(
    QuestionMessage,
    QuizMessage,
    VALID_QUESTION_TYPES,
    VALID_DIFFICULTY_LEVELS
)
from app.utils.helpers import (
    validate_object_id,
    normalize_text
)

from app.exceptions.bad_request_exception import (
    BadRequestException
)

from app.exceptions.conflict_exception import (
    ConflictException
)

from app.exceptions.resource_not_found_exception import (ResourceNotFoundException)

from app.utils.loggers import (
    logger
)



class QuestionService:
    """
    Handles question management operations.
    """

    @staticmethod
    def validate_question_type(
            question_type: str
    ):
        """
        Validate question type.
        """
        question_type = question_type.lower()
        if question_type not in VALID_QUESTION_TYPES:

            logger.warning(
                "Invalid question type '%s'.",
                question_type
            )

            raise BadRequestException(
                QuestionMessage.INVALID_QUESTION_TYPE
            )

    @staticmethod
    def validate_difficulty(
            difficulty: str
    ):
        """
        Validate difficulty level.
        """

        difficulty = difficulty.lower()
        if difficulty not in VALID_DIFFICULTY_LEVELS:

            logger.warning(
                "Invalid difficulty level '%s'.",
                difficulty
            )

            raise BadRequestException(
                QuestionMessage.INVALID_DIFFICULTY
            )

    @staticmethod
    def validate_correct_answer(
            question: QuestionCreate
            | QuestionUpdate
    ):
        """
        Validate correct answer according
        to question type.
        """

        if question.question_type.lower() == "mcq":

            if question.correct_answer not in question.options:

                logger.warning(
                    "Correct answer is not present in options."
                )

                raise BadRequestException(
                    QuestionMessage.INVALID_CORRECT_ANSWER
                )

        elif question.question_type.lower() == "true_false":

            if set(question.options) != {
                "True",
                "False"
            }:

                logger.warning(
                    "Invalid options for True/False question."
                )

                raise BadRequestException(
                    QuestionMessage.INVALID_TRUE_FALSE_OPTIONS
                )
            correct_answer = question.correct_answer.strip().lower()

            if correct_answer not in [
                "true",
                "false"
            ]:

                logger.warning(
                    "Invalid correct answer for True/False question."
                )

                raise BadRequestException(
                    QuestionMessage.INVALID_TRUE_FALSE_ANSWER
                )
    @staticmethod
    async def create_question(
            quiz_id: str,
            question: QuestionCreate,
            current_user: dict
    ) -> MessageResponse:
        """
        Create a new question.
        """

        logger.info(
            "Creating a new question."
        )

        quiz_object_id = validate_object_id(
            quiz_id
        )

        existing_quiz = await Repository.get_quiz_by_id(
            quiz_object_id
        )

        if not existing_quiz:

            logger.warning(
                "Quiz '%s' not found.",
                quiz_id
            )

            raise ResourceNotFoundException(
                QuizMessage.NOT_FOUND
            )
        question_text = normalize_text(question.question)

        existing_question = (await Repository.get_duplicate_question(
            question_text,
            quiz_id
        )
        )
        if existing_question:

            logger.warning(
                "Duplicate question found."
            )

            raise ConflictException(
                QuestionMessage.ALREADY_EXISTS
            )
        QuestionService.validate_question_type(
            question.question_type
        )   
        QuestionService.validate_difficulty(
            question.difficulty
        )
        QuestionService.validate_correct_answer(
            question
        )
        current_time = datetime.now(
            timezone.utc
        )
        question_data = question.model_dump()
        question_data["question"] = question_text
        question_data["question_type"] = question.question_type.lower()
        question_data["difficulty"] = question.difficulty.lower()  
        question_data["quiz_id"] = quiz_id
        question_data["created_by"] = current_user["username"]
        question_data["created_at"] = current_time
        question_data["updated_at"] = current_time
        await Repository.create_question(
            question_data       
        )
        logger.info(
            "Question created successfully."
        )
        return MessageResponse(
            message=QuestionMessage.CREATED
        )
            
    @staticmethod
    async def get_questions_by_quiz(
            quiz_id: str
    ):
        """
        Retrieve all questions for a specific quiz.
        """

        logger.info(
            "Retrieving questions for quiz '%s'.",
            quiz_id
        )

        quiz_object_id = validate_object_id(
            quiz_id
        )

        existing_quiz = await Repository.get_quiz_by_id(
            quiz_object_id
        )

        if not existing_quiz:

            logger.warning(
                "Quiz '%s' not found.",
                quiz_id
            )

            raise ResourceNotFoundException(
                QuizMessage.NOT_FOUND
            )

        questions = await Repository.get_questions_by_quiz(
            quiz_id
        )

        for question in questions:

            question["id"] = str(
                question.pop("_id")
            )
        logger.info(
            "Retrieved %d questions for quiz '%s'.",
            len(questions),
            quiz_id
        )
        return questions
    
    @staticmethod
    async def get_question_by_id(
            question_id: str
    ):
        """
        Retrieve a question by its ID.
        """

        logger.info(
            "Retrieving question '%s'.",
            question_id
        )

        question_object_id = validate_object_id(
            question_id
        )

        question = await Repository.get_question_by_id(
            question_object_id
        )
        if not question:
            logger.warning(
                "Question '%s' not found.",
                question_id
            )
            raise ResourceNotFoundException(
                QuestionMessage.NOT_FOUND
            )
        question["id"] = str(
            question.pop("_id")
        )
        logger.info(
            "Retrieved question '%s' successfully.",
            question_id
        )
        return question
    
    @staticmethod
    async def update_question(
            question_id: str,
            question: QuestionUpdate,
            
    ) -> MessageResponse:
        """
        Update an existing question.
        """

        logger.info(
            "Updating question '%s'.",
            question_id
        )

        question_object_id = validate_object_id(
            question_id
        )

        existing_question = await Repository.get_question_by_id(
            question_object_id
        )

        if not existing_question:

            logger.warning(
                "Question '%s' not found.",
                question_id
            )

            raise ResourceNotFoundException(
                QuestionMessage.NOT_FOUND
            )
        question_text=normalize_text(question.question)
        duplicate_question = await Repository.get_duplicate_question_for_update(
            question_text,
            existing_question["quiz_id"],
            question_object_id
        )

        if duplicate_question:

            logger.warning(
                "Duplicate question found."
            )

            raise ConflictException(
                QuestionMessage.ALREADY_EXISTS
            )
        QuestionService.validate_question_type(
            question.question_type  
        )
        QuestionService.validate_difficulty(
            question.difficulty
        )
        QuestionService.validate_correct_answer(
            question
        )   

        question_data = question.model_dump()
        question_data["question"] = question_text
        question_data["question_type"] = question.question_type.lower()
        question_data["difficulty"] = question.difficulty.lower()
        question_data["updated_at"] = datetime.now(
            timezone.utc
        )

        await Repository.update_question(
            question_object_id,
            question_data
        )
        logger.info(
            "Question '%s' updated successfully.",
            question_id
        )
        return MessageResponse(
            message=QuestionMessage.UPDATED
        )

    @staticmethod
    async def delete_question(
            question_id: str
    ) -> MessageResponse:
        """
        Delete a question by its ID.
        """

        logger.info(
            "Deleting question '%s'.",
            question_id
        )

        question_object_id = validate_object_id(
            question_id
        )

        existing_question = await Repository.get_question_by_id(
            question_object_id
        )

        if not existing_question:

            logger.warning(
                "Question '%s' not found.",
                question_id
            )

            raise ResourceNotFoundException(
                QuestionMessage.NOT_FOUND
            )

        await Repository.delete_question(
            question_object_id
        )
        logger.info(
            "Question '%s' deleted successfully.",
            question_id
        )
        return MessageResponse(
            message=QuestionMessage.DELETED
        )