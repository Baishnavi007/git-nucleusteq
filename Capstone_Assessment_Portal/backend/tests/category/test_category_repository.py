"""
Test cases for Category Repository
"""

import pytest

from bson import ObjectId

from unittest.mock import (
    AsyncMock,
    MagicMock
)

from app.repository import Repository


@pytest.mark.asyncio
async def test_get_all_categories(mocker):
    """
    Test retrieving all categories.
    """

    mock_categories = mocker.patch(
        "app.repository.db.categories"
    )

    mock_cursor = MagicMock()

    mock_cursor.to_list = AsyncMock(
        return_value=[
            {
                "_id": ObjectId(),
                "name": "Programming",
                "description": "Programming quizzes"
            }
        ]
    )

    mock_categories.find.return_value = mock_cursor

    response = await Repository.get_all_categories()

    assert len(response) == 1

    mock_categories.find.assert_called_once_with()

    mock_cursor.to_list.assert_awaited_once_with(
        length=None
    )


@pytest.mark.asyncio
async def test_get_category_by_name(mocker):
    """
    Test retrieving category by name.
    """

    mock_categories = mocker.patch(
        "app.repository.db.categories"
    )

    mock_categories.find_one = AsyncMock(
        return_value={
            "_id": ObjectId(),
            "name": "Programming",
            "description": "Programming quizzes"
        }
    )

    response = await Repository.get_category_by_name(
        "Programming"
    )

    assert response["name"] == "Programming"

    mock_categories.find_one.assert_awaited_once_with(
        {
            "name": {
                "$regex": "^Programming$",
                "$options": "i"
            }
        }
    )


@pytest.mark.asyncio
async def test_get_category_by_id(mocker):
    """
    Test retrieving category by id.
    """

    mock_categories = mocker.patch(
        "app.repository.db.categories"
    )

    category_id = ObjectId()

    mock_categories.find_one = AsyncMock(
        return_value={
            "_id": category_id,
            "name": "Programming"
        }
    )

    response = await Repository.get_category_by_id(
        category_id
    )

    assert response["_id"] == category_id

    mock_categories.find_one.assert_awaited_once_with(
        {
            "_id": category_id
        }
    )


@pytest.mark.asyncio
async def test_create_category(mocker):
    """
    Test creating category.
    """

    mock_categories = mocker.patch(
        "app.repository.db.categories"
    )

    mock_categories.insert_one = AsyncMock()

    category_data = {
        "name": "Programming",
        "description": "Programming quizzes"
    }

    await Repository.create_category(
        category_data
    )

    mock_categories.insert_one.assert_awaited_once_with(
        category_data
    )


@pytest.mark.asyncio
async def test_update_category(mocker):
    """
    Test updating category.
    """

    mock_categories = mocker.patch(
        "app.repository.db.categories"
    )

    mock_categories.update_one = AsyncMock()

    category_id = ObjectId()

    update_data = {
        "name": "Java"
    }

    await Repository.update_category(
        category_id,
        update_data
    )

    mock_categories.update_one.assert_awaited_once_with(
        {
            "_id": category_id
        },
        {
            "$set": update_data
        }
    )


@pytest.mark.asyncio
async def test_delete_category(mocker):
    """
    Test deleting category.
    """

    mock_categories = mocker.patch(
        "app.repository.db.categories"
    )

    mock_categories.delete_one = AsyncMock()

    category_id = ObjectId()

    await Repository.delete_category(
        category_id
    )

    mock_categories.delete_one.assert_awaited_once_with(
        {
            "_id": category_id
        }
    )


@pytest.mark.asyncio
async def test_get_duplicate_category(mocker):
    """
    Test retrieving duplicate category.
    """

    mock_categories = mocker.patch(
        "app.repository.db.categories"
    )

    category_id = ObjectId()

    mock_categories.find_one = AsyncMock(
        return_value={
            "_id": ObjectId(),
            "name": "Programming"
        }
    )

    await Repository.get_duplicate_category(
        "Programming",
        category_id
    )

    mock_categories.find_one.assert_awaited_once_with(
        {
            "name": {
                "$regex": "^Programming$",
                "$options": "i"
            },
            "_id": {
                "$ne": category_id
            }
        }
    )


@pytest.mark.asyncio
async def test_get_quizzes_by_category(mocker):
    """
    Test retrieving quizzes by category.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    mock_cursor = MagicMock()

    mock_cursor.to_list = AsyncMock(
        return_value=[
            {
                "_id": ObjectId(),
                "title": "Java Quiz"
            }
        ]
    )

    mock_quizzes.find.return_value = mock_cursor

    response = await Repository.get_quizzes_by_category(
        "category123"
    )

    assert len(response) == 1

    mock_quizzes.find.assert_called_once_with(
        {
            "category_id": "category123"
        }
    )

    mock_cursor.to_list.assert_awaited_once_with(
        length=None
    )


@pytest.mark.asyncio
async def test_delete_quizzes_by_category(mocker):
    """
    Test deleting quizzes by category.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    mock_quizzes.delete_many = AsyncMock()

    await Repository.delete_quizzes_by_category(
        "category123"
    )

    mock_quizzes.delete_many.assert_awaited_once_with(
        {
            "category_id": "category123"
        }
    )