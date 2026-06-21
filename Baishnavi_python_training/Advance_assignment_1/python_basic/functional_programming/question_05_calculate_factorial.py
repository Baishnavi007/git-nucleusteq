"""
Question 5

Write a recursive function
to calculate factorial.
"""


def calculate_factorial(number: int) -> int:
    """
    Return the factorial
    using recursion.
    """

    # The factorial of 0 and 1 is 1.
    if number <= 1:
        return 1

    # Recursive call breaks the problem into smaller sub problems.
    # the problem gets broken down into smaller sub problems once until the base condition is met.
    return number * calculate_factorial(number - 1)


if __name__ == "__main__":

    print("\n--- Factorial using Recursion ---")

    number = int(input("Enter a number: "))

    if number < 0:
        print("Enter a non-negative number.")
    else:

        # Display the factorial of the given number.
        print(calculate_factorial(number))