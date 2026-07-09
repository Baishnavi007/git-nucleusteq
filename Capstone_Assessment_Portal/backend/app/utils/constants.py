"""
Application constants
"""

ADMIN = "admin"
STUDENT = "student"


from enum import Enum


class AuthMessage:
    """
    Authentication messages.
    """

    INVALID_CREDENTIALS = "Invalid email or password"
    EMAIL_ALREADY_EXISTS = "Email already exists"
    USER_REGISTERED = "User registered successfully"
    ADMIN_ACCESS_REQUIRED = "Admin access required"


class CategoryMessage:
    """
    Category messages.
    """

    CREATED = "Category created successfully."
    UPDATED = "Category updated successfully."
    DELETED = "Category deleted successfully."

    ALREADY_EXISTS = "Category already exists."
    NOT_FOUND = "Category not found."
    INVALID_ID = "Invalid ID format."


class QuizMessage:
    """
    Quiz messages.
    """

    CREATED = "Quiz created successfully."
    UPDATED = "Quiz updated successfully."
    DELETED = "Quiz deleted successfully."

    PUBLISHED = "Quiz published successfully."
    UNPUBLISHED = "Quiz unpublished successfully."

    ALREADY_EXISTS = "Quiz already exists."
    NOT_FOUND = "Quiz not found."
    INVALID_ID = "Invalid ID format."

    ALREADY_PUBLISHED = "Quiz is already published."
    ALREADY_UNPUBLISHED = "Quiz is already unpublished."


class QuestionMessage:
    """
    Question messages.
    """

    CREATED = "Question created successfully."
    UPDATED = "Question updated successfully."
    DELETED = "Question deleted successfully."

    ALREADY_EXISTS = "Question already exists."
    NOT_FOUND = "Question not found."
    INVALID_ID = "Invalid ID format."
    INVALID_QUESTION_TYPE = "Invalid question type."
    INVALID_DIFFICULTY = "Invalid difficulty level."
    INVALID_CORRECT_ANSWER = "Correct answer is not present in options."
    INVALID_TRUE_FALSE_OPTIONS = "Invalid options for True/False question."
    INVALID_TRUE_FALSE_ANSWER = "Invalid correct answer for True/False question."


class QuestionType(str, Enum):
    """
    Question types.
    """

    MCQ = "MCQ"

VALID_QUESTION_TYPES = {
    "mcq",
    "true_false"
}

VALID_DIFFICULTY_LEVELS = {
    "easy",
    "medium",
    "hard"
}