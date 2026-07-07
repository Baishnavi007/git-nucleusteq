"""
Quiz attempt request and response schemas
"""

from datetime import datetime

from pydantic import (
    BaseModel,
    Field
)


class AttemptQuestionSnapshot(BaseModel):
    """
    Snapshot of a question stored inside an attempt.
    """

    question_id: str

    question: str

    question_type: str

    options: list[str]

    correct_answer: str

    difficulty: str

    tags: list[str]
    
    marks: int = Field(
        gt=0
    )


class QuizSnapshot(BaseModel):
    """
    Snapshot of quiz stored inside an attempt.
    """

    title: str

    description: str

    category_id: str

    category_name: str

    duration: int = Field(
        gt=0
    )

    questions: list[
        AttemptQuestionSnapshot
    ]


class StudentAnswer(BaseModel):
    """
    Student answer schema.
    """

    question_id: str

    selected_answer: str

class AttemptCreate(BaseModel):
    """
    Schema for starting a quiz attempt.
    """

    quiz_id: str = Field(
        description="Quiz ID"
    )

class AttemptResponse(BaseModel):
    """
    Response after starting an attempt.
    """

    id: str

    quiz_id: str

    attempt_number: int

    status: str

    started_at: datetime

    submitted_at: datetime | None = None


class AttemptQuestionResponse(BaseModel):
    """
    Question returned during an attempt.
    """

    id: str

    question: str

    question_type: str

    options: list[str]

    difficulty: str

    marks: int

    selected_answer: str | None = None