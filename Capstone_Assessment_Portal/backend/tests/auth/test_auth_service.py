"""
Test cases for AuthService
"""

import pytest

from unittest.mock import (
    AsyncMock,
    mock_open,
    patch
)

from app.services.auth_service import AuthService

from app.schemas.user_schema import (
    UserRegister,
    UserLogin
)

from app.exceptions.conflict_exception import (
    ConflictException
)

from app.exceptions.bad_request_exception import (
    BadRequestException
)

from app.exceptions.unauthorized_exception import (
    UnauthorizedException
)
@pytest.mark.asyncio
async def test_register_success(mocker):
    """
    Test successful user registration.
    """

    user = UserRegister(

        first_name="John",

        last_name="Doe",

        username="johndoe",

        email="john@gmail.com",

        password="encrypted_password"

    )

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_email",

        new=AsyncMock(return_value=None)

    )

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_username",

        new=AsyncMock(return_value=None)

    )

    mocker.patch(

        "app.services.auth_service.decrypt_password",

        return_value="password123"

    )

    mocker.patch(

        "app.services.auth_service.hash_password",

        return_value="hashed_password"

    )

    create_user = mocker.patch(

        "app.services.auth_service.Repository.create_user",

        new=AsyncMock()

    )

    response = await AuthService.register(user)

    assert response == {

        "message":

        "User registered successfully. Please login to continue."

    }

    create_user.assert_awaited_once()

@pytest.mark.asyncio
async def test_register_duplicate_email(mocker):
    """
    Test registration with existing email.
    """

    user = UserRegister(

        first_name="John",

        last_name="Doe",

        username="johndoe",

        email="john@gmail.com",

        password="encrypted_password"

    )

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_email",

        new=AsyncMock(

            return_value={"email": "john@gmail.com"}

        )

    )

    with pytest.raises(ConflictException):

        await AuthService.register(user)

@pytest.mark.asyncio
async def test_register_duplicate_username(mocker):
    """
    Test registration with existing username.
    """

    user = UserRegister(

        first_name="John",

        last_name="Doe",

        username="johndoe",

        email="john@gmail.com",

        password="encrypted_password"

    )

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_email",

        new=AsyncMock(return_value=None)

    )

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_username",

        new=AsyncMock(

            return_value={"username": "johndoe"}

        )

    )

    with pytest.raises(ConflictException):

        await AuthService.register(user)

@pytest.mark.asyncio
async def test_register_invalid_encrypted_password(mocker):
    """
    Test registration with invalid encrypted password.
    """

    user = UserRegister(

        first_name="John",

        last_name="Doe",

        username="johndoe",

        email="john@gmail.com",

        password="invalid_password"

    )

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_email",

        new=AsyncMock(return_value=None)

    )

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_username",

        new=AsyncMock(return_value=None)

    )

    mocker.patch(

        "app.services.auth_service.decrypt_password",

        side_effect=Exception()

    )

    with pytest.raises(BadRequestException):

        await AuthService.register(user)

@pytest.mark.asyncio
async def test_register_password_too_short(mocker):
    """
    Test registration with short password.
    """

    user = UserRegister(

        first_name="John",

        last_name="Doe",

        username="johndoe",

        email="john@gmail.com",

        password="encrypted"

    )

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_email",

        new=AsyncMock(return_value=None)

    )

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_username",

        new=AsyncMock(return_value=None)

    )

    mocker.patch(

        "app.services.auth_service.decrypt_password",

        return_value="1234"

    )

    with pytest.raises(BadRequestException):

        await AuthService.register(user)

@pytest.mark.asyncio
async def test_register_password_too_long(mocker):
    """
    Test registration with long password.
    """

    user = UserRegister(

        first_name="John",

        last_name="Doe",

        username="johndoe",

        email="john@gmail.com",

        password="encrypted"

    )

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_email",

        new=AsyncMock(return_value=None)

    )

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_username",

        new=AsyncMock(return_value=None)

    )

    mocker.patch(

        "app.services.auth_service.decrypt_password",

        return_value="abcdefghijklmnopqrstuvwxyz"

    )

    with pytest.raises(BadRequestException):

        await AuthService.register(user)

@pytest.mark.asyncio
async def test_login_success(mocker):
    """
    Test successful login.
    """

    user = UserLogin(

        email_or_username="john@gmail.com",

        password="encrypted_password"

    )

    existing_user = {

        "_id": "123",

        "username": "johndoe",

        "email": "john@gmail.com",

        "password": "hashed_password",

        "role": "student"

    }

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_email_or_username",

        new=AsyncMock(return_value=existing_user)

    )

    mocker.patch(

        "app.services.auth_service.decrypt_password",

        return_value="password123"

    )

    mocker.patch(

        "app.services.auth_service.verify_password",

        return_value=True

    )

    mocker.patch(

        "app.services.auth_service.create_access_token",

        return_value="access_token"

    )

    mocker.patch(

        "app.services.auth_service.create_refresh_token",

        return_value="refresh_token"

    )

    response = await AuthService.login(user)

    assert response.access_token == "access_token"

    assert response.refresh_token == "refresh_token"

    assert response.role == "student"

    assert response.username == "johndoe"

@pytest.mark.asyncio
async def test_login_user_not_found(mocker):
    """
    Test login when user does not exist.
    """

    user = UserLogin(

        email_or_username="john@gmail.com",

        password="encrypted_password"

    )

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_email_or_username",

        new=AsyncMock(return_value=None)

    )

    with pytest.raises(UnauthorizedException):

        await AuthService.login(user)

@pytest.mark.asyncio
async def test_login_wrong_password(mocker):
    """
    Test login with wrong password.
    """

    user = UserLogin(

        email_or_username="john@gmail.com",

        password="encrypted_password"

    )

    existing_user = {

        "_id": "123",

        "username": "johndoe",

        "email": "john@gmail.com",

        "password": "hashed_password",

        "role": "student"

    }

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_email_or_username",

        new=AsyncMock(return_value=existing_user)

    )

    mocker.patch(

        "app.services.auth_service.decrypt_password",

        return_value="password123"

    )

    mocker.patch(

        "app.services.auth_service.verify_password",

        return_value=False

    )

    with pytest.raises(UnauthorizedException):

        await AuthService.login(user)

@pytest.mark.asyncio
async def test_login_invalid_encrypted_password(mocker):
    """
    Test login with invalid encrypted password.
    """

    user = UserLogin(

        email_or_username="john@gmail.com",

        password="encrypted_password"

    )

    existing_user = {

        "_id": "123",

        "username": "johndoe",

        "email": "john@gmail.com",

        "password": "hashed_password",

        "role": "student"

    }

    mocker.patch(

        "app.services.auth_service.Repository.get_user_by_email_or_username",

        new=AsyncMock(return_value=existing_user)

    )

    mocker.patch(

        "app.services.auth_service.decrypt_password",

        side_effect=Exception()

    )

    with pytest.raises(BadRequestException):

        await AuthService.login(user)

@pytest.mark.asyncio
async def test_refresh_token_success(mocker):
    """
    Test successful access token regeneration.
    """

    payload = {

        "user_id": "123",

        "username": "johndoe",

        "email": "john@gmail.com",

        "role": "student",

        "type": "refresh"

    }

    mocker.patch(

        "app.services.auth_service.decode_refresh_token",

        return_value=payload

    )

    mocker.patch(

        "app.services.auth_service.create_access_token",

        return_value="new_access_token"

    )

    response = await AuthService.regenerate_refresh_token(
        "refresh_token"
    )

    assert response.access_token == "new_access_token"

    assert response.token_type == "bearer"

@pytest.mark.asyncio
async def test_refresh_token_invalid_type(mocker):
    """
    Test refresh token with invalid token type.
    """

    payload = {

        "user_id": "123",

        "username": "johndoe",

        "email": "john@gmail.com",

        "role": "student",

        "type": "access"

    }

    mocker.patch(

        "app.services.auth_service.decode_refresh_token",

        return_value=payload

    )

    with pytest.raises(UnauthorizedException):

        await AuthService.regenerate_refresh_token(
            "token"
        )
@pytest.mark.asyncio
async def test_get_public_key(mocker):
    """
    Test retrieving public key.
    """

    mock_file = mock_open(

        read_data="PUBLIC_KEY"

    )

    mocker.patch(

        "builtins.open",

        mock_file

    )

    response = await AuthService.get_public_key()

    assert response == {

        "publicKey": "PUBLIC_KEY"

    }