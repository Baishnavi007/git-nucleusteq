"""
Test cases for Category Schemas
"""

import pytest
from pydantic import ValidationError

from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)



def test_category_create_schema():
    """
    Test CategoryCreate schema.
    """

    category = CategoryCreate(
        name="Programming",
        description="Programming quizzes"
    )

    assert category.name == "Programming"
    assert category.description == "Programming quizzes"


def test_category_update_schema():
    """
    Test CategoryUpdate schema.
    """

    category = CategoryUpdate(
        name="Java",
        description="Java related quizzes"
    )

    assert category.name == "Java"
    assert category.description == "Java related quizzes"


def test_category_response_schema():
    """
    Test CategoryResponse schema.
    """

    response = CategoryResponse(
        id="123",
        name="Programming",
        description="Programming quizzes"
    )

    assert response.id == "123"
    assert response.name == "Programming"
    assert response.description == "Programming quizzes"


def test_category_create_invalid_name():
    """
    Test invalid category name.
    """

    with pytest.raises(ValidationError):
        CategoryCreate(
            name="A",
            description="Programming quizzes"
        )


def test_category_create_invalid_description():
    """
    Test invalid description.
    """

    with pytest.raises(ValidationError):
        CategoryCreate(
            name="Programming",
            description="abc"
        )


def test_category_create_invalid_pattern():
    """
    Test invalid category name pattern.
    """

    with pytest.raises(ValidationError):
        CategoryCreate(
            name="Programming@123",
            description="Programming quizzes"
        )


def test_category_update_invalid_name():
    """
    Test invalid update name.
    """

    with pytest.raises(ValidationError):
        CategoryUpdate(
            name="A",
            description="Programming quizzes"
        )


def test_category_update_invalid_description():
    """
    Test invalid update description.
    """

    with pytest.raises(ValidationError):
        CategoryUpdate(
            name="Programming",
            description="abc"
        )


def test_category_update_invalid_pattern():
    """
    Test invalid update name pattern.
    """

    with pytest.raises(ValidationError):
        CategoryUpdate(
            name="Java@123",
            description="Programming quizzes"
        )