"""
Authentication business logic
"""

from app.repository import Repository

from app.schemas.user_schema import (
    UserRegister,
    UserLogin,
    LoginResponse,
    RefreshTokenResponse
)

from app.security.password_manager import (
    hash_password,
    verify_password
)

from app.security.jwt_manager import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token
)

from app.utils.constants import (
    STUDENT
)

from app.security.decryption import (
    decrypt_password
)

from app.exceptions.bad_request_exception import (
    BadRequestException 
)

from app.exceptions.unauthorized_exception import (
    UnauthorizedException
)

from app.exceptions.conflict_exception import (
    ConflictException
)

from app.utils.loggers import (
    logger
)

PUBLIC_KEY_PATH = "app/keys/public_key.pem"

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

            raise ConflictException(
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

            raise ConflictException(
                "Username already exists. Please login"
            )
        try:
            decrypted_password = decrypt_password(
                user.password,
            )
        except Exception:
            logger.warning(
                "Unable to decrypt password during registration."
            )
            raise BadRequestException(
                "Invalid encrypted password."
            )
        if (len(decrypted_password) < 5 or
            len(decrypted_password) > 20):
            raise BadRequestException(
                "Password must be between 5 and 20 characters."
            )

            

        user_data = user.model_dump()

        user_data["role"] = STUDENT

        user_data["password"] = hash_password(
            decrypted_password
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

            raise UnauthorizedException(
                "Invalid credentials"
            )
        try:
            decrypted_password = decrypt_password(
                user.password,
            )
        except Exception:
            logger.warning(
                "Unable to decrypt password during login."
            )
            raise BadRequestException(
                "Invalid encrypted password."
            )
        if (len(decrypted_password) < 5 or
            len(decrypted_password) > 20):
            raise BadRequestException(
                "Password must be between 5 and 20 characters."
            )

        if not verify_password(
                decrypted_password,
                existing_user["password"]
        ):

            logger.warning(
                "Invalid password for user: %s",
                user.email_or_username
            )

            raise UnauthorizedException(
                "Invalid credentials"
            )

        access_token = create_access_token(
            existing_user
        )

        refresh_token = create_refresh_token(
            existing_user
        )

        logger.info(
            "User logged in successfully: %s",
            existing_user["username"]
        )

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=existing_user["role"],
            token_type="bearer"
        )
    
    @staticmethod
    async def regenerate_refresh_token(
        refresh_token: str
    ) -> RefreshTokenResponse:
        """
        Regenerate a new refresh token using the provided refresh token.
        """                                         
        
        logger.info(
            "Regenerating refresh token."
        )

        payload = decode_refresh_token(
            refresh_token
        )

        if payload.get("type") != "refresh":
            logger.warning(
                "Invalid token type for refresh token regeneration."
            )
            raise UnauthorizedException(
                "Invalid token type"
            )
        access_token = create_access_token(
            {
                "_id": payload["user_id"],

                "username": payload["username"],

                "email": payload["email"],

                "role": payload["role"]
            }
        
        )

        logger.info(
            "Refresh token regenerated successfully for user: %s",
            payload["username"]
        )

        return RefreshTokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
    
    @staticmethod
    async def get_public_key():
        """
        Retrieve RSA public key
        for frontend password encryption.
        """

        logger.info(
            "Public key requested."
        )

        with open(

                PUBLIC_KEY_PATH,

                "r",

                encoding="utf-8"

        ) as key_file:

            public_key = key_file.read()

        logger.info(
            "Public key returned successfully."
        )

        return {

            "publicKey": public_key

        }    