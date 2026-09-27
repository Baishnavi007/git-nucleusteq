"""
Data Structures - Tuple Operations
"""


# Question 28
# Create a tuple and access elements.

def display_tuple_elements(
        student_details: tuple
) -> None:
    """
    Display all elements present in a tuple.
    """

    print("\nTuple Elements:")

    for index in range(len(student_details)):

        print(
            f"Element at Index "
            f"{index}: "
            f"{student_details[index]}"
        )


# Question 29
# Convert tuple into list and modify it.

def update_student_details(
        student_details: tuple,
        index: int,
        new_value: str | int
) -> list:
    """
    Convert tuple to list and update
    a specific element.
    """

    modified_student_list = list(
        student_details
    )

    # Validate index before updating

    if (
        index < 0
        or
        index >= len(modified_student_list)
    ):
        raise IndexError(
            "Invalid index provided."
        )

    modified_student_list[index] = (
        new_value
    )

    return modified_student_list


if __name__ == "__main__":

    student_details = (
        "Baishnavi",
        23,
        "CSE"
    )

    print(
        "\nQuestion 28 "
    )

    display_tuple_elements(
        student_details
    )

    print(
        "\nQuestion 29"
    )

    modified_student_details = (
        update_student_details(
            student_details,
            2,
            "Computer Science"
        )
    )

    print(
        f"\nOriginal Tuple: "
        f"{student_details}"
    )

    print(
        f"Modified List: "
        f"{modified_student_details}"
    )