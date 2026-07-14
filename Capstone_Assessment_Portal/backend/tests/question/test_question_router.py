"""
Test cases for Question Router
"""

from unittest.mock import AsyncMock
from bson import ObjectId

from main import app

from app.security.auth_guard import (
    admin_only
)

from app.utils.constants import (
    QuestionMessage
)


def test_create_question_route(client, mocker):
    """
    Test create question endpoint.
    """

    quiz_id = str(ObjectId())

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "role": "admin",
        "username": "admin"
    }

    mocker.patch(
        "app.routers.question_router.QuestionService.create_question",
        new=AsyncMock(
            return_value={
                "id": str(ObjectId()),
                "quiz_id": quiz_id,
                "question": "What is Python?",
                "question_type": "mcq",
                "options": [
                    "Java",
                    "Python"
                ],
                "correct_answer": "Python",
                "difficulty": "easy",
                "tags": [
                    "python"
                ],
                "marks": 5,
                "created_by": "admin",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        )
    )

    response = client.post(
        f"/questions/quiz/{quiz_id}",
        json={
            "question": "What is Python?",
            "question_type": "mcq",
            "options": [
                "Java",
                "Python"
            ],
            "correct_answer": "Python",
            "difficulty": "easy",
            "tags": [
                "python"
            ],
            "marks": 5
        }
    )

    assert response.status_code == 201
    assert response.json()["question"] == "What is Python?"

    app.dependency_overrides.clear()


def test_get_question_by_id_route(client, mocker):
    """
    Test get question by id endpoint.
    """

    question_id = str(ObjectId())

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "role": "admin"
    }

    mocker.patch(
        "app.routers.question_router.QuestionService.get_question_by_id",
        new=AsyncMock(
            return_value={
                "id": question_id,
                "quiz_id": str(ObjectId()),
                "question": "What is Python?",
                "question_type": "mcq",
                "options": [
                    "Java",
                    "Python"
                ],
                "correct_answer": "Python",
                "difficulty": "easy",
                "tags": [
                    "python"
                ],
                "marks": 5,
                "created_by": "admin",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        )
    )

    response = client.get(
        f"/questions/{question_id}"
    )

    assert response.status_code == 200
    assert response.json()["question"] == "What is Python?"

    app.dependency_overrides.clear()


def test_get_questions_by_quiz_route(client, mocker):
    """
    Test get questions by quiz endpoint.
    """

    quiz_id = str(ObjectId())

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "role": "admin"
    }

    mocker.patch(
        "app.routers.question_router.QuestionService.get_questions_by_quiz",
        new=AsyncMock(
            return_value=[
                {
                    "id": str(ObjectId()),
                    "quiz_id": quiz_id,
                    "question": "What is Python?",
                    "question_type": "mcq",
                    "options": [
                        "Java",
                        "Python"
                    ],
                    "correct_answer": "Python",
                    "difficulty": "easy",
                    "tags": [
                        "python"
                    ],
                    "marks": 5,
                    "created_by": "admin",
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                }
            ]
        )
    )

    response = client.get(
        f"/questions/quiz/{quiz_id}"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1

    app.dependency_overrides.clear()


def test_update_question_route(client, mocker):
    """
    Test update question endpoint.
    """

    question_id = str(ObjectId())

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "role": "admin"
    }

    mocker.patch(
        "app.routers.question_router.QuestionService.update_question",
        new=AsyncMock(
            return_value={
                "message": QuestionMessage.UPDATED
            }
        )
    )

    response = client.put(
        f"/questions/{question_id}",
        json={
            "question": "Updated Question",
            "question_type": "mcq",
            "options": [
                "Java",
                "Python"
            ],
            "correct_answer": "Python",
            "difficulty": "easy",
            "tags": [
                "python"
            ],
            "marks": 5
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == QuestionMessage.UPDATED

    app.dependency_overrides.clear()


def test_delete_question_route(client, mocker):
    """
    Test delete question endpoint.
    """

    question_id = str(ObjectId())

    app.dependency_overrides[admin_only] = lambda: {
        "email": "admin@gmail.com",
        "role": "admin"
    }

    mocker.patch(
        "app.routers.question_router.QuestionService.delete_question",
        new=AsyncMock(
            return_value={
                "message": QuestionMessage.DELETED
            }
        )
    )

    response = client.delete(
        f"/questions/{question_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == QuestionMessage.DELETED

    app.dependency_overrides.clear()