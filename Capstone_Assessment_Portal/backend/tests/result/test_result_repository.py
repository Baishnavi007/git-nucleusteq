"""
Test cases for Result Repository
"""

import pytest

from unittest.mock import (
    AsyncMock,
    MagicMock
)

from bson import ObjectId

from app.repository import Repository
from app.config.database import db
from app.utils.constants import QuizAttemptStatus


@pytest.mark.asyncio
async def test_get_result_by_attempt_id(mocker):
    """
    Test get result by attempt id
    """

    mock_attempts = mocker.patch.object(
        db,
        "attempts"
    )

    attempt_id = ObjectId()

    mock_attempts.find_one = AsyncMock(
        return_value={
            "_id": attempt_id,
            "status": QuizAttemptStatus.SUBMITTED,
        }
    )

    response = await Repository.get_result_by_attempt_id(
        attempt_id
    )

    assert response["_id"] == attempt_id

    mock_attempts.find_one.assert_awaited_once_with(
        {
            "_id": attempt_id,
            "status": {
                "$in": [
                    QuizAttemptStatus.SUBMITTED,
                    QuizAttemptStatus.TIME_EXPIRED
                ]
            }
        }
    )


@pytest.mark.asyncio
async def test_get_student_results(mocker):
    """
    Test get student results
    """

    mock_attempts = mocker.patch.object(
        db,
        "attempts"
    )

    student_id = str(ObjectId())

    mock_cursor = MagicMock()

    mock_cursor.to_list = AsyncMock(
        return_value=[
            {
                "_id": ObjectId(),
                "student_id": student_id,
                "status": QuizAttemptStatus.SUBMITTED,
            }
        ]
    )

    mock_attempts.find.return_value = mock_cursor

    response = await Repository.get_student_results(
        student_id
    )

    assert len(response) == 1

    mock_attempts.find.assert_called_once_with(
        {
            "student_id": student_id,
            "status": {
                "$in": [
                    QuizAttemptStatus.SUBMITTED,
                    QuizAttemptStatus.TIME_EXPIRED
                ]
            }
        }
    )

    mock_cursor.to_list.assert_awaited_once_with(
        length=None
    )


@pytest.mark.asyncio
async def test_get_all_results(mocker):
    """
    Test get all results
    """

    mock_attempts = mocker.patch.object(
        db,
        "attempts"
    )

    mock_cursor = MagicMock()

    mock_cursor.to_list = AsyncMock(
        return_value=[
            {
                "_id": ObjectId(),
                "status": QuizAttemptStatus.SUBMITTED,
            }
        ]
    )

    mock_attempts.find.return_value = mock_cursor

    response = await Repository.get_all_results()

    assert len(response) == 1

    mock_attempts.find.assert_called_once_with(
        {
            "status": {
                "$in": [
                    QuizAttemptStatus.SUBMITTED,
                    QuizAttemptStatus.TIME_EXPIRED
                ]
            }
        }
    )

    mock_cursor.to_list.assert_awaited_once_with(
        length=None
    )