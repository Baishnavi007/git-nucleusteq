"""
Database repository

Responsibilities:
- Handle all database operations.
- Keep database queries separate from business logic.
"""

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