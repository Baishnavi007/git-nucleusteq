"""
Pytest test cases for
the add_numbers function.
"""

from question_01_addition import (
    add_numbers
)


def test_add_positive_numbers() -> None:
    assert add_numbers(10, 20) == 30


def test_add_negative_numbers() -> None:
    assert add_numbers(-5, -3) == -8


def test_add_zero() -> None:
    assert add_numbers(8, 0) == 8


def test_add_mixed_numbers() -> None:
    assert add_numbers(10, -4) == 6