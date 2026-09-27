"""
Question 6

Write a recursive function
to calculate Fibonacci.

"""


def calculate_fibonacci(number: int) -> int:
    """
    Return the Fibonacci value
    using recursion.
    """

    # The Fibonacci of 0 is 0 and the Fibonacci of 1 is 1.
    if number <= 1:
        return number

    # Recursive call which calculates the previous two Fibonacci values.
    return (
            calculate_fibonacci(number - 1)
            + calculate_fibonacci(number - 2)
    )


if __name__ == "__main__":

    print("\n---Fibonacci using recursion ---")

    number = int(input("Enter a level: "))

    if number < 0:
        print("Enter a non-negative number.")
    else:

        # Print the Fibonacci value for the level provided.
        print(calculate_fibonacci(number))