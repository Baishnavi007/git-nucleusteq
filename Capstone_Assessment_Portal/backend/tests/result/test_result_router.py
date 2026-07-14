"""
Test cases for Result routes
"""

from datetime import datetime, UTC
from unittest.mock import AsyncMock

from bson import ObjectId

from main import app

from app.security.auth_guard import (
    get_current_user,
    admin_only
)


def student_result():

    return {

        "attempt_id": str(ObjectId()),

        "quiz_id": str(ObjectId()),

        "student_id": str(ObjectId()),

        "student_name": "Baishnavi Singh",

        "student_email": "student@test.com",

        "quiz_title": "Python Quiz",

        "attempt_number": 1,

        "score": 8,

        "total_marks": 10,

        "percentage": 80,

        "passing_percentage": 50,

        "passing_marks": 5,

        "is_pass": True,

        "started_at": datetime.now(UTC),

        "submitted_at": datetime.now(UTC),

        "questions": []

    }


def history_result():

    return {

        "attempt_id": str(ObjectId()),

        "student_id": str(ObjectId()),

        "student_name": "Baishnavi Singh",

        "student_email": "student@test.com",

        "quiz_id": str(ObjectId()),

        "quiz_title": "Python Quiz",

        "attempt_number": 1,

        "score": 8,

        "total_marks": 10,

        "percentage": 80,

        "is_pass": True,

        "submitted_at": datetime.now(UTC)

    }


def test_get_student_results_route(
    client,
    mocker
):
    """
    Test student result history endpoint.
    """

    app.dependency_overrides[get_current_user] = lambda: {

        "email": "student@test.com",

        "user_id": str(ObjectId())

    }

    mocker.patch(

        "app.routers.result_router.ResultService.get_student_results",

        new=AsyncMock(

            return_value=[

                history_result()

            ]

        )

    )

    response = client.get(

        "/results/history"

    )

    assert response.status_code == 200

    assert len(

        response.json()

    ) == 1

    assert response.json()[0][

        "quiz_title"

    ] == "Python Quiz"

    app.dependency_overrides.clear()


def test_get_all_results_route(
    client,
    mocker
):
    """
    Test admin result history endpoint.
    """

    app.dependency_overrides[admin_only] = lambda: {

        "email": "admin@test.com",

        "user_id": str(ObjectId())

    }

    mocker.patch(

        "app.routers.result_router.ResultService.get_all_results",

        new=AsyncMock(

            return_value=[

                history_result()

            ]

        )

    )

    response = client.get(

        "/results/admin"

    )

    assert response.status_code == 200

    assert len(

        response.json()

    ) == 1

    assert response.json()[0][

        "score"

    ] == 8

    app.dependency_overrides.clear()


def test_get_result_route(
    client,
    mocker
):
    """
    Test student result endpoint.
    """

    attempt_id = str(

        ObjectId()

    )

    result = student_result()

    result["attempt_id"] = attempt_id

    app.dependency_overrides[get_current_user] = lambda: {

        "email": "student@test.com",

        "user_id": str(ObjectId())

    }

    mocker.patch(

        "app.routers.result_router.ResultService.get_result",

        new=AsyncMock(

            return_value=result

        )

    )

    response = client.get(

        f"/results/{attempt_id}"

    )

    assert response.status_code == 200

    assert response.json()[

        "attempt_id"

    ] == attempt_id

    assert response.json()[

        "score"

    ] == 8

    app.dependency_overrides.clear()


def test_get_result_admin_route(
    client,
    mocker
):
    """
    Test admin result endpoint.
    """

    attempt_id = str(

        ObjectId()

    )

    result = student_result()

    result["attempt_id"] = attempt_id

    app.dependency_overrides[admin_only] = lambda: {

        "email": "admin@test.com",

        "user_id": str(ObjectId())

    }

    mocker.patch(

        "app.routers.result_router.ResultService.get_result_admin",

        new=AsyncMock(

            return_value=result

        )

    )

    response = client.get(

        f"/results/admin/{attempt_id}"

    )

    assert response.status_code == 200

    assert response.json()[

        "quiz_title"

    ] == "Python Quiz"

    assert response.json()[

        "score"

    ] == 8

    app.dependency_overrides.clear()