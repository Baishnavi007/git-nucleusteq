"""
Test cases for QuizService
"""

import pytest
from unittest.mock import AsyncMock
from bson import ObjectId

from app.services.quiz_service import QuizService
from app.schemas.quiz_schema import QuizCreate
from app.exceptions.conflict_exception import (
    ConflictException
)
from app.exceptions.resource_not_found_exception import (
    ResourceNotFoundException
)
from app.exceptions.bad_request_exception import (
    BadRequestException
)

from app.schemas.quiz_schema import QuizUpdate


@pytest.mark.asyncio
async def test_create_quiz_success(mocker):
    """
    Test create quiz successfully.
    """

    category_id = str(ObjectId())

    quiz = QuizCreate(
        title="Java Quiz",
        description="Basic Java Programming Quiz",
        duration=30,
        passing_percentage=40
    )

    current_user = {
        "username": "admin"
    }

    mocker.patch(
        "app.services.quiz_service.Repository.get_category_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(),
                "name": "Programming"
            }
        )
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_title",
        new=AsyncMock(return_value=None)
    )

    create_quiz = mocker.patch(
        "app.services.quiz_service.Repository.create_quiz",
        new=AsyncMock()
    )

    response = await QuizService.create_quiz(
        category_id,
        quiz,
        current_user
    )

    assert response.message == "Quiz created successfully."

    create_quiz.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_quiz_duplicate(mocker):
    """
    Test duplicate quiz.
    """

    category_id = str(ObjectId())

    quiz = QuizCreate(
        title="Java Quiz",
        description="Basic Java Programming Quiz",
        duration=30,
        passing_percentage=40
    )

    current_user = {
        "username": "admin"
    }

    mocker.patch(
        "app.services.quiz_service.Repository.get_category_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId()
            }
        )
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_title",
        new=AsyncMock(
            return_value={
                "_id": ObjectId()
            }
        )
    )

    with pytest.raises(
        ConflictException
    ):
        await QuizService.create_quiz(
            category_id,
            quiz,
            current_user
        )


@pytest.mark.asyncio
async def test_create_quiz_category_not_found(mocker):
    """
    Test category not found.
    """

    category_id = str(ObjectId())

    quiz = QuizCreate(
        title="Java Quiz",
        description="Basic Java Programming Quiz",
        duration=30,
        passing_percentage=40
    )

    current_user = {
        "username": "admin"
    }

    mocker.patch(
        "app.services.quiz_service.Repository.get_category_by_id",
        new=AsyncMock(
            return_value=None
        )
    )

    with pytest.raises(
        ResourceNotFoundException
    ):
        await QuizService.create_quiz(
            category_id,
            quiz,
            current_user
        )


@pytest.mark.asyncio
async def test_get_all_quizzes(mocker):
    """
    Test get all quizzes.
    """

    quiz_id = ObjectId()

    mocker.patch(
        "app.services.quiz_service.Repository.get_all_quizzes",
        new=AsyncMock(
            return_value=[
                {
                    "_id": quiz_id,
                    "title": "Java Quiz",
                    "category_id": str(ObjectId())
                }
            ]
        )
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_category_by_id",
        new=AsyncMock(
            return_value={
                "name": "Programming"
            }
        )
    )

    response = await QuizService.get_all_quizzes()

    assert len(response) == 1
    assert response[0]["title"] == "Java Quiz"
    assert response[0]["category_name"] == "Programming"



@pytest.mark.asyncio
async def test_get_quiz_by_id(mocker):
    """
    Test get quiz by id.
    """

    quiz_id = ObjectId()

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": quiz_id,
                "title": "Java Quiz",
                "category_id": str(ObjectId())
            }
        )
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_category_by_id",
        new=AsyncMock(
            return_value={
                "name": "Programming"
            }
        )
    )

    response = await QuizService.get_quiz_by_id(
        str(quiz_id)
    )

    assert response["title"] == "Java Quiz"
    assert response["category_name"] == "Programming"


@pytest.mark.asyncio
async def test_get_quiz_by_id_not_found(mocker):
    """
    Test quiz not found.
    """

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new=AsyncMock(return_value=None)
    )

    with pytest.raises(
        ResourceNotFoundException
    ):
        await QuizService.get_quiz_by_id(
            str(ObjectId())
        )


@pytest.mark.asyncio
async def test_update_quiz_success(mocker):
    """
    Test update quiz successfully.
    """

    quiz_id = ObjectId()

    quiz = QuizUpdate(
        title="Advanced Java",
        description="Advanced Java Programming Quiz",
        duration=45,
        passing_percentage=50
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": quiz_id,
                "category_id": str(ObjectId())
            }
        )
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_duplicate_quiz",
        new=AsyncMock(return_value=None)
    )

    update_quiz = mocker.patch(
        "app.services.quiz_service.Repository.update_quiz",
        new=AsyncMock()
    )

    response = await QuizService.update_quiz(
        str(quiz_id),
        quiz
    )

    assert response.message == "Quiz updated successfully."

    update_quiz.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_quiz_not_found(mocker):
    """
    Test update quiz not found.
    """

    quiz = QuizUpdate(
        title="Advanced Java",
        description="Advanced Java Programming Quiz",
        duration=45,
        passing_percentage=50
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new=AsyncMock(return_value=None)
    )

    with pytest.raises(
        ResourceNotFoundException
    ):
        await QuizService.update_quiz(
            str(ObjectId()),
            quiz
        )


@pytest.mark.asyncio
async def test_update_quiz_duplicate(mocker):
    """
    Test duplicate quiz while updating.
    """

    quiz_id = ObjectId()

    quiz = QuizUpdate(
        title="Advanced Java",
        description="Advanced Java Programming Quiz",
        duration=45,
        passing_percentage=50
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": quiz_id,
                "category_id": str(ObjectId())
            }
        )
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_duplicate_quiz",
        new=AsyncMock(
            return_value={
                "_id": ObjectId()
            }
        )
    )

    with pytest.raises(
        ConflictException
    ):
        await QuizService.update_quiz(
            str(quiz_id),
            quiz
        )


@pytest.mark.asyncio
async def test_publish_quiz_success(mocker):
    """
    Test publish quiz successfully.
    """

    quiz_id = ObjectId()

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": quiz_id,
                "title": "Java Quiz",
                "total_questions": 5,
                "is_published": False
            }
        )
    )

    update_quiz = mocker.patch(
        "app.services.quiz_service.Repository.update_quiz",
        new=AsyncMock()
    )

    response = await QuizService.publish_quiz(
        str(quiz_id)
    )

    assert response.message == "Quiz published successfully."

    update_quiz.assert_awaited_once()


@pytest.mark.asyncio
async def test_publish_quiz_not_found(mocker):
    """
    Test publish quiz not found.
    """

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new=AsyncMock(return_value=None)
    )

    with pytest.raises(
        ResourceNotFoundException
    ):
        await QuizService.publish_quiz(
            str(ObjectId())
        )


@pytest.mark.asyncio
async def test_publish_quiz_without_questions(mocker):
    """
    Test publish quiz without questions.
    """

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(),
                "title": "Java Quiz",
                "total_questions": 0,
                "is_published": False
            }
        )
    )

    with pytest.raises(
        BadRequestException
    ):
        await QuizService.publish_quiz(
            str(ObjectId())
        )


@pytest.mark.asyncio
async def test_publish_quiz_already_published(mocker):
    """
    Test already published quiz.
    """

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(),
                "title": "Java Quiz",
                "total_questions": 5,
                "is_published": True
            }
        )
    )

    with pytest.raises(
        ConflictException
    ):
        await QuizService.publish_quiz(
            str(ObjectId())
        )


@pytest.mark.asyncio
async def test_unpublish_quiz_success(mocker):
    """
    Test unpublish quiz successfully.
    """

    quiz_id = ObjectId()

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": quiz_id,
                "title": "Java Quiz",
                "is_published": True
            }
        )
    )

    update_quiz = mocker.patch(
        "app.services.quiz_service.Repository.update_quiz",
        new=AsyncMock()
    )

    response = await QuizService.unpublish_quiz(
        str(quiz_id)
    )

    assert response.message == "Quiz unpublished successfully."

    update_quiz.assert_awaited_once()


@pytest.mark.asyncio
async def test_unpublish_quiz_not_found(mocker):
    """
    Test unpublish quiz not found.
    """

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new=AsyncMock(return_value=None)
    )

    with pytest.raises(
        ResourceNotFoundException
    ):
        await QuizService.unpublish_quiz(
            str(ObjectId())
        )


@pytest.mark.asyncio
async def test_unpublish_quiz_already_unpublished(mocker):
    """
    Test already unpublished quiz.
    """

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "_id": ObjectId(),
                "title": "Java Quiz",
                "is_published": False
            }
        )
    )

    with pytest.raises(
        ConflictException
    ):
        await QuizService.unpublish_quiz(
            str(ObjectId())
        )