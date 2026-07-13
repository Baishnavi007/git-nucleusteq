"""
Test cases for Quiz routes
"""

from unittest.mock import AsyncMock
from bson import ObjectId

from main import app

from app.security.auth_guard import (
    get_current_user,
    admin_only
)

from app.utils.constants import (
    QuizMessage
)


def test_create_quiz_route(client, mocker):
    """
    Test create quiz endpoint.
    """

    category_id = str(ObjectId())

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "username": "admin",
        "role": "admin",
    }

    mocker.patch(
        "app.routers.quiz_router.QuizService.create_quiz",
        new=AsyncMock(
            return_value={
                "message": QuizMessage.CREATED
            }
        )
    )

    response = client.post(
        f"/quizzes/category/{category_id}",
        json={
            "title": "Java Quiz",
            "description": "Basic Java Programming Quiz",
            "duration": 30,
            "passing_percentage": 40
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == QuizMessage.CREATED

    app.dependency_overrides.clear()


def test_get_all_quizzes_route(client, mocker):
    """
    Test get all quizzes endpoint.
    """

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "role": "admin"
    }

    mocker.patch(
        "app.routers.quiz_router.QuizService.get_all_quizzes",
        new=AsyncMock(
            return_value=[]
        )
    )

    response = client.get("/quizzes")

    assert response.status_code == 200

    app.dependency_overrides.clear()


def test_get_quizzes_by_category_route(client, mocker):
    """
    Test get quizzes by category endpoint.
    """

    category_id = str(ObjectId())

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "role": "admin"
    }

    mocker.patch(
        "app.routers.quiz_router.QuizService.get_quizzes_by_category",
        new=AsyncMock(
            return_value=[]
        )
    )

    response = client.get(
        f"/quizzes/category/{category_id}"
    )

    assert response.status_code == 200

    app.dependency_overrides.clear()


def test_get_quiz_by_id_route(client, mocker):
    """
    Test get quiz by id endpoint.
    """

    quiz_id = str(ObjectId())

    app.dependency_overrides[get_current_user] = lambda: {
        "email": "student@gmail.com",
        "role": "student"
    }

    mocker.patch(
        "app.routers.quiz_router.QuizService.get_quiz_by_id",
        new=AsyncMock(
            return_value={
                "id": quiz_id,
                "title": "Java Quiz",
                "description": "Basic Java Programming Quiz",
                "category_id": str(ObjectId()),
                "category_name": "Programming",
                "duration": 30,
                "is_published": False,
                "max_attempts": 3,
                "created_by": "admin",
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00",
                "passing_percentage": 40,
                "total_questions": 0,
                "total_marks": 0
            }
        )
    )

    response = client.get(f"/quizzes/{quiz_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Java Quiz"

    app.dependency_overrides.clear()


def test_update_quiz_route(client, mocker):
    """
    Test update quiz endpoint.
    """

    quiz_id = str(ObjectId())

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "role": "admin"
    }

    mocker.patch(
        "app.routers.quiz_router.QuizService.update_quiz",
        new=AsyncMock(
            return_value={
                "message": QuizMessage.UPDATED
            }
        )
    )

    response = client.put(
        f"/quizzes/{quiz_id}",
        json={
            "title": "Updated Quiz",
            "description": "Updated Java Programming Quiz",
            "duration": 45,
            "passing_percentage": 50
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == QuizMessage.UPDATED

    app.dependency_overrides.clear()


def test_publish_quiz_route(client, mocker):
    """
    Test publish quiz endpoint.
    """

    quiz_id = str(ObjectId())

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "role": "admin"
    }

    mocker.patch(
        "app.routers.quiz_router.QuizService.publish_quiz",
        new=AsyncMock(
            return_value={
                "message": QuizMessage.PUBLISHED
            }
        )
    )

    response = client.patch(
        f"/quizzes/{quiz_id}/publish"
    )

    assert response.status_code == 200
    assert response.json()["message"] == QuizMessage.PUBLISHED

    app.dependency_overrides.clear()


def test_unpublish_quiz_route(client, mocker):
    """
    Test unpublish quiz endpoint.
    """

    quiz_id = str(ObjectId())

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "role": "admin"
    }

    mocker.patch(
        "app.routers.quiz_router.QuizService.unpublish_quiz",
        new=AsyncMock(
            return_value={
                "message": QuizMessage.UNPUBLISHED
            }
        )
    )

    response = client.patch(
        f"/quizzes/{quiz_id}/unpublish"
    )

    assert response.status_code == 200
    assert response.json()["message"] == QuizMessage.UNPUBLISHED

    app.dependency_overrides.clear()


def test_delete_quiz_route(client, mocker):
    """
    Test delete quiz endpoint.
    """

    quiz_id = str(ObjectId())

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "role": "admin"
    }

    mocker.patch(
        "app.routers.quiz_router.QuizService.delete_quiz",
        new=AsyncMock(
            return_value={
                "message": QuizMessage.DELETED
            }
        )
    )

    response = client.delete(
        f"/quizzes/{quiz_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == QuizMessage.DELETED

    app.dependency_overrides.clear()