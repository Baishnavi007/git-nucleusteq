"""
Question 7:
Create a custom exception called AgeException
and raise it if age is less than 18.
"""


MINIMUM_AGE = 18


class AgeException(Exception):
    """
    Raised when age validation fails.
    """


def validate_age(age: int) -> int:
    """
    Validate the user's age.

    Args:
        age: Age entered by the user.

    Returns:
        Valid age.

    Raises:
        AgeException:
            If age is invalid.
    """

    if age < 0:
        raise AgeException(
            "Age cannot be negative."
        )

    elif age < MINIMUM_AGE:
        raise AgeException(
            "Age must be at least 18."
        )

    return age


def main() -> None:
    """
    Execute the program.
    """

    try:
        user_age = int(
            input("Enter your age: ")
        )

        validated_age = validate_age(
            user_age
        )

        print(
            f"Valid age: {validated_age}"
        )

    except AgeException as error:
        print(
            f"Age Error: {error}"
        )


if __name__ == "__main__":
    main()