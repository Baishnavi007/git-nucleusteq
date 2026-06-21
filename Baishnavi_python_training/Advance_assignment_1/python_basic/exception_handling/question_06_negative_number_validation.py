"""
Question 6:
Raise a ValueError if the number is negative.
"""


def validate_number(number: int) -> int:
    """
    Validate that the number is not negative.

    Args:
        number: Number entered by the user.

    Returns:
        The validated number.

    Raises:
        ValueError:
            If the number is negative.
    """

    if number < 0:
        raise ValueError(
            "Negative numbers are not allowed."
        )

    return number


def main() -> None:
    """
    Execute the program.
    """

    try:
        user_number = int(
            input("Enter a number: ")
        )

        validated_number = validate_number(
            user_number
        )

        print(
            f"Valid number: "
            f"{validated_number}"
        )

    except ValueError as error:
        print(
            f"Error: {error}"
        )


if __name__ == "__main__":
    main()