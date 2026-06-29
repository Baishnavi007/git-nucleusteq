"""
User request and response schemas
"""

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """
    Schema for user registration
    """
    first_name: str = Field(
        min_length=2, 
        max_length=20, 
        pattern=r"^[A-Za-z]+$"
    )

    last_name: str = Field(
        min_length=2, 
        max_length=20,
        pattern=r"^[A-Za-z]+$"
    )
    
    username: str = Field(
        min_length=4, 
        max_length=20, 
        pattern=r"^[A-Za-z0-9_.-]+$"
    )
    email: EmailStr

    password: str = Field(
        min_length=5, 
        max_length=20, 
        pattern=r"^[A-Za-z0-9@#$]+$"
    )


class UserLogin(BaseModel):
    """
    Schema for user login
    """
    email_or_username: str

    password: str = Field(
        min_length=5, 
        max_length=20, 
        pattern=r"^[A-Za-z0-9@#$]+$"
    )


class LoginResponse(BaseModel):
    access_token: str
    role: str
    token_type: str    


class UserResponse(BaseModel):
    """
    Schema for returning user information
    """
    id: str
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    role: str