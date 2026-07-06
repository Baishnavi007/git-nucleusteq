"""
Test cases for Quiz routes
"""

from datetime import datetime, timezone

from bson import ObjectId

from main import app

from app.security.auth_guard import (
    get_current_user,
    admin_only,
)

from app.services.quiz_service import (
    QuizService
)


def test_create_quiz(client, mocker):
    """
    Test create quiz.
    """

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "username": "admin",
        "role": "admin",
    }

    category_id = str(ObjectId())

    mocker.patch.object(
        QuizService,
        "create_quiz",
        return_value={
            "message": "Quiz created successfully."
        },
    )

    response = client.post(
        f"/quizzes/category/{category_id}",
        json={
            "title": "Java Basics",
            "description": "Quiz covering Java fundamentals.",
            "duration": 30,
        },
    )

    assert response.status_code == 201

    app.dependency_overrides.clear()


def test_get_quizzes_by_category(client, mocker):
    """
    Test get quizzes by category.
    """

    app.dependency_overrides[get_current_user] = lambda: {
        "email": "student@gmail.com",
        "role": "student",
    }

    category_id = str(ObjectId())

    mocker.patch.object(
        QuizService,
        "get_quizzes_by_category",
        return_value=[
            {
                "id": str(ObjectId()),
                "title": "Java Basics",
                "description": "Quiz covering Java fundamentals.",
                "category_id": category_id,
                "category_name": "Programming",
                "duration": 30,
                "created_by": "admin",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            }
        ],
    )

    response = client.get(
        f"/quizzes/category/{category_id}"
    )

    assert response.status_code == 200

    app.dependency_overrides.clear()


def test_get_quiz_by_id(client, mocker):
    """
    Test get quiz by id.
    """

    app.dependency_overrides[get_current_user] = lambda: {
        "email": "student@gmail.com",
        "role": "student",
    }

    quiz_id = str(ObjectId())

    mocker.patch.object(
        QuizService,
        "get_quiz_by_id",
        return_value={
            "id": quiz_id,
            "title": "Java Basics",
            "description": "Quiz covering Java fundamentals.",
            "category_id": str(ObjectId()),
            "category_name": "Programming",
            "duration": 30,
            "created_by": "admin",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
    )

    response = client.get(
        f"/quizzes/{quiz_id}"
    )

    assert response.status_code == 200

    app.dependency_overrides.clear()


def test_update_quiz(client, mocker):
    """
    Test update quiz.
    """

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "username": "admin",
        "role": "admin",
    }

    quiz_id = str(ObjectId())

    mocker.patch.object(
        QuizService,
        "update_quiz",
        return_value={
            "message": "Quiz updated successfully."
        },
    )

    response = client.put(
        f"/quizzes/{quiz_id}",
        json={
            "title": "Advanced Java",
            "description": "Advanced Java quiz.",
            "duration": 45,
        },
    )

    assert response.status_code == 200

    app.dependency_overrides.clear()


def test_delete_quiz(client, mocker):
    """
    Test delete quiz.
    """

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "username": "admin",
        "role": "admin",
    }

    quiz_id = str(ObjectId())

    mocker.patch.object(
        QuizService,
        "delete_quiz",
        return_value={
            "message": "Quiz deleted successfully."
        },
    )

    response = client.delete(
        f"/quizzes/{quiz_id}"
    )

    assert response.status_code == 200

    app.dependency_overrides.clear()