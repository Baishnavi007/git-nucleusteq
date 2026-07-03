"""
Test cases for QuizService
"""

import pytest

from unittest.mock import (
    AsyncMock,
)

from bson import ObjectId

from app.services.quiz_service import QuizService

from app.schemas.quiz_schema import (
    QuizCreate,
    QuizUpdate,
)

from app.exceptions.conflict_exception import (
    ConflictException,
)

from app.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)


@pytest.mark.asyncio
async def test_create_quiz_success(mocker):
    """
    Test successful quiz creation.
    """

    category_id = str(
        ObjectId()
    )

    current_user = {
        "username": "admin"
    }

    mocker.patch(
        "app.services.quiz_service.Repository.get_category_by_id",
        new_callable=AsyncMock,
        return_value={
            "_id": ObjectId(category_id),
            "name": "Programming",
        },
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_title",
        new_callable=AsyncMock,
        return_value=None,
    )

    mock_create = mocker.patch(
        "app.services.quiz_service.Repository.create_quiz",
        new_callable=AsyncMock,
    )

    quiz = QuizCreate(
        title="Java Basics",
        description="Quiz covering Java fundamentals.",
        duration=30,
    )

    response = await QuizService.create_quiz(
        category_id,
        quiz,
        current_user,
    )

    assert response["message"] == "Quiz created successfully."

    mock_create.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_quiz_duplicate(mocker):
    """
    Test duplicate quiz creation.
    """

    category_id = str(
        ObjectId()
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_category_by_id",
        new_callable=AsyncMock,
        return_value={
            "_id": ObjectId(category_id),
        },
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_title",
        new_callable=AsyncMock,
        return_value={
            "title": "Java Basics",
        },
    )

    quiz = QuizCreate(
        title="Java Basics",
        description="Quiz covering Java fundamentals.",
        duration=30,
    )

    with pytest.raises(
        ConflictException
    ):
        await QuizService.create_quiz(
            category_id,
            quiz,
            {
                "username": "admin",
            },
        )


@pytest.mark.asyncio
async def test_get_quizzes_by_category(mocker):
    """
    Test get quizzes by category.
    """

    category_id = str(
        ObjectId()
    )

    object_id = ObjectId(
        category_id
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_category_by_id",
        new_callable=AsyncMock,
        return_value={
            "_id": object_id,
            "name": "Programming",
        },
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_quizzes_by_category",
        new_callable=AsyncMock,
        return_value=[
            {
                "_id": ObjectId(),
                "title": "Java Basics",
                "description": "Quiz",
                "category_id": object_id,
                "duration": 30,
                "created_by": "admin",
            }
        ],
    )

    response = await QuizService.get_quizzes_by_category(
        category_id
    )

    assert len(response) == 1

    assert response[0]["category_name"] == "Programming"


@pytest.mark.asyncio
async def test_get_quiz_by_id_success(mocker):
    """
    Test get quiz by id.
    """

    quiz_id = str(
        ObjectId()
    )

    category_id = ObjectId()

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new_callable=AsyncMock,
        return_value={
            "_id": ObjectId(quiz_id),
            "title": "Java Basics",
            "description": "Quiz",
            "category_id": category_id,
            "duration": 30,
            "created_by": "admin",
        },
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_category_by_id",
        new_callable=AsyncMock,
        return_value={
            "_id": category_id,
            "name": "Programming",
        },
    )

    response = await QuizService.get_quiz_by_id(
        quiz_id
    )

    assert response["title"] == "Java Basics"

    assert response["category_name"] == "Programming"


@pytest.mark.asyncio
async def test_update_quiz_success(mocker):
    """
    Test successful quiz update.
    """

    quiz_id = str(
        ObjectId()
    )

    category_id = ObjectId()

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new_callable=AsyncMock,
        return_value={
            "_id": ObjectId(quiz_id),
            "category_id": category_id,
        },
    )

    mocker.patch(
        "app.services.quiz_service.Repository.get_duplicate_quiz",
        new_callable=AsyncMock,
        return_value=None,
    )

    mock_update = mocker.patch(
        "app.services.quiz_service.Repository.update_quiz",
        new_callable=AsyncMock,
    )

    quiz = QuizUpdate(
        title="Advanced Java",
        description="Advanced Java quiz.",
        duration=45,
    )

    response = await QuizService.update_quiz(
        quiz_id,
        quiz,
    )

    assert response["message"] == "Quiz updated successfully."

    mock_update.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_quiz_not_found(mocker):
    """
    Test update quiz when quiz does not exist.
    """

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new_callable=AsyncMock,
        return_value=None,
    )

    quiz = QuizUpdate(
        title="Advanced Java",
        description="Advanced Java quiz.",
        duration=45,
    )

    with pytest.raises(
        ResourceNotFoundException
    ):
        await QuizService.update_quiz(
            str(ObjectId()),
            quiz,
        )


@pytest.mark.asyncio
async def test_delete_quiz_success(mocker):
    """
    Test successful quiz deletion.
    """

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new_callable=AsyncMock,
        return_value={
            "_id": ObjectId(),
            "title": "Java Basics",
        },
    )

    mock_delete = mocker.patch(
        "app.services.quiz_service.Repository.delete_quiz",
        new_callable=AsyncMock,
    )

    response = await QuizService.delete_quiz(
        str(ObjectId())
    )

    assert response["message"] == "Quiz deleted successfully."

    mock_delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_quiz_not_found(mocker):
    """
    Test delete quiz when quiz does not exist.
    """

    mocker.patch(
        "app.services.quiz_service.Repository.get_quiz_by_id",
        new_callable=AsyncMock,
        return_value=None,
    )

    with pytest.raises(
        ResourceNotFoundException
    ):
        await QuizService.delete_quiz(
            str(ObjectId())
        )