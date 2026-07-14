"""
Test cases for QuizAttemptService
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from bson import ObjectId

from app.services.quiz_attempt_service import QuizAttemptService

from app.schemas.quiz_attempt_schema import (
    StudentAnswer,
)

from app.exceptions.bad_request_exception import (
    BadRequestException,
)

from app.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)

from app.utils.constants import (
    QuizAttemptMessage,
    QuizAttemptStatus,
    QuizMessage,
    QuestionMessage,
    CategoryMessage,
)


@pytest.mark.asyncio
async def test_start_attempt_success(mocker):
    """
    Test successful quiz attempt creation.
    """

    quiz_id = str(ObjectId())
    category_id = str(ObjectId())

    mock_quiz = {
        "_id": ObjectId(quiz_id),
        "title": "Python Quiz",
        "description": "Basic Python Quiz",
        "category_id": category_id,
        "duration": 30,
        "total_questions": 1,
        "total_marks": 10,
        "passing_percentage": 40,
        "is_published": True,
    }

    mock_questions = [
        {
            "_id": ObjectId(),
            "question": "Python is?",
            "question_type": "MCQ",
            "options": ["Language", "Database"],
            "correct_answer": "Language",
            "difficulty": "Easy",
            "tags": ["python"],
            "marks": 10,
        }
    ]

    mock_category = {
        "_id": ObjectId(category_id),
        "name": "Programming",
    }

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_quiz_by_id",
        new=AsyncMock(return_value=mock_quiz),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_questions_by_quiz",
        new=AsyncMock(return_value=mock_questions),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_category_by_id",
        new=AsyncMock(return_value=mock_category),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_active_attempt",
        new=AsyncMock(return_value=None),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_student_attempts",
        new=AsyncMock(return_value=[]),
    )

    inserted = MagicMock()
    inserted.inserted_id = ObjectId()

    mock_create = mocker.patch(
        "app.services.quiz_attempt_service.Repository.create_attempt",
        new=AsyncMock(return_value=inserted),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_attempt_by_id",
        new=AsyncMock(
            return_value={
                "_id": inserted.inserted_id,
                "quiz_id": quiz_id,
                "attempt_number": 1,
                "status": QuizAttemptStatus.IN_PROGRESS,
                "started_at": datetime.now(timezone.utc),
                "submitted_at": None,
            }
        ),
    )

    response = await QuizAttemptService.start_attempt(
        quiz_id,
        {
            "user_id": str(ObjectId()),
            "email": "student@test.com",
        },
    )

    assert response.quiz_id == quiz_id
    assert response.attempt_number == 1
    assert response.status == QuizAttemptStatus.IN_PROGRESS

    mock_create.assert_awaited_once()


@pytest.mark.asyncio
async def test_start_attempt_quiz_not_found(mocker):
    """
    Test start attempt when quiz does not exist.
    """

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_quiz_by_id",
        new=AsyncMock(return_value=None),
    )

    with pytest.raises(ResourceNotFoundException) as exc:

        await QuizAttemptService.start_attempt(
            str(ObjectId()),
            {
                "user_id": str(ObjectId()),
                "email": "student@test.com",
            },
        )

    assert str(exc.value) == QuizMessage.NOT_FOUND


@pytest.mark.asyncio
async def test_start_attempt_not_published(mocker):
    """
    Test start attempt when quiz is unpublished.
    """

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(),
                "is_published": False,
            }
        ),
    )

    with pytest.raises(BadRequestException) as exc:

        await QuizAttemptService.start_attempt(
            str(ObjectId()),
            {
                "user_id": str(ObjectId()),
                "email": "student@test.com",
            },
        )

    assert str(exc.value) == QuizMessage.NOT_PUBLISHED


@pytest.mark.asyncio
async def test_start_attempt_no_questions(mocker):
    """
    Test start attempt when quiz has no questions.
    """

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(),
                "category_id": str(ObjectId()),
                "is_published": True,
            }
        ),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_questions_by_quiz",
        new=AsyncMock(return_value=[]),
    )

    with pytest.raises(ResourceNotFoundException) as exc:

        await QuizAttemptService.start_attempt(
            str(ObjectId()),
            {
                "user_id": str(ObjectId()),
                "email": "student@test.com",
            },
        )

    assert str(exc.value) == QuestionMessage.NOT_FOUND

@pytest.mark.asyncio
async def test_start_attempt_category_not_found(mocker):
    """
    Test start attempt when category does not exist.
    """

    quiz_id = str(ObjectId())
    category_id = str(ObjectId())

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(quiz_id),
                "category_id": category_id,
                "is_published": True,
            }
        ),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_questions_by_quiz",
        new=AsyncMock(
            return_value=[
                {
                    "_id": ObjectId(),
                    "question": "Python?",
                    "question_type": "MCQ",
                    "options": ["A", "B"],
                    "correct_answer": "A",
                    "difficulty": "Easy",
                    "tags": [],
                    "marks": 5,
                }
            ]
        ),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_category_by_id",
        new=AsyncMock(return_value=None),
    )

    with pytest.raises(ResourceNotFoundException) as exc:

        await QuizAttemptService.start_attempt(
            quiz_id,
            {
                "user_id": str(ObjectId()),
                "email": "student@test.com",
            },
        )

    assert str(exc.value) == CategoryMessage.NOT_FOUND


@pytest.mark.asyncio
async def test_start_attempt_already_active(mocker):
    """
    Test start attempt when another attempt is already active.
    """

    quiz_id = str(ObjectId())
    category_id = str(ObjectId())

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(quiz_id),
                "category_id": category_id,
                "is_published": True,
            }
        ),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_questions_by_quiz",
        new=AsyncMock(
            return_value=[
                {
                    "_id": ObjectId(),
                    "question": "Python?",
                    "question_type": "MCQ",
                    "options": ["A", "B"],
                    "correct_answer": "A",
                    "difficulty": "Easy",
                    "tags": [],
                    "marks": 5,
                }
            ]
        ),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_category_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(category_id),
                "name": "Programming",
            }
        ),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_active_attempt",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(),
            }
        ),
    )

    with pytest.raises(BadRequestException) as exc:

        await QuizAttemptService.start_attempt(
            quiz_id,
            {
                "user_id": str(ObjectId()),
                "email": "student@test.com",
            },
        )

    assert str(exc.value) == QuizAttemptMessage.ATTEMPT_ALREADY_IN_PROGRESS


@pytest.mark.asyncio
async def test_start_attempt_max_attempts(mocker):
    """
    Test start attempt when maximum attempts reached.
    """

    quiz_id = str(ObjectId())
    category_id = str(ObjectId())

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(quiz_id),
                "category_id": category_id,
                "is_published": True,
            }
        ),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_questions_by_quiz",
        new=AsyncMock(
            return_value=[
                {
                    "_id": ObjectId(),
                    "question": "Python?",
                    "question_type": "MCQ",
                    "options": ["A", "B"],
                    "correct_answer": "A",
                    "difficulty": "Easy",
                    "tags": [],
                    "marks": 5,
                }
            ]
        ),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_category_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(category_id),
                "name": "Programming",
            }
        ),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_active_attempt",
        new=AsyncMock(return_value=None),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_student_attempts",
        new=AsyncMock(
            return_value=[
                {"attempt_number": 1},
                {"attempt_number": 2},
                {"attempt_number": 3},
            ]
        ),
    )

    with pytest.raises(BadRequestException) as exc:

        await QuizAttemptService.start_attempt(
            quiz_id,
            {
                "user_id": str(ObjectId()),
                "email": "student@test.com",
            },
        )

    assert str(exc.value) == QuizAttemptMessage.MAX_ATTEMPTS_REACHED


@pytest.mark.asyncio
async def test_get_attempt_questions_success(mocker):
    """
    Test get attempt questions successfully.
    """

    attempt_id = str(ObjectId())
    student_id = str(ObjectId())

    mock_attempt = {
        "_id": ObjectId(attempt_id),
        "student_id": student_id,
        "status": QuizAttemptStatus.IN_PROGRESS,
        "started_at": datetime.now(timezone.utc),
        "answers": {
           "q1": "Python"
        },
        "snapshot": {
            "duration": 30,
            "questions": [
                {
                    "question_id": "q1",
                    "question": "Python is?",
                    "question_type": "MCQ",
                    "options": ["Java", "Python"],
                    "difficulty": "Easy",
                    "tags": [], 
                    "marks": 5,
                }
            ]
        },
    }

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_attempt_by_id",
        new=AsyncMock(return_value=mock_attempt),
    )

    response = await QuizAttemptService.get_attempt_questions(
        attempt_id,
        {
            "user_id": student_id,
        },
    )

    assert len(response) == 1
    assert response[0].question == "Python is?"
    assert response[0].selected_answer == "Python"

@pytest.mark.asyncio
async def test_save_answer_success(mocker):
    """
    Test save answer successfully.
    """

    attempt_id = str(ObjectId())
    student_id = str(ObjectId())

    mock_attempt = {
        "_id": ObjectId(attempt_id),
        "student_id": student_id,
        "status": QuizAttemptStatus.IN_PROGRESS,
        "answers": {},
        "started_at": datetime.now(timezone.utc),
        "snapshot": {
            "duration":30,
            "questions": [
                {   
                    "question_id": "q1",
                    "correct_answer": "Python",
                    "options": ["Java", "Python"],
                }
            ]
        },
    }

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_attempt_by_id",
        new=AsyncMock(return_value=mock_attempt),
    )

    mock_update = mocker.patch(
        "app.services.quiz_attempt_service.Repository.update_attempt",
        new=AsyncMock(),
    )

    response = await QuizAttemptService.save_answer(
        attempt_id,
        StudentAnswer(
            question_id="q1",
            selected_answer="Python",
        ),
        {
            "user_id": student_id,
        },
    )

    assert response.message == QuizAttemptMessage.ANSWER_SAVED
    mock_update.assert_awaited_once()


@pytest.mark.asyncio
async def test_submit_attempt_success(mocker):
    """
    Test submit attempt successfully.
    """

    attempt_id = str(ObjectId())
    student_id = str(ObjectId())

    mock_attempt = {
        "_id": ObjectId(attempt_id),
        "student_id": student_id,
        "status": QuizAttemptStatus.IN_PROGRESS,
        "started_at": datetime.now(timezone.utc),
        "answers": [
            {
                "question_id": "q1",
                "selected_answer": "Python",
            }
        ],
        "snapshot": {
            "duration": 30,
            "questions": [
                {
                    "question_id": "q1",
                    "correct_answer": "Python",
                    "marks": 5,
                }
            ],
            "total_marks": 5,
            "passing_marks": 2,
        },
    }

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_attempt_by_id",
        new=AsyncMock(return_value=mock_attempt),
    )

    mocker.patch(
        "app.services.quiz_attempt_service.calculate_score",
        return_value=(5, True),
    )

    mock_update = mocker.patch(
        "app.services.quiz_attempt_service.Repository.update_attempt",
        new=AsyncMock(),
    )

    response = await QuizAttemptService.submit_attempt(
        attempt_id,
        {
            "user_id": student_id,
        },
    )

    assert response.message == QuizAttemptMessage.SUBMITTED
    mock_update.assert_awaited_once()


@pytest.mark.asyncio
async def test_submit_attempt_already_submitted(mocker):
    """
    Test submit already submitted attempt.
    """

    attempt_id = str(ObjectId())
    student_id = str(ObjectId())

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_attempt_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(attempt_id),
                "student_id": student_id,
                "status": QuizAttemptStatus.SUBMITTED,
            }
        ),
    )

    with pytest.raises(BadRequestException):

        await QuizAttemptService.submit_attempt(
            attempt_id,
            {
                "user_id": student_id,
            },
        )


@pytest.mark.asyncio
async def test_get_student_attempts_success(mocker):
    """
    Test get student attempts.
    """

    quiz_id = str(ObjectId())
    student_id = str(ObjectId())

    mocker.patch(
    "app.services.quiz_attempt_service.Repository.get_quiz_by_id",
    new=AsyncMock(
        return_value={
            "_id": ObjectId(quiz_id),
            "title": "Python Quiz",
        }
    ),
)
    

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_student_attempts",
        new=AsyncMock(
            return_value=[
                {
                    "_id": ObjectId(),
                    "quiz_id": quiz_id,
                    "attempt_number": 1,
                    "status": QuizAttemptStatus.SUBMITTED,
                    "started_at": datetime.now(timezone.utc),
                    "submitted_at": datetime.now(timezone.utc),
                },
                {
                    "_id": ObjectId(),
                    "quiz_id": quiz_id,
                    "attempt_number": 2,
                    "status": QuizAttemptStatus.IN_PROGRESS,
                    "started_at": datetime.now(timezone.utc),
                    "submitted_at": None,
                },
            ]
        ),
    )

    response = await QuizAttemptService.get_student_attempts(
        quiz_id,
        {
            "user_id": student_id,
            "email": "student@test.com",
        },
    )

    assert len(response) == 2
    assert response[0].attempt_number == 1
    assert response[1].attempt_number == 2

@pytest.mark.asyncio
async def test_get_attempt_questions_not_found(mocker):
    """
    Test get attempt questions when attempt does not exist.
    """

    attempt_id = str(ObjectId())

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_attempt_by_id",
        new=AsyncMock(return_value=None),
    )

    with pytest.raises(ResourceNotFoundException) as exc:

        await QuizAttemptService.get_attempt_questions(
            attempt_id,
            {
                "user_id": str(ObjectId()),
            },
        )

    assert str(exc.value) == QuizAttemptMessage.NOT_FOUND


@pytest.mark.asyncio
async def test_save_answer_question_not_found(mocker):
    """
    Test save answer when question does not exist in snapshot.
    """

    attempt_id = str(ObjectId())
    student_id = str(ObjectId())

    mock_attempt = {
        "_id": ObjectId(attempt_id),
        "student_id": student_id,
        "status": QuizAttemptStatus.IN_PROGRESS,
        "started_at": datetime.now(timezone.utc),
        "answers": [],
        "snapshot": {
            "duration": 30,
            "questions": [
                {
                    "question_id": "q1",
                    "question": "Python is?",
                    "options": ["Java", "Python"],
                    "correct_answer": "Python",
                }
            ]
        },
    }

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_attempt_by_id",
        new=AsyncMock(return_value=mock_attempt),
    )

    with pytest.raises(ResourceNotFoundException) as exc:

        await QuizAttemptService.save_answer(
            attempt_id,
            StudentAnswer(
                question_id="invalid_question",
                selected_answer="Python",
            ),
            {
                "user_id": student_id,
            },
        )

    assert str(exc.value) == QuestionMessage.NOT_FOUND


@pytest.mark.asyncio
async def test_submit_attempt_not_found(mocker):
    """
    Test submit attempt when attempt does not exist.
    """

    attempt_id = str(ObjectId())

    mocker.patch(
        "app.services.quiz_attempt_service.Repository.get_attempt_by_id",
        new=AsyncMock(return_value=None),
    )

    with pytest.raises(ResourceNotFoundException) as exc:

        await QuizAttemptService.submit_attempt(
            attempt_id,
            {
                "user_id": str(ObjectId()),
            },
        )

    assert str(exc.value) == QuizAttemptMessage.NOT_FOUND