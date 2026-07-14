"""
Test cases for Repository
"""

import pytest
from unittest.mock import AsyncMock

from app.repository import Repository


@pytest.mark.asyncio
async def test_get_user_by_email(mocker):
    """
    Test get user by email
    """

    mock_users = mocker.patch(
        "app.repository.db.users"
    )

    mock_users.find_one = AsyncMock(
        return_value={
            "_id": "1",
            "email": "john@gmail.com",
            "username": "john123",
            "password": "hashed_password",
            "role": "student",
        }
    )

    response = await Repository.get_user_by_email(
        "john@gmail.com"
    )

    assert response["email"] == "john@gmail.com"

    mock_users.find_one.assert_awaited_once_with(
        {
            "email": "john@gmail.com"
        }
    )


@pytest.mark.asyncio
async def test_get_user_by_username(mocker):
    """
    Test get user by username
    """

    mock_users = mocker.patch(
        "app.repository.db.users"
    )

    mock_users.find_one = AsyncMock(
        return_value={
            "_id": "1",
            "email": "john@gmail.com",
            "username": "john123",
            "password": "hashed_password",
            "role": "student",
        }
    )

    response = await Repository.get_user_by_username(
        "john123"
    )

    assert response["username"] == "john123"

    mock_users.find_one.assert_awaited_once_with(
        {
            "username": "john123"
        }
    )


@pytest.mark.asyncio
async def test_get_user_by_email_or_username(mocker):
    """
    Test get user by email or username
    """

    mock_users = mocker.patch(
        "app.repository.db.users"
    )

    mock_users.find_one = AsyncMock(
        return_value={
            "_id": "1",
            "email": "john@gmail.com",
            "username": "john123",
            "password": "hashed_password",
            "role": "student",
        }
    )

    response = await Repository.get_user_by_email_or_username(
        "john@gmail.com"
    )

    assert response["email"] == "john@gmail.com"

    mock_users.find_one.assert_awaited_once_with(
        {
            "$or": [
                {
                    "email": "john@gmail.com"
                },
                {
                    "username": "john@gmail.com"
                }
            ]
        }
    )


@pytest.mark.asyncio
async def test_create_user(mocker):
    """
    Test create user
    """

    mock_users = mocker.patch(
        "app.repository.db.users"
    )

    mock_users.insert_one = AsyncMock()

    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "john123",
        "email": "john@gmail.com",
        "password": "hashed_password",
        "role": "student",
    }

    await Repository.create_user(
        user_data
    )

    mock_users.insert_one.assert_awaited_once_with(
        user_data
    )