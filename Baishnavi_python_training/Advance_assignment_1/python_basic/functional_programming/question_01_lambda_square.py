"""
Question 1

Write a lambda function to find
the square of a number.
"""


def find_square(number: int) -> int:
    """
    Return the square of
    the given number.
    """

    # Lambda function performs the square calculation.
    return (lambda value: value ** 2)(number)


if __name__ == "__main__":

    print("\n--- Lambda Square ---")

    number = int(input("Enter a number: "))

    print(
        f"Square: "
        f"{find_square(number)}"
    )