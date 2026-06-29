"""
Password encryption and verification utilities
"""

from passlib.context import CryptContext

# Password hashing configuration using bcrypt
password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Convert plain password into hashed password
    """
    return password_context.hash(password)


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    """
    Match plain password against stored hash
    """
    return password_context.verify(
        plain_password,
        hashed_password
    )