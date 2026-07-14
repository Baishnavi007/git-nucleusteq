"""
Test cases for ResultService
"""

from datetime import datetime, UTC

import pytest

from unittest.mock import AsyncMock

from bson import ObjectId

from app.schemas.result_schema import AttemptHistoryResponse

from app.services.result_service import ResultService

from app.exceptions.resource_not_found_exception import (
    ResourceNotFoundException
)
def sample_attempt(
        student_id: str,
        score: int = 8,
        passing_marks: int = 5
):
    """
    Sample quiz attempt document
    """

    return {

        "_id": ObjectId(),

        "quiz_id": "quiz123",

        "student_id": student_id,

        "attempt_number": 1,

        "score": score,

        "started_at": datetime.now(UTC),

        "submitted_at": datetime.now(UTC),

        "answers": {

            "q1": "Python"

        },

        "snapshot": {

            "title": "Python Quiz",

            "total_marks": 10,

            "passing_marks": passing_marks,

            "passing_percentage": 50,

            "questions": [

                {

                    "question_id": "q1",

                    "question": "Python is?",

                    "options": [

                        "Java",

                        "Python"

                    ],

                    "correct_answer": "Python",

                    "marks": 10,

                }

            ]

        }

    }
@pytest.mark.asyncio
async def test_get_result_success(
    mocker
):
    """
    Test get result successfully.
    """

    student_id = str(ObjectId())

    mocker.patch(

        "app.services.result_service.get_attempt",

        new=AsyncMock(

            return_value=sample_attempt(
                student_id
            )

        )

    )

    mocker.patch(

        "app.services.result_service.Repository.get_user_by_id",

        new=AsyncMock(

            return_value={

                "first_name": "Baishnavi",

                "last_name": "Singh",

                "email": "student@test.com"

            }

        )

    )

    response = await ResultService.get_result(

        str(ObjectId()),

        {

            "user_id": student_id

        }

    )

    assert response.quiz_title == "Python Quiz"

    assert response.score == 8

    assert response.student_name == "Baishnavi Singh"

@pytest.mark.asyncio
async def test_calculate_percentage(
    mocker
):
    """
    Test percentage calculation.
    """

    student_id = str(ObjectId())

    mocker.patch(

        "app.services.result_service.get_attempt",

        new=AsyncMock(

            return_value=sample_attempt(

                student_id,

                score=7

            )

        )

    )

    mocker.patch(

        "app.services.result_service.Repository.get_user_by_id",

        new=AsyncMock(

            return_value={

                "first_name": "Baishnavi",

                "last_name": "Singh",

                "email": "student@test.com"

            }

        )

    )

    response = await ResultService.get_result(

        str(ObjectId()),

        {

            "user_id": student_id

        }

    )

    assert response.score == 7

    assert response.percentage == 70

@pytest.mark.asyncio
async def test_pass_fail_validation(
    mocker
):
    """
    Test pass/fail validation.
    """

    student_id = str(ObjectId())

    mocker.patch(

        "app.services.result_service.get_attempt",

        new=AsyncMock(

            return_value=sample_attempt(

                student_id,

                score=4,

                passing_marks=5

            )

        )

    )

    mocker.patch(

        "app.services.result_service.Repository.get_user_by_id",

        new=AsyncMock(

            return_value={

                "first_name": "Baishnavi",

                "last_name": "Singh",

                "email": "student@test.com"

            }

        )

    )

    response = await ResultService.get_result(

        str(ObjectId()),

        {

            "user_id": student_id

        }

    )

    assert response.is_pass is False

@pytest.mark.asyncio
async def test_get_student_results(
    mocker
):
    """
    Test fetch student results.
    """

    student_id = str(ObjectId())

    mocker.patch(

        "app.services.result_service.Repository.get_student_results",

        new=AsyncMock(

            return_value=[
                sample_attempt(student_id)
            ]

        )

    )

    mocker.patch(

        "app.services.result_service.Repository.get_user_by_id",

        new=AsyncMock(

            return_value={

                "first_name": "Baishnavi",

                "last_name": "Singh",

                "email": "student@test.com"

            }

        )

    )

    response = await ResultService.get_student_results(

        {

            "user_id": student_id

        }

    )

    assert len(response) == 1

    assert response[0].quiz_title == "Python Quiz"

    assert response[0].student_name == "Baishnavi Singh"

@pytest.mark.asyncio
async def test_get_all_results(
    mocker
):
    """
    Test fetch all results.
    """

    student_id = str(ObjectId())

    mocker.patch(

        "app.services.result_service.Repository.get_all_results",

        new=AsyncMock(

            return_value=[
                sample_attempt(student_id)
            ]

        )

    )

    mocker.patch(

        "app.services.result_service.Repository.get_user_by_id",

        new=AsyncMock(

            return_value={

                "first_name": "Baishnavi",

                "last_name": "Singh",

                "email": "student@test.com"

            }

        )

    )

    response = await ResultService.get_all_results()

    assert len(response) == 1

    assert response[0].quiz_title == "Python Quiz"

    assert response[0].student_name == "Baishnavi Singh"

@pytest.mark.asyncio
async def test_get_result_admin(
    mocker
):
    """
    Test admin result.
    """

    student_id = str(ObjectId())

    mocker.patch(

        "app.services.result_service.get_attempt",

        new=AsyncMock(

            return_value=sample_attempt(student_id)

        )

    )

    mocker.patch(

        "app.services.result_service.Repository.get_user_by_id",

        new=AsyncMock(

            return_value={

                "first_name": "Baishnavi",

                "last_name": "Singh",

                "email": "student@test.com"

            }

        )

    )

    response = await ResultService.get_result_admin(

        str(ObjectId())

    )

    assert response.quiz_title == "Python Quiz"

    assert response.student_name == "Baishnavi Singh"

    assert len(response.questions) == 1

@pytest.mark.asyncio
async def test_get_result_student_not_owner(
    mocker
):
    """
    Test unauthorized student.
    """

    mocker.patch(

        "app.services.result_service.get_attempt",

        new=AsyncMock(

            return_value=sample_attempt(

                str(ObjectId())

            )

        )

    )

    with pytest.raises(

        ResourceNotFoundException

    ):

        await ResultService.get_result(

            str(ObjectId()),

            {

                "user_id": str(ObjectId())

            }

        )

@pytest.mark.asyncio
async def test_result_question_breakdown(
    mocker
):
    """
    Test result contains question breakdown.
    """

    student_id = str(ObjectId())

    mocker.patch(

        "app.services.result_service.get_attempt",

        new=AsyncMock(

            return_value=sample_attempt(student_id)

        )

    )

    mocker.patch(

        "app.services.result_service.Repository.get_user_by_id",

        new=AsyncMock(

            return_value={

                "first_name": "Baishnavi",

                "last_name": "Singh",

                "email": "student@test.com"

            }

        )

    )

    response = await ResultService.get_result(

        str(ObjectId()),

        {

            "user_id": student_id

        }

    )

    question = response.questions[0]

    assert question.question == "Python is?"

    assert question.correct_answer == "Python"

    assert question.selected_answer == "Python"

    assert question.obtained_marks == 10

    assert question.is_correct is True

@pytest.mark.asyncio
async def test_get_student_results_empty(
    mocker
):
    """
    Test empty student results.
    """

    student_id = str(ObjectId())

    mocker.patch(

        "app.services.result_service.Repository.get_student_results",

        new=AsyncMock(

            return_value=[]

        )

    )

    response = await ResultService.get_student_results(

        {

            "user_id": student_id

        }

    )

    assert response == []
