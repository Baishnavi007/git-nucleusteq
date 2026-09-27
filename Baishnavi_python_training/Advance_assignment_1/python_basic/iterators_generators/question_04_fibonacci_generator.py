
"""
Question 4 

Write a generator to produce
Fibonacci numbers.
"""


def generate_fibonacci(
        limit: int
):
    """
    Generate Fibonacci numbers
    up to the given count.
    """

    first_number = 0
    second_number = 1

    for _ in range(limit):

        # Return the current Fibonacci number.
        yield first_number

        # Find the next two numbers.
        first_number, second_number = (
            second_number,
            first_number + second_number
        )


if __name__ == "__main__":

    print("\n--- Fibonacci Generator ---")

    num = int(input("Enter limit: "))

    if num < 1:
        print(" Enter a positive number.")
    else:
        for number in generate_fibonacci(num):
            print(number)