"""
Authentication and authorization helper functions
"""

from fastapi import (
    Depends
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from app.security.jwt_manager import (
    decode_access_token
)

from app.utils.constants import (
    ADMIN,
    STUDENT
)

from app.utils.loggers import (
    logger
)

from app.exceptions.unauthorized_exception import (
    UnauthorizedException
)

from app.exceptions.forbidden_exception import (
    ForbiddenException
)

# Extract JWT token from Authorization header
bearer_scheme = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(
            bearer_scheme
        )
):
    """
    Validate JWT token and return authenticated user.
    """

    try:

        logger.info(
            "Token verification started."
        )

        token = credentials.credentials

        payload = decode_access_token(
            token
        )

        logger.info(
            "Token verified successfully for '%s'.",
            payload["email"]
        )

        return payload

    except Exception:

        logger.warning(
            "Invalid or expired token received."
        )

        raise UnauthorizedException(
            "Invalid or expired token"
        )


def admin_only(
        user: dict = Depends(
            get_current_user
        )
):
    """
    Allow access only to admin users.
    """

    logger.info(
        "Checking admin access for '%s'.",
        user["email"]
    )

    if user.get("role") != ADMIN:

        logger.warning(
            "Admin access denied for '%s'.",
            user["email"]
        )

        raise ForbiddenException(
            "Admin access required"
        )

    logger.info(
        "Admin access granted for '%s'.",
        user["email"]
    )

    return user


def student_only(
        user: dict = Depends(
            get_current_user
        )
):
    """
    Allow access only to student users.
    """

    logger.info(
        "Checking student access for '%s'.",
        user["email"]
    )

    if user.get("role") != STUDENT:

        logger.warning(
            "Student access denied for '%s'.",
            user["email"]
        )

        raise ForbiddenException(
            "Student access required"
        )

    logger.info(
        "Student access granted for '%s'.",
        user["email"]
    )

    return user