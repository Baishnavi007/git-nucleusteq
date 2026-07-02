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

    password: str


class UserLogin(BaseModel):
    """
    Schema for user login
    """
    email_or_username: str

    password: str 

class LoginResponse(BaseModel):
    access_token: str
    refresh_token:str
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

class RefreshTokenRequest(BaseModel):
    """
    Schema for refresh token request
    """
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    """
    Schema for refresh token response
    """
    access_token: str
    token_type: str