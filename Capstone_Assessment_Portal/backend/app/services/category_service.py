"""
Category business logic
"""

from datetime import datetime, timezone

from bson import ObjectId

from app.config.database import db
from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate
)
from app.utils.helpers import validate_object_id
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
    Handles category management operations
    """

    @staticmethod
    async def create_category(
            category: CategoryCreate,
            current_user: dict
    ):
        """
        Create a new category
        """

        existing_category = await db.categories.find_one(
            {
                "name": {
                    "$regex": f"^{category.name}$",
                    "$options": "i"
                }
            }
        )

        if existing_category:
            logger.warning(
                "Category already exists."
            )
            raise ConflictException(
                "Category already exists."
            )

        category_data = category.model_dump()

        category_data["created_by"] = current_user["username"]

        category_data["created_at"] = datetime.now(
            timezone.utc
        )

        await db.categories.insert_one(
            category_data
        )

        return {
            "message": "Category created successfully."
        }

    @staticmethod
    async def get_all_categories():
        """
        Retrieve all categories
        """

        categories = await db.categories.find().to_list(
            length=None
        )

        for category in categories:

            category["id"] = str(
                category.pop("_id")
            )

        return categories

    @staticmethod
    async def update_category(
            category_id: str,
            category: CategoryUpdate
    ):
        """
        Update an existing category
        """

        category_object_id = validate_object_id(
            category_id
        )
        existing_category = await db.categories.find_one(
            {
                "_id": category_object_id
            }
        )

        if not existing_category:
            logger.warning(
                "Category not found."
            )
            raise ResourceNotFoundException(
                "Category not found."
            )

        duplicate_category = await db.categories.find_one(
            {
                "name": {
                    "$regex": f"^{category.name}$",
                    "$options": "i"
                },
                "_id": {
                    "$ne": category_object_id
                }
            }
        )

        if duplicate_category:
            logger.warning(
                "Category already exists."
            )
            raise ConflictException(
                "Category already exists."
            )

        await db.categories.update_one(
            {
                "_id": category_object_id
            },
            {
                "$set": category.model_dump()
            }
        )

        return {
            "message": "Category updated successfully."
        }

    @staticmethod
    async def delete_category(
            category_id: str
    ):
        """
        Delete an existing category
        """

        category_object_id = validate_object_id(
            category_id
        )

        existing_category = await db.categories.find_one(
            {
                "_id": category_object_id
            }
        )

        if not existing_category:
            logger.warning(
                "Category not found."
            )
            raise ResourceNotFoundException(
                "Category not found."
            )

        await db.categories.delete_one(
            {
                "_id": category_object_id
            }
        )

        return {
            "message": "Category deleted successfully."
        }
    
    @staticmethod
    async def get_category_by_id(
            category_id: str
    ):
        """
        Retrieve a category by its ID
        """

        category_object_id = validate_object_id(
            category_id
        )

        category = await db.categories.find_one(
            {
                "_id": category_object_id
            }
        )

        if not category:
            logger.warning(
                "Category not found."
            )
            raise ResourceNotFoundException(
                "Category not found."
            )

        category["id"] = str(
            category.pop("_id")
        )
        logger.info(
            "Category retrieved successfully."
        )

        return category