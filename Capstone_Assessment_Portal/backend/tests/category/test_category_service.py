"""
Test cases for CategoryService
"""

import pytest
from bson import ObjectId
from unittest.mock import AsyncMock

from app.services.category_service import CategoryService

from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate

)

from app.exceptions.conflict_exception import (
    ConflictException
)

from app.exceptions.resource_not_found_exception import (
    ResourceNotFoundException
)


# ============================================================
# CREATE CATEGORY
# ============================================================

@pytest.mark.asyncio
async def test_create_category_success(mocker):
    """
    Test successful category creation.
    """

    mocker.patch(
        "app.services.category_service.Repository.get_category_by_name",
        new_callable=AsyncMock,
        return_value=None
    )

    mock_create = mocker.patch(
        "app.services.category_service.Repository.create_category",
        new_callable=AsyncMock
    )

    category = CategoryCreate(
        name="Programming",
        description="Programming quizzes"
    )

    current_user = {
        "username": "admin01"
    }

    response = await CategoryService.create_category(
        category,
        current_user
    )

    assert response.message == "Category created successfully."

    mock_create.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_category_duplicate(mocker):
    """
    Test duplicate category.
    """

    mocker.patch(
        "app.services.category_service.Repository.get_category_by_name",
        new_callable=AsyncMock,
        return_value={
            "_id": ObjectId(),
            "name": "Programming"
        }
    )

    category = CategoryCreate(
        name="Programming",
        description="Programming quizzes"
    )

    current_user = {
        "username": "admin01"
    }

    with pytest.raises(
        ConflictException
    ):
        await CategoryService.create_category(
            category,
            current_user
        )


# ============================================================
# GET ALL CATEGORIES
# ============================================================

@pytest.mark.asyncio
async def test_get_all_categories(mocker):
    """
    Test fetching all categories.
    """

    mocker.patch(
        "app.services.category_service.Repository.get_all_categories",
        new_callable=AsyncMock,
        return_value=[
            {
                "_id": ObjectId(),
                "name": "Programming",
                "description": "Programming quizzes"
            },
            {
                "_id": ObjectId(),
                "name": "Java",
                "description": "Java quizzes"
            }
        ]
    )

    response = await CategoryService.get_all_categories()

    assert len(response) == 2

    assert "id" in response[0]

    assert "_id" not in response[0]


@pytest.mark.asyncio
async def test_get_all_categories_empty(mocker):
    """
    Test fetching empty category list.
    """

    mocker.patch(
        "app.services.category_service.Repository.get_all_categories",
        new_callable=AsyncMock,
        return_value=[]
    )

    response = await CategoryService.get_all_categories()

    assert response == []


# ============================================================
# GET CATEGORY BY ID
# ============================================================

@pytest.mark.asyncio
async def test_get_category_by_id_success(mocker):
    """
    Test fetching category by id.
    """

    category_id = str(
        ObjectId()
    )

    mocker.patch(
        "app.services.category_service.validate_object_id",
        return_value=ObjectId(category_id)
    )

    mocker.patch(
        "app.services.category_service.Repository.get_category_by_id",
        new_callable=AsyncMock,
        return_value={
            "_id": ObjectId(category_id),
            "name": "Programming",
            "description": "Programming quizzes"
        }
    )

    response = await CategoryService.get_category_by_id(
        category_id
    )

    assert response["name"] == "Programming"

    assert "id" in response


@pytest.mark.asyncio
async def test_get_category_by_id_not_found(mocker):
    """
    Test category not found.
    """

    category_id = str(
        ObjectId()
    )

    mocker.patch(
        "app.services.category_service.validate_object_id",
        return_value=ObjectId(category_id)
    )

    mocker.patch(
        "app.services.category_service.Repository.get_category_by_id",
        new_callable=AsyncMock,
        return_value=None
    )

    with pytest.raises(
        ResourceNotFoundException
    ):
        await CategoryService.get_category_by_id(
            category_id
        )


@pytest.mark.asyncio
async def test_get_category_by_id_invalid_objectid(mocker):
    """
    Test invalid object id.
    """

    mocker.patch(
        "app.services.category_service.validate_object_id",
        side_effect=Exception()
    )

    with pytest.raises(
        Exception
    ):
        await CategoryService.get_category_by_id(
            "invalid-id"
        )

# ============================================================
# UPDATE CATEGORY
# ============================================================

@pytest.mark.asyncio
async def test_update_category_success(mocker):
    """
    Test successful category update.
    """

    category_id = str(ObjectId())

    mocker.patch(
        "app.services.category_service.validate_object_id",
        return_value=ObjectId(category_id)
    )

    mocker.patch(
        "app.services.category_service.Repository.get_category_by_id",
        new_callable=AsyncMock,
        return_value={
            "_id": ObjectId(category_id),
            "name": "Programming"
        }
    )

    mocker.patch(
        "app.services.category_service.Repository.get_duplicate_category",
        new_callable=AsyncMock,
        return_value=None
    )

    mock_update = mocker.patch(
        "app.services.category_service.Repository.update_category",
        new_callable=AsyncMock
    )

    category = CategoryUpdate(
        name="Java",
        description="Java quizzes"
    )

    response = await CategoryService.update_category(
        category_id,
        category
    )

    assert response.message == "Category updated successfully."

    mock_update.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_category_not_found(mocker):
    """
    Test update when category does not exist.
    """

    category_id = str(ObjectId())

    mocker.patch(
        "app.services.category_service.validate_object_id",
        return_value=ObjectId(category_id)
    )

    mocker.patch(
        "app.services.category_service.Repository.get_category_by_id",
        new_callable=AsyncMock,
        return_value=None
    )

    category = CategoryUpdate(
        name="Java",
        description="Java quizzes"
    )

    with pytest.raises(ResourceNotFoundException):
        await CategoryService.update_category(
            category_id,
            category
        )


@pytest.mark.asyncio
async def test_update_category_duplicate(mocker):
    """
    Test duplicate category while updating.
    """

    category_id = str(ObjectId())

    mocker.patch(
        "app.services.category_service.validate_object_id",
        return_value=ObjectId(category_id)
    )

    mocker.patch(
        "app.services.category_service.Repository.get_category_by_id",
        new_callable=AsyncMock,
        return_value={
            "_id": ObjectId(category_id)
        }
    )

    mocker.patch(
        "app.services.category_service.Repository.get_duplicate_category",
        new_callable=AsyncMock,
        return_value={
            "_id": ObjectId()
        }
    )

    category = CategoryUpdate(
        name="Programming",
        description="Programming quizzes"
    )

    with pytest.raises(ConflictException):
        await CategoryService.update_category(
            category_id,
            category
        )


# ============================================================
# DELETE CATEGORY
# ============================================================

@pytest.mark.asyncio
async def test_delete_category_success(mocker):
    """
    Test successful category deletion.
    """

    category_id = str(ObjectId())

    mocker.patch(
        "app.services.category_service.validate_object_id",
        return_value=ObjectId(category_id)
    )

    mocker.patch(
        "app.services.category_service.Repository.get_category_by_id",
        new_callable=AsyncMock,
        return_value={
            "_id": ObjectId(category_id)
        }
    )

    mocker.patch(
        "app.services.category_service.Repository.get_quizzes_by_category",
        new_callable=AsyncMock,
        return_value=[]
    )

    mock_delete_quizzes = mocker.patch(
        "app.services.category_service.Repository.delete_quizzes_by_category",
        new_callable=AsyncMock
    )

    mock_delete_category = mocker.patch(
        "app.services.category_service.Repository.delete_category",
        new_callable=AsyncMock
    )

    response = await CategoryService.delete_category(
        category_id
    )

    assert response.message == "Category deleted successfully."

    mock_delete_quizzes.assert_awaited_once()

    mock_delete_category.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_category_not_found(mocker):
    """
    Test delete when category does not exist.
    """

    category_id = str(ObjectId())

    mocker.patch(
        "app.services.category_service.validate_object_id",
        return_value=ObjectId(category_id)
    )

    mocker.patch(
        "app.services.category_service.Repository.get_category_by_id",
        new_callable=AsyncMock,
        return_value=None
    )

    with pytest.raises(ResourceNotFoundException):
        await CategoryService.delete_category(
            category_id
        )


@pytest.mark.asyncio
async def test_delete_category_with_quizzes(mocker):
    """
    Test delete category having quizzes.
    """

    category_id = str(ObjectId())

    quiz_id = ObjectId()

    mocker.patch(
        "app.services.category_service.validate_object_id",
        return_value=ObjectId(category_id)
    )

    mocker.patch(
        "app.services.category_service.Repository.get_category_by_id",
        new_callable=AsyncMock,
        return_value={
            "_id": ObjectId(category_id)
        }
    )

    mocker.patch(
        "app.services.category_service.Repository.get_quizzes_by_category",
        new_callable=AsyncMock,
        return_value=[
            {
                "_id": quiz_id
            }
        ]
    )

    mock_delete_questions = mocker.patch(
        "app.services.category_service.Repository.delete_questions_by_quiz",
        new_callable=AsyncMock
    )

    mock_delete_quizzes = mocker.patch(
        "app.services.category_service.Repository.delete_quizzes_by_category",
        new_callable=AsyncMock
    )

    mock_delete_category = mocker.patch(
        "app.services.category_service.Repository.delete_category",
        new_callable=AsyncMock
    )

    await CategoryService.delete_category(
        category_id
    )

    mock_delete_questions.assert_awaited_once_with(
        str(quiz_id)
    )

    mock_delete_quizzes.assert_awaited_once()

    mock_delete_category.assert_awaited_once()