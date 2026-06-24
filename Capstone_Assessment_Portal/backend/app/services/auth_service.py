"""
Authentication business logic
"""

from app.config.database import db
from app.schemas.user_schema import (
    UserRegister,
    UserLogin,
    LoginResponse
)
from app.security.password_manager import (
    hash_password,
    verify_password
)
from app.security.jwt_manager import create_access_token
from app.utils.constants import STUDENT


class AuthService:
    """
    Handles user authentication operations
    """

    @staticmethod
    async def register(user: UserRegister):
        """
        Create a new student account
        """

        existing_email = await db.users.find_one(
            {"email": user.email}
        )

        if existing_email:
            raise ValueError(
                "Email already exists.Please login"
            )

        existing_username = await db.users.find_one(
            {"username": user.username}
        )

        if existing_username:
            raise ValueError(
                "Username already exists. Please login"
            )

        user_data = user.model_dump()

        user_data["role"] = STUDENT

        user_data["password"] = hash_password(
            user.password
        )

        #student data is saved in the database
        await db.users.insert_one(
            user_data
        )

        return {
            "message": "User registered successfully. Please login to continue."
        }

    @staticmethod
    async def login(
            user: UserLogin
    ) -> LoginResponse:
        """
        Authenticate user and generate JWT token
        """

        existing_user = await db.users.find_one(
            {
                "$or": [
                    {
                        "email":
                        user.email_or_username
                    },
                    {
                        "username":
                        user.email_or_username
                    }
                ]
            }
        )

        if not existing_user:
            raise ValueError(
                "Invalid credentials"
            )

        if not verify_password(
                user.password,
                existing_user["password"]
        ):
            raise ValueError(
                "Invalid credentials"
            )

        token = create_access_token(
            existing_user
        )

        return LoginResponse(
            access_token=token,
            role=existing_user["role"],
            token_type="bearer"
        )