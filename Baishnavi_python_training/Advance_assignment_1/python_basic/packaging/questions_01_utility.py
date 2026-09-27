"""
Question 1:
Import and use utility functions.
"""

from utility_functions import (
    calculate_square,
    convert_to_uppercase
)


def main() -> None:
    """
    Execute the program.
    """

    print(
        calculate_square(5)
    )

    print(
        convert_to_uppercase(
            "baishnavi"
        )
    )


if __name__ == "__main__":
    main()