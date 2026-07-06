"""
Test cases for quiz schemas
"""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.schemas.quiz_schema import (
    QuizCreate,
    QuizUpdate,
    QuizResponse,
)


def test_quiz_create_valid():
    """
    Test QuizCreate schema with valid data.
    """

    quiz = QuizCreate(
        title="Java Basics",
        description="Quiz covering Java fundamentals.",
        duration=30,
    )

    assert quiz.title == "Java Basics"
    assert quiz.description == "Quiz covering Java fundamentals."
    assert quiz.duration == 30


def test_quiz_create_empty_title():
    """
    Test QuizCreate schema with empty title.
    """

    with pytest.raises(ValidationError):

        QuizCreate(
            title="   ",
            description="Quiz covering Java fundamentals.",
            duration=30,
        )


def test_quiz_create_invalid_duration():
    """
    Test QuizCreate schema with invalid duration.
    """

    with pytest.raises(ValidationError):

        QuizCreate(
            title="Java Basics",
            description="Quiz covering Java fundamentals.",
            duration=0,
        )


def test_quiz_update_valid():
    """
    Test QuizUpdate schema with valid data.
    """

    quiz = QuizUpdate(
        title="Advanced Java",
        description="Advanced Java quiz.",
        duration=45,
    )

    assert quiz.title == "Advanced Java"
    assert quiz.description == "Advanced Java quiz."
    assert quiz.duration == 45


def test_quiz_update_empty_description():
    """
    Test QuizUpdate schema with empty description.
    """

    with pytest.raises(ValidationError):

        QuizUpdate(
            title="Advanced Java",
            description="      ",
            duration=45,
        )


def test_quiz_response_valid():
    """
    Test QuizResponse schema with valid data.
    """

    quiz = QuizResponse(
        id="123",
        title="Java Basics",
        description="Quiz covering Java fundamentals.",
        category_id="456",
        category_name="Programming",
        duration=30,
        created_by="admin",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    assert quiz.id == "123"
    assert quiz.title == "Java Basics"
    assert quiz.category_name == "Programming"