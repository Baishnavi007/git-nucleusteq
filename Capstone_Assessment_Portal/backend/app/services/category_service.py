"""
Category business logic
"""

from datetime import (
    datetime,
    timezone
)

from app.repository import Repository

from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate
)

from app.schemas.common_schema import (
    MessageResponse
)

from app.utils.helpers import (
    validate_object_id
)

from app.utils.constants import (
    CategoryMessage
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


class CategoryService:
    """
    Handles category management operations.
    """

    @staticmethod
    async def create_category(
            category: CategoryCreate,
            current_user: dict
    ) -> MessageResponse:
        """
        Create a new category.
        """

        logger.info(
            "Creating category '%s'.",
            category.name
        )

        existing_category = (
            await Repository.get_category_by_name(
                category.name
            )
        )

        if existing_category:

            logger.warning(
                "Category '%s' already exists.",
                category.name
            )

            raise ConflictException(
                CategoryMessage.ALREADY_EXISTS
            )

        category_data = category.model_dump()

        category_data["created_by"] = (
            current_user["username"]
        )

        category_data["created_at"] = (
            datetime.now(
                timezone.utc
            )
        )

        await Repository.create_category(
            category_data
        )

        logger.info(
            "Category '%s' created successfully.",
            category.name
        )

        return MessageResponse(
            message=CategoryMessage.CREATED
        )

    @staticmethod
    async def get_all_categories():
        """
        Retrieve all categories.
        """

        logger.info(
            "Fetching all categories."
        )

        categories = (
            await Repository.get_all_categories()
        )

        for category in categories:

            category["id"] = str(
                category.pop("_id")
            )

        logger.info(
            "%d categories fetched successfully.",
            len(categories)
        )

        return categories

    @staticmethod
    async def get_category_by_id(
            category_id: str
    ):
        """
        Retrieve a category by its ID.
        """

        logger.info(
            "Fetching category '%s'.",
            category_id
        )

        category_object_id = validate_object_id(
            category_id
        )

        category = (
            await Repository.get_category_by_id(
                category_object_id
            )
        )

        if not category:

            logger.warning(
                "Category '%s' not found.",
                category_id
            )

            raise ResourceNotFoundException(
                CategoryMessage.NOT_FOUND
            )

        category["id"] = str(
            category.pop("_id")
        )

        logger.info(
            "Category '%s' retrieved successfully.",
            category_id
        )

        return category

    @staticmethod
    async def update_category(
            category_id: str,
            category: CategoryUpdate
    ) -> MessageResponse:
        """
        Update an existing category.
        """

        logger.info(
            "Updating category '%s'.",
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
                CategoryMessage.NOT_FOUND
            )

        duplicate_category = (
            await Repository.get_duplicate_category(
                category.name,
                category_object_id
            )
        )

        if duplicate_category:

            logger.warning(
                "Category '%s' already exists.",
                category.name
            )

            raise ConflictException(
                CategoryMessage.ALREADY_EXISTS
            )

        await Repository.update_category(
            category_object_id,
            category.model_dump()
        )

        logger.info(
            "Category '%s' updated successfully.",
            category_id
        )

        return MessageResponse(
            message=CategoryMessage.UPDATED
        )

    @staticmethod
    async def delete_category(
            category_id: str
    ) -> MessageResponse:
        """
        Delete an existing category.
        """

        logger.info(
            "Deleting category '%s'.",
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
                CategoryMessage.NOT_FOUND
            )
        quizzes = await Repository.get_quizzes_by_category(
            category_id
        )

        
        for quiz in quizzes:
            await Repository.delete_questions_by_quiz(
                str(
                    quiz["_id"]
                )
            )
        await Repository.delete_quizzes_by_category(
            category_id
        )

        await Repository.delete_category(
            category_object_id
        )

        logger.info(
            "Category '%s' deleted successfully.",
            category_id
        )

        return MessageResponse(
            message=CategoryMessage.DELETED
        )