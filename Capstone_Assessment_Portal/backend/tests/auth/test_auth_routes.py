"""
Test cases for Authentication Routes
"""

from unittest.mock import AsyncMock

import pytest

from main import app

from app.security.auth_guard import (
    get_current_user,
    admin_only,
    student_only
)


@pytest.fixture(autouse=True)
def clear_overrides():
    """
    Clear dependency overrides after every test.
    """
    yield
    app.dependency_overrides.clear()


def test_register_success(client, mocker):
    """
    Test register endpoint.
    """

    mocker.patch(
        "app.routers.auth_router.AuthService.register",
        new=AsyncMock(
            return_value={
                "message": (
                    "User registered successfully. "
                    "Please login to continue."
                )
            }
        )
    )

    response = client.post(
        "/auth/register",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "john@gmail.com",
            "password": "encrypted"
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == (
        "User registered successfully. Please login to continue."
    )


def test_login_success(client, mocker):
    """
    Test login endpoint.
    """

    mocker.patch(
        "app.routers.auth_router.AuthService.login",
        new=AsyncMock(
            return_value={
                "access_token": "abc",
                "refresh_token": "xyz",
                "role": "student",
                "token_type": "bearer",
                "username": "john"
            }
        )
    )

    response = client.post(
        "/auth/login",
        json={
            "email_or_username": "john@gmail.com",
            "password": "encrypted"
        }
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "abc"


def test_get_public_key(client, mocker):
    """
    Test public key endpoint.
    """

    mocker.patch(
        "app.routers.auth_router.AuthService.get_public_key",
        new=AsyncMock(
            return_value={
                "publicKey": "PUBLIC_KEY"
            }
        )
    )

    response = client.get("/auth/public-key")

    assert response.status_code == 200
    assert response.json()["publicKey"] == "PUBLIC_KEY"


def test_refresh_token(client, mocker):
    """
    Test refresh token endpoint.
    """

    mocker.patch(
        "app.routers.auth_router.AuthService.regenerate_refresh_token",
        new=AsyncMock(
            return_value={
                "access_token": "new_access",
                "token_type": "bearer"
            }
        )
    )

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": "dummy"
        }
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "new_access"


def test_get_current_user(client):
    """
    Test current user endpoint.
    """

    app.dependency_overrides[get_current_user] = lambda: {
        "user_id": "123",
        "username": "john",
        "email": "john@gmail.com",
        "role": "student"
    }

    response = client.get(
        "/auth/current-user",
        headers={
            "Authorization": "Bearer dummy-token"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == "john"


def test_admin_dashboard(client):
    """
    Test admin dashboard endpoint.
    """

    app.dependency_overrides[admin_only] = lambda: {
        "user_id": "1",
        "username": "admin",
        "email": "admin@gmail.com",
        "role": "admin"
    }

    response = client.get(
        "/auth/admin/dashboard",
        headers={
            "Authorization": "Bearer dummy-token"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome Admin"


def test_student_dashboard(client):
    """
    Test student dashboard endpoint.
    """

    app.dependency_overrides[student_only] = lambda: {
        "user_id": "1",
        "username": "john",
        "email": "john@gmail.com",
        "role": "student"
    }

    response = client.get(
        "/auth/student/dashboard",
        headers={
            "Authorization": "Bearer dummy-token"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome Student"