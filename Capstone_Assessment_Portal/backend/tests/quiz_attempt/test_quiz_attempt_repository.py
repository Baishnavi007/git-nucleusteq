"""
Test cases for Quiz Attempt Repository
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from bson import ObjectId

from app.repository import Repository
from app.utils.constants import QuizAttemptStatus


@pytest.mark.asyncio
async def test_create_attempt(mocker):
    """
    Test create attempt.
    """

    mock_attempts = mocker.patch(
        "app.repository.db.attempts"
    )

    mock_attempts.insert_one = AsyncMock()

    attempt_data = {
        "student_id": "student123",
        "quiz_id": "quiz123",
    }

    await Repository.create_attempt(
        attempt_data
    )

    mock_attempts.insert_one.assert_awaited_once_with(
        attempt_data
    )


@pytest.mark.asyncio
async def test_get_attempt_by_id(mocker):
    """
    Test get attempt by id.
    """

    mock_attempts = mocker.patch(
        "app.repository.db.attempts"
    )

    attempt_id = ObjectId()

    mock_attempts.find_one = AsyncMock(
        return_value={
            "_id": attempt_id,
            "status": QuizAttemptStatus.IN_PROGRESS,
        }
    )

    response = await Repository.get_attempt_by_id(
        attempt_id
    )

    assert response["_id"] == attempt_id

    mock_attempts.find_one.assert_awaited_once_with(
        {
            "_id": attempt_id
        }
    )


@pytest.mark.asyncio
async def test_get_student_attempts(mocker):
    """
    Test get student attempts.
    """

    mock_attempts = mocker.patch(
        "app.repository.db.attempts"
    )

    cursor = MagicMock()

    cursor.to_list = AsyncMock(
        return_value=[
            {
                "_id": ObjectId(),
                "student_id": "student123",
                "quiz_id": "quiz123",
            },
            {
                "_id": ObjectId(),
                "student_id": "student123",
                "quiz_id": "quiz123",
            },
        ]
    )

    mock_attempts.find.return_value = cursor

    response = await Repository.get_student_attempts(
        "student123",
        "quiz123",
    )

    assert len(response) == 2

    mock_attempts.find.assert_called_once_with(
        {
            "student_id": "student123",
            "quiz_id": "quiz123",
        }
    )

    cursor.to_list.assert_awaited_once_with(
        length=None
    )


@pytest.mark.asyncio
async def test_get_active_attempt(mocker):
    """
    Test get active attempt.
    """

    mock_attempts = mocker.patch(
        "app.repository.db.attempts"
    )

    mock_attempts.find_one = AsyncMock(
        return_value={
            "_id": ObjectId(),
            "student_id": "student123",
            "quiz_id": "quiz123",
            "status": QuizAttemptStatus.IN_PROGRESS,
        }
    )

    response = await Repository.get_active_attempt(
        "student123",
        "quiz123",
    )

    assert response["status"] == QuizAttemptStatus.IN_PROGRESS

    mock_attempts.find_one.assert_awaited_once_with(
        {
            "student_id": "student123",
            "quiz_id": "quiz123",
            "status": QuizAttemptStatus.IN_PROGRESS,
        }
    )


@pytest.mark.asyncio
async def test_update_attempt(mocker):
    """
    Test update attempt.
    """

    mock_attempts = mocker.patch(
        "app.repository.db.attempts"
    )

    mock_attempts.update_one = AsyncMock()

    attempt_id = ObjectId()

    update_data = {
        "status": QuizAttemptStatus.SUBMITTED
    }

    await Repository.update_attempt(
        attempt_id,
        update_data,
    )

    mock_attempts.update_one.assert_awaited_once_with(
        {
            "_id": attempt_id
        },
        {
            "$set": update_data
        },
    )


@pytest.mark.asyncio
async def test_get_student_results(mocker):
    """
    Test get student results.
    """

    mock_attempts = mocker.patch(
        "app.repository.db.attempts"
    )

    cursor = MagicMock()

    cursor.to_list = AsyncMock(
        return_value=[
            {
                "_id": ObjectId(),
                "student_id": "student123",
                "status": QuizAttemptStatus.SUBMITTED,
            },
            {
                "_id": ObjectId(),
                "student_id": "student123",
                "status": QuizAttemptStatus.TIME_EXPIRED,
            },
        ]
    )

    mock_attempts.find.return_value = cursor

    response = await Repository.get_student_results(
        "student123"
    )

    assert len(response) == 2

    mock_attempts.find.assert_called_once_with(
        {
            "student_id": "student123",
            "status": {
                "$in": [
                    QuizAttemptStatus.SUBMITTED,
                    QuizAttemptStatus.TIME_EXPIRED,
                ]
            },
        }
    )

    cursor.to_list.assert_awaited_once_with(
        length=None
    )