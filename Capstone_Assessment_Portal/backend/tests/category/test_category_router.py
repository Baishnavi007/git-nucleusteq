"""
Test cases for Category Router
"""

from unittest.mock import AsyncMock
from bson import ObjectId

from fastapi.testclient import TestClient

from main import app

from app.security.auth_guard import (
    get_current_user,
    admin_only,
)

client = TestClient(app)


def override_current_user():
    return {
        "email": "admin@gmail.com",
        "username": "admin01",
        "user_id": "123",
        "role": "admin",
    }


app.dependency_overrides[get_current_user] = override_current_user
app.dependency_overrides[admin_only] = override_current_user


def test_get_all_categories(mocker):
    """
    Test get all categories route.
    """

    mocker.patch(
        "app.routers.category_router.CategoryService.get_all_categories",
        new_callable=AsyncMock,
        return_value=[
            {
                "id": str(ObjectId()),
                "name": "Programming",
                "description": "Programming quizzes",
            }
        ],
    )

    response = client.get("/categories")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_category_by_id(mocker):
    """
    Test get category by id route.
    """

    category_id = str(ObjectId())

    mocker.patch(
        "app.routers.category_router.CategoryService.get_category_by_id",
        new_callable=AsyncMock,
        return_value={
            "id": category_id,
            "name": "Programming",
            "description": "Programming quizzes",
        },
    )

    response = client.get(
        f"/categories/{category_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == category_id


def test_create_category(mocker):
    """
    Test create category route.
    """

    mocker.patch(
        "app.routers.category_router.CategoryService.create_category",
        new_callable=AsyncMock,
        return_value={
            "message": "Category created successfully."
        },
    )

    response = client.post(
        "/categories",
        json={
            "name": "Programming",
            "description": "Programming quizzes",
        },
    )

    assert response.status_code == 201

    assert response.json() == {
        "message": "Category created successfully."
    }


def test_update_category(mocker):
    """
    Test update category route.
    """

    category_id = str(ObjectId())

    mocker.patch(
        "app.routers.category_router.CategoryService.update_category",
        new_callable=AsyncMock,
        return_value={
            "message": "Category updated successfully."
        },
    )

    response = client.put(
        f"/categories/{category_id}",
        json={
            "name": "Java",
            "description": "Java quizzes",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Category updated successfully."
    }


def test_delete_category(mocker):
    """
    Test delete category route.
    """

    category_id = str(ObjectId())

    mocker.patch(
        "app.routers.category_router.CategoryService.delete_category",
        new_callable=AsyncMock,
        return_value={
            "message": "Category deleted successfully."
        },
    )

    response = client.delete(
        f"/categories/{category_id}"
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Category deleted successfully."
    }


def teardown_module():
    """
    Clear dependency overrides after tests.
    """

    app.dependency_overrides.clear()