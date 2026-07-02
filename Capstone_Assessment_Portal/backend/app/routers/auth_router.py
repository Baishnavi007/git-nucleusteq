"""
Authentication routes
"""

from fastapi import (
    APIRouter,
    Depends,
    status
)

from app.schemas.user_schema import (
    UserRegister,
    UserLogin,
    LoginResponse,
    RefreshTokenRequest
)

from app.services.auth_service import (
    AuthService
)

from app.security.auth_guard import (
    get_current_user,
    admin_only,
    student_only
)

from app.utils.loggers import (
    logger
)


router = APIRouter(

    prefix="/auth",

    tags=["Authentication"]

)


@router.post(

    "/register",

    status_code=status.HTTP_201_CREATED

)
async def register_user(
        user: UserRegister
):
    """
    Register a new user account.
    """

    logger.info(
        "Registration request received for '%s'.",
        user.email
    )

    return await AuthService.register(
        user
    )


@router.post(

    "/login",

    response_model=LoginResponse

)
async def login_user(
        user: UserLogin
):
    """
    Authenticate an existing user.
    """

    logger.info(
        "Login request received for '%s'.",
        user.email_or_username
    )

    return await AuthService.login(
        user
    )


@router.post(
    "/refresh"
)
async def refresh_access_token(
        data: RefreshTokenRequest
):
    """
    Generate a new access token
    using refresh token.
    """

    logger.info(
        "Refresh token request received."
    )

    return await AuthService.regenerate_access_token(

        data.refresh_token

    )


@router.get(
    "/current-user"
)
async def get_current_user_details(
        current_user=Depends(
            get_current_user
        )
):
    """
    Return authenticated user's details.
    """

    return current_user


@router.get(
    "/admin/dashboard"
)
async def admin_dashboard(
        current_user=Depends(
            admin_only
        )
):
    """
    Test endpoint for admin users.
    """

    logger.info(
        "Admin dashboard accessed by '%s'.",
        current_user["email"]
    )

    return {

        "message": "Welcome Admin",

        "user": current_user

    }


@router.get(
    "/student/dashboard"
)
async def student_dashboard(
        current_user=Depends(
            student_only
        )
):
    """
    Test endpoint for student users.
    """

    logger.info(
        "Student dashboard accessed by '%s'.",
        current_user["email"]
    )

    return {

        "message": "Welcome Student",

        "user": current_user

    }


@router.get(
    "/public-key"
)
async def get_public_key():
    """
    Return RSA public key.
    """

    logger.info(
        "Public key requested."
    )

    return await AuthService.get_public_key()