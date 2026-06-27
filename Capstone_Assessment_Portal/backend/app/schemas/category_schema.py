"""
Category request and response schemas
"""

from pydantic import BaseModel, Field


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


class CategoryResponse(BaseModel):
    """
    Schema for returning category details
    """

    id: str
    name: str
    description: str