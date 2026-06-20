"""
Question 2:
Handle ZeroDivisionError while dividing two numbers.
"""


def divide_numbers(
    numerator: float,
    denominator: float
) -> float:
    """
    Divide two numbers.

    Args:
        numerator: Number to be divided.
        denominator: Number by which division is performed.

    Returns:
        Division result.

    Raises:
        ZeroDivisionError:
            If denominator is zero.
    """

    return numerator / denominator


if __name__ == "__main__":
    try:
        first_number = float(
            input("Enter first number: ")
        )

        second_number = float(
            input("Enter second number: ")
        )

        result = divide_numbers(
            first_number,
            second_number
        )

        print(
            f"Division Result: {result}"
        )

    except ZeroDivisionError:
        print(
            "Cannot divide by zero."
        )