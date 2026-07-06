"""
Quiz request and response schemas
"""

from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    field_validator
)


class QuizCreate(BaseModel):
    """
    Schema for creating a new quiz.
    """

    title: str = Field(
        min_length=3,
        max_length=100
    )

    description: str = Field(
        min_length=10,
        max_length=300
    )

    duration: int = Field(
        gt=0
    )

    @field_validator(
        "title",
        "description"
    )
    @classmethod
    def validate_text_fields(
            cls,
            value: str
    ):
        """
        Trim spaces and validate text fields.
        """

        value = value.strip()

        if not value:

            raise ValueError(
                "Field cannot be empty."
            )

        return value


class QuizUpdate(BaseModel):
    """
    Schema for updating an existing quiz.
    """

    title: str = Field(
        min_length=3,
        max_length=100
    )

    description: str = Field(
        min_length=10,
        max_length=300
    )

    duration: int = Field(
        gt=0
    )

    @field_validator(
        "title",
        "description"
    )
    @classmethod
    def validate_text_fields(
            cls,
            value: str
    ):
        """
        Trim spaces and validate text fields.
        """

        value = value.strip()

        if not value:

            raise ValueError(
                "Field cannot be empty."
            )

        return value


class QuizResponse(BaseModel):
    """
    Schema for returning quiz details.
    """

    id: str

    title: str

    description: str

    category_id: str

    category_name: str

    duration: int

    created_by: str

    created_at: datetime

    updated_at: datetime