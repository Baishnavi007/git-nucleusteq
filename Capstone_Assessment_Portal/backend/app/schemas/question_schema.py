"""
Question request and response schemas
"""

from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    field_validator
)


class QuestionCreate(BaseModel):
    """
    Schema for creating a new question.
    """

    question: str = Field(
        min_length=5,
        max_length=500
    )

    question_type: str

    options: list[str]

    correct_answer: str

    difficulty: str

    tags: list[str]

    marks: int = Field(
        gt=0
    )

    @field_validator(
        "question",
        "correct_answer"
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

    @field_validator(
        "tags"
    )
    @classmethod
    def validate_tags(
            cls,
            value: list[str]
    ):
        """
        Trim spaces and validate tags.
        """

        if not value:

            raise ValueError(
                "At least one tag is required."
            )

        cleaned_tags = []

        for tag in value:

            tag = tag.strip()

            if not tag:

                raise ValueError(
                    "Tag cannot be empty."
                )

            cleaned_tags.append(
                tag
            )

        return cleaned_tags

    @field_validator(
        "options"
    )
    @classmethod
    def validate_options(
            cls,
            value: list[str]
    ):
        """
        Trim spaces and validate options.
        """

        if len(value) < 2:

            raise ValueError(
                "At least two options are required."
            )

        cleaned_options = []

        for option in value:

            option = option.strip()

            if not option:

                raise ValueError(
                    "Option cannot be empty."
                )

            cleaned_options.append(
                option
            )

        return cleaned_options


class QuestionUpdate(BaseModel):
    """
    Schema for updating an existing question.
    """

    question: str = Field(
        min_length=5,
        max_length=500
    )

    question_type: str

    options: list[str]

    correct_answer: str

    difficulty: str

    tags: list[str]

    marks: int = Field(
        gt=0
    )

    @field_validator(
        "question",
        "correct_answer"
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

    @field_validator(
        "tags"
    )
    @classmethod
    def validate_tags(
            cls,
            value: list[str]
    ):
        """
        Trim spaces and validate tags.
        """

        if not value:

            raise ValueError(
                "At least one tag is required."
            )

        cleaned_tags = []

        for tag in value:

            tag = tag.strip()

            if not tag:

                raise ValueError(
                    "Tag cannot be empty."
                )

            cleaned_tags.append(
                tag
            )

        return cleaned_tags

    @field_validator(
        "options"
    )
    @classmethod
    def validate_options(
            cls,
            value: list[str]
    ):
        """
        Trim spaces and validate options.
        """

        if len(value) < 2:

            raise ValueError(
                "At least two options are required."
            )

        cleaned_options = []

        for option in value:

            option = option.strip()

            if not option:

                raise ValueError(
                    "Option cannot be empty."
                )

            cleaned_options.append(
                option
            )

        return cleaned_options


class QuestionResponse(BaseModel):
    """
    Schema for returning question details.
    """

    id: str

    quiz_id: str

    question: str

    question_type: str

    options: list[str]

    correct_answer: str

    difficulty: str

    tags: list[str]

    marks: int

    created_by: str

    created_at: datetime

    updated_at: datetime