"""
Question 1:
Handle ValueError when the user enters
an invalid integer.
"""


def convert_to_integer(user_input: str) -> int:
    """
    Convert a string into an integer.

    Args:
        user_input: Value entered by the user.

    Returns:
        Converted integer value.

    Raises:
        ValueError:
            If the input is not a valid integer.
    """

    return int(user_input)


if __name__ == "__main__":
    try:
        entered_value = input(
            "Enter an integer: "
        )

        converted_number = convert_to_integer(
            entered_value
        )

        print(
            f"Valid integer entered: "
            f"{converted_number}"
        )

    except ValueError:
        print(
            "Invalid input. "
            "Please enter a valid integer."
        )