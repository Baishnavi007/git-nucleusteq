"""
Question 3

Create a function with a logical bug
and use pdb to identify the issue.
"""

import pdb


def calculate_average(
    marks: list[int]
) -> float:
    """
    Calculate the average marks.
    """

    pdb.set_trace()

    total_marks = sum(marks)

    # Logical bug:
    average_marks = (
        total_marks /
        (len(marks) - 1)
    )

    return average_marks


if __name__ == "__main__":

    student_marks = [
        80,
        90,
        100
    ]

    print(
        calculate_average(
            student_marks
        )
    )