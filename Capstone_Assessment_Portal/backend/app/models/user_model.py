"""
User model for database operations
"""

from pydantic import BaseModel, EmailStr

from app.utils.constants import STUDENT


class UserModel(BaseModel):
    """
    User document structure
    """

    first_name: str

    last_name: str

    username: str

    email: EmailStr

    password: str

    role: str = STUDENT