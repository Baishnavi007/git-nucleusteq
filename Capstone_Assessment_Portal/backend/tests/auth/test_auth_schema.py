"""
Unit tests for authentication schemas.
"""

import pytest
from pydantic import ValidationError

from app.schemas.user_schema import (
    UserRegister,
    UserLogin,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse
)


def test_user_register_valid():
    """
    Test valid user registration schema.
    """

    user = UserRegister(
        first_name="John",
        last_name="Doe",
        username="johndoe",
        email="john@example.com",
        password="encrypted_password"
    )

    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.username == "johndoe"
    assert user.email == "john@example.com"
    assert user.password == "encrypted_password"


def test_user_register_invalid_first_name():
    """
    Test invalid first name.
    """

    with pytest.raises(ValidationError):

        UserRegister(
            first_name="J1",
            last_name="Doe",
            username="johndoe",
            email="john@example.com",
            password="encrypted_password"
        )


def test_user_register_invalid_last_name():
    """
    Test invalid last name.
    """

    with pytest.raises(ValidationError):

        UserRegister(
            first_name="John",
            last_name="D0e",
            username="johndoe",
            email="john@example.com",
            password="encrypted_password"
        )


def test_user_register_invalid_username():
    """
    Test invalid username.
    """

    with pytest.raises(ValidationError):

        UserRegister(
            first_name="John",
            last_name="Doe",
            username="@john",
            email="john@example.com",
            password="encrypted_password"
        )


def test_user_register_invalid_email():
    """
    Test invalid email.
    """

    with pytest.raises(ValidationError):

        UserRegister(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="invalid-email",
            password="encrypted_password"
        )


def test_user_login_valid():
    """
    Test valid login schema.
    """

    login = UserLogin(
        email_or_username="john@example.com",
        password="encrypted_password"
    )

    assert login.email_or_username == "john@example.com"
    assert login.password == "encrypted_password"


def test_login_response_schema():
    """
    Test login response schema.
    """

    response = LoginResponse(
        access_token="access_token",
        refresh_token="refresh_token",
        role="student",
        token_type="bearer",
        username="johndoe"
    )

    assert response.role == "student"
    assert response.token_type == "bearer"
    assert response.username == "johndoe"


def test_refresh_token_request_schema():
    """
    Test refresh token request schema.
    """

    request = RefreshTokenRequest(
        refresh_token="refresh_token"
    )

    assert request.refresh_token == "refresh_token"


def test_refresh_token_response_schema():
    """
    Test refresh token response schema.
    """

    response = RefreshTokenResponse(
        access_token="new_access_token",
        token_type="bearer"
    )

    assert response.access_token == "new_access_token"
    assert response.token_type == "bearer"