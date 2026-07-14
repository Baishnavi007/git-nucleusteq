"""
Test cases for Category Router
"""

from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from main import app

from app.security.auth_guard import (
    get_current_user,
    admin_only,
)


@pytest.fixture(autouse=True)
def clear_overrides():
    """
    Clear dependency overrides after every test.
    """
    yield
    app.dependency_overrides.clear()


def override_current_user():
    """
    Mock authenticated admin user.
    """
    return {
        "email": "admin@gmail.com",
        "username": "admin01",
        "user_id": "123",
        "role": "admin",
    }


def test_get_all_categories(client, mocker):
    """
    Test get all categories route.
    """

    app.dependency_overrides[get_current_user] = override_current_user

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

    response = client.get(
        "/categories",
        headers={
            "Authorization": "Bearer dummy-token"
        }
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_category_by_id(client, mocker):
    """
    Test get category by id route.
    """

    app.dependency_overrides[get_current_user] = override_current_user

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
        f"/categories/{category_id}",
        headers={
            "Authorization": "Bearer dummy-token"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == category_id


def test_create_category(client, mocker):
    """
    Test create category route.
    """

    app.dependency_overrides[admin_only] = override_current_user

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
        headers={
            "Authorization": "Bearer dummy-token"
        }
    )

    assert response.status_code == 201

    assert response.json() == {
        "message": "Category created successfully."
    }


def test_update_category(client, mocker):
    """
    Test update category route.
    """

    app.dependency_overrides[admin_only] = override_current_user

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
        headers={
            "Authorization": "Bearer dummy-token"
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Category updated successfully."
    }


def test_delete_category(client, mocker):
    """
    Test delete category route.
    """

    app.dependency_overrides[admin_only] = override_current_user

    category_id = str(ObjectId())

    mocker.patch(
        "app.routers.category_router.CategoryService.delete_category",
        new_callable=AsyncMock,
        return_value={
            "message": "Category deleted successfully."
        },
    )

    response = client.delete(
        f"/categories/{category_id}",
        headers={
            "Authorization": "Bearer dummy-token"
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Category deleted successfully."
    }