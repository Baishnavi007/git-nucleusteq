"""
Test cases for QuestionService
"""

import pytest

from unittest.mock import (
    AsyncMock,
    patch,
)

from bson import ObjectId

from app.services.question_service import (
    QuestionService,
)

from app.schemas.question_schema import (
    QuestionCreate,
    QuestionUpdate,
)

from app.utils.constants import (
    QuestionMessage,
)

from app.exceptions.bad_request_exception import (
    BadRequestException,
)

from app.exceptions.conflict_exception import (
    ConflictException,
)

from app.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)

@pytest.mark.asyncio
async def test_create_question_success(mocker):
    """
    Test successful question creation.
    """

    quiz_id = str(ObjectId())

    mocker.patch(
        "app.services.question_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(quiz_id)
            }
        ),
    )

    mocker.patch(
        "app.services.question_service.Repository.get_duplicate_question",
        new=AsyncMock(
            return_value=None
        ),
    )

    mocker.patch(
        "app.services.question_service.Repository.create_question",
        new=AsyncMock(),
    )

    mocker.patch(
        "app.services.question_service.QuestionService.update_quiz_statistics",
        new=AsyncMock(),
    )

    question = QuestionCreate(
        question="What is Python?",
        question_type="mcq",
        options=["Java", "Python", "C++"],
        correct_answer="Python",
        difficulty="easy",
        tags=["python"],
        marks=5,
    )

    response = await QuestionService.create_question(
        quiz_id,
        question,
        {
            "username": "admin"
        }
    )

    assert response.message == QuestionMessage.CREATED

@pytest.mark.asyncio
async def test_create_question_quiz_not_found():
    """
    Test create question when quiz does not exist.
    """

    quiz_id = str(ObjectId())

    with patch(
        "app.services.question_service.Repository.get_quiz_by_id",
        new=AsyncMock(return_value=None),
    ):

        question = QuestionCreate(
            question="What is Python?",
            question_type="mcq",
            options=["Java", "Python"],
            correct_answer="Python",
            difficulty="easy",
            tags=["python"],
            marks=5,
        )

        with pytest.raises(ResourceNotFoundException):
            await QuestionService.create_question(
                quiz_id,
                question,
                {
                    "username": "admin"
                }
            )

@pytest.mark.asyncio
async def test_create_question_duplicate(mocker):
    """
    Test duplicate question.
    """

    quiz_id = str(ObjectId())

    mocker.patch(
        "app.services.question_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(quiz_id)
            }
        ),
    )

    mocker.patch(
        "app.services.question_service.Repository.get_duplicate_question",
        new=AsyncMock(
            return_value={
                "_id": ObjectId()
            }
        ),
    )

    question = QuestionCreate(
        question="What is Python?",
        question_type="mcq",
        options=["Java", "Python"],
        correct_answer="Python",
        difficulty="easy",
        tags=["python"],
        marks=5,
    )

    with pytest.raises(ConflictException):
        await QuestionService.create_question(
            quiz_id,
            question,
            {
                "username": "admin"
            }
        )

def test_validate_question_type_invalid():
    """
    Test invalid question type.
    """

    with pytest.raises(BadRequestException):
        QuestionService.validate_question_type(
            "xyz"
        )

@pytest.mark.asyncio
async def test_get_questions_by_quiz_success(mocker):
    """
    Test get questions by quiz.
    """

    quiz_id = str(ObjectId())

    mocker.patch(
        "app.services.question_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(quiz_id)
            }
        ),
    )

    mocker.patch(
        "app.services.question_service.Repository.get_questions_by_quiz",
        new=AsyncMock(
            return_value=[
                {
                    "_id": ObjectId(),
                    "question": "What is Python?",
                    "quiz_id": quiz_id,
                    "question_type": "mcq",
                    "options": ["Java", "Python"],
                    "correct_answer": "Python",
                    "difficulty": "easy",
                    "tags": ["python"],
                    "marks": 5,
                }
            ]
        ),
    )

    response = await QuestionService.get_questions_by_quiz(
        quiz_id
    )

    assert len(response) == 1
    assert response[0]["question"] == "What is Python?"

@pytest.mark.asyncio
async def test_get_questions_by_quiz_not_found(mocker):
    """
    Test get questions when quiz does not exist.
    """

    mocker.patch(
        "app.services.question_service.Repository.get_quiz_by_id",
        new=AsyncMock(return_value=None),
    )

    with pytest.raises(ResourceNotFoundException):
        await QuestionService.get_questions_by_quiz(
            str(ObjectId())
        )   

@pytest.mark.asyncio
async def test_get_question_by_id_success(mocker):
    """
    Test get question by id.
    """

    question_id = ObjectId()

    mocker.patch(
        "app.services.question_service.Repository.get_question_by_id",
        new=AsyncMock(
            return_value={
                "_id": question_id,
                "question": "What is Python?",
                "quiz_id": "quiz123",
                "question_type": "mcq",
                "options": ["Java", "Python"],
                "correct_answer": "Python",
                "difficulty": "easy",
                "tags": ["python"],
                "marks": 5,
            }
        ),
    )

    response = await QuestionService.get_question_by_id(
        str(question_id)
    )

    assert response["question"] == "What is Python?"
    assert response["id"] == str(question_id)

@pytest.mark.asyncio
async def test_get_question_by_id_not_found(mocker):
    """
    Test get question by id when question does not exist.
    """

    mocker.patch(
        "app.services.question_service.Repository.get_question_by_id",
        new=AsyncMock(return_value=None),
    )

    with pytest.raises(ResourceNotFoundException):
        await QuestionService.get_question_by_id(
            str(ObjectId())
        )
@pytest.mark.asyncio
async def test_update_question_success(mocker):
    """
    Test successful question update.
    """

    question_id = str(ObjectId())

    mocker.patch(
        "app.services.question_service.Repository.get_question_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(question_id),
                "quiz_id": "quiz123",
                "question": "Old Question",
            }
        ),
    )

    mocker.patch(
        "app.services.question_service.Repository.get_duplicate_question_for_update",
        new=AsyncMock(return_value=None),
    )

    mocker.patch(
        "app.services.question_service.Repository.update_question",
        new=AsyncMock(),
    )

    mocker.patch(
        "app.services.question_service.QuestionService.update_quiz_statistics",
        new=AsyncMock(),
    )

    question = QuestionUpdate(
        question="Updated Question",
        question_type="mcq",
        options=["Java", "Python"],
        correct_answer="Python",
        difficulty="easy",
        tags=["python"],
        marks=5,
    )

    response = await QuestionService.update_question(
        question_id,
        question,
    )

    assert response.message == QuestionMessage.UPDATED

@pytest.mark.asyncio
async def test_update_question_not_found(mocker):
    """
    Test update question when question not found.
    """

    mocker.patch(
        "app.services.question_service.Repository.get_question_by_id",
        new=AsyncMock(return_value=None),
    )

    question = QuestionUpdate(
        question="Updated Question",
        question_type="mcq",
        options=["A", "B"],
        correct_answer="A",
        difficulty="easy",
        tags=["python"],
        marks=5,
    )

    with pytest.raises(ResourceNotFoundException):
        await QuestionService.update_question(
            str(ObjectId()),
            question,
        )

@pytest.mark.asyncio
async def test_delete_question_success(mocker):
    """
    Test successful question deletion.
    """

    mocker.patch(
        "app.services.question_service.Repository.get_question_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(),
                "quiz_id": "quiz123",
            }
        ),
    )

    mock_delete = mocker.patch(
        "app.services.question_service.Repository.delete_question",
        new=AsyncMock(),
    )

    mocker.patch(
        "app.services.question_service.QuestionService.update_quiz_statistics",
        new=AsyncMock(),
    )

    response = await QuestionService.delete_question(
        str(ObjectId())
    )

    assert response.message == QuestionMessage.DELETED

    mock_delete.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_question_not_found(mocker):
    """
    Test delete question when question does not exist.
    """

    mocker.patch(
        "app.services.question_service.Repository.get_question_by_id",
        new=AsyncMock(return_value=None),
    )

    with pytest.raises(ResourceNotFoundException):
        await QuestionService.delete_question(
            str(ObjectId())
        )

def test_validate_difficulty_invalid():
    """
    Test invalid difficulty.
    """

    with pytest.raises(BadRequestException):
        QuestionService.validate_difficulty(
            "very_hard"
        )
