"""
Data Structures - Set Operations
"""


# Question 30
# Perform union, intersection, and difference on two sets.

def perform_set_operations(
        enrolled_students: set[int],
        placement_students: set[int]
) -> tuple[
    set[int],
    set[int],
    set[int]
]:
    """
    Perform union, intersection,
    and difference operations on sets.
    """

    combined_students = (
        enrolled_students.union(
            placement_students
        )
    )

    common_students = (
        enrolled_students.intersection(
            placement_students
        )
    )

    unique_enrolled_students = (
        enrolled_students.difference(
            placement_students
        )
    )

    return (
        combined_students,
        common_students,
        unique_enrolled_students
    )


# Question 31
# Remove duplicates from a list using set.

def remove_duplicate_scores(
        scores: list[int]
) -> list[int]:
    """
    Remove duplicate values from a list.
    """

    if not scores:
        return []

    return list(set(scores))


if __name__ == "__main__":

    print(
        "\nQuestion 30"
    )

    enrolled_students = {
        101,
        102,
        103,
        104,
        105
    }

    placement_students = {
        104,
        105,
        106,
        107,
        108
    }

    (
        combined_students,
        common_students,
        unique_enrolled_students
    ) = perform_set_operations(
        enrolled_students,
        placement_students
    )

    print(
        f"Enrolled Students: "
        f"{enrolled_students}"
    )

    print(
        f"Placement Students: "
        f"{placement_students}"
    )

    print(
        f"Union: "
        f"{combined_students}"
    )

    print(
        f"Intersection: "
        f"{common_students}"
    )

    print(
        f"Difference: "
        f"{unique_enrolled_students}"
    )

    print(
        "\nQuestion 31 "
    )

    student_scores = [
        85,
        90,
        85,
        78,
        90,
        95
    ]

    unique_scores = (
        remove_duplicate_scores(
            student_scores
        )
    )

    print(
        f"Original Scores: "
        f"{student_scores}"
    )

    print(
        f"Unique Scores: "
        f"{unique_scores}"
    )