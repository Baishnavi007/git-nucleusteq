"""
Question 4:
Handle multiple exceptions in a single program.
"""


def divide_numbers(
    numerator: float,
    denominator: float
) -> float:
    """
    Divide two numbers.

    Args:
        numerator: Dividend value.
        denominator: Divisor value.

    Returns:
        Division result.
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
            f"Result: {result}"
        )

    except ValueError:
        print(
            "Please enter valid numeric values."
        )

    except ZeroDivisionError:
        print(
            "Cannot divide by zero."
        )