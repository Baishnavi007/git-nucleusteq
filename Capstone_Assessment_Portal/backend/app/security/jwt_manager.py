"""
JWT token generation and validation
"""

from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")


def create_access_token(user: dict) -> str:
    """
    Generate JWT access token
    """

    expiry_time = (
        datetime.now(timezone.utc)
        + timedelta(hours=2)
    )

    payload = {
        "user_id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "exp": expiry_time
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str):
    """
    Decode and validate JWT token
    """

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )