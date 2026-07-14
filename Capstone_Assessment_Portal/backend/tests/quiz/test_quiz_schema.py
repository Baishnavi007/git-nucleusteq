"""
Test cases for Quiz Schemas
"""

import pytest

from pydantic import ValidationError

from app.schemas.quiz_schema import (
    QuizCreate,
    QuizUpdate,
    QuizResponse
)


def test_quiz_create_schema():
    """
    Test valid quiz create schema.
    """

    quiz = QuizCreate(
        title="Java Basics",
        description="This quiz covers Java fundamentals.",
        duration=30,
        passing_percentage=40
    )

    assert quiz.title == "Java Basics"
    assert quiz.description == "This quiz covers Java fundamentals."
    assert quiz.duration == 30
    assert quiz.passing_percentage == 40


def test_quiz_create_trim_spaces():
    """
    Test trimming spaces from title and description.
    """

    quiz = QuizCreate(
        title="   Java Basics   ",
        description="   This quiz covers Java fundamentals.   ",
        duration=30,
        passing_percentage=50
    )

    assert quiz.title == "Java Basics"
    assert quiz.description == "This quiz covers Java fundamentals."


def test_quiz_create_empty_title():
    """
    Test empty title validation.
    """

    with pytest.raises(ValidationError):

        QuizCreate(
            title="   ",
            description="Valid description here.",
            duration=30,
            passing_percentage=40
        )


def test_quiz_create_empty_description():
    """
    Test empty description validation.
    """

    with pytest.raises(ValidationError):

        QuizCreate(
            title="Java",
            description="     ",
            duration=30,
            passing_percentage=40
        )


def test_quiz_create_invalid_duration():
    """
    Test invalid duration.
    """

    with pytest.raises(ValidationError):

        QuizCreate(
            title="Java",
            description="Valid description here.",
            duration=0,
            passing_percentage=40
        )


def test_quiz_create_invalid_passing_percentage():
    """
    Test invalid passing percentage.
    """

    with pytest.raises(ValidationError):

        QuizCreate(
            title="Java",
            description="Valid description here.",
            duration=30,
            passing_percentage=101
        )


def test_quiz_update_schema():
    """
    Test valid quiz update schema.
    """

    quiz = QuizUpdate(
        title="Advanced Java",
        description="Advanced Java concepts covered.",
        duration=45,
        passing_percentage=60
    )

    assert quiz.title == "Advanced Java"
    assert quiz.description == "Advanced Java concepts covered."
    assert quiz.duration == 45
    assert quiz.passing_percentage == 60


def test_quiz_update_trim_spaces():
    """
    Test trimming spaces in update schema.
    """

    quiz = QuizUpdate(
        title="   Python   ",
        description="   Python Quiz Description   ",
        duration=40,
        passing_percentage=50
    )

    assert quiz.title == "Python"
    assert quiz.description == "Python Quiz Description"


def test_quiz_update_invalid_duration():
    """
    Test invalid duration in update schema.
    """

    with pytest.raises(ValidationError):

        QuizUpdate(
            title="Java",
            description="Valid description here.",
            duration=-10,
            passing_percentage=40
        )


def test_quiz_update_invalid_passing_percentage():
    """
    Test invalid passing percentage in update schema.
    """

    with pytest.raises(ValidationError):

        QuizUpdate(
            title="Java",
            description="Valid description here.",
            duration=30,
            passing_percentage=0
        )


def test_quiz_response_schema():
    """
    Test quiz response schema.
    """

    from datetime import datetime

    response = QuizResponse(
        id="123",
        title="Java",
        description="Java Quiz",
        category_id="cat123",
        category_name="Programming",
        duration=30,
        is_published=False,
        max_attempts=3,
        created_by="admin",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        passing_percentage=40,
        total_questions=10,
        total_marks=100
    )

    assert response.id == "123"
    assert response.title == "Java"
    assert response.category_name == "Programming"
    assert response.total_questions == 10
    assert response.total_marks == 100