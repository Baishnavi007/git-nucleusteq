"""
Authentication business logic
"""

from app.repository import Repository

from app.schemas.user_schema import (
    UserRegister,
    UserLogin,
    LoginResponse
)

from app.security.password_manager import (
    hash_password,
    verify_password
)

from app.security.jwt_manager import (
    create_access_token
)

from app.utils.constants import (
    STUDENT
)

from app.utils.loggers import (
    logger
)


class AuthService:
    """
    Handles user authentication operations
    """

    @staticmethod
    async def register(
            user: UserRegister
    ):
        """
        Create a new student account.
        """

        logger.info(
            "Registration request received for email: %s",
            user.email
        )

        existing_email = await Repository.get_user_by_email(
            user.email
        )

        if existing_email:

            logger.warning(
                "Registration failed. Email already exists: %s",
                user.email
            )

            raise ValueError(
                "Email already exists.Please login"
            )

        existing_username = await Repository.get_user_by_username(
            user.username
        )

        if existing_username:

            logger.warning(
                "Registration failed. Username already exists: %s",
                user.username
            )

            raise ValueError(
                "Username already exists. Please login"
            )

        user_data = user.model_dump()

        user_data["role"] = STUDENT

        user_data["password"] = hash_password(
            user.password
        )

        # Save user into database
        await Repository.create_user(
            user_data
        )

        logger.info(
            "User registered successfully: %s",
            user.username
        )

        return {
            "message": (
                "User registered successfully. "
                "Please login to continue."
            )
        }

    @staticmethod
    async def login(
            user: UserLogin
    ) -> LoginResponse:
        """
        Authenticate user and generate JWT token.
        """

        logger.info(
            "Login attempt for: %s",
            user.email_or_username
        )

        existing_user = (
            await Repository.get_user_by_email_or_username(
                user.email_or_username
            )
        )

        if not existing_user:

            logger.warning(
                "Invalid login attempt for: %s",
                user.email_or_username
            )

            raise ValueError(
                "Invalid credentials"
            )

        if not verify_password(
                user.password,
                existing_user["password"]
        ):

            logger.warning(
                "Invalid password for user: %s",
                user.email_or_username
            )

            raise ValueError(
                "Invalid credentials"
            )

        token = create_access_token(
            existing_user
        )

        logger.info(
            "User logged in successfully: %s",
            existing_user["username"]
        )

        return LoginResponse(
            access_token=token,
            role=existing_user["role"],
            token_type="bearer"
        )