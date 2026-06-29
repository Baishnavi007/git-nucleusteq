"""
Authentication and authorization helper functions
"""

from fastapi import (
    Depends,
    HTTPException,
    status
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


# Extract JWT token from Authorization header
bearer_scheme = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(
            bearer_scheme
        )
):
    """
    Validate JWT token and return user payload
    """

    try:
        token = credentials.credentials

        payload = decode_access_token(token)

        return payload

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


def admin_only(
        user: dict = Depends(get_current_user)
):
    """
    Allow access only to admin users
    """

    if user.get("role") != ADMIN:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user


def student_only(
        user: dict = Depends(get_current_user)
):
    """
    Allow access only to student users
    """

    if user.get("role") != STUDENT:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student access required"
        )

    return user