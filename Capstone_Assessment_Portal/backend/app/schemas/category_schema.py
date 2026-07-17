"""
Category request and response schemas
"""

from pydantic import BaseModel, Field, field_validator

from app.utils.helpers import normalize_text


class CategoryCreate(BaseModel):
    """
    Schema for creating a new category
    """

    name: str = Field(
        min_length=2,
        max_length=50,
        pattern=r"^[A-Za-z0-9 ]+$"
    )

    description: str = Field(
        min_length=5,
        max_length=200
    )

    @field_validator("name", "description")
    @classmethod
    def normalize_text_fields(cls, value: str):
        value = normalize_text(value)
        if not value:
            raise ValueError("Field cannot be empty or whitespace only.")
        return value


class CategoryUpdate(BaseModel):
    """
    Schema for updating an existing category
    """

    name: str = Field(
        min_length=2,
        max_length=50,
        pattern=r"^[A-Za-z0-9 ]+$"
    )

    description: str = Field(
        min_length=5,
        max_length=200
    )

    @field_validator("name", "description")
    @classmethod
    def normalize_text_fields(cls, value: str):
        value = normalize_text(value)
        if not value:
            raise ValueError("Field cannot be empty or whitespace only.")
        return value


class CategoryResponse(BaseModel):
    """
    Schema for returning category details
    """

    id: str
    name: str
    description: str