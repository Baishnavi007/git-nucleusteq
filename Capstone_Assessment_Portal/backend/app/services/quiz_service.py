"""
Quiz business logic
"""

from datetime import (
    datetime,
    timezone
)

from app.repository import Repository

from app.schemas.quiz_schema import (
    QuizCreate,
    QuizUpdate
)

from app.utils.helpers import (
    validate_object_id
)

from app.exceptions.conflict_exception import (
    ConflictException
)

from app.exceptions.resource_not_found_exception import (
    ResourceNotFoundException
)

from app.utils.loggers import (
    logger
)


class QuizService:
    """
    Handles quiz management operations.
    """

    @staticmethod
    async def create_quiz(
            category_id: str,
            quiz: QuizCreate,
            current_user: dict
    ):
        """
        Create a new quiz.
        """

        logger.info(
            "Creating quiz '%s'.",
            quiz.title
        )

        category_object_id = validate_object_id(
            category_id
        )

        existing_category = (
            await Repository.get_category_by_id(
                category_object_id
            )
        )

        if not existing_category:

            logger.warning(
                "Category '%s' not found.",
                category_id
            )

            raise ResourceNotFoundException(
                "Category not found."
            )

        existing_quiz = (
            await Repository.get_quiz_by_title(
                quiz.title,
                category_object_id
            )
        )

        if existing_quiz:

            logger.warning(
                "Quiz '%s' already exists.",
                quiz.title
            )

            raise ConflictException(
                "Quiz already exists."
            )

        current_time = datetime.now(
            timezone.utc
        )

        quiz_data = quiz.model_dump()

        quiz_data["category_id"] = (
            category_object_id
        )

        quiz_data["created_by"] = (
            current_user["username"]
        )

        quiz_data["created_at"] = (
            current_time
        )

        quiz_data["updated_at"] = (
            current_time
        )

        await Repository.create_quiz(
            quiz_data
        )

        logger.info(
            "Quiz '%s' created successfully.",
            quiz.title
        )

        return {
            "message": "Quiz created successfully."
        }

    @staticmethod
    async def get_quizzes_by_category(
            category_id: str
    ):
        """
        Retrieve all quizzes of a category.
        """

        logger.info(
            "Fetching quizzes for category '%s'.",
            category_id
        )

        category_object_id = validate_object_id(
            category_id
        )

        existing_category = (
            await Repository.get_category_by_id(
                category_object_id
            )
        )

        if not existing_category:

            logger.warning(
                "Category '%s' not found.",
                category_id
            )

            raise ResourceNotFoundException(
                "Category not found."
            )

        quizzes = (
            await Repository.get_quizzes_by_category(
                category_object_id
            )
        )

        for quiz in quizzes:

            quiz["id"] = str(
                quiz.pop("_id")
            )

            quiz["category_id"] = str(
                quiz["category_id"]
            )

            quiz["category_name"] = (
                existing_category["name"]
            )

        logger.info(
            "%d quizzes fetched successfully.",
            len(quizzes)
        )

        return quizzes

    @staticmethod
    async def get_quiz_by_id(
            quiz_id: str
    ):
        """
        Retrieve quiz details.
        """

        logger.info(
            "Fetching quiz '%s'.",
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
                "Quiz not found."
            )

        category = (
            await Repository.get_category_by_id(
                quiz["category_id"]
            )
        )

        quiz["id"] = str(
            quiz.pop("_id")
        )

        quiz["category_id"] = str(
            quiz["category_id"]
        )

        quiz["category_name"] = (
            category["name"]
        )

        logger.info(
            "Quiz '%s' fetched successfully.",
            quiz["title"]
        )

        return quiz

    @staticmethod
    async def update_quiz(
            quiz_id: str,
            quiz: QuizUpdate
    ):
        """
        Update an existing quiz.
        """

        logger.info(
            "Updating quiz '%s'.",
            quiz_id
        )

        quiz_object_id = validate_object_id(
            quiz_id
        )

        existing_quiz = (
            await Repository.get_quiz_by_id(
                quiz_object_id
            )
        )

        if not existing_quiz:

            logger.warning(
                "Quiz '%s' not found.",
                quiz_id
            )

            raise ResourceNotFoundException(
                "Quiz not found."
            )

        duplicate_quiz = (
            await Repository.get_duplicate_quiz(
                quiz.title,
                existing_quiz["category_id"],
                quiz_object_id
            )
        )

        if duplicate_quiz:

            logger.warning(
                "Quiz '%s' already exists.",
                quiz.title
            )

            raise ConflictException(
                "Quiz already exists."
            )

        quiz_data = quiz.model_dump()

        quiz_data["updated_at"] = (
            datetime.now(
                timezone.utc
            )
        )

        await Repository.update_quiz(
            quiz_object_id,
            quiz_data
        )

        logger.info(
            "Quiz '%s' updated successfully.",
            quiz.title
        )

        return {
            "message": "Quiz updated successfully."
        }

    @staticmethod
    async def delete_quiz(
            quiz_id: str
    ):
        """
        Delete an existing quiz.
        """

        logger.info(
            "Deleting quiz '%s'.",
            quiz_id
        )

        quiz_object_id = validate_object_id(
            quiz_id
        )

        existing_quiz = (
            await Repository.get_quiz_by_id(
                quiz_object_id
            )
        )

        if not existing_quiz:

            logger.warning(
                "Quiz '%s' not found.",
                quiz_id
            )

            raise ResourceNotFoundException(
                "Quiz not found."
            )

        await Repository.delete_quiz(
            quiz_object_id
        )

        logger.info(
            "Quiz '%s' deleted successfully.",
            existing_quiz["title"]
        )

        return {
            "message": "Quiz deleted successfully."
        }