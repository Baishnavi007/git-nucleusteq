"""
Test cases for Repository quiz methods
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from bson import ObjectId

from app.repository import Repository


@pytest.mark.asyncio
async def test_get_quiz_by_title(mocker):
    """
    Test get quiz by title.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    category_id = ObjectId()

    mock_quizzes.find_one = AsyncMock(
        return_value={
            "_id": ObjectId(),
            "title": "Java Basics",
            "category_id": category_id,
        }
    )

    response = await Repository.get_quiz_by_title(
        "Java Basics",
        category_id,
    )

    assert response["title"] == "Java Basics"

    mock_quizzes.find_one.assert_awaited_once_with(
        {
            "title": {
                "$regex": "^Java Basics$",
                "$options": "i",
            },
            "category_id": category_id,
        }
    )


@pytest.mark.asyncio
async def test_create_quiz(mocker):
    """
    Test create quiz.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    mock_quizzes.insert_one = AsyncMock()

    quiz_data = {
        "title": "Java Basics",
        "description": "Java fundamentals",
        "duration": 30,
        "category_id": ObjectId(),
    }

    await Repository.create_quiz(
        quiz_data
    )

    mock_quizzes.insert_one.assert_awaited_once_with(
        quiz_data
    )


@pytest.mark.asyncio
async def test_get_quizzes_by_category(mocker):
    """
    Test get quizzes by category.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    category_id = ObjectId()

    mock_cursor = MagicMock()

    mock_cursor.to_list = AsyncMock(
        return_value=[
            {
                "_id": ObjectId(),
                "title": "Java Basics",
                "category_id": category_id,
            }
        ]
    )

    mock_quizzes.find.return_value = mock_cursor

    response = await Repository.get_quizzes_by_category(
        category_id
    )

    assert len(response) == 1

    mock_quizzes.find.assert_called_once_with(
        {
            "category_id": category_id
        }
    )

    mock_cursor.to_list.assert_awaited_once_with(
        length=None
    )


@pytest.mark.asyncio
async def test_get_quiz_by_id(mocker):
    """
    Test get quiz by id.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    quiz_id = ObjectId()

    mock_quizzes.find_one = AsyncMock(
        return_value={
            "_id": quiz_id,
            "title": "Java Basics",
        }
    )

    response = await Repository.get_quiz_by_id(
        quiz_id
    )

    assert response["_id"] == quiz_id

    mock_quizzes.find_one.assert_awaited_once_with(
        {
            "_id": quiz_id
        }
    )


@pytest.mark.asyncio
async def test_get_duplicate_quiz(mocker):
    """
    Test get duplicate quiz.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    quiz_id = ObjectId()

    category_id = ObjectId()

    mock_quizzes.find_one = AsyncMock(
        return_value={
            "_id": ObjectId(),
            "title": "Java Basics",
        }
    )

    await Repository.get_duplicate_quiz(
        "Java Basics",
        category_id,
        quiz_id,
    )

    mock_quizzes.find_one.assert_awaited_once_with(
        {
            "title": {
                "$regex": "^Java Basics$",
                "$options": "i",
            },
            "category_id": category_id,
            "_id": {
                "$ne": quiz_id,
            },
        }
    )


@pytest.mark.asyncio
async def test_update_quiz(mocker):
    """
    Test update quiz.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    mock_quizzes.update_one = AsyncMock()

    quiz_id = ObjectId()

    update_data = {
        "title": "Advanced Java"
    }

    await Repository.update_quiz(
        quiz_id,
        update_data,
    )

    mock_quizzes.update_one.assert_awaited_once_with(
        {
            "_id": quiz_id
        },
        {
            "$set": update_data
        },
    )


@pytest.mark.asyncio
async def test_delete_quiz(mocker):
    """
    Test delete quiz.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    mock_quizzes.delete_one = AsyncMock()

    quiz_id = ObjectId()

    await Repository.delete_quiz(
        quiz_id
    )

    mock_quizzes.delete_one.assert_awaited_once_with(
        {
            "_id": quiz_id
        }
    )