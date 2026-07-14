"""
Test cases for Quiz Attempt Schemas
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.quiz_attempt_schema import (
    AttemptQuestionSnapshot,
    QuizSnapshot,
    StudentAnswer,
    AttemptCreate,
    AttemptResponse,
    AttemptQuestionResponse,
)


def test_attempt_question_snapshot_valid():
    """
    Test valid attempt question snapshot.
    """

    question = AttemptQuestionSnapshot(
        question_id="question123",
        question="Python is interpreted?",
        question_type="true_false",
        options=["True", "False"],
        correct_answer="True",
        difficulty="easy",
        tags=["python"],
        marks=2,
    )

    assert question.question == "Python is interpreted?"
    assert question.correct_answer == "True"
    assert question.marks == 2


def test_attempt_question_snapshot_invalid_marks():
    """
    Test invalid marks.
    """

    with pytest.raises(ValidationError):
        AttemptQuestionSnapshot(
            question_id="question123",
            question="Python is interpreted?",
            question_type="true_false",
            options=["True", "False"],
            correct_answer="True",
            difficulty="easy",
            tags=["python"],
            marks=0,
        )


def test_quiz_snapshot_valid():
    """
    Test valid quiz snapshot.
    """

    quiz = QuizSnapshot(
        title="Python Quiz",
        description="Basic Python Quiz",
        category_id="cat123",
        category_name="Programming",
        duration=30,
        questions=[
            AttemptQuestionSnapshot(
                question_id="question123",
                question="Python is interpreted?",
                question_type="true_false",
                options=["True", "False"],
                correct_answer="True",
                difficulty="easy",
                tags=["python"],
                marks=2,
            )
        ],
        total_questions=1,
        total_marks=2,
        passing_percentage=50,
        passing_marks=1,
    )

    assert quiz.title == "Python Quiz"
    assert len(quiz.questions) == 1


def test_student_answer_valid():
    """
    Test valid student answer.
    """

    answer = StudentAnswer(
        question_id="question123",
        selected_answer="True",
    )

    assert answer.selected_answer == "True"


def test_attempt_create_valid():
    """
    Test valid attempt creation.
    """

    attempt = AttemptCreate(
        quiz_id="quiz123"
    )

    assert attempt.quiz_id == "quiz123"


def test_attempt_response_schema():
    """
    Test attempt response schema.
    """

    now = datetime.now()

    response = AttemptResponse(
        id="attempt123",
        quiz_id="quiz123",
        attempt_number=1,
        status="in_progress",
        started_at=now,
        submitted_at=None,
    )

    assert response.id == "attempt123"
    assert response.status == "in_progress"
    assert response.attempt_number == 1


def test_attempt_question_response_schema():
    """
    Test attempt question response.
    """

    response = AttemptQuestionResponse(
        id="question123",
        question="Python is interpreted?",
        question_type="true_false",
        options=["True", "False"],
        difficulty="easy",
        marks=2,
    )

    assert response.id == "question123"
    assert response.question == "Python is interpreted?"
    assert response.selected_answer is None


def test_attempt_question_response_with_selected_answer():
    """
    Test attempt question response with selected answer.
    """

    response = AttemptQuestionResponse(
        id="question123",
        question="Python is interpreted?",
        question_type="true_false",
        options=["True", "False"],
        difficulty="easy",
        marks=2,
        selected_answer="True",
    )

    assert response.selected_answer == "True"