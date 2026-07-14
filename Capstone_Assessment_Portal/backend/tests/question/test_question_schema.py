"""
Test cases for Question schemas
"""

import pytest
from pydantic import ValidationError

from app.schemas.question_schema import (
    QuestionCreate,
    QuestionUpdate,
    QuestionResponse,
)


def test_question_create_valid():
    """
    Test QuestionCreate schema with valid data.
    """

    question = QuestionCreate(
        question="What is Python?",
        question_type="mcq",
        options=["Java", "Python", "C++", "Go"],
        correct_answer="Python",
        difficulty="easy",
        tags=["programming"],
        marks=5,
    )

    assert question.question == "What is Python?"
    assert question.correct_answer == "Python"
    assert question.marks == 5


def test_question_create_invalid_question():
    """
    Test QuestionCreate schema with invalid question.
    """

    with pytest.raises(ValidationError):
        QuestionCreate(
            question="Test",
            question_type="mcq",
            options=["A", "B"],
            correct_answer="A",
            difficulty="easy",
            tags=["tag"],
            marks=5,
        )


def test_question_update_valid():
    """
    Test QuestionUpdate schema with valid data.
    """

    question = QuestionUpdate(
        question="Updated question?",
        question_type="mcq",
        options=["Yes", "No"],
        correct_answer="Yes",
        difficulty="easy",
        tags=["updated"],
        marks=10,
    )

    assert question.question == "Updated question?"
    assert question.marks == 10


def test_question_update_invalid_marks():
    """
    Test QuestionUpdate schema with invalid marks.
    """

    with pytest.raises(ValidationError):
        QuestionUpdate(
            question="Updated question?",
            question_type="mcq",
            options=["Yes", "No"],
            correct_answer="Yes",
            difficulty="easy",
            tags=["updated"],
            marks=0,
        )


def test_question_response_valid():
    """
    Test QuestionResponse schema.
    """

    question = QuestionResponse(
        id="123",
        quiz_id="quiz123",
        question="What is Python?",
        question_type="mcq",
        options=["Java", "Python", "C++", "Go"],
        correct_answer="Python",
        difficulty="easy",
        tags=["programming"],
        marks=5,
        created_by="admin",
        created_at="2025-01-01T00:00:00",
        updated_at="2025-01-01T00:00:00",
    )

    assert question.id == "123"
    assert question.quiz_id == "quiz123"
    assert question.correct_answer == "Python"


def test_question_create_invalid_options():
    """
    Test QuestionCreate with less than two options.
    """

    with pytest.raises(ValidationError):
        QuestionCreate(
            question="What is Python?",
            question_type="mcq",
            options=["Python"],
            correct_answer="Python",
            difficulty="easy",
            tags=["programming"],
            marks=5,
        )


def test_question_create_invalid_tags():
    """
    Test QuestionCreate with empty tags.
    """

    with pytest.raises(ValidationError):
        QuestionCreate(
            question="What is Python?",
            question_type="mcq",
            options=["Java", "Python"],
            correct_answer="Python",
            difficulty="easy",
            tags=[],
            marks=5,
        )