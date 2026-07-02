"""
Database repository

Responsibilities:
- Handle all database operations.
- Keep database queries separate from business logic.
"""

from bson import ObjectId

from app.config.database import db


class Repository:
    """
    Handles database operations.
    """

    @staticmethod
    async def get_user_by_email(
            email: str
    ):
        """
        Retrieve user by email.
        """

        return await db.users.find_one(
            {
                "email": email
            }
        )

    @staticmethod
    async def get_user_by_username(
            username: str
    ):
        """
        Retrieve user by username.
        """

        return await db.users.find_one(
            {
                "username": username
            }
        )

    @staticmethod
    async def get_user_by_email_or_username(
            email_or_username: str
    ):
        """
        Retrieve user using email or username.
        """

        return await db.users.find_one(
            {
                "$or": [
                    {
                        "email": email_or_username
                    },
                    {
                        "username": email_or_username
                    }
                ]
            }
        )

    @staticmethod
    async def create_user(
            user_data: dict
    ):
        """
        Save new user.
        """

        return await db.users.insert_one(
            user_data
        )

    @staticmethod
    async def get_category_by_id(
            category_id: ObjectId
    ):
        """
        Retrieve category by id.
        """

        return await db.categories.find_one(
            {
                "_id": category_id
            }
        )

    @staticmethod
    async def get_quiz_by_title(
            title: str,
            category_id: ObjectId
    ):
        """
        Retrieve quiz by title within a category.
        """

        return await db.quizzes.find_one(
            {
                "title": {
                    "$regex": f"^{title}$",
                    "$options": "i"
                },
                "category_id": category_id
            }
        )
    @staticmethod
    async def get_duplicate_quiz(
            title: str,
            category_id: ObjectId,
            quiz_id: ObjectId
    ):
        """
        Retrieve duplicate quiz while updating.
        """

        return await db.quizzes.find_one(
            {
                "title": {
                    "$regex": f"^{title}$",
                    "$options": "i"
                },
                "category_id": category_id,
                "_id": {
                    "$ne": quiz_id
                }
            }
        )

    @staticmethod
    async def create_quiz(
            quiz_data: dict
    ):
        """
        Save new quiz.
        """

        return await db.quizzes.insert_one(
            quiz_data
        )

    @staticmethod
    async def get_quizzes_by_category(
            category_id: ObjectId
    ):
        """
        Retrieve all quizzes of a category.
        """

        return await db.quizzes.find(
            {
                "category_id": category_id
            }
        ).to_list(
            length=None
        )

    @staticmethod
    async def get_quiz_by_id(
            quiz_id: ObjectId
    ):
        """
        Retrieve quiz by id.
        """

        return await db.quizzes.find_one(
            {
                "_id": quiz_id
            }
        )

    @staticmethod
    async def update_quiz(
            quiz_id: ObjectId,
            quiz_data: dict
    ):
        """
        Update an existing quiz.
        """

        return await db.quizzes.update_one(
            {
                "_id": quiz_id
            },
            {
                "$set": quiz_data
            }
        )

    @staticmethod
    async def delete_quiz(
            quiz_id: ObjectId
    ):
        """
        Delete a quiz.
        """

        return await db.quizzes.delete_one(
            {
                "_id": quiz_id
            }
        )

