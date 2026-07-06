"""
Utility functions for password hashing and verification.
"""

from passlib.context import CryptContext

from app.utils.loggers import logger

# Configure bcrypt as the password hashing algorithm.
password_context = CryptContext(

    schemes=["bcrypt"],

    deprecated="auto"

)


def hash_password(
        password: str
) -> str:
    """
    Hash the user's plain text password before storing it.
    """

    logger.info(
        "Generating password hash."
    )

    hashed_password = password_context.hash(
        password
    )

    logger.info(
        "Password hashed successfully."
    )

    return hashed_password


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    """
    Compare the entered password with the stored hash.
    """

    logger.info(
        "Validating user password."
    )

    is_valid = password_context.verify(

        plain_password,

        hashed_password

    )

    logger.info(
        "Password validation completed."
    )

    return is_valid