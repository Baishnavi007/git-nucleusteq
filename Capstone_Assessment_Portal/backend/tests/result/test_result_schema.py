"""
Test cases for result schemas
"""

from datetime import datetime, UTC

import pytest

from pydantic import ValidationError

from app.schemas.result_schema import (
    ResultQuestionResponse,
    ResultResponse,
    AttemptHistoryResponse,
)


def test_result_question_response_schema():
    """
    Test ResultQuestionResponse schema
    """

    result = ResultQuestionResponse(
        question="What is Python?",
        options=["Java", "Python"],
        selected_answer="Python",
        correct_answer="Python",
        marks=2,
        obtained_marks=2,
        is_correct=True,
    )

    assert result.question == "What is Python?"
    assert result.selected_answer == "Python"
    assert result.correct_answer == "Python"
    assert result.is_correct is True



def test_result_response_schema():
    """
    Test ResultResponse schema
    """

    result = ResultResponse(
        attempt_id="attempt123",
        quiz_id="quiz123",
        quiz_title="Python Quiz",
        student_id="student123",
        student_name="Baishnavi Singh",
        student_email="student@test.com",
        attempt_number=1,
        score=8,
        total_marks=10,
        percentage=80,
        passing_percentage=50,
        passing_marks=5,
        is_pass=True,
        started_at=datetime.now(UTC),
        submitted_at=datetime.now(UTC),
        questions=[],
    )

    assert result.score == 8
    assert result.percentage == 80
    assert result.student_name == "Baishnavi Singh"
    assert result.questions == []



def test_result_response_invalid_percentage():
    """
    Test ResultResponse validation
    """

    with pytest.raises(ValidationError):

        ResultResponse(
            attempt_id="attempt123",
            quiz_id="quiz123",
            quiz_title="Python Quiz",
            student_id="student123",
            student_name="Baishnavi Singh",
            student_email="student@test.com",
            attempt_number=1,
            score=8,
            total_marks=10,
            percentage=101,
            passing_percentage=50,
            passing_marks=5,
            is_pass=True,
            started_at=datetime.now(UTC),
            submitted_at=datetime.now(UTC),
            questions=[],
        )



def test_attempt_history_response_schema():
    """
    Test AttemptHistoryResponse schema
    """

    history = AttemptHistoryResponse(
        attempt_id="attempt123",
        student_id="student123",
        student_name="Baishnavi Singh",
        student_email="student@test.com",
        quiz_id="quiz123",
        quiz_title="Python Quiz",
        attempt_number=1,
        score=9,
        total_marks=10,
        percentage=90,
        is_pass=True,
        submitted_at=datetime.now(UTC),
    )

    assert history.student_name == "Baishnavi Singh"
    assert history.quiz_title == "Python Quiz"
    assert history.score == 9
    assert history.is_pass is True



def test_result_question_response_invalid_marks():
    """
    Test invalid marks validation
    """

    with pytest.raises(ValidationError):

        ResultQuestionResponse(
            question="What is Python?",
            options=["Java", "Python"],
            selected_answer="Python",
            correct_answer="Python",
            marks=0,
            obtained_marks=0,
            is_correct=False,
        )