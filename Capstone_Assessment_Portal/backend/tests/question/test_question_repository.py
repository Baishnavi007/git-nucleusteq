"""
Test cases for Question Repository
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from bson import ObjectId

from app.repository import Repository


@pytest.mark.asyncio
async def test_create_question(mocker):
    """
    Test create question.
    """

    mock_questions = mocker.patch("app.repository.db.questions")

    mock_questions.insert_one = AsyncMock()

    question_data = {
        "question": "What is Python?",
        "marks": 5,
    }

    await Repository.create_question(question_data)

    mock_questions.insert_one.assert_awaited_once_with(
        question_data
    )


@pytest.mark.asyncio
async def test_get_question_by_id(mocker):
    """
    Test get question by id.
    """

    mock_questions = mocker.patch("app.repository.db.questions")

    question_id = ObjectId()

    mock_questions.find_one = AsyncMock(
        return_value={
            "_id": question_id,
            "question": "What is Python?"
        }
    )

    response = await Repository.get_question_by_id(
        question_id
    )

    assert response["_id"] == question_id

    mock_questions.find_one.assert_awaited_once_with(
        {"_id": question_id}
    )


@pytest.mark.asyncio
async def test_get_questions_by_quiz(mocker):
    """
    Test get questions by quiz.
    """

    mock_questions = mocker.patch("app.repository.db.questions")

    quiz_id = "quiz123"

    cursor = MagicMock()

    cursor.to_list = AsyncMock(
        return_value=[
            {
                "_id": ObjectId(),
                "quiz_id": quiz_id,
                "question": "Question 1",
            },
            {
                "_id": ObjectId(),
                "quiz_id": quiz_id,
                "question": "Question 2",
            },
        ]
    )

    mock_questions.find.return_value = cursor

    response = await Repository.get_questions_by_quiz(
        quiz_id
    )

    assert len(response) == 2

    mock_questions.find.assert_called_once_with(
        {"quiz_id": quiz_id}
    )

    cursor.to_list.assert_awaited_once_with(
        length=None
    )


@pytest.mark.asyncio
async def test_get_duplicate_question(mocker):
    """
    Test duplicate question.
    """

    mock_questions = mocker.patch("app.repository.db.questions")

    mock_questions.find_one = AsyncMock(
        return_value={
            "_id": ObjectId(),
            "question": "What is Python?"
        }
    )

    await Repository.get_duplicate_question(
        "What is Python?",
        "quiz123"
    )

    mock_questions.find_one.assert_awaited_once_with(
        {
            "question": "What is Python?",
            "quiz_id": "quiz123"
        }
    )


@pytest.mark.asyncio
async def test_get_duplicate_question_for_update(mocker):
    """
    Test duplicate question while update.
    """

    mock_questions = mocker.patch("app.repository.db.questions")

    question_id = ObjectId()

    mock_questions.find_one = AsyncMock(
        return_value={
            "_id": ObjectId(),
            "question": "What is Python?"
        }
    )

    await Repository.get_duplicate_question_for_update(
        "What is Python?",
        "quiz123",
        question_id
    )

    mock_questions.find_one.assert_awaited_once_with(
        {
            "question": {
                "$regex": "^What is Python?$",
                "$options": "i",
            },
            "quiz_id": "quiz123",
            "_id": {
                "$ne": question_id
            },
        }
    )


@pytest.mark.asyncio
async def test_update_question(mocker):
    """
    Test update question.
    """

    mock_questions = mocker.patch("app.repository.db.questions")

    mock_questions.update_one = AsyncMock()

    question_id = ObjectId()

    update_data = {
        "marks": 10
    }

    await Repository.update_question(
        question_id,
        update_data
    )

    mock_questions.update_one.assert_awaited_once_with(
        {
            "_id": question_id
        },
        {
            "$set": update_data
        }
    )


@pytest.mark.asyncio
async def test_delete_question(mocker):
    """
    Test delete question.
    """

    mock_questions = mocker.patch("app.repository.db.questions")

    mock_questions.delete_one = AsyncMock()

    question_id = ObjectId()

    await Repository.delete_question(
        question_id
    )

    mock_questions.delete_one.assert_awaited_once_with(
        {
            "_id": question_id
        }
    )


@pytest.mark.asyncio
async def test_delete_questions_by_quiz(mocker):
    """
    Test delete questions by quiz.
    """

    mock_questions = mocker.patch("app.repository.db.questions")

    mock_questions.delete_many = AsyncMock()

    await Repository.delete_questions_by_quiz(
        "quiz123"
    )

    mock_questions.delete_many.assert_awaited_once_with(
        {
            "quiz_id": "quiz123"
        }
    )