"""
Use mathematical package.
"""

from arithmetic_operations import (
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers
)


def main() -> None:
    """
    Execute the program.
    """

    print(
        add_numbers(10, 5)
    )

    print(
        subtract_numbers(10, 5)
    )

    print(
        multiply_numbers(10, 5)
    )

    print(
        divide_numbers(10, 5)
    )


if __name__ == "__main__":
    main()