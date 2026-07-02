"""
Utility functions for generating and validating JWT tokens.
"""

from datetime import (
    datetime,
    timedelta,
    timezone
)

import os

from dotenv import load_dotenv
from jose import jwt

from app.utils.loggers import logger

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES"
    )
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv(
        "REFRESH_TOKEN_EXPIRE_DAYS"
    )
)


def create_access_token(
        user: dict
) -> str:
    """
    Create a short-lived JWT access token
    for authenticated requests.
    """

    logger.info(
        "Generating access token for user '%s'.",
        user["email"]
    )

    expiry_time = (
        datetime.now(
            timezone.utc
        )
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {

        "user_id": str(
            user["_id"]
        ),

        "username": user["username"],

        "email": user["email"],

        "role": user["role"],

        "type": "access",

        "exp": expiry_time

    }

    token = jwt.encode(

        payload,

        SECRET_KEY,

        algorithm=ALGORITHM

    )

    logger.info(
        "Access token generated successfully for '%s'.",
        user["email"]
    )

    return token


def create_refresh_token(
        user: dict
) -> str:
    """
    Create a long-lived JWT refresh token
    used to issue new access tokens.
    """

    logger.info(
        "Generating refresh token for user '%s'.",
        user["email"]
    )

    expiry_time = (

        datetime.now(
            timezone.utc
        )

        + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )

    )

    payload = {

        "user_id": str(
            user["_id"]
        ),

        "username": user["username"],

        "email": user["email"],

        "role": user["role"],

        "type": "refresh",

        "exp": expiry_time

    }

    token = jwt.encode(

        payload,

        SECRET_KEY,

        algorithm=ALGORITHM

    )

    logger.info(
        "Refresh token generated successfully for '%s'.",
        user["email"]
    )

    return token


def decode_access_token(
        token: str
):
    """
    Decode and verify an access token.
    """

    logger.info(
        "Validating access token."
    )

    payload = jwt.decode(

        token,

        SECRET_KEY,

        algorithms=[ALGORITHM]

    )

    logger.info(
        "Access token validated for '%s'.",
        payload["email"]
    )

    return payload


def decode_refresh_token(
        token: str
):
    """
    Decode and verify a refresh token.
    """

    logger.info(
        "Validating refresh token."
    )

    payload = jwt.decode(

        token,

        SECRET_KEY,

        algorithms=[ALGORITHM]

    )

    logger.info(
        "Refresh token validated for '%s'.",
        payload["email"]
    )

    return payload