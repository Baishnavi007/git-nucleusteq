"""
Test cases for Quiz Repository
"""

import pytest

from unittest.mock import (
    AsyncMock,
    MagicMock
)

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

    mock_quizzes.find_one = AsyncMock(
        return_value={
            "_id": ObjectId(),
            "title": "Java Quiz",
            "category_id": "cat123"
        }
    )

    response = await Repository.get_quiz_by_title(
        "Java Quiz",
        "cat123"
    )

    assert response["title"] == "Java Quiz"

    mock_quizzes.find_one.assert_awaited_once_with(
        {
            "title": {
                "$regex": "^Java Quiz$",
                "$options": "i"
            },
            "category_id": "cat123"
        }
    )


@pytest.mark.asyncio
async def test_get_duplicate_quiz(mocker):
    """
    Test duplicate quiz lookup.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    quiz_id = ObjectId()

    mock_quizzes.find_one = AsyncMock(
        return_value={
            "_id": ObjectId(),
            "title": "Java Quiz"
        }
    )

    await Repository.get_duplicate_quiz(
        "Java Quiz",
        "cat123",
        quiz_id
    )

    mock_quizzes.find_one.assert_awaited_once_with(
        {
            "title": {
                "$regex": "^Java Quiz$",
                "$options": "i"
            },
            "category_id": "cat123",
            "_id": {
                "$ne": quiz_id
            }
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

    quiz = {
        "title": "Java Quiz"
    }

    await Repository.create_quiz(
        quiz
    )

    mock_quizzes.insert_one.assert_awaited_once_with(
        quiz
    )


@pytest.mark.asyncio
async def test_get_all_quizzes(mocker):
    """
    Test get all quizzes.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    cursor = MagicMock()

    cursor.to_list = AsyncMock(
        return_value=[
            {
                "_id": ObjectId(),
                "title": "Java Quiz"
            }
        ]
    )

    mock_quizzes.find.return_value = cursor

    response = await Repository.get_all_quizzes()

    assert len(response) == 1

    mock_quizzes.find.assert_called_once()

    cursor.to_list.assert_awaited_once_with(
        length=None
    )


@pytest.mark.asyncio
async def test_get_quizzes_by_category(mocker):
    """
    Test get quizzes by category.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    cursor = MagicMock()

    cursor.to_list = AsyncMock(
        return_value=[
            {
                "_id": ObjectId(),
                "category_id": "cat123"
            }
        ]
    )

    mock_quizzes.find.return_value = cursor

    response = await Repository.get_quizzes_by_category(
        "cat123"
    )

    assert len(response) == 1

    mock_quizzes.find.assert_called_once_with(
        {
            "category_id": "cat123"
        }
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
            "title": "Java Quiz"
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
        "title": "Updated Quiz"
    }

    await Repository.update_quiz(
        quiz_id,
        update_data
    )

    mock_quizzes.update_one.assert_awaited_once_with(
        {
            "_id": quiz_id
        },
        {
            "$set": update_data
        }
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

@pytest.mark.asyncio
async def test_publish_quiz(mocker):
    """
    Test publish quiz.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    mock_quizzes.update_one = AsyncMock()

    quiz_id = ObjectId()

    await Repository.publish_quiz(
        quiz_id
    )

    mock_quizzes.update_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_unpublish_quiz(mocker):
    """
    Test unpublish quiz.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    mock_quizzes.update_one = AsyncMock()

    quiz_id = ObjectId()

    await Repository.unpublish_quiz(
        quiz_id
    )

    mock_quizzes.update_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_published_quizzes_by_category(mocker):
    """
    Test get published quizzes by category.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    cursor = MagicMock()

    cursor.to_list = AsyncMock(
        return_value=[
            {
                "_id": ObjectId(),
                "title": "Java Quiz",
                "is_published": True
            }
        ]
    )

    mock_quizzes.find.return_value = cursor

    response = await Repository.get_published_quizzes_by_category(
        "cat123"
    )

    assert len(response) == 1

    mock_quizzes.find.assert_called_once()


@pytest.mark.asyncio
async def test_delete_quizzes_by_category(mocker):
    """
    Test delete quizzes by category.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    mock_quizzes.delete_many = AsyncMock()

    await Repository.delete_quizzes_by_category(
        "cat123"
    )

    mock_quizzes.delete_many.assert_awaited_once_with(
        {
            "category_id": "cat123"
        }
    )


@pytest.mark.asyncio
async def test_update_quiz_statistics(mocker):
    """
    Test update quiz statistics.
    """

    mock_quizzes = mocker.patch(
        "app.repository.db.quizzes"
    )

    mock_quizzes.update_one = AsyncMock()

    quiz_id = ObjectId()

    await Repository.update_quiz_statistics(
        quiz_id,
        10,
        100
    )

    mock_quizzes.update_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_calculate_quiz_statistics(mocker):
    """
    Test calculate quiz statistics.
    """

    mock_questions = mocker.patch(
        "app.repository.db.questions"
    )

    cursor = MagicMock()

    cursor.to_list = AsyncMock(
        return_value=[
            {
                "marks": 5
            },
            {
                "marks": 10
            }
        ]
    )

    mock_questions.find.return_value = cursor

    total_questions, total_marks = (
        await Repository.calculate_quiz_statistics(
            "quiz123"
        )
    )

    assert total_questions == 2
    assert total_marks == 15