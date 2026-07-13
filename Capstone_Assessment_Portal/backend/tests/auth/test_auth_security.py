"""
Test cases for Authentication Security
"""

import pytest

from unittest.mock import MagicMock

from app.security.password_manager import (
    hash_password,
    verify_password
)

from app.security.jwt_manager import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token
)

from app.security.decryption import (
    decrypt_password
)

from app.security.auth_guard import (
    get_current_user,
    admin_only,
    student_only
)

from app.exceptions.bad_request_exception import (
    BadRequestException
)

from app.exceptions.unauthorized_exception import (
    UnauthorizedException
)

from app.exceptions.forbidden_exception import (
    ForbiddenException
)
def test_hash_and_verify_password():
    """
    Test password hashing and verification.
    """

    password = "Password@123"

    hashed_password = hash_password(
        password
    )

    assert hashed_password != password

    assert verify_password(

        password,

        hashed_password

    )

def test_verify_wrong_password():
    """
    Test invalid password verification.
    """

    hashed_password = hash_password(
        "Password@123"
    )

    assert verify_password(

        "WrongPassword",

        hashed_password

    ) is False

def test_create_and_decode_access_token():
    """
    Test access token generation.
    """

    user = {

        "_id": "1",

        "username": "john",

        "email": "john@gmail.com",

        "role": "student"

    }

    token = create_access_token(
        user
    )

    payload = decode_access_token(
        token
    )

    assert payload["email"] == user["email"]

    assert payload["role"] == user["role"]

    assert payload["type"] == "access"

def test_create_and_decode_refresh_token():
    """
    Test refresh token generation.
    """

    user = {

        "_id": "1",

        "username": "john",

        "email": "john@gmail.com",

        "role": "student"

    }

    token = create_refresh_token(
        user
    )

    payload = decode_refresh_token(
        token
    )

    assert payload["email"] == user["email"]

    assert payload["role"] == user["role"]

    assert payload["type"] == "refresh"

def test_invalid_access_token():
    """
    Test invalid access token.
    """

    with pytest.raises(Exception):

        decode_access_token(

            "invalid_token"

        )

def test_invalid_refresh_token():
    """
    Test invalid refresh token.
    """

    with pytest.raises(Exception):

        decode_refresh_token(

            "invalid_token"

        )

def test_get_current_user_success(mocker):
    """
    Test valid access token.
    """

    mocker.patch(

        "app.security.auth_guard.decode_access_token",

        return_value={

            "user_id": "1",

            "username": "john",

            "email": "john@gmail.com",

            "role": "student"

        }

    )

    credentials = MagicMock()

    credentials.credentials = "valid_token"

    user = get_current_user(

        credentials

    )

    assert user["email"] == "john@gmail.com"

    assert user["role"] == "student"

def test_get_current_user_invalid_token(mocker):
    """
    Test invalid access token.
    """

    mocker.patch(

        "app.security.auth_guard.decode_access_token",

        side_effect=Exception()

    )

    credentials = MagicMock()

    credentials.credentials = "invalid_token"

    with pytest.raises(UnauthorizedException):

        get_current_user(

            credentials

        )

def test_admin_only_success():
    """
    Test admin authorization.
    """

    user = {

        "email": "admin@gmail.com",

        "role": "admin"

    }

    assert admin_only(

        user

    ) == user

def test_admin_only_forbidden():
    """
    Test admin authorization failure.
    """

    user = {

        "email": "student@gmail.com",

        "role": "student"

    }

    with pytest.raises(ForbiddenException):

        admin_only(

            user

        )

def test_student_only_success():
    """
    Test student authorization.
    """

    user = {

        "email": "student@gmail.com",

        "role": "student"

    }

    assert student_only(

        user

    ) == user
def test_student_only_forbidden():
    """
    Test student authorization failure.
    """

    user = {

        "email": "admin@gmail.com",

        "role": "admin"

    }

    with pytest.raises(ForbiddenException):

        student_only(

            user

        )